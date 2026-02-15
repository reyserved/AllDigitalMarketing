#!/usr/bin/env python3
"""
AntV Infographic Generator for Dream Assurance Group
Generates professional, artistic infographics using AntV system.

This replaces the Python PIL approach which produced basic wireframes.
AntV creates publication-quality infographics with sophisticated design.
"""

import json
import os
from typing import Dict, List


class AntVInfographicGenerator:
    """
    Generate AntV infographic HTML files from config data.

    Uses AntV Infographic system (https://infographic.antv.vision/)
    to create professional, artistic infographics with:
    - 50+ sophisticated templates
    - Built-in effects (gradients, shadows, patterns)
    - Professional icon library
    - SVG export capability
    - Custom fonts and theming
    """

    # Dream Assurance brand colors
    BRAND_PALETTE = ['#C92A39', '#1D252D', '#F8F9FA', '#28A745', '#FF9800', '#FFC107']

    def __init__(self, output_dir: str = '../antv-generated'):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

    def generate_auto_insurance(self, state: str, data: Dict) -> str:
        """
        Generate auto insurance infographic HTML.

        Args:
            state: State name (e.g., "Kentucky")
            data: Dictionary with liability_limits, pip, scenario

        Returns:
            Path to generated HTML file
        """
        # Extract data
        per_person = data['liability_limits']['bodily_injury_per_person']
        per_accident = data['liability_limits']['bodily_injury_per_accident']
        property_damage = data['liability_limits']['property_damage']

        # Build AntV syntax
        syntax = f"""infographic list-zigzag-down-compact-card
theme
  palette
    - #C92A39
    - #1D252D
    - #F8F9FA
    - #28A745
  base
    text
      font-family Roboto:wght@400;700;900
data
  title {state} Auto Insurance
  subtitle Mandatory Minimum Coverage Requirements
  desc Understanding liability limits and PIP requirements
  lists
    - label 25/50/25 Liability Limits
      desc State minimum coverage per person / per accident / property damage
      icon shield check
    - label Bodily Injury Per Person
      desc {per_person['description']}
      value {per_person['amount']}
      icon user
    - label Bodily Injury Per Accident
      desc {per_accident['description']}
      value {per_accident['amount']}
      icon users
    - label Property Damage
      desc {property_damage['description']}
      value {property_damage['amount']}
      icon car
    - label Personal Injury Protection
      desc {data['pip']['label']} - {' and '.join(data['pip']['covers'])}
      value {data['pip']['amount']}
      icon heart pulse
    - label Real-World Scenario
      desc {data['scenario']['description']}
      value ${data['scenario']['total']:,} covered
      icon check circle"""

        return self._create_html(f"{state.lower()}-auto-insurance", syntax)

    def generate_home_insurance_risks(self, state: str, data: Dict) -> str:
        """
        Generate home insurance risks infographic HTML.

        Args:
            state: State name (e.g., "Kentucky")
            data: Dictionary with risks and action_alert

        Returns:
            Path to generated HTML file
        """
        # Build risk items
        risk_items = []
        for risk in data['risks']:
            risk_type = risk['type'].upper()
            risk_desc = f"{risk['level']} RISK - "

            if 'types' in risk:
                risk_desc += ", ".join(risk['types'])
            else:
                risk_desc += risk.get('context', '')

            # Choose icon based on risk type
            if 'FLOOD' in risk_type or 'Flood' in risk_type:
                icon_name = 'water'
            elif 'TORNADO' in risk_type or 'Tornado' in risk_type:
                icon_name = 'wind'
            elif 'WINTER' in risk_type or 'ICE' in risk_type or 'Winter' in risk_type:
                icon_name = 'snowflake'
            else:
                icon_name = 'warning'

            risk_items.append(f"""    - label {risk_type}
      desc {risk_desc[:80]}
      icon {icon_name}
      value {risk['level']}""")

        risks_syntax = "\n".join(risk_items)

        # Build AntV syntax
        syntax = f"""infographic list-grid-badge-card
theme
  palette
    - #C92A39
    - #FF9800
    - #1D252D
    - #F8F9FA
  stylize rough
data
  title {state} Home Insurance Risks
  desc Protect your home from weather-related damage
  lists
{risks_syntax}"""

        return self._create_html(f"{state.lower()}-home-risks", syntax)

    def _create_html(self, filename: str, syntax: str) -> str:
        """
        Create complete HTML file with AntV infographic embedded.

        Args:
            filename: Name for the HTML file (without extension)
            syntax: AntV Infographic syntax string

        Returns:
            Path to created HTML file
        """
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{filename.replace('-', ' ').title()} - Dream Assurance Group</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700;900&display=swap" rel="stylesheet">
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        body {{
            font-family: 'Roboto', sans-serif;
            background: linear-gradient(135deg, #f5f5f5 0%, #e8e8e8 100%);
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            min-height: 100vh;
            padding: 40px 20px;
        }}
        .wrapper {{
            width: 100%;
            max-width: 1400px;
            display: flex;
            flex-direction: column;
            align-items: center;
        }}
        h1 {{
            margin-bottom: 30px;
            color: #1D252D;
            font-size: 28px;
            font-weight: 900;
            text-align: center;
            letter-spacing: -0.5px;
        }}
        #container {{
            width: 100%;
            height: 85vh;
            background: white;
            border-radius: 20px;
            box-shadow: 0 25px 80px rgba(29, 37, 45, 0.15), 0 10px 30px rgba(29, 37, 45, 0.1);
            overflow: hidden;
        }}
        #export-btn {{
            position: fixed;
            top: 30px;
            right: 30px;
            padding: 16px 32px;
            background: linear-gradient(135deg, #C92A39 0%, #a02030 100%);
            color: white;
            border: none;
            border-radius: 12px;
            font-size: 16px;
            font-weight: 700;
            cursor: pointer;
            box-shadow: 0 6px 20px rgba(201, 42, 57, 0.4);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            letter-spacing: 0.5px;
        }}
        #export-btn:hover {{
            background: linear-gradient(135deg, #1D252D 0%, #0d1216 100%);
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(201, 42, 57, 0.5);
        }}
        #export-btn:active {{
            transform: translateY(0);
        }}
        .instructions {{
            margin-top: 20px;
            padding: 15px 25px;
            background: white;
            border-radius: 10px;
            font-size: 14px;
            color: #555;
            text-align: center;
            box-shadow: 0 4px 15px rgba(0,0,0,0.08);
        }}
        .instructions strong {{
            color: #C92A39;
        }}
    </style>
</head>
<body>
    <div class="wrapper">
        <h1>{filename.replace('-', ' ').title()}</h1>
        <button id="export-btn">Export SVG</button>
        <div id="container"></div>
        <div class="instructions">
            <strong>Instructions:</strong> Click "Export SVG" to download high-quality vector file • Open in any modern browser • Adjust zoom if needed
        </div>
    </div>
    <script src="https://unpkg.com/@antv/infographic@latest/dist/infographic.min.js"></script>
    <script>
        const infographic = new AntVInfographic.Infographic({{
            container: '#container',
            width: '100%',
            height: '100%',
        }});

        document.fonts?.ready.then(() => {{
            infographic.render(`{syntax}`);
        }}).catch((error) => {{
            console.error('Error waiting for fonts to load:', error);
            infographic.render(`{syntax}`);
        }});

        document.getElementById('export-btn').addEventListener('click', async () => {{
            try {{
                const svgDataUrl = await infographic.toDataURL({{ type: 'svg' }});
                const link = document.createElement('a');
                link.download = '{filename}.svg';
                link.href = svgDataUrl;
                link.click();
                console.log('SVG exported successfully!');
            }} catch (error) {{
                console.error('Error exporting SVG:', error);
                alert('Failed to export SVG. Please try again.');
            }}
        }});
    </script>
</body>
</html>"""

        filepath = os.path.join(self.output_dir, f"{filename}.html")
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html)

        return filepath


def generate_from_data_file(data_file: str, state: str):
    """
    Generate both auto and home insurance infographics from data file.

    Args:
        data_file: Path to JSON data file
        state: State name
    """
    with open(data_file, 'r') as f:
        data = json.load(f)

    generator = AntVInfographicGenerator()

    print("=" * 70)
    print(f"Generating AntV Infographics for {state}")
    print("=" * 70)

    # Auto insurance
    auto_path = generator.generate_auto_insurance(state, data['auto_insurance'])
    print(f"✓ Auto insurance: {auto_path}")

    # Home insurance
    home_path = generator.generate_home_insurance_risks(state, data['home_insurance'])
    print(f"✓ Home insurance risks: {home_path}")

    print("=" * 70)
    print("Open HTML files in browser to view professional infographics")
    print("Click 'Export SVG' button to download high-quality vector files")
    print("=" * 70)


if __name__ == "__main__":
    # Get the directory of this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_file = os.path.join(script_dir, '../data/kentucky-insurance-data.json')

    generate_from_data_file(data_file, "Kentucky")
