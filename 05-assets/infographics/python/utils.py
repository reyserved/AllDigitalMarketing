#!/usr/bin/env python3
"""
Utility functions for Kentucky insurance infographic generation.
"""

from PIL import Image, ImageDraw, ImageFont
from typing import Tuple, Optional
import os

# Dream Assurance Brand Colors
COLORS = {
    'brand_red': '#C92A39',
    'brand_dark': '#1D252D',
    'white': '#FFFFFF',
    'light_accent': '#F8F9FA',
    'success_green': '#28A745',
    'orange': '#FF9800',
    'yellow': '#FFC107',
    'gray_light': '#E0E0E0',
    'gray_mid': '#757575',
    'gray_dark': '#555555'
}


def get_color(color: str) -> Tuple[int, int, int]:
    """Get RGB color tuple from hex code or color name."""
    # Check if it's already in COLORS dict
    if color in COLORS:
        hex_color = COLORS[color].lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    # Otherwise treat as hex code
    hex_color = color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))


def create_canvas(width: int, height: int, bg_color: str = 'white') -> Image.Image:
    """Create a new image canvas with specified background."""
    color = get_color(bg_color)
    return Image.new('RGB', (width, height), color)


def draw_rounded_rectangle(draw: ImageDraw.Draw, coords: Tuple[int, int, int, int],
                           radius: int = 10, fill: Optional[str] = None,
                           outline: Optional[str] = None, width: int = 1) -> None:
    """Draw a rounded rectangle."""
    x1, y1, x2, y2 = coords
    draw.rounded_rectangle([(x1, y1), (x2, y2)], radius=radius,
                          fill=get_color(fill) if fill else None,
                          outline=get_color(outline) if outline else None,
                          width=width)


def draw_text_centered(draw: ImageDraw.Draw, text: str, position: Tuple[int, int],
                      font: ImageFont.FreeTypeFont, color: str = 'brand_dark') -> None:
    """Draw text centered at position."""
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    x, y = position
    draw.text((x - text_width // 2, y - text_height // 2), text,
             fill=get_color(color), font=font)


def draw_text_left(draw: ImageDraw.Draw, text: str, position: Tuple[int, int],
                   font: ImageFont.FreeTypeFont, color: str = 'brand_dark') -> None:
    """Draw text left-aligned at position."""
    x, y = position
    draw.text((x, y), text, fill=get_color(color), font=font)


def get_font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    """Get font with specified size and weight."""
    # Try common system fonts, fallback to default
    font_names = [
        '/System/Library/Fonts/Helvetica.ttc',  # macOS
        '/System/Library/Fonts/Helvetica-Bold.ttc',  # macOS bold
        '/System/Library/Fonts/Supplemental/Arial.ttf',  # macOS
        '/System/Library/Fonts/Supplemental/Arial Bold.ttf',  # macOS bold
        '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',  # Linux
        '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',  # Linux bold
        'C:\\Windows\\Fonts\\arial.ttf',  # Windows
        'C:\\Windows\\Fonts\\arialbd.ttf'  # Windows bold
    ]

    if bold:
        bold_fonts = [f.replace('.ttf', '-Bold.ttf').replace('.ttc', '-Bold.ttc') for f in font_names]
        font_names.extend(bold_fonts)

    for font_name in font_names:
        if os.path.exists(font_name):
            try:
                return ImageFont.truetype(font_name, size)
            except:
                pass

    # Fallback to default font
    return ImageFont.load_default()


def ensure_output_dir():
    """Ensure output directory exists."""
    output_dir = os.path.join(os.path.dirname(__file__), '..', 'output')
    os.makedirs(output_dir, exist_ok=True)
    return output_dir


def wrap_text(draw: ImageDraw.Draw, text: str, font: ImageFont.FreeTypeFont,
              max_width: int) -> list:
    """Wrap text to fit within max_width."""
    words = text.split(' ')
    lines = []
    current_line = []

    for word in words:
        test_line = ' '.join(current_line + [word])
        bbox = draw.textbbox((0, 0), test_line, font=font)
        if bbox[2] - bbox[0] <= max_width:
            current_line.append(word)
        else:
            if current_line:
                lines.append(' '.join(current_line))
            current_line = [word]

    if current_line:
        lines.append(' '.join(current_line))

    return lines
