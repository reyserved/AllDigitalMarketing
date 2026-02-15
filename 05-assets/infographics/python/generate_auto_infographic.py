#!/usr/bin/env python3
"""
Kentucky Auto Insurance Infographic Generator - Sophisticated Design
High-end visual design with bold color blocking, layered elements, and professional typography.
"""

from PIL import Image, ImageDraw, ImageFont
import utils
import json
import os

# Load data
data_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'kentucky-insurance-data.json')
with open(data_path, 'r') as f:
    data = json.load(f)

auto_data = data['auto_insurance']

# Canvas dimensions (print quality at 150 DPI)
WIDTH = 1200
HEIGHT = 2000


def draw_hero_header(draw: ImageDraw.Draw, y_start: int) -> int:
    """Draw dramatic hero header with bold typography and color blocking."""
    header_height = 400

    # Main color block - dark background with slight gradient
    for i in range(header_height):
        factor = i / header_height
        color = (
            int(utils.get_color('brand_dark')[0] * (1 - factor * 0.1)),
            int(utils.get_color('brand_dark')[1] * (1 - factor * 0.1)),
            int(utils.get_color('brand_dark')[2] * (1 - factor * 0.1))
        )
        draw.rectangle([(0, y_start + i), (WIDTH, y_start + i + 1)], fill=color)

    # Bold geometric accent - red diagonal stripe
    draw.polygon([
        (WIDTH * 0.6, y_start),
        (WIDTH, y_start + 100),
        (WIDTH, y_start + 250),
        (WIDTH * 0.75, y_start + header_height)
    ], fill=utils.get_color('brand_red'))

    # Large typography - KENTUCKY
    title_font = utils.get_font(72, bold=True)
    draw.text((80, y_start + 60), "KENTUCKY",
             fill=utils.get_color('white'), font=title_font)

    # Subtitle - smaller but bold
    sub_font = utils.get_font(32, bold=True)
    draw.text((80, y_start + 140), "AUTO INSURANCE",
             fill=utils.get_color('white'), font=sub_font)

    # Required minimums text
    tag_font = utils.get_font(20)
    draw.text((80, y_start + 190), "MANDATORY MINIMUM COVERAGE",
             fill=utils.get_color('light_accent'), font=tag_font)

    # No-fault badge on red stripe
    badge_font = utils.get_font(16, bold=True)
    draw.text((WIDTH - 180, y_start + 120), "CHOICE",
             fill=utils.get_color('white'), font=badge_font)
    draw.text((WIDTH - 180, y_start + 145), "NO-FAULT",
             fill=utils.get_color('white'), font=badge_font)
    draw.text((WIDTH - 180, y_start + 170), "STATE",
             fill=utils.get_color('white'), font=badge_font)

    # Source attribution - bottom right
    source_font = utils.get_font(12)
    draw.text((WIDTH - 350, y_start + header_height - 30),
             "Source: Kentucky Transportation Cabinet",
             fill=utils.get_color('gray_mid'), font=source_font)

    return y_start + header_height


def draw_big_numbers_section(draw: ImageDraw.Draw, y_start: int) -> int:
    """Draw massive 25/50/25 numbers with dramatic presentation."""
    section_height = 350

    # White background
    draw.rectangle([(0, y_start), (WIDTH, y_start + section_height)],
                  fill=utils.get_color('white'))

    # Section label - small and refined
    label_font = utils.get_font(14, bold=True)
    label_text = "STATE MINIMUM LIABILITY LIMITS"
    label_bbox = draw.textbbox((0, 0), label_text, font=label_font)
    label_width = label_bbox[2] - label_bbox[0]
    draw.text(((WIDTH - label_width) // 2, y_start + 25), label_text,
             fill=utils.get_color('gray_mid'), font=label_font)

    # Massive numbers - truly dramatic
    numbers_font = utils.get_font(140, bold=True)
    numbers_text = "25  50  25"
    numbers_bbox = draw.textbbox((0, 0), numbers_text, font=numbers_font)
    numbers_width = numbers_bbox[2] - numbers_bbox[0]

    # Draw numbers with slight shadow effect
    shadow_offset = 3
    draw.text(((WIDTH - numbers_width) // 2 + shadow_offset, y_start + 60 + shadow_offset),
             numbers_text, fill=utils.get_color('gray_light'), font=numbers_font)
    draw.text(((WIDTH - numbers_width) // 2, y_start + 60),
             numbers_text, fill=utils.get_color('brand_red'), font=numbers_font)

    # Dollar signs - elegant and smaller
    dollar_font = utils.get_font(48, bold=True)
    positions = [WIDTH // 2 - 280, WIDTH // 2, WIDTH // 2 + 280]
    for pos in positions:
        draw.text((pos - 15, y_start + 110), "$",
                 fill=utils.get_color('brand_red'), font=dollar_font)

    # Bottom labels - clean and aligned
    label_font_small = utils.get_font(16, bold=True)
    labels = ["PER PERSON", "PER ACCIDENT", "PROPERTY"]
    x_positions = [WIDTH // 2 - 280, WIDTH // 2, WIDTH // 2 + 280]

    for label, x in zip(labels, x_positions):
        label_bbox = draw.textbbox((0, 0), label, font=label_font_small)
        label_w = label_bbox[2] - label_bbox[0]
        draw.text((x - label_w // 2, y_start + 230), label,
                 fill=utils.get_color('brand_dark'), font=label_font_small)

    # Sub-labels
    sub_font = utils.get_font(13)
    sublabels = ["Bodily Injury", "Bodily Injury", "Damage"]
    for sublabel, x in zip(sublabels, x_positions):
        sub_bbox = draw.textbbox((0, 0), sublabel, font=sub_font)
        sub_w = sub_bbox[2] - sub_bbox[0]
        draw.text((x - sub_w // 2, y_start + 255), sublabel,
                 fill=utils.get_color('gray_mid'), font=sub_font)

    # Dollar amounts below
    amount_font = utils.get_font(20, bold=True)
    amounts = ["$25,000", "$50,000", "$25,000"]
    for amount, x in zip(amounts, x_positions):
        amt_bbox = draw.textbbox((0, 0), amount, font=amount_font)
        amt_w = amt_bbox[2] - amt_bbox[0]
        draw.text((x - amt_w // 2, y_start + 285), amount,
                 fill=utils.get_color('brand_dark'), font=amount_font)

    return y_start + section_height


def draw_coverage_grid(draw: ImageDraw.Draw, y_start: int) -> int:
    """Draw three coverage cards in sophisticated grid layout."""
    section_height = 450

    # Light gray background section
    draw.rectangle([(0, y_start), (WIDTH, y_start + section_height)],
                  fill=utils.get_color('light_accent'))

    margin = 80
    card_width = (WIDTH - 2 * margin - 60) // 3
    card_height = 320

    coverage_data = [
        {
            'title': 'BODILY INJURY',
            'subtitle': 'PER PERSON',
            'amount': '$25K',
            'desc': 'Each person injured in an accident you cause',
            'color': 'brand_red'
        },
        {
            'title': 'BODILY INJURY',
            'subtitle': 'PER ACCIDENT',
            'amount': '$50K',
            'desc': 'Total for all injuries in one accident',
            'color': 'brand_dark'
        },
        {
            'title': 'PROPERTY',
            'subtitle': 'DAMAGE',
            'amount': '$25K',
            'desc': 'Another person\'s vehicle or property',
            'color': 'brand_dark'
        }
    ]

    for i, card in enumerate(coverage_data):
        x = margin + i * (card_width + 30)

        # Card shadow
        shadow_offset = 4
        draw.rectangle([(x + shadow_offset, y_start + 40 + shadow_offset),
                       (x + card_width + shadow_offset, y_start + 40 + card_height + shadow_offset)],
                      fill=utils.get_color('gray_light'))

        # White card
        draw.rectangle([(x, y_start + 40), (x + card_width, y_start + 40 + card_height)],
                      fill=utils.get_color('white'))

        # Color accent bar at top
        accent_height = 8
        draw.rectangle([(x, y_start + 40), (x + card_width, y_start + 40 + accent_height)],
                      fill=utils.get_color(card['color']))

        # Title - bold and small
        title_font = utils.get_font(18, bold=True)
        title_bbox = draw.textbbox((0, 0), card['title'], font=title_font)
        title_w = title_bbox[2] - title_bbox[0]
        draw.text((x + (card_width - title_w) // 2, y_start + 70), card['title'],
                 fill=utils.get_color('gray_dark'), font=title_font)

        # Subtitle
        sub_font = utils.get_font(14, bold=True)
        sub_bbox = draw.textbbox((0, 0), card['subtitle'], font=sub_font)
        sub_w = sub_bbox[2] - sub_bbox[0]
        draw.text((x + (card_width - sub_w) // 2, y_start + 95), card['subtitle'],
                 fill=utils.get_color('brand_red'), font=sub_font)

        # Amount - large and bold
        amount_font = utils.get_font(56, bold=True)
        amount_bbox = draw.textbbox((0, 0), card['amount'], font=amount_font)
        amount_w = amount_bbox[2] - amount_bbox[0]
        draw.text((x + (card_width - amount_w) // 2, y_start + 150), card['amount'],
                 fill=utils.get_color(card['color']), font=amount_font)

        # Description - wrapped and refined
        desc_font = utils.get_font(13)
        words = card['desc'].split(' ')
        lines = []
        current_line = []
        for word in words:
            test = ' '.join(current_line + [word])
            bbox = draw.textbbox((0, 0), test, font=desc_font)
            if bbox[2] - bbox[0] < card_width - 40:
                current_line.append(word)
            else:
                lines.append(' '.join(current_line))
                current_line = [word]
        if current_line:
            lines.append(' '.join(current_line))

        desc_y = y_start + 230
        for line in lines[:2]:
            line_bbox = draw.textbbox((0, 0), line, font=desc_font)
            line_w = line_bbox[2] - line_bbox[0]
            draw.text((x + (card_width - line_w) // 2, desc_y), line,
                     fill=utils.get_color('gray_mid'), font=desc_font)
            desc_y += 20

    return y_start + section_height


def draw_pip_section(draw: ImageDraw.Draw, y_start: int) -> int:
    """Draw PIP section with bold color blocking."""
    section_height = 200

    # Split background - red and white
    draw.rectangle([(0, y_start), (WIDTH * 0.35, y_start + section_height)],
                  fill=utils.get_color('brand_red'))
    draw.rectangle([(WIDTH * 0.35, y_start), (WIDTH, y_start + section_height)],
                  fill=utils.get_color('white'))

    # PIP label on red
    pip_font = utils.get_font(48, bold=True)
    draw.text((WIDTH * 0.175 - 60, y_start + 60), "PIP",
             fill=utils.get_color('white'), font=pip_font)

    pip_sub = utils.get_font(14, bold=True)
    draw.text((WIDTH * 0.175 - 90, y_start + 120), "PERSONAL INJURY",
             fill=utils.get_color('white'), font=pip_sub)
    draw.text((WIDTH * 0.175 - 90, y_start + 140), "PROTECTION",
             fill=utils.get_color('white'), font=pip_sub)

    # Amount on white
    amount_font = utils.get_font(52, bold=True)
    draw.text((WIDTH * 0.35 + 60, y_start + 50), "$10,000",
             fill=utils.get_color('brand_red'), font=amount_font)

    # Label
    label_font = utils.get_font(16, bold=True)
    draw.text((WIDTH * 0.35 + 60, y_start + 120), "MINIMUM REQUIRED",
             fill=utils.get_color('brand_dark'), font=label_font)

    # Bullet points
    bullet_font = utils.get_font(14)
    bullets = auto_data['pip']['covers']
    bullet_y = y_start + 155
    for bullet in bullets:
        draw.text((WIDTH * 0.35 + 65, bullet_y), f"• {bullet}",
                 fill=utils.get_color('gray_dark'), font=bullet_font)
        bullet_y += 22

    return y_start + section_height


def draw_scenario_section(draw: ImageDraw.Draw, y_start: int) -> int:
    """Draw real-world scenario with clean presentation."""
    section_height = 350

    # White background
    draw.rectangle([(0, y_start), (WIDTH, y_start + section_height)],
                  fill=utils.get_color('white'))

    # Section header
    header_font = utils.get_font(20, bold=True)
    header_text = "REAL-WORLD SCENARIO"
    header_bbox = draw.textbbox((0, 0), header_text, font=header_font)
    header_w = header_bbox[2] - header_bbox[0]
    draw.text(((WIDTH - header_w) // 2, y_start + 30), header_text,
             fill=utils.get_color('brand_dark'), font=header_font)

    # Scenario description
    desc_font = utils.get_font(15)
    scenario_text = auto_data['scenario']['description']
    scenario_bbox = draw.textbbox((0, 0), scenario_text, font=desc_font)
    scenario_w = scenario_bbox[2] - scenario_bbox[0]
    draw.text(((WIDTH - scenario_w) // 2, y_start + 65), scenario_text,
             fill=utils.get_color('gray_dark'), font=desc_font)

    # Breakdown box
    box_y = y_start + 100
    box_height = 150
    margin = 100
    box_width = WIDTH - 2 * margin

    # Subtle background
    draw.rectangle([(margin, box_y), (margin + box_width, box_y + box_height)],
                  fill=utils.get_color('light_accent'))

    # Items
    item_font = utils.get_font(16)
    amount_font = utils.get_font(16, bold=True)
    item_y = box_y + 25

    for item in auto_data['scenario']['breakdown']:
        text = f"{item['item']}:"
        amount = f"${item['amount']:,}"

        text_bbox = draw.textbbox((0, 0), text, font=item_font)
        amount_bbox = draw.textbbox((0, 0), amount, font=amount_font)

        draw.text((margin + 30, item_y), text,
                 fill=utils.get_color('gray_dark'), font=item_font)
        draw.text((margin + box_width - amount_bbox[2] - 30, item_y), amount,
                 fill=utils.get_color('brand_dark'), font=amount_font)

        # Divider line
        draw.line([(margin + 30, item_y + 28), (margin + box_width - 30, item_y + 28)],
                 fill=utils.get_color('gray_light'), width=1)
        item_y += 35

    # Total result - bold and dramatic
    result_y = box_y + box_height + 20
    result_font = utils.get_font(24, bold=True)
    total = auto_data['scenario']['total']

    # Green checkmark
    check_font = utils.get_font(36)
    draw.text((margin + 30, result_y), "✓",
             fill=utils.get_color('success_green'), font=check_font)

    # Result text
    result_text = f"Coverage pays: ${total:,}"
    draw.text((margin + 80, result_y + 5), result_text,
             fill=utils.get_color('success_green'), font=result_font)

    # Out of pocket
    oop_font = utils.get_font(16)
    draw.text((margin + 80, result_y + 40), "(You pay $0 out of pocket)",
             fill=utils.get_color('success_green'), font=oop_font)

    return y_start + section_height


def main():
    """Generate the sophisticated auto insurance infographic."""
    # Create canvas
    img = utils.create_canvas(WIDTH, HEIGHT, 'white')
    draw = ImageDraw.Draw(img)

    # Draw all sections
    current_y = 0
    current_y = draw_hero_header(draw, current_y)
    current_y = draw_big_numbers_section(draw, current_y)
    current_y = draw_coverage_grid(draw, current_y)
    current_y = draw_pip_section(draw, current_y)
    current_y = draw_scenario_section(draw, current_y)

    # Save final output
    output_dir = utils.ensure_output_dir()
    output_path = os.path.join(output_dir, 'kentucky-auto-insurance-infographic.png')
    img.save(output_path, quality=95, optimize=True)

    print("✓ Sophisticated Auto Insurance Infographic Generated!")
    print(f"  Output: {output_path}")
    print(f"  Dimensions: {WIDTH}x{HEIGHT}px")
    print(f"  File size: {os.path.getsize(output_path) / 1024:.1f} KB")


if __name__ == "__main__":
    main()
