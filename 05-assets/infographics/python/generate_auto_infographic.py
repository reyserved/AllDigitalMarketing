#!/usr/bin/env python3
"""
Kentucky Auto Insurance Infographic Generator
Generates professional PNG infographic explaining Kentucky's auto insurance requirements.
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
HEIGHT = 1800


def draw_gradient_header(draw: ImageDraw.Draw, y_start: int, height: int) -> int:
    """Draw gradient header with title and subtitle."""
    y_end = y_start + height
    for i, y in enumerate(range(y_start, y_end)):
        # Gradient from brand_dark to slightly lighter
        factor = i / height
        color = (
            int(utils.get_color(utils.COLORS['brand_dark'])[0] * (1 - factor * 0.15)),
            int(utils.get_color(utils.COLORS['brand_dark'])[1] * (1 - factor * 0.15)),
            int(utils.get_color(utils.COLORS['brand_dark'])[2] * (1 - factor * 0.15))
        )
        draw.rectangle([(0, y), (WIDTH, y + 1)], fill=color)

    # Title
    title_font = utils.get_font(48, bold=True)
    utils.draw_text_centered(draw, "Kentucky Auto Insurance",
                            (WIDTH // 2, y_start + 50), title_font, 'white')
    utils.draw_text_centered(draw, "Requirements",
                            (WIDTH // 2, y_start + 110), title_font, 'white')

    # Subtitle
    sub_font = utils.get_font(24)
    utils.draw_text_centered(draw, "Choice No-Fault State | Mandatory Minimum Coverage",
                            (WIDTH // 2, y_start + 180), sub_font, 'white')

    # Source badge
    badge_font = utils.get_font(16)
    badge_x, badge_y = WIDTH // 2, y_start + 220
    badge_width = 420
    badge_height = 36
    utils.draw_rounded_rectangle(draw, (badge_x - badge_width//2, badge_y - badge_height//2,
                                       badge_x + badge_width//2, badge_y + badge_height//2),
                                radius=18, fill='light_accent')
    utils.draw_text_centered(draw, f"Source: {auto_data['source']}",
                            (badge_x, badge_y), badge_font, 'brand_dark')

    return y_end


def draw_hero_display(draw: ImageDraw.Draw, y_start: int) -> int:
    """Draw the large 25/50/25 display."""
    margin = 60
    section_height = 320

    # White background with red border
    utils.draw_rounded_rectangle(draw, (margin, y_start, WIDTH - margin, y_start + section_height),
                                radius=12, fill='white', outline='brand_red', width=4)

    # Main numbers display
    numbers_font = utils.get_font(96, bold=True)
    utils.draw_text_centered(draw, "25 / 50 / 25",
                            (WIDTH // 2, y_start + 80), numbers_font, 'brand_red')

    # Label
    label_font = utils.get_font(32, bold=True)
    utils.draw_text_centered(draw, "State Minimum Liability Limits",
                            (WIDTH // 2, y_start + 160), label_font, 'brand_dark')

    # Three column breakdown
    col_y = y_start + 220
    col_font = utils.get_font(22, bold=True)
    col_spacing = WIDTH // 3

    utils.draw_text_centered(draw, "$25K",
                            (col_spacing // 2, col_y), col_font, 'brand_dark')
    utils.draw_text_centered(draw, "Per Person",
                            (col_spacing // 2, col_y + 30), utils.get_font(18), 'brand_dark')

    utils.draw_text_centered(draw, "$50K",
                            (col_spacing + col_spacing // 2, col_y), col_font, 'brand_dark')
    utils.draw_text_centered(draw, "Per Accident",
                            (col_spacing + col_spacing // 2, col_y + 30), utils.get_font(18), 'brand_dark')

    utils.draw_text_centered(draw, "$25K",
                            (col_spacing * 2 + col_spacing // 2, col_y), col_font, 'brand_dark')
    utils.draw_text_centered(draw, "Property Damage",
                            (col_spacing * 2 + col_spacing // 2, col_y + 30), utils.get_font(18), 'brand_dark')

    return y_start + section_height


def draw_coverage_breakdown(draw: ImageDraw.Draw, y_start: int) -> int:
    """Draw three coverage cards in columns."""
    margin = 60
    card_width = (WIDTH - 2 * margin - 40) // 3
    card_height = 420
    spacing = 20

    coverage_types = [
        {
            'title': 'Bodily Injury\nPer Person',
            'amount': '$25,000',
            'description': 'Maximum coverage for each individual injured in an accident you cause',
            'example': 'Covers medical expenses, rehabilitation costs, and lost wages'
        },
        {
            'title': 'Bodily Injury\nPer Accident',
            'amount': '$50,000',
            'description': 'Total coverage for all injuries in a single accident, regardless of number of people',
            'example': 'If 3 people are injured, this $50,000 is split among all claims'
        },
        {
            'title': 'Property Damage',
            'amount': '$25,000',
            'description': 'Damage to another person\'s vehicle, property, or structures',
            'example': 'Repairs to another driver\'s car, fence, mailbox, or building'
        }
    ]

    for i, coverage in enumerate(coverage_types):
        x = margin + i * (card_width + spacing)

        # Card background
        utils.draw_rounded_rectangle(draw, (x, y_start, x + card_width, y_start + card_height),
                                    radius=10, fill='light_accent', outline='gray_light', width=2)

        # Amount
        amount_font = utils.get_font(52, bold=True)
        utils.draw_text_centered(draw, coverage['amount'],
                                (x + card_width // 2, y_start + 50), amount_font, 'brand_red')

        # Title
        title_font = utils.get_font(22, bold=True)
        lines = coverage['title'].split('\n')
        title_y = y_start + 120
        for line in lines:
            utils.draw_text_centered(draw, line, (x + card_width // 2, title_y), title_font, 'brand_dark')
            title_y += 28

        # Description
        desc_font = utils.get_font(15)
        wrapped = utils.wrap_text(draw, coverage['description'], desc_font, card_width - 40)
        desc_y = y_start + 180
        for line in wrapped[:3]:
            utils.draw_text_centered(draw, line, (x + card_width // 2, desc_y), desc_font, 'gray_dark')
            desc_y += 20

        # Example
        example_font = utils.get_font(13)
        example_text = f"Example: {coverage['example']}"
        bbox = draw.textbbox((0, 0), example_text, font=example_font)
        if bbox[2] - bbox[0] > card_width - 40:
            example_text = example_text[:55] + "..."

        utils.draw_text_centered(draw, example_text,
                                (x + card_width // 2, y_start + card_height - 45),
                                example_font, 'gray_mid')

    return y_start + card_height


def draw_pip_panel(draw: ImageDraw.Draw, y_start: int) -> int:
    """Draw Personal Injury Protection panel."""
    margin = 60
    panel_height = 180

    # Background
    utils.draw_rounded_rectangle(draw, (margin, y_start, WIDTH - margin, y_start + panel_height),
                                radius=10, fill='light_accent')

    # Title
    title_font = utils.get_font(28, bold=True)
    utils.draw_text_centered(draw, "Personal Injury Protection (PIP)",
                            (WIDTH // 2, y_start + 30), title_font, 'brand_dark')

    # Amount
    amount_font = utils.get_font(36, bold=True)
    utils.draw_text_centered(draw, f"Minimum Required: {auto_data['pip']['label']}",
                            (WIDTH // 2, y_start + 80), amount_font, 'brand_red')

    # Bullets
    bullet_font = utils.get_font(18)
    bullets = auto_data['pip']['covers']
    bullet_y = y_start + 125
    bullet_spacing = 250

    for i, bullet in enumerate(bullets):
        x_pos = WIDTH // 2 - len(bullets) * bullet_spacing // 2 + i * bullet_spacing + bullet_spacing // 2
        draw.text((x_pos, bullet_y), f"• {bullet}",
                 fill=utils.get_color(utils.COLORS['gray_dark']), font=bullet_font)

    return y_start + panel_height


def draw_scenario_panel(draw: ImageDraw.Draw, y_start: int) -> int:
    """Draw real-world coverage scenario."""
    margin = 60
    panel_height = 320

    # Border panel
    utils.draw_rounded_rectangle(draw, (margin, y_start, WIDTH - margin, y_start + panel_height),
                                radius=10, fill='white', outline='gray_light', width=2)

    # Title
    title_font = utils.get_font(24, bold=True)
    utils.draw_text_left(draw, "COVERAGE SCENARIO EXAMPLE",
                        (margin + 20, y_start + 20), title_font, 'brand_dark')

    # Description
    desc_font = utils.get_font(18)
    scenario_desc = auto_data['scenario']['description']
    utils.draw_text_left(draw, scenario_desc,
                        (margin + 20, y_start + 60), desc_font, 'gray_dark')

    # Breakdown
    breakdown_y = y_start + 110
    breakdown_font = utils.get_font(20)

    for item in auto_data['scenario']['breakdown']:
        text = f"{item['item']}: ${item['amount']:,}"
        utils.draw_text_left(draw, text, (margin + 40, breakdown_y), breakdown_font, 'gray_dark')
        breakdown_y += 30

    # Result
    result_font = utils.get_font(22, bold=True)
    total = auto_data['scenario']['total']
    check_y = breakdown_y + 20

    # Draw checkmark in green
    check_font = utils.get_font(32)
    draw.text((margin + 40, check_y), "✓",
             fill=utils.get_color(utils.COLORS['success_green']),
             font=check_font)
    draw.text((margin + 75, check_y), f"Your 25/50/25 coverage pays: ${total:,}",
             fill=utils.get_color(utils.COLORS['success_green']),
             font=result_font)

    # Out of pocket
    oop_font = utils.get_font(18)
    draw.text((margin + 75, check_y + 35), "(You pay $0 out of pocket)",
             fill=utils.get_color(utils.COLORS['success_green']),
             font=oop_font)

    return y_start + panel_height


def main():
    """Generate the auto insurance infographic."""
    # Create canvas
    img = utils.create_canvas(WIDTH, HEIGHT, 'white')
    draw = ImageDraw.Draw(img)

    # Draw all sections
    current_y = 0
    current_y = draw_gradient_header(draw, current_y, 280)
    current_y = draw_hero_display(draw, current_y + 20)
    current_y = draw_coverage_breakdown(draw, current_y + 40)
    current_y = draw_pip_panel(draw, current_y + 30)
    current_y = draw_scenario_panel(draw, current_y + 30)

    # Save final output
    output_dir = utils.ensure_output_dir()
    output_path = os.path.join(output_dir, 'kentucky-auto-insurance-infographic.png')
    img.save(output_path, quality=95, optimize=True)

    print("✓ Auto Insurance Infographic Generated Successfully!")
    print(f"  Output: {output_path}")
    print(f"  Dimensions: {WIDTH}x{HEIGHT}px")
    print(f"  File size: {os.path.getsize(output_path) / 1024:.1f} KB")


if __name__ == "__main__":
    main()
