# Universal Infographic Generation Guide
## Dream Assurance Group - Template System Documentation

---

## Quick Start

### For Kentucky Personal Insurance (Already Done)
```bash
cd "05-assets/infographics/python"
python3 generate_auto_infographic.py
python3 generate_home_infographic.py
```

### For Any New State or Content
Follow the **3-Step Process** below.

---

## Step 1: Research & Data Collection

### Authoritative Data Sources (.gov required)

**Auto Insurance Requirements:**
- Search: `[State Name] auto insurance minimum requirements`
- Visit: State DMV/Transportation Cabinet website
- Extract: Liability limits (25/50/25 format), PIP requirements, no-fault status

**Home Insurance Risks:**
- Search: `[State Name] weather risks homeowners insurance`
- Visit: NOAA/NWS state offices, FEMA regional offices
- Extract: Weather statistics, risk zones, historical events

**Always verify:**
- ✓ Data is from .gov or authoritative research sites
- ✓ Information is current (within last year)
- ✓ Sources are cited accurately

### Data Structure Template

**For Auto Insurance Pages:**
```json
{
  "state": "StateName",
  "source": "Authority Name (url)",
  "state_type": "No-Fault/Choice No-Fault/Tort",
  "liability_limits": {
    "per_person": {"number": "25", "amount": "$25,000", "short": "$25K", "description": "..."},
    "per_accident": {"number": "50", "amount": "$50,000", "short": "$50K", "description": "..."},
    "property": {"number": "25", "amount": "$25,000", "short": "$25K", "description": "..."}
  },
  "pip": {"label": "$10,000", "amount": "$10,000", "covers": ["...", "..."]},
  "scenario": {"description": "...", "breakdown": [...], "total": 48000}
}
```

**For Home Insurance Pages:**
```json
{
  "state": "StateName",
  "source": "NWS | FEMA",
  "sources": ["Source 1", "Source 2", "Source 3"],
  "risks": [
    {"type": "Risk Name", "level": "HIGH/MODERATE", "types": [...], "fact": "...", "protection": [...]},
    {"type": "Risk Name", "level": "HIGH/MODERATE", "context": "...", "fact": "...", "protection": [...]}
  ],
  "action_alert": {"warning": "...", "statistic": "...", "actions": [...]}
}
```

---

## Step 2: Create Configuration File

### Option A: Manual JSON Creation

Create a config file in `05-assets/infographics/configs/`:

**Example: `kansas-auto-config.json`**
```json
{
  "template": "state_auto",
  "data": {
    "state": "Kansas",
    "source": "Kansas Insurance Department (insurance.kansas.gov)",
    "state_type": "Tort",
    "liability_limits": {
      "per_person": {"number": "25", "amount": "$25,000", "short": "$25K", "description": "Each person injured in an accident you cause"},
      "per_accident": {"number": "50", "amount": "$50,000", "short": "$50K", "description": "Total for all injuries in one accident"},
      "property": {"number": "25", "amount": "$25,000", "short": "$25K", "description": "Damage to another's vehicle or property"}
    },
    "pip": {"label": "Not Required", "amount": "N/A", "covers": ["Kansas is a tort state"]},
    "scenario": {
      "description": "You cause an accident injuring two people and damaging a parked car",
      "breakdown": [{"item": "Person 1 medical bills", "amount": 18000}, {"item": "Person 2 medical bills", "amount": 22000}, {"item": "Parked car damage", "amount": 8000}],
      "total": 48000
    }
  }
}
```

### Option B: Use AI Assistant Prompt

**Copy and paste this prompt to generate configuration files:**

```
Create a JSON config file for [STATE] auto insurance infographic using this template:

{
  "template": "state_auto",
  "data": {
    "state": "[STATE NAME]",
    "source": "[State Insurance Department URL]",
    "state_type": "[Tort/No-Fault/Choice No-Fault]",
    "liability_limits": {
      "per_person": {"number": "[NUMBER]", "amount": "$[AMOUNT]", "short": "$[SHORT]", "description": "[Clear explanation]"},
      "per_accident": {"number": "[NUMBER]", "amount": "$[AMOUNT]", "short": "$[SHORT]", "description": "[Clear explanation]"},
      "property": {"number": "[NUMBER]", "amount": "$[AMOUNT]", "short": "$[SHORT]", "description": "[Clear explanation]"}
    },
    "pip": {"label": "$[AMOUNT or 'Not Required']", "amount": "$[AMOUNT or 'N/A']", "covers": ["[What it covers]"]},
    "scenario": {
      "description": "[Realistic scenario]",
      "breakdown": [{"item": "[Cost item]", "amount": [number]}, ...],
      "total": [sum of amounts]
    }
  }
}

Research from: [State Insurance Department website URL]
```

**For Home Insurance Risk Infographics:**

```
Create a JSON config file for [STATE] home insurance risks infographic using this template:

{
  "template": "state_home",
  "data": {
    "state": "[STATE NAME]",
    "source": "National Weather Service (weather.gov) | FEMA (fema.gov)",
    "sources": ["[Source 1]", "[Source 2]", "[Source 3]"],
    "risks": [
      {
        "type": "[Risk Type 1: e.g., Flooding]",
        "level": "HIGH or MODERATE",
        "types": ["[Type 1]", "[Type 2]", "[Type 3]"],
        "fact": "[State-specific fact with statistic]",
        "protection": ["[Protection 1]", "[Protection 2]", "[Protection 3]"]
      },
      {
        "type": "[Risk Type 2]",
        "level": "HIGH or MODERATE",
        "context": "[Context description]",
        "fact": "[State-specific fact with statistic]",
        "protection": ["[Protection 1]", "[Protection 2]", "[Protection 3]"]
      }
    ],
    "action_alert": {
      "warning": "[Important warning about coverage exclusion]",
      "statistic": "[Relevant statistic]",
      "actions": ["[Action 1]", "[Action 2]", "[Action 3]"]
    }
  }
}

Research from: NWS state office, FEMA regional office, state climate office
```

---

## Step 3: Generate the Infographic

### Method A: Using Template System (Recommended)

```bash
cd "05-assets/infographics/python"

# Auto insurance
python3 -c "
from template_system import StateAutoInsuranceTemplate
import json

with open('../configs/your-state-auto-config.json', 'r') as f:
    config = json.load(f)

template = StateAutoInsuranceTemplate()
template.generate(config['data'])
template.save('../output/your-state-auto-insurance-infographic.png')
"

# Home insurance
python3 -c "
from template_system import StateHomeInsuranceTemplate
import json

with open('../configs/your-state-home-config.json', 'r') as f:
    config = json.load(f)

template = StateHomeInsuranceTemplate()
template.generate(config['data'])
template.save('../output/your-state-home-insurance-infographic.png')
"
```

### Method B: Using Original Generators

Edit and run the existing generators with new data:

```bash
# Update data file
cp data/kentucky-insurance-data.json data/your-state-insurance-data.json
# Edit the JSON file with your state's data

# Run generators
python3 generate_auto_infographic.py
python3 generate_home_infographic.py
```

---

## Template System Reference

### Available Templates

| Template | Best For | File |
|----------|----------|------|
| `StateAutoInsuranceTemplate` | State auto insurance requirements | `template_system.py` |
| `StateHomeInsuranceTemplate` | State home insurance risks | `template_system.py` |
| `InfographicTemplate` | Custom infographics | `template_system.py` |

### Template Components

All templates include these reusable components:

- `draw_gradient_header()` - Hero header with red accent
- `draw_big_numbers()` - Massive hero numbers display
- `draw_coverage_grid()` - 3-column coverage cards
- `draw_split_panel()` - Split color panels (PIP, etc.)
- `draw_scenario_box()` - Real-world scenario breakdown
- `draw_risk_cards()` - 3-column risk card grid
- `draw_action_alert()` - Red-border action panels
- `draw_footer()` - Data source attribution

### Custom Colors

Dream Assurance brand colors (auto-applied):
- Primary Red: `#C92A39`
- Primary Dark: `#1D252D`
- Success Green: `#28A745`
- Warning Orange: `#FF9800`
- Caution Yellow: `#FFC107`

---

## Output Specifications

**File Format:** PNG
**Dimensions:** 1200px wide (height varies by content)
**Quality:** 95% optimized
**File Size:** Typically 100-150 KB
**DPI:** Effectively 150 DPI (suitable for web and print)

**Naming Convention:**
```
[state]-[service]-infographic.png
Examples:
- kentucky-auto-insurance-infographic.png
- kansas-home-insurance-infographic.png
- texas-flood-insurance-infographic.png
```

---

## Content Types That Work

### High Priority (Use Templates Directly)
- State auto insurance requirements
- State home insurance risks
- State health insurance minimums
- State life insurance requirements

### Medium Priority (Adapt Templates)
- Commercial insurance requirements
- Flood insurance by region
- Earthquake insurance zones
- Wildfire risk areas

### Lower Priority (Custom Development)
- Insurance process flows
- Comparison charts
- Statistical trend visualizations
- Industry-specific coverage guides

---

## Quality Checklist

Before finalizing any infographic:

**Content Accuracy:**
- [ ] All data from authoritative sources (.gov preferred)
- [ ] Numbers and statistics verified
- [ ] Sources cited correctly
- [ ] Scenario totals are accurate

**Design Quality:**
- [ ] Dream Assurance brand colors used correctly
- [ ] Typography hierarchy is clear
- [ ] Text is readable at all sizes
- [ ] Visual flow guides the eye naturally
- [ ] White space is balanced

**Technical Quality:**
- [ ] PNG file is under 200 KB
- [ ] Resolution is 1200px wide minimum
- [ ] No text overflow or clipping
- [ ] All sections render correctly

**Brand Consistency:**
- [ ] Red accent color is #C92A39
- [ ] Dark color is #1D252D
- [ ] Font family is consistent (Helvetica/Arial)
- [ ] Layout follows established patterns

---

## Troubleshooting

**Text Overflow:**
- Reduce font size in template
- Shorten description text
- Increase card/section height

**Colors Look Wrong:**
- Verify hex codes in config
- Check color name references
- Ensure `get_color()` is being called

**Font Issues:**
- System fonts should auto-detect
- If fonts look wrong, specify absolute path in `get_font()`

**File Too Large:**
- Reduce quality to 85-90
- Simplify gradients
- Reduce canvas height

---

## Advanced Customization

### Creating Custom Templates

```python
from template_system import InfographicTemplate

class CustomTemplate(InfographicTemplate):
    def generate(self, data):
        self.create_canvas()

        # Use component methods
        self.draw_gradient_header(...)
        self.draw_big_numbers(...)

        # Or add custom sections
        self.draw_custom_section(...)

        self.save(output_path)
```

### Adding New Components

```python
def draw_custom_component(self, content: Dict, height: int = 300):
    """Draw custom section."""
    # Background
    self.draw.rectangle([(0, self.current_y), (self.width, self.current_y + height)],
                      fill=self.get_color('light_accent'))

    # Your custom drawing code here
    # ...

    self.current_y += height
    return self.current_y
```

---

## Example Prompts for Future Infographics

### For New State Pages

```
I need to create infographics for [STATE] personal insurance page.

1. Research auto insurance requirements for [STATE] from [STATE DMV/Insurance Department website]
2. Research home insurance risks for [STATE] from NOAA, FEMA, NWS
3. Create JSON config files following the templates in 05-assets/infographics/configs/
4. Generate both infographics using the template system in 05-assets/infographics/python/template_system.py

Ensure all data is from authoritative .gov sources and matches Dream Assurance brand standards.
```

### For Service-Specific Pages

```
Create an infographic for [SERVICE TYPE] showing:

1. Key requirements/minimums
2. Coverage options
3. Real-world scenario
4. Action items for getting coverage

Use the Dream Assurance template system and adapt the existing components to fit this content type.
```

### For Regional Risk Assessments

```
Generate a home insurance risk infographic for [REGION] showing:

1. Top 3 weather risks (flooding, wind, etc.)
2. Risk levels (HIGH/MODERATE)
3. Historical facts/statistics for each risk
4. Recommended protection measures
5. Action alert for commonly excluded coverage

Research data from regional NWS offices and FEMA.
```

---

## File Management

**Config Files:** `05-assets/infographics/configs/`
- Name pattern: `[state]-[service]-config.json`
- Example: `kansas-auto-config.json`

**Output Files:** `05-assets/infographics/output/`
- Name pattern: `[state]-[service]-infographic.png`
- Example: `kansas-auto-insurance-infographic.png`

**Data Files:** `05-assets/infographics/data/`
- Store raw research data here
- Include source URLs and retrieval dates

---

## Maintenance & Updates

**When to Update:**
- State requirements change (annually review)
- New risk data available from NWS/FEMA
- Brand guidelines updated
- Template system improvements

**Update Process:**
1. Fetch latest data from authoritative sources
2. Update config JSON files
3. Regenerate PNG files
4. Replace old files on website
5. Clear CDN/browser cache

---

## Support & Questions

For issues or questions:
1. Check this documentation
2. Review example config files
3. Test with simple cases first
4. Verify data sources are authoritative

**Remember:** All infographic data MUST come from .gov or authoritative research sources. This ensures accuracy and builds trust with visitors.
