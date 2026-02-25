#!/usr/bin/env python3
"""Authorize to Google Drive and export image links from a folder tree."""

from __future__ import annotations

import argparse
import base64
import csv
import hashlib
import json
import re
import secrets
import sys
import time
from collections import deque
from pathlib import Path
from typing import Any
from urllib.parse import parse_qs, urlencode, urlparse

import requests

SCOPE = "https://www.googleapis.com/auth/drive.readonly"
DEFAULT_CREDENTIALS = (
    "docs/plans/"
    "client_secret_376509910271-q6idl37d9luifogvddj9rge9eh6jt8il.apps.googleusercontent.com.json"
)
DEFAULT_STATE_FILE = "tmp/gdrive_oauth_state.json"
DEFAULT_TOKEN_FILE = "tmp/gdrive_token.json"
DRIVE_FILES_API = "https://www.googleapis.com/drive/v3/files"


def _read_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def _write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=True)


def _b64url(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).decode("ascii").rstrip("=")


def _load_client_config(path: Path) -> dict[str, str]:
    raw = _read_json(path)
    section = raw.get("installed") or raw.get("web")
    if not section:
        raise ValueError(f"Invalid OAuth client file: {path}")
    needed = ["client_id", "client_secret", "auth_uri", "token_uri"]
    missing = [k for k in needed if not section.get(k)]
    if missing:
        raise ValueError(f"OAuth client config missing: {', '.join(missing)}")
    redirect_uri = (
        section.get("redirect_uris", [None])[0]
        or section.get("redirect_uri")
        or "http://localhost"
    )
    return {
        "client_id": section["client_id"],
        "client_secret": section["client_secret"],
        "auth_uri": section["auth_uri"],
        "token_uri": section["token_uri"],
        "redirect_uri": redirect_uri,
    }


def _parse_folder_id(value: str) -> str:
    value = value.strip()
    m = re.search(r"/folders/([A-Za-z0-9_-]+)", value)
    if m:
        return m.group(1)
    m = re.fullmatch(r"[A-Za-z0-9_-]{10,}", value)
    if m:
        return value
    parsed = urlparse(value)
    if parsed.query:
        q = parse_qs(parsed.query)
        if "id" in q and q["id"]:
            return q["id"][0]
    raise ValueError(f"Could not parse folder ID from: {value}")


def _token_is_expired(token: dict[str, Any], skew: int = 60) -> bool:
    created = int(token.get("created_at", 0))
    expires_in = int(token.get("expires_in", 0))
    if not created or not expires_in:
        return False
    return int(time.time()) >= (created + expires_in - skew)


def auth_start(credentials_path: Path, state_path: Path) -> None:
    cfg = _load_client_config(credentials_path)
    state = secrets.token_urlsafe(24)
    code_verifier = _b64url(secrets.token_bytes(64))
    code_challenge = _b64url(hashlib.sha256(code_verifier.encode("ascii")).digest())
    params = {
        "client_id": cfg["client_id"],
        "redirect_uri": cfg["redirect_uri"],
        "response_type": "code",
        "scope": SCOPE,
        "access_type": "offline",
        "prompt": "consent",
        "state": state,
        "code_challenge": code_challenge,
        "code_challenge_method": "S256",
    }
    auth_url = f'{cfg["auth_uri"]}?{urlencode(params)}'
    state_data = {
        "state": state,
        "code_verifier": code_verifier,
        "redirect_uri": cfg["redirect_uri"],
        "created_at": int(time.time()),
    }
    _write_json(state_path, state_data)
    print("Open this URL in your browser, approve access, and copy the final redirected URL:")
    print(auth_url)
    print("")
    print("Then run:")
    print(
        "python3 scripts/gdrive_image_links.py auth-complete "
        f'--redirected-url "PASTE_REDIRECTED_URL_HERE"'
    )


def auth_complete(
    credentials_path: Path,
    state_path: Path,
    token_path: Path,
    redirected_url: str,
) -> None:
    cfg = _load_client_config(credentials_path)
    state_data = _read_json(state_path)

    parsed = urlparse(redirected_url.strip())
    query = parse_qs(parsed.query)
    if "error" in query:
        raise RuntimeError(f"OAuth error: {query['error'][0]}")
    if "code" not in query or not query["code"]:
        raise RuntimeError("Redirected URL does not contain an authorization code.")
    code = query["code"][0]
    returned_state = query.get("state", [""])[0]
    expected_state = state_data.get("state", "")
    if returned_state != expected_state:
        raise RuntimeError("State mismatch; refusing to continue.")

    token_resp = requests.post(
        cfg["token_uri"],
        data={
            "client_id": cfg["client_id"],
            "client_secret": cfg["client_secret"],
            "code": code,
            "code_verifier": state_data["code_verifier"],
            "redirect_uri": state_data["redirect_uri"],
            "grant_type": "authorization_code",
        },
        timeout=60,
    )
    if not token_resp.ok:
        raise RuntimeError(
            f"Token exchange failed ({token_resp.status_code}): {token_resp.text}"
        )
    token = token_resp.json()
    token["created_at"] = int(time.time())
    if "scope" not in token:
        token["scope"] = SCOPE
    _write_json(token_path, token)
    print(f"Token saved to {token_path}")


def _refresh_token(
    credentials_path: Path, token_path: Path, token: dict[str, Any]
) -> dict[str, Any]:
    refresh_token = token.get("refresh_token")
    if not refresh_token:
        raise RuntimeError("Token is expired and no refresh_token is available.")
    cfg = _load_client_config(credentials_path)
    resp = requests.post(
        cfg["token_uri"],
        data={
            "client_id": cfg["client_id"],
            "client_secret": cfg["client_secret"],
            "refresh_token": refresh_token,
            "grant_type": "refresh_token",
        },
        timeout=60,
    )
    if not resp.ok:
        raise RuntimeError(f"Token refresh failed ({resp.status_code}): {resp.text}")
    update = resp.json()
    token["access_token"] = update["access_token"]
    token["expires_in"] = update.get("expires_in", token.get("expires_in", 0))
    token["scope"] = update.get("scope", token.get("scope", SCOPE))
    token["created_at"] = int(time.time())
    if update.get("refresh_token"):
        token["refresh_token"] = update["refresh_token"]
    _write_json(token_path, token)
    return token


def _auth_headers(access_token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {access_token}"}


def _drive_get_file(access_token: str, file_id: str) -> dict[str, Any]:
    resp = requests.get(
        f"{DRIVE_FILES_API}/{file_id}",
        params={
            "fields": "id,name,mimeType,webViewLink",
            "supportsAllDrives": "true",
        },
        headers=_auth_headers(access_token),
        timeout=60,
    )
    if not resp.ok:
        raise RuntimeError(
            f"Failed to fetch folder metadata ({resp.status_code}): {resp.text}"
        )
    return resp.json()


def _drive_list_children(
    access_token: str, parent_id: str, page_token: str | None = None
) -> dict[str, Any]:
    params = {
        "q": f"'{parent_id}' in parents and trashed=false",
        "fields": (
            "nextPageToken,"
            "files(id,name,mimeType,webViewLink,shortcutDetails(targetId,targetMimeType))"
        ),
        "pageSize": "1000",
        "supportsAllDrives": "true",
        "includeItemsFromAllDrives": "true",
    }
    if page_token:
        params["pageToken"] = page_token
    resp = requests.get(
        DRIVE_FILES_API,
        params=params,
        headers=_auth_headers(access_token),
        timeout=60,
    )
    if not resp.ok:
        raise RuntimeError(f"Drive list failed ({resp.status_code}): {resp.text}")
    return resp.json()


def export_image_links(
    credentials_path: Path, token_path: Path, folder_input: str, out_path: Path
) -> None:
    folder_id = _parse_folder_id(folder_input)
    token = _read_json(token_path)
    if _token_is_expired(token):
        token = _refresh_token(credentials_path, token_path, token)
    access_token = token.get("access_token")
    if not access_token:
        raise RuntimeError("No access_token found in token file.")

    root = _drive_get_file(access_token, folder_id)
    root_name = root.get("name", folder_id)

    rows: list[dict[str, Any]] = []
    queue = deque([(folder_id, root_name)])
    visited_folders: set[str] = set()

    while queue:
        current_folder_id, current_path = queue.popleft()
        if current_folder_id in visited_folders:
            continue
        visited_folders.add(current_folder_id)

        page_token = None
        while True:
            payload = _drive_list_children(access_token, current_folder_id, page_token)
            for item in payload.get("files", []):
                item_id = item["id"]
                name = item.get("name", "")
                mime = item.get("mimeType", "")
                path_in_tree = f"{current_path}/{name}"

                if mime == "application/vnd.google-apps.folder":
                    queue.append((item_id, path_in_tree))
                    continue

                is_shortcut = mime == "application/vnd.google-apps.shortcut"
                shortcut = item.get("shortcutDetails") or {}
                target_id = shortcut.get("targetId", "")
                target_mime = shortcut.get("targetMimeType", "")
                is_image = mime.startswith("image/") or (
                    is_shortcut and target_mime.startswith("image/")
                )
                if not is_image:
                    continue

                effective_file_id = target_id if (is_shortcut and target_id) else item_id
                drive_link = (
                    f"https://drive.google.com/file/d/{effective_file_id}/view?usp=drive_link"
                )
                rows.append(
                    {
                        "path": path_in_tree,
                        "file_name": name,
                        "mime_type": mime,
                        "file_id": effective_file_id,
                        "drive_link": drive_link,
                        "web_view_link": item.get("webViewLink", ""),
                        "is_shortcut": str(is_shortcut).lower(),
                        "shortcut_target_id": target_id,
                        "shortcut_target_mime_type": target_mime,
                    }
                )

            page_token = payload.get("nextPageToken")
            if not page_token:
                break

    rows.sort(key=lambda r: (r["path"].lower(), r["file_name"].lower()))
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "path",
        "file_name",
        "mime_type",
        "file_id",
        "drive_link",
        "web_view_link",
        "is_shortcut",
        "shortcut_target_id",
        "shortcut_target_mime_type",
    ]
    with out_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Folder ID: {folder_id}")
    print(f"Images found: {len(rows)}")
    print(f"CSV written: {out_path}")


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Authorize Google Drive and export image links from a folder."
    )
    parser.add_argument(
        "--credentials",
        default=DEFAULT_CREDENTIALS,
        help="Path to OAuth client JSON.",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p_start = sub.add_parser("auth-start", help="Generate OAuth URL.")
    p_start.add_argument("--state-file", default=DEFAULT_STATE_FILE)

    p_complete = sub.add_parser("auth-complete", help="Exchange auth code for token.")
    p_complete.add_argument("--state-file", default=DEFAULT_STATE_FILE)
    p_complete.add_argument("--token-file", default=DEFAULT_TOKEN_FILE)
    p_complete.add_argument("--redirected-url", required=True)

    p_export = sub.add_parser("export", help="Export image links to CSV.")
    p_export.add_argument("--token-file", default=DEFAULT_TOKEN_FILE)
    p_export.add_argument("--folder", required=True, help="Folder URL or folder ID.")
    p_export.add_argument(
        "--out",
        default="output/drive_image_links.csv",
        help="Output CSV path.",
    )
    return parser


def main() -> int:
    parser = _build_parser()
    args = parser.parse_args()

    credentials = Path(args.credentials)
    if not credentials.exists():
        print(f"Credentials file not found: {credentials}", file=sys.stderr)
        return 1

    try:
        if args.command == "auth-start":
            auth_start(credentials, Path(args.state_file))
        elif args.command == "auth-complete":
            auth_complete(
                credentials,
                Path(args.state_file),
                Path(args.token_file),
                args.redirected_url,
            )
        elif args.command == "export":
            export_image_links(
                credentials,
                Path(args.token_file),
                args.folder,
                Path(args.out),
            )
        else:
            parser.print_help()
            return 1
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
