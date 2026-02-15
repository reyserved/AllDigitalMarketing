# Universal Infographic Template System
## Dream Assurance Group - High-End Infographic Generation

A sophisticated, component-based Python system for generating professional infographics that match or exceed Dream Assurance Group's existing design standards.

---

## 🎯 What This System Does

**Generates publication-quality infographics for:**
- State insurance pages (auto, home, life, health)
- Risk assessment visualizations
- Insurance requirement guides
- Any Dream Assurance content needing visual explanation

**Design Quality:**
- Bold color blocking with red accents
- Professional typography hierarchy
- Layered visual depth
- Clean information architecture
- Matches Kansas example quality

---

## 📁 File Structure

```
05-assets/infographics/
├── configs/                    # Configuration files for each infographic
│   ├── kentucky-auto-config.json
│   └── kentucky-home-config.json
├── data/                       # Raw data from .gov sources
│   └── kentucky-insurance-data.json
├── output/                     # Generated PNG files
│   ├── kentucky-auto-insurance-infographic.png
│   └── kentucky-home-insurance-infographic.png
├── python/
│   ├── template_system.py      # Universal template system (USE THIS)
│   ├── generate_kentucky_sophisticated.py
│   ├── generate_auto_infographic.py
│   ├── generate_home_infographic.py
│   └── utils.py
├── GENERATION_GUIDE.md         # Complete guide for creating infographics
└── README.md                   # This file
```

---

## 🚀 Quick Start

### Generate Kentucky Infographics (Already Done)
```bash
cd "05-assets/infographics/python"
python3 generate_kentucky_sophisticated.py
```

### Generate Infographics for Any State

**Step 1: Create Config File**

Create `configs/[state]-auto-config.json`:
```json
{
  "template": "state_auto",
  "data": {
    "state": "Kansas",
    "source": "Kansas Insurance Department (insurance.kansas.gov)",
    "state_type": "Tort",
    "liability_limits": {
      "per_person": {"number": "25", "amount": "$25,000", "short": "$25K", "description": "Each person injured"},
      "per_accident": {"number": "50", "amount": "$50,000", "short": "$50K", "description": "Total per accident"},
      "property": {"number": "25", "amount": "$25,000", "short": "$25K", "description": "Property damage"}
    },
    "pip": {"label": "Not Required", "amount": "N/A", "covers": ["Kansas is a tort state"]},
    "scenario": {
      "description": "You cause an accident injuring two people",
      "breakdown": [{"item": "Person 1", "amount": 18000}, {"item": "Person 2", "amount": 22000}],
      "total": 40000
    }
  }
}
```

**Step 2: Generate**
```python
from template_system import StateAutoInsuranceTemplate
import json

with open('../configs/kansas-auto-config.json', 'r') as f:
    config = json.load(f)

template = StateAutoInsuranceTemplate()
template.generate(config['data'])
template.save('../output/kansas-auto-insurance-infographic.png')
```

---

## 🎨 Available Templates

| Template | Use Case | Output Size |
|----------|----------|-------------|
| `StateAutoInsuranceTemplate` | State auto insurance requirements | 1200x2000px |
| `StateHomeInsuranceTemplate` | State home insurance risks | 1200x2000px |
| `InfographicTemplate` | Custom infographics | Variable |

---

## 🧩 Reusable Components

All templates include these pre-built components:

### Header Components
- `draw_gradient_header()` - Hero header with red diagonal accent
- Bold typography (72pt title, 32pt subtitle)
- Source badge attribution

### Data Display Components
- `draw_big_numbers()` - 140pt hero numbers with shadow
- `draw_coverage_grid()` - 3-column card grid with shadows
- `draw_split_panel()` - Red/white split panels (e.g., PIP)

### Content Components
- `draw_scenario_box()` - Real-world scenario with breakdown
- `draw_risk_cards()` - 3-column risk cards with badges
- `draw_action_alert()` - Red-border action panels

### Footer Components
- `draw_footer()` - Data source attribution

---

## 🎨 Design Specifications

### Brand Colors
```python
'brand_red': '#C92A39'      # Primary accent
'brand_dark': '#1D252D'     # Headers, text
'white': '#FFFFFF'          # Card backgrounds
'light_accent': '#F8F9FA'   # Contrast sections
'success_green': '#28A745'  # Checkmarks, positive
'orange': '#FF9800'         # Moderate risk
'yellow': '#FFC107'         # Caution indicators
```

### Typography Scale
- Hero titles: 72pt bold
- Section headers: 20-26pt bold
- Data numbers: 48-140pt bold
- Body text: 13-16pt
- Labels: 11-14pt bold

### Layout Patterns
- Width: 1200px (standard)
- Margins: 60-100px
- Card shadows: 4px offset
- Border radius: 8-12px
- Grid spacing: 20-30px

---

## 📝 Prompt Templates for Future Infographics

### For Any State Auto Insurance Page

```
I need to create a sophisticated auto insurance infographic for [STATE].

1. Research [STATE] auto insurance minimum requirements from:
   - [STATE DMV/Insurance Department website]
   - Look for: Liability limits (25/50/25 format), PIP requirements, no-fault status

2. Create a config file following this structure:
{
  "template": "state_auto",
  "data": {
    "state": "[STATE]",
    "source": "[Authority URL]",
    "state_type": "[Tort/No-Fault/Choice No-Fault]",
    "liability_limits": {
      "per_person": {"number": "[XX]", "amount": "$XX,XXX", "short": "$XXK", "description": "[Clear explanation]"},
      "per_accident": {"number": "[XX]", "amount": "$XX,XXX", "short": "$XXK", "description": "[Clear explanation]"},
      "property": {"number": "[XX]", "amount": "$XX,XXX", "short": "$XXK", "description": "[Clear explanation]"}
    },
    "pip": {"label": "$XX,XXX or Not Required", "amount": "$XX,XXX or N/A", "covers": ["What it covers"]},
    "scenario": {
      "description": "[Realistic accident scenario]",
      "breakdown": [{"item": "[Cost item]", "amount": [number]}, ...],
      "total": [sum]
    }
  }
}

3. Generate using:
from template_system import StateAutoInsuranceTemplate
template = StateAutoInsuranceTemplate()
template.generate(config['data'])
template.save('../output/[state]-auto-insurance-infographic.png')

Ensure Dream Assurance brand colors (#C92A39, #1D252D) and professional design quality matching the Kansas example.
```

### For Any State Home Insurance Risks

```
I need to create a sophisticated home insurance risk infographic for [STATE].

1. Research [STATE] weather risks from:
   - National Weather Service (weather.gov) - [STATE] office
   - FEMA (fema.gov) - regional office
   - State climate center
   Look for: Flooding, tornadoes, hurricanes, wildfires, earthquakes, winter storms

2. Create a config file following this structure:
{
  "template": "state_home",
  "data": {
    "state": "[STATE]",
    "source": "NWS | FEMA",
    "sources": ["[Source 1]", "[Source 2]", "[Source 3]"],
    "risks": [
      {
        "type": "[Risk Name]",
        "level": "HIGH or MODERATE",
        "types": ["[Type 1]", "[Type 2]", "[Type 3]"],
        "fact": "[State-specific fact with statistic]",
        "protection": ["[Protection 1]", "[Protection 2]", "[Protection 3]"]
      }
    ],
    "action_alert": {
      "warning": "[Coverage exclusion warning]",
      "statistic": "[Relevant statistic]",
      "actions": ["[Action 1]", "[Action 2]", "[Action 3]"]
    }
  }
}

3. Generate using:
from template_system import StateHomeInsuranceTemplate
template = StateHomeInsuranceTemplate()
template.generate(config['data'])
template.save('../output/[state]-home-insurance-infographic.png')

Ensure each risk card includes: risk type badge, fact box with red left border, protection checklist.
```

---

## ✅ Quality Checklist

**Before finalizing any infographic:**

- [ ] All data from authoritative .gov sources
- [ ] Brand colors are correct (#C92A39, #1D252D)
- [ ] Typography hierarchy is clear
- [ ] Visual flow guides the eye naturally
- [ ] Text is readable at all sizes
- [ ] File size is under 200 KB
- [ ] Resolution is 1200px wide minimum
- [ ] Sources are properly cited
- [ ] Scenario totals are accurate

---

## 🔧 Customization

### Create Custom Template

```python
from template_system import InfographicTemplate

class MyCustomTemplate(InfographicTemplate):
    def generate(self, data):
        self.create_canvas()

        # Use existing components
        self.draw_gradient_header(...)
        self.draw_big_numbers(...)

        # Add custom sections
        self.draw_my_custom_section(...)

        self.save(output_path)
```

### Modify Component Styling

```python
# In your template class
def draw_gradient_header(self, title, subtitle, source, height=500):  # Changed height
    # Custom implementation
    pass
```

---

## 📊 Output Specifications

**Format:** PNG
**Width:** 1200px (standard)
**Height:** Variable (typically 1800-2200px)
**Quality:** 95% optimized
**File Size:** 90-150 KB typical
**DPI:** ~150 DPI (web + print ready)

---

## 🛠️ Troubleshooting

**Text overflows cards:**
- Reduce font size in component call
- Shorten description text in config
- Increase card_height parameter

**Colors look wrong:**
- Verify hex codes: #C92A39 (red), #1D252D (dark)
- Check color name references in config
- Ensure get_color() is being called

**Font doesn't look right:**
- System fonts auto-detect (Helvetica/Arial)
- Specify absolute font path if needed in get_font()

**File too large:**
- Reduce quality to 85-90 in save() call
- Simplify gradients
- Reduce canvas height

---

## 📚 Documentation

- **GENERATION_GUIDE.md** - Complete step-by-step guide for creating any infographic
- **configs/** - Example configuration files
- **template_system.py** - Full system documentation in docstrings

---

## 🎯 Best Practices

1. **Always** source data from .gov websites
2. **Always** verify numbers and statistics
3. **Always** cite sources accurately
4. **Always** test generated PNG before publishing
5. **Always** maintain brand color consistency
6. **Always** keep text concise and scannable

---

## 🚀 Next Steps

To create infographics for new content:

1. **Review** GENERATION_GUIDE.md for detailed instructions
2. **Research** authoritative data sources
3. **Create** config file using templates above
4. **Generate** using template_system.py
5. **Verify** output quality and accuracy
6. **Deploy** to appropriate web page

---

## 💡 Pro Tips

- **Batch Generation:** Create multiple config files, then loop through them
- **Version Control:** Commit config files to track data changes
- **Automated Updates:** Schedule quarterly data refreshes from .gov sources
- **Quality Assurance:** Always preview PNG before website deployment

---

## 📧 Support

For issues or questions:
1. Check GENERATION_GUIDE.md
2. Review example config files
3. Verify data source authenticity
4. Test with simple case first

**Remember:** Authoritative .gov sources only! This ensures accuracy and builds trust.
