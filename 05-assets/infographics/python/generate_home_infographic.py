#!/usr/bin/env python3
"""
Kentucky Home Insurance Risk Infographic Generator
Generates professional PNG infographic showing Kentucky weather risks and insurance needs.
"""

from PIL import Image, ImageDraw, ImageFont
import utils
import json
import os

# Load data
data_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'kentucky-insurance-data.json')
with open(data_path, 'r') as f:
    data = json.load(f)

home_data = data['home_insurance']

# Canvas dimensions
WIDTH = 1200
HEIGHT = 2100


def draw_gradient_header(draw: ImageDraw.Draw, y_start: int, height: int) -> int:
    """Draw header for home insurance infographic."""
    y_end = y_start + height
    for i, y in enumerate(range(y_start, y_end)):
        factor = i / height
        color = (
            int(utils.get_color(utils.COLORS['brand_dark'])[0] * (1 - factor * 0.15)),
            int(utils.get_color(utils.COLORS['brand_dark'])[1] * (1 - factor * 0.15)),
            int(utils.get_color(utils.COLORS['brand_dark'])[2] * (1 - factor * 0.15))
        )
        draw.rectangle([(0, y), (WIDTH, y + 1)], fill=color)

    # Title
    title_font = utils.get_font(44, bold=True)
    utils.draw_text_centered(draw, "Common Kentucky Home",
                            (WIDTH // 2, y_start + 50), title_font, 'white')
    utils.draw_text_centered(draw, "Insurance Risks",
                            (WIDTH // 2, y_start + 100), title_font, 'white')

    # Subtitle
    sub_font = utils.get_font(22)
    utils.draw_text_centered(draw, "Protect Your Home From Weather-Related Damage",
                            (WIDTH // 2, y_start + 170), sub_font, 'white')

    # Source badge
    badge_font = utils.get_font(14)
    badge_x, badge_y = WIDTH // 2, y_start + 210
    badge_width = 480
    badge_height = 32
    utils.draw_rounded_rectangle(draw, (badge_x - badge_width//2, badge_y - badge_height//2,
                                       badge_x + badge_width//2, badge_y + badge_height//2),
                                radius=16, fill='light_accent')
    utils.draw_text_centered(draw, f"Source: {home_data['source']}",
                            (badge_x, badge_y), badge_font, 'brand_dark')

    return y_end


def draw_map_panel(draw: ImageDraw.Draw, y_start: int) -> int:
    """Draw stylized Kentucky map with risk zones."""
    margin = 60
    panel_height = 360

    # Background
    utils.draw_rounded_rectangle(draw, (margin, y_start, WIDTH - margin, y_start + panel_height),
                                radius=10, fill='white', outline='gray_light', width=2)

    # Map placeholder (stylized)
    map_x = WIDTH // 2
    map_y = y_start + 140
    map_width = 420
    map_height = 140

    # Draw simplified Kentucky outline (rounded rect)
    utils.draw_rounded_rectangle(draw, (map_x - map_width//2, map_y - map_height//2,
                                       map_x + map_width//2, map_y + map_height//2),
                                radius=30, fill='light_accent', outline='brand_dark', width=3)

    # Risk zone indicators
    zones = [
        {'x': map_x + 100, 'y': map_y - 20, 'color': 'brand_red', 'label': 'Tornado'},
        {'x': map_x - 110, 'y': map_y + 30, 'color': 'orange', 'label': 'Flood'},
        {'x': map_x + 30, 'y': map_y + 20, 'color': 'yellow', 'label': 'Moderate'}
    ]

    for zone in zones:
        # Draw zone circle
        draw.ellipse([(zone['x'] - 28, zone['y'] - 28), (zone['x'] + 28, zone['y'] + 28)],
                    fill=utils.get_color(utils.COLORS[zone['color']]),
                    outline=utils.get_color(utils.COLORS['brand_dark']), width=2)

    # Legend
    legend_y = y_start + 270
    legend_font = utils.get_font(16)
    legend_items = [
        ('yellow', 'Moderate Risk'),
        ('orange', 'High Flood Areas'),
        ('brand_red', 'Tornado Regions')
    ]

    legend_x = WIDTH // 2 - 220
    for color, label in legend_items:
        # Color box
        draw.rectangle([(legend_x, legend_y), (legend_x + 22, legend_y + 22)],
                      fill=utils.get_color(utils.COLORS[color]))
        # Label
        utils.draw_text_left(draw, label, (legend_x + 32, legend_y), legend_font, 'brand_dark')
        legend_x += 160

    # Bottom label
    label_font = utils.get_font(20, bold=True)
    utils.draw_text_centered(draw, "Know Your Local Risk Factors",
                            (WIDTH // 2, y_start + panel_height - 20), label_font, 'brand_dark')

    return y_start + panel_height


def draw_risk_cards(draw: ImageDraw.Draw, y_start: int) -> int:
    """Draw three risk cards for flooding, tornadoes, and winter storms."""
    margin = 60
    card_width = (WIDTH - 2 * margin - 40) // 3
    card_height = 680
    spacing = 20

    for i, risk in enumerate(home_data['risks']):
        x = margin + i * (card_width + spacing)
        y = y_start

        # Card background
        utils.draw_rounded_rectangle(draw, (x, y, x + card_width, y + card_height),
                                    radius=10, fill='white', outline='gray_light', width=2)

        # Header background
        header_height = 110
        utils.draw_rounded_rectangle(draw, (x + 2, y + 2, x + card_width - 2, y + header_height),
                                    radius=8, fill='light_accent')

        # Risk type title
        title_font = utils.get_font(26, bold=True)
        utils.draw_text_centered(draw, risk['type'].upper(),
                                (x + card_width // 2, y + 35), title_font, 'brand_dark')

        # Risk level badge
        badge_color = 'brand_red' if risk['level'] == 'HIGH' else 'orange'
        badge_font = utils.get_font(14, bold=True)
        badge_width = 100
        badge_height = 28
        badge_x = x + card_width // 2
        badge_y = y + 70

        utils.draw_rounded_rectangle(draw, (badge_x - badge_width//2, badge_y - badge_height//2,
                                           badge_x + badge_width//2, badge_y + badge_height//2),
                                    radius=14, fill=badge_color)
        utils.draw_text_centered(draw, risk['level'],
                                (badge_x, badge_y), badge_font, 'white')

        # Content
        content_y = y + header_height + 20
        content_font = utils.get_font(15)
        line_height = 22

        # Types or context
        if 'types' in risk:
            text = f"Types: {', '.join(risk['types'])}"
        else:
            text = risk.get('context', '')

        # Word wrap
        wrapped = utils.wrap_text(draw, text, content_font, card_width - 40)

        for line in wrapped[:3]:
            utils.draw_text_centered(draw, line, (x + card_width // 2, content_y), content_font, 'gray_dark')
            content_y += line_height

        # Kentucky fact box
        fact_y = content_y + 15
        fact_height = 100
        utils.draw_rounded_rectangle(draw, (x + 20, fact_y, x + card_width - 20, fact_y + fact_height),
                                    radius=6, fill='light_accent')
        # Red left border
        draw.rectangle([(x + 22, fact_y), (x + 28, fact_y + fact_height)],
                      fill=utils.get_color(utils.COLORS['brand_red']))

        fact_font = utils.get_font(13, bold=True)
        fact_label = "Kentucky Fact:"
        utils.draw_text_left(draw, fact_label, (x + 40, fact_y + 10), fact_font, 'brand_dark')

        # Wrap fact text
        fact_text = risk['fact']
        fact_lines = utils.wrap_text(draw, fact_text, utils.get_font(12), card_width - 65)

        fact_text_y = fact_y + 35
        for fact_line in fact_lines[:3]:
            utils.draw_text_centered(draw, fact_line, (x + card_width // 2, fact_text_y),
                                    utils.get_font(12), 'gray_dark')
            fact_text_y += 18

        # Protection needed
        protect_y = fact_y + fact_height + 20
        protect_font = utils.get_font(15, bold=True)
        utils.draw_text_left(draw, "Protection Needed:",
                            (x + 20, protect_y), protect_font, 'brand_dark')

        protect_y += 25
        protect_item_font = utils.get_font(13)
        for protection in risk['protection']:
            protect_text = f"✓ {protection}"
            utils.draw_text_left(draw, protect_text, (x + 25, protect_y),
                                protect_item_font, 'gray_dark')
            protect_y += 22

    return y_start + card_height


def draw_action_panel(draw: ImageDraw.Draw, y_start: int) -> int:
    """Draw action alert panel about flood insurance."""
    margin = 60
    panel_height = 260

    # Background with red left border
    panel_width = WIDTH - 2 * margin
    draw.rectangle([(margin, y_start), (margin + 6, y_start + panel_height)],
                  fill=utils.get_color(utils.COLORS['brand_red']))
    utils.draw_rounded_rectangle(draw, (margin + 6, y_start, margin + panel_width, y_start + panel_height),
                                radius=10, fill='light_accent')

    # Warning icon
    icon_font = utils.get_font(48)
    utils.draw_text_centered(draw, "⚠️", (WIDTH // 2, y_start + 30), icon_font, 'brand_dark')

    # Title
    title_font = utils.get_font(24, bold=True)
    title_text = home_data['action_alert']['warning']
    utils.draw_text_centered(draw, title_text, (WIDTH // 2, y_start + 75), title_font, 'brand_dark')

    # Statistic
    stat_font = utils.get_font(20)
    stat_text = home_data['action_alert']['statistic']
    utils.draw_text_centered(draw, stat_text, (WIDTH // 2, y_start + 115), stat_font, 'brand_dark')

    # Action items
    action_y = y_start + 150
    action_font = utils.get_font(16)
    for action in home_data['action_alert']['actions']:
        utils.draw_text_centered(draw, f"→ {action}", (WIDTH // 2, action_y), action_font, 'gray_dark')
        action_y += 28

    return y_start + panel_height


def draw_footer(draw: ImageDraw.Draw, y_start: int) -> int:
    """Draw footer with data sources."""
    margin = 60
    footer_height = 60

    # Background
    draw.rectangle([(margin, y_start), (WIDTH - margin, y_start + footer_height)],
                  fill=utils.get_color(utils.COLORS['light_accent']))

    # Divider line
    draw.line([(margin, y_start), (WIDTH - margin, y_start)],
             fill=utils.get_color(utils.COLORS['gray_light']), width=2)

    # Source text
    footer_font = utils.get_font(11)
    footer_text = "Data sources: National Weather Service (weather.gov) | Federal Emergency Management Agency (fema.gov) | Kentucky Climate Center"
    utils.draw_text_centered(draw, footer_text, (WIDTH // 2, y_start + 32), footer_font, 'gray_mid')

    return y_start + footer_height


def main():
    """Generate the home insurance infographic."""
    # Create canvas
    img = utils.create_canvas(WIDTH, HEIGHT, 'white')
    draw = ImageDraw.Draw(img)

    # Draw all sections
    current_y = 0
    current_y = draw_gradient_header(draw, current_y, 280)
    current_y = draw_map_panel(draw, current_y + 30)
    current_y = draw_risk_cards(draw, current_y + 40)
    current_y = draw_action_panel(draw, current_y + 40)
    current_y = draw_footer(draw, current_y + 20)

    # Save final output
    output_dir = utils.ensure_output_dir()
    output_path = os.path.join(output_dir, 'kentucky-home-insurance-infographic.png')
    img.save(output_path, quality=95, optimize=True)

    print("✓ Home Insurance Infographic Generated Successfully!")
    print(f"  Output: {output_path}")
    print(f"  Dimensions: {WIDTH}x{HEIGHT}px")
    print(f"  File size: {os.path.getsize(output_path) / 1024:.1f} KB")


if __name__ == "__main__":
    main()
