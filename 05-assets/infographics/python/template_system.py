#!/usr/bin/env python3
"""
Universal Infographic Template System for Dream Assurance Group
A flexible, component-based system for generating high-quality infographics
matching or exceeding the design standards of existing Dream Assurance materials.

This system can generate infographics for:
- State insurance pages (auto, home, life, health)
- Risk assessment visualizations
- Process flow charts
- Comparison tables
- Statistical data visualizations
"""

from PIL import Image, ImageDraw, ImageFont
from typing import Dict, List, Tuple, Optional, Any
import json
import os


class InfographicTemplate:
    """Base class for infographic templates."""

    def __init__(self, width: int = 1200, height: int = 2000):
        self.width = width
        self.height = height
        self.img = None
        self.draw = None
        self.current_y = 0

        # Dream Assurance Brand Colors
        self.colors = {
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

    def get_color(self, color_name: str) -> Tuple[int, int, int]:
        """Convert color name or hex to RGB tuple."""
        if color_name in self.colors:
            hex_color = self.colors[color_name].lstrip('#')
            return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        hex_color = color_name.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

    def get_font(self, size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
        """Get system font with fallback."""
        font_names = [
            '/System/Library/Fonts/Helvetica.ttc',
            '/System/Library/Fonts/Helvetica-Bold.ttc',
            '/System/Library/Fonts/Supplemental/Arial.ttf',
            '/System/Library/Fonts/Supplemental/Arial Bold.ttf',
            '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',
            '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',
            'C:\\Windows\\Fonts\\arial.ttf',
            'C:\\Windows\\Fonts\\arialbd.ttf'
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
        return ImageFont.load_default()

    def wrap_text(self, text: str, font: ImageFont.FreeTypeFont, max_width: int) -> List[str]:
        """Wrap text to fit within max_width."""
        words = text.split(' ')
        lines = []
        current_line = []

        for word in words:
            test_line = ' '.join(current_line + [word])
            bbox = self.draw.textbbox((0, 0), test_line, font=font)
            if bbox[2] - bbox[0] <= max_width:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                current_line = [word]

        if current_line:
            lines.append(' '.join(current_line))

        return lines

    def create_canvas(self, bg_color: str = 'white'):
        """Create new image canvas."""
        color = self.get_color(bg_color)
        self.img = Image.new('RGB', (self.width, self.height), color)
        self.draw = ImageDraw.Draw(self.img)
        self.current_y = 0

    # ========== COMPONENT: GRADIENT HEADER ==========
    def draw_gradient_header(self, title: str, subtitle: str,
                            source: str, height: int = 400,
                            badge_text: Optional[str] = None) -> int:
        """
        Draw sophisticated gradient header with red diagonal accent.

        Args:
            title: Main title (e.g., "KENTUCKY")
            subtitle: Subtitle (e.g., "AUTO INSURANCE")
            source: Data source attribution
            height: Header height in pixels
            badge_text: Optional badge text on red stripe
        """
        # Gradient background
        for i in range(height):
            factor = i / height
            color = (
                int(self.get_color('brand_dark')[0] * (1 - factor * 0.1)),
                int(self.get_color('brand_dark')[1] * (1 - factor * 0.1)),
                int(self.get_color('brand_dark')[2] * (1 - factor * 0.1))
            )
            self.draw.rectangle([(0, self.current_y + i), (self.width, self.current_y + i + 1)], fill=color)

        # Red diagonal accent stripe
        self.draw.polygon([
            (self.width * 0.6, self.current_y),
            (self.width, self.current_y + 100),
            (self.width, self.current_y + 250),
            (self.width * 0.75, self.current_y + height)
        ], fill=self.get_color('brand_red'))

        # Title - large and bold
        title_font = self.get_font(72, bold=True)
        self.draw.text((80, self.current_y + 60), title,
                      fill=self.get_color('white'), font=title_font)

        # Subtitle
        sub_font = self.get_font(32, bold=True)
        self.draw.text((80, self.current_y + 140), subtitle,
                      fill=self.get_color('white'), font=sub_font)

        # Badge text on red stripe
        if badge_text:
            badge_font = self.get_font(16, bold=True)
            lines = badge_text.split('\n')
            badge_y = self.current_y + 120
            for line in lines:
                self.draw.text((self.width - 180, badge_y), line,
                             fill=self.get_color('white'), font=badge_font)
                badge_y += 25

        # Source attribution
        source_font = self.get_font(12)
        self.draw.text((self.width - 350, self.current_y + height - 30),
                      f"Source: {source}",
                      fill=self.get_color('gray_mid'), font=source_font)

        self.current_y += height
        return self.current_y

    # ========== COMPONENT: BIG NUMBERS HERO ==========
    def draw_big_numbers(self, numbers: List[str], labels: List[str],
                         sublabels: List[str], amounts: List[str],
                         section_label: str = "STATE MINIMUM LIABILITY LIMITS",
                         height: int = 350) -> int:
        """
        Draw massive hero numbers with dramatic presentation.

        Args:
            numbers: List of numbers (e.g., ["25", "50", "25"])
            labels: List of primary labels
            sublabels: List of secondary labels
            amounts: List of dollar amounts
            section_label: Section header text
        """
        # White background
        self.draw.rectangle([(0, self.current_y), (self.width, self.current_y + height)],
                          fill=self.get_color('white'))

        # Section label
        label_font = self.get_font(14, bold=True)
        label_bbox = self.draw.textbbox((0, 0), section_label, font=label_font)
        label_width = label_bbox[2] - label_bbox[0]
        self.draw.text(((self.width - label_width) // 2, self.current_y + 25), section_label,
                      fill=self.get_color('gray_mid'), font=label_font)

        # Massive numbers with shadow
        numbers_font = self.get_font(140, bold=True)
        numbers_text = '  '.join(numbers)
        numbers_bbox = self.draw.textbbox((0, 0), numbers_text, font=numbers_font)
        numbers_width = numbers_bbox[2] - numbers_bbox[0]

        # Shadow
        shadow_offset = 3
        self.draw.text(((self.width - numbers_width) // 2 + shadow_offset, self.current_y + 60 + shadow_offset),
                      numbers_text, fill=self.get_color('gray_light'), font=numbers_font)
        # Main numbers
        self.draw.text(((self.width - numbers_width) // 2, self.current_y + 60),
                      numbers_text, fill=self.get_color('brand_red'), font=numbers_font)

        # Dollar signs
        dollar_font = self.get_font(48, bold=True)
        positions = [self.width // 2 - 280, self.width // 2, self.width // 2 + 280]
        for pos in positions:
            self.draw.text((pos - 15, self.current_y + 110), "$",
                          fill=self.get_color('brand_red'), font=dollar_font)

        # Labels
        label_font_small = self.get_font(16, bold=True)
        sub_font = self.get_font(13)
        amount_font = self.get_font(20, bold=True)

        for label, sublabel, amount, x in zip(labels, sublabels, amounts, positions):
            # Primary label
            label_bbox = self.draw.textbbox((0, 0), label, font=label_font_small)
            label_w = label_bbox[2] - label_bbox[0]
            self.draw.text((x - label_w // 2, self.current_y + 230), label,
                          fill=self.get_color('brand_dark'), font=label_font_small)

            # Sublabel
            sub_bbox = self.draw.textbbox((0, 0), sublabel, font=sub_font)
            sub_w = sub_bbox[2] - sub_bbox[0]
            self.draw.text((x - sub_w // 2, self.current_y + 255), sublabel,
                          fill=self.get_color('gray_mid'), font=sub_font)

            # Amount
            amt_bbox = self.draw.textbbox((0, 0), amount, font=amount_font)
            amt_w = amt_bbox[2] - amt_bbox[0]
            self.draw.text((x - amt_w // 2, self.current_y + 285), amount,
                          fill=self.get_color('brand_dark'), font=amount_font)

        self.current_y += height
        return self.current_y

    # ========== COMPONENT: COVERAGE GRID ==========
    def draw_coverage_grid(self, cards: List[Dict], height: int = 450) -> int:
        """
        Draw 3-column grid of coverage cards.

        Args:
            cards: List of card dictionaries with keys:
                - title: Card title
                - subtitle: Card subtitle
                - amount: Dollar amount
                - description: Description text
                - color: 'brand_red' or 'brand_dark'
        """
        # Light gray background
        self.draw.rectangle([(0, self.current_y), (self.width, self.current_y + height)],
                          fill=self.get_color('light_accent'))

        margin = 80
        card_width = (self.width - 2 * margin - 60) // 3
        card_height = 320

        for i, card in enumerate(cards):
            x = margin + i * (card_width + 30)

            # Shadow
            shadow_offset = 4
            self.draw.rectangle([(x + shadow_offset, self.current_y + 40 + shadow_offset),
                              (x + card_width + shadow_offset, self.current_y + 40 + card_height + shadow_offset)],
                             fill=self.get_color('gray_light'))

            # White card
            self.draw.rectangle([(x, self.current_y + 40), (x + card_width, self.current_y + 40 + card_height)],
                              fill=self.get_color('white'))

            # Color accent bar
            self.draw.rectangle([(x, self.current_y + 40), (x + card_width, self.current_y + 48)],
                              fill=self.get_color(card.get('color', 'brand_dark')))

            # Title
            title_font = self.get_font(18, bold=True)
            title_bbox = self.draw.textbbox((0, 0), card['title'], font=title_font)
            title_w = title_bbox[2] - title_bbox[0]
            self.draw.text((x + (card_width - title_w) // 2, self.current_y + 70), card['title'],
                          fill=self.get_color('gray_dark'), font=title_font)

            # Subtitle
            sub_font = self.get_font(14, bold=True)
            sub_bbox = self.draw.textbbox((0, 0), card['subtitle'], font=sub_font)
            sub_w = sub_bbox[2] - sub_bbox[0]
            self.draw.text((x + (card_width - sub_w) // 2, self.current_y + 95), card['subtitle'],
                          fill=self.get_color('brand_red'), font=sub_font)

            # Amount
            amount_font = self.get_font(56, bold=True)
            amount_bbox = self.draw.textbbox((0, 0), card['amount'], font=amount_font)
            amount_w = amount_bbox[2] - amount_bbox[0]
            self.draw.text((x + (card_width - amount_w) // 2, self.current_y + 150), card['amount'],
                          fill=self.get_color(card.get('color', 'brand_dark')), font=amount_font)

            # Description
            desc_font = self.get_font(13)
            lines = self.wrap_text(card['description'], desc_font, card_width - 40)
            desc_y = self.current_y + 230
            for line in lines[:2]:
                line_bbox = self.draw.textbbox((0, 0), line, font=desc_font)
                line_w = line_bbox[2] - line_bbox[0]
                self.draw.text((x + (card_width - line_w) // 2, desc_y), line,
                             fill=self.get_color('gray_mid'), font=desc_font)
                desc_y += 20

        self.current_y += height
        return self.current_y

    # ========== COMPONENT: SPLIT PANEL ==========
    def draw_split_panel(self, left_text: str, right_title: str,
                         right_amount: str, right_label: str,
                         bullets: List[str], left_color: str = 'brand_red',
                         height: int = 200) -> int:
        """
        Draw split color panel (e.g., PIP section).

        Args:
            left_text: Text on colored side (e.g., "PIP")
            right_title: Title on white side
            right_amount: Dollar amount
            right_label: Label below amount
            bullets: List of bullet points
            left_color: Color for left side
        """
        # Split background
        split_point = self.width * 0.35
        self.draw.rectangle([(0, self.current_y), (split_point, self.current_y + height)],
                          fill=self.get_color(left_color))
        self.draw.rectangle([(split_point, self.current_y), (self.width, self.current_y + height)],
                          fill=self.get_color('white'))

        # Left side text
        pip_font = self.get_font(48, bold=True)
        self.draw.text((split_point * 0.5 - 60, self.current_y + 60), left_text,
                      fill=self.get_color('white'), font=pip_font)

        # Right side amount
        amount_font = self.get_font(52, bold=True)
        self.draw.text((split_point + 60, self.current_y + 50), right_amount,
                      fill=self.get_color(left_color), font=amount_font)

        # Right side label
        label_font = self.get_font(16, bold=True)
        self.draw.text((split_point + 60, self.current_y + 120), right_label,
                      fill=self.get_color('brand_dark'), font=label_font)

        # Bullets
        bullet_font = self.get_font(14)
        bullet_y = self.current_y + 155
        for bullet in bullets:
            self.draw.text((split_point + 65, bullet_y), f"• {bullet}",
                          fill=self.get_color('gray_dark'), font=bullet_font)
            bullet_y += 22

        self.current_y += height
        return self.current_y

    # ========== COMPONENT: SCENARIO BOX ==========
    def draw_scenario_box(self, title: str, description: str,
                          breakdown: List[Dict], total: int,
                          height: int = 350) -> int:
        """
        Draw real-world scenario box with breakdown.

        Args:
            title: Section title
            description: Scenario description
            breakdown: List of {item, amount} dicts
            total: Total amount
        """
        # White background
        self.draw.rectangle([(0, self.current_y), (self.width, self.current_y + height)],
                          fill=self.get_color('white'))

        # Section header
        header_font = self.get_font(20, bold=True)
        header_bbox = self.draw.textbbox((0, 0), title, font=header_font)
        header_w = header_bbox[2] - header_bbox[0]
        self.draw.text(((self.width - header_w) // 2, self.current_y + 30), title,
                      fill=self.get_color('brand_dark'), font=header_font)

        # Description
        desc_font = self.get_font(15)
        desc_bbox = self.draw.textbbox((0, 0), description, font=desc_font)
        desc_w = desc_bbox[2] - desc_bbox[0]
        self.draw.text(((self.width - desc_w) // 2, self.current_y + 65), description,
                      fill=self.get_color('gray_dark'), font=desc_font)

        # Breakdown box
        box_y = self.current_y + 100
        box_height = 150
        margin = 100
        box_width = self.width - 2 * margin

        self.draw.rectangle([(margin, box_y), (margin + box_width, box_y + box_height)],
                          fill=self.get_color('light_accent'))

        # Items
        item_font = self.get_font(16)
        amount_font = self.get_font(16, bold=True)
        item_y = box_y + 25

        for item in breakdown:
            text = f"{item['item']}:"
            amount = f"${item['amount']:,}"

            amount_bbox = self.draw.textbbox((0, 0), amount, font=amount_font)
            self.draw.text((margin + 30, item_y), text,
                          fill=self.get_color('gray_dark'), font=item_font)
            self.draw.text((margin + box_width - amount_bbox[2] - 30, item_y), amount,
                          fill=self.get_color('brand_dark'), font=amount_font)

            self.draw.line([(margin + 30, item_y + 28), (margin + box_width - 30, item_y + 28)],
                          fill=self.get_color('gray_light'), width=1)
            item_y += 35

        # Result
        result_y = box_y + box_height + 20
        result_font = self.get_font(24, bold=True)
        check_font = self.get_font(36)

        self.draw.text((margin + 30, result_y), "✓",
                      fill=self.get_color('success_green'), font=check_font)
        self.draw.text((margin + 80, result_y + 5), f"Coverage pays: ${total:,}",
                      fill=self.get_color('success_green'), font=result_font)

        oop_font = self.get_font(16)
        self.draw.text((margin + 80, result_y + 40), "(You pay $0 out of pocket)",
                      fill=self.get_color('success_green'), font=oop_font)

        self.current_y += height
        return self.current_y

    # ========== COMPONENT: RISK CARDS ==========
    def draw_risk_cards(self, risks: List[Dict], height: int = 680) -> int:
        """
        Draw 3-column grid of risk cards.

        Args:
            risks: List of risk dictionaries with keys:
                - type: Risk type name
                - level: 'HIGH' or 'MODERATE'
                - context: Context description
                - types: List of risk types
                - fact: Kentucky-specific fact
                - protection: List of protection items
        """
        margin = 60
        card_width = (self.width - 2 * margin - 40) // 3
        card_height = height - 40
        spacing = 20

        for i, risk in enumerate(risks):
            x = margin + i * (card_width + spacing)
            y = self.current_y

            # Card background
            self.draw.rectangle([(x, y), (x + card_width, y + card_height)],
                              fill=self.get_color('white'),
                              outline=self.get_color('gray_light'), width=2)

            # Header background
            header_height = 110
            self.draw.rectangle([(x + 2, y + 2), (x + card_width - 2, y + header_height)],
                              fill=self.get_color('light_accent'))

            # Risk type
            title_font = self.get_font(26, bold=True)
            self.draw.text((x + card_width // 2, y + 35), risk['type'].upper(),
                          fill=self.get_color('brand_dark'), font=title_font)

            # Risk level badge
            badge_color = 'brand_red' if risk['level'] == 'HIGH' else 'orange'
            badge_font = self.get_font(14, bold=True)
            badge_width = 100
            badge_height = 28

            badge_x = x + card_width // 2
            badge_y = y + 70

            # Draw badge background
            self.draw.rectangle([(badge_x - badge_width//2, badge_y - badge_height//2),
                               (badge_x + badge_width//2, badge_y + badge_height//2)],
                              fill=self.get_color(badge_color))

            # Badge text
            badge_bbox = self.draw.textbbox((0, 0), risk['level'], font=badge_font)
            badge_w = badge_bbox[2] - badge_bbox[0]
            self.draw.text((badge_x - badge_w // 2, badge_y - 10), risk['level'],
                          fill=self.get_color('white'), font=badge_font)

            # Content
            content_y = y + header_height + 20

            # Types or context
            content_font = self.get_font(15)
            if 'types' in risk:
                text = f"Types: {', '.join(risk['types'])}"
            else:
                text = risk.get('context', '')

            lines = self.wrap_text(text, content_font, card_width - 40)
            for line in lines[:3]:
                line_bbox = self.draw.textbbox((0, 0), line, font=content_font)
                line_w = line_bbox[2] - line_bbox[0]
                self.draw.text((x + card_width // 2 - line_w // 2, content_y), line,
                             fill=self.get_color('gray_dark'), font=content_font)
                content_y += 22

            # Fact box
            fact_y = content_y + 15
            fact_height = 100
            self.draw.rectangle([(x + 20, fact_y), (x + card_width - 20, fact_y + fact_height)],
                              fill=self.get_color('light_accent'))
            self.draw.rectangle([(x + 20, fact_y), (x + 26, fact_y + fact_height)],
                              fill=self.get_color('brand_red'))

            fact_font = self.get_font(13, bold=True)
            self.draw.text((x + 40, fact_y + 10), "Kentucky Fact:",
                          fill=self.get_color('brand_dark'), font=fact_font)

            fact_lines = self.wrap_text(risk['fact'], self.get_font(12), card_width - 65)
            fact_text_y = fact_y + 35
            for fact_line in fact_lines[:3]:
                fact_line_bbox = self.draw.textbbox((0, 0), fact_line, font=self.get_font(12))
                fact_line_w = fact_line_bbox[2] - fact_line_bbox[0]
                self.draw.text((x + card_width // 2 - fact_line_w // 2, fact_text_y), fact_line,
                             fill=self.get_color('gray_dark'), font=self.get_font(12))
                fact_text_y += 18

            # Protection needed
            protect_y = fact_y + fact_height + 20
            protect_font = self.get_font(15, bold=True)
            self.draw.text((x + 20, protect_y), "Protection Needed:",
                          fill=self.get_color('brand_dark'), font=protect_font)

            protect_y += 25
            protect_item_font = self.get_font(13)
            for protection in risk['protection']:
                self.draw.text((x + 25, protect_y), f"✓ {protection}",
                             fill=self.get_color('gray_dark'), font=protect_item_font)
                protect_y += 22

        self.current_y += height
        return self.current_y

    # ========== COMPONENT: ACTION ALERT ==========
    def draw_action_alert(self, warning: str, statistic: str,
                          actions: List[str], height: int = 260) -> int:
        """
        Draw action alert panel with red border.

        Args:
            warning: Warning message
            statistic: Statistic text
            actions: List of action items
        """
        margin = 60
        panel_width = self.width - 2 * margin

        # Red left border
        self.draw.rectangle([(margin, self.current_y), (margin + 6, self.current_y + height)],
                          fill=self.get_color('brand_red'))

        # Light accent background
        self.draw.rectangle([(margin + 6, self.current_y), (margin + panel_width, self.current_y + height)],
                          fill=self.get_color('light_accent'))

        # Warning icon
        icon_font = self.get_font(48)
        self.draw.text((self.width // 2, self.current_y + 30), "⚠️",
                      fill=self.get_color('brand_dark'), font=icon_font)

        # Title
        title_font = self.get_font(24, bold=True)
        title_bbox = self.draw.textbbox((0, 0), warning, font=title_font)
        title_w = title_bbox[2] - title_bbox[0]
        self.draw.text((self.width // 2 - title_w // 2, self.current_y + 75), warning,
                      fill=self.get_color('brand_dark'), font=title_font)

        # Statistic
        stat_font = self.get_font(20)
        stat_bbox = self.draw.textbbox((0, 0), statistic, font=stat_font)
        stat_w = stat_bbox[2] - stat_bbox[0]
        self.draw.text((self.width // 2 - stat_w // 2, self.current_y + 115), statistic,
                      fill=self.get_color('brand_dark'), font=stat_font)

        # Action items
        action_y = self.current_y + 150
        action_font = self.get_font(16)
        for action in actions:
            action_bbox = self.draw.textbbox((0, 0), f"→ {action}", font=action_font)
            action_w = action_bbox[2] - action_bbox[0]
            self.draw.text((self.width // 2 - action_w // 2, action_y), f"→ {action}",
                          fill=self.get_color('gray_dark'), font=action_font)
            action_y += 28

        self.current_y += height
        return self.current_y

    # ========== COMPONENT: FOOTER ==========
    def draw_footer(self, sources: List[str], height: int = 60) -> int:
        """
        Draw footer with data sources.

        Args:
            sources: List of source names/URLs
        """
        margin = 60

        # Background
        self.draw.rectangle([(margin, self.current_y), (self.width - margin, self.current_y + height)],
                          fill=self.get_color('light_accent'))

        # Divider
        self.draw.line([(margin, self.current_y), (self.width - margin, self.current_y)],
                      fill=self.get_color('gray_light'), width=2)

        # Source text
        footer_font = self.get_font(11)
        footer_text = " | ".join(sources)
        footer_bbox = self.draw.textbbox((0, 0), footer_text, font=footer_font)
        footer_w = footer_bbox[2] - footer_bbox[0]
        self.draw.text((self.width // 2 - footer_w // 2, self.current_y + 32), footer_text,
                      fill=self.get_color('gray_mid'), font=footer_font)

        self.current_y += height
        return self.current_y

    def save(self, filepath: str, quality: int = 95):
        """Save infographic to file."""
        if self.img:
            self.img.save(filepath, quality=quality, optimize=True)
            print(f"✓ Infographic saved: {filepath}")
            print(f"  Dimensions: {self.width}x{self.height}px")
            print(f"  File size: {os.path.getsize(filepath) / 1024:.1f} KB")


# ========== PRESET TEMPLATES ==========

class StateAutoInsuranceTemplate(InfographicTemplate):
    """Template for state auto insurance requirements infographics."""

    def generate(self, data: Dict):
        """Generate auto insurance infographic from data."""
        self.create_canvas()

        # Header
        badge = "CHOICE\nNO-FAULT\nSTATE" if data.get('state_type') == 'Choice No-Fault' else None
        self.draw_gradient_header(
            title=data['state'].upper(),
            subtitle="AUTO INSURANCE",
            source=data['source'],
            badge_text=badge
        )

        # Big numbers
        limits = data['liability_limits']
        self.draw_big_numbers(
            numbers=[limits['per_person']['number'], limits['per_accident']['number'], limits['property']['number']],
            labels=["PER PERSON", "PER ACCIDENT", "PROPERTY"],
            sublabels=["Bodily Injury", "Bodily Injury", "Damage"],
            amounts=[limits['per_person']['amount'], limits['per_accident']['amount'], limits['property']['amount']]
        )

        # Coverage grid
        cards = [
            {
                'title': 'BODILY INJURY',
                'subtitle': 'PER PERSON',
                'amount': limits['per_person']['short'],
                'description': limits['per_person']['description'],
                'color': 'brand_red'
            },
            {
                'title': 'BODILY INJURY',
                'subtitle': 'PER ACCIDENT',
                'amount': limits['per_accident']['short'],
                'description': limits['per_accident']['description'],
                'color': 'brand_dark'
            },
            {
                'title': 'PROPERTY',
                'subtitle': 'DAMAGE',
                'amount': limits['property']['short'],
                'description': limits['property']['description'],
                'color': 'brand_dark'
            }
        ]
        self.draw_coverage_grid(cards)

        # PIP section
        self.draw_split_panel(
            left_text="PIP",
            right_title=data['pip']['label'],
            right_amount=data['pip']['amount'],
            right_label="MINIMUM REQUIRED",
            bullets=data['pip']['covers']
        )

        # Scenario
        self.draw_scenario_box(
            title="REAL-WORLD SCENARIO",
            description=data['scenario']['description'],
            breakdown=data['scenario']['breakdown'],
            total=data['scenario']['total']
        )


class StateHomeInsuranceTemplate(InfographicTemplate):
    """Template for state home insurance risk infographics."""

    def generate(self, data: Dict):
        """Generate home insurance risk infographic from data."""
        self.create_canvas()

        # Header
        self.draw_gradient_header(
            title=data['state'].upper(),
            subtitle="HOME INSURANCE RISKS",
            source=data['source']
        )

        # Risk cards
        self.draw_risk_cards(data['risks'])

        # Action alert
        self.draw_action_alert(
            warning=data['action_alert']['warning'],
            statistic=data['action_alert']['statistic'],
            actions=data['action_alert']['actions']
        )

        # Footer
        self.draw_footer(data['sources'])


# ========== UTILITY FUNCTIONS ==========

def generate_from_config(config_file: str, output_file: str):
    """
    Generate infographic from configuration file.

    Args:
        config_file: Path to JSON config file
        output_file: Path for output PNG file
    """
    with open(config_file, 'r') as f:
        config = json.load(f)

    template_type = config.get('template', 'state_auto')

    if template_type == 'state_auto':
        template = StateAutoInsuranceTemplate()
    elif template_type == 'state_home':
        template = StateHomeInsuranceTemplate()
    else:
        template = InfographicTemplate()

    template.generate(config['data'])
    template.save(output_file)


if __name__ == "__main__":
    print("Universal Infographic Template System for Dream Assurance Group")
    print("This module provides flexible templates for generating high-quality infographics.")
    print("\nAvailable templates:")
    print("  - StateAutoInsuranceTemplate: State auto insurance requirements")
    print("  - StateHomeInsuranceTemplate: State home insurance risks")
    print("\nUsage: Import this module and use the template classes directly.")
