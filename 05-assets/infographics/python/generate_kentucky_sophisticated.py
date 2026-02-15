#!/usr/bin/env python3
"""
Generate sophisticated Kentucky insurance infographics using the universal template system.
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(__file__))

from template_system import StateAutoInsuranceTemplate, StateHomeInsuranceTemplate
import json

# Load Kentucky data
data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
output_dir = os.path.join(os.path.dirname(__file__), '..', 'output')

with open(os.path.join(data_dir, 'kentucky-insurance-data.json'), 'r') as f:
    data = json.load(f)

# Generate Auto Insurance Infographic
print("="*60)
print("Generating Kentucky Auto Insurance Infographic...")
print("="*60)

auto_template = StateAutoInsuranceTemplate()
auto_template.generate({
    'state': 'Kentucky',
    'source': 'Kentucky Transportation Cabinet (kytc.ky.gov)',
    'state_type': 'Choice No-Fault',
    'liability_limits': {
        'per_person': {
            'number': '25',
            'amount': '$25,000',
            'short': '$25K',
            'description': 'Each person injured in an accident you cause'
        },
        'per_accident': {
            'number': '50',
            'amount': '$50,000',
            'short': '$50K',
            'description': 'Total for all injuries in one accident'
        },
        'property': {
            'number': '25',
            'amount': '$25,000',
            'short': '$25K',
            'description': 'Another person\'s vehicle or property'
        }
    },
    'pip': {
        'label': '$10,000',
        'amount': '$10,000',
        'covers': ['Medical expenses', 'Lost wages regardless of fault']
    },
    'scenario': {
        'description': 'You cause an accident injuring two people and damaging a parked car',
        'breakdown': [
            {'item': 'Person 1 medical bills', 'amount': 18000},
            {'item': 'Person 2 medical bills', 'amount': 22000},
            {'item': 'Parked car damage', 'amount': 8000}
        ],
        'total': 48000
    }
})
auto_template.save(os.path.join(output_dir, 'kentucky-auto-insurance-infographic.png'))

print("\n" + "="*60)
print("Generating Kentucky Home Insurance Infographic...")
print("="*60)

home_template = StateHomeInsuranceTemplate()
home_template.generate({
    'state': 'Kentucky',
    'source': 'National Weather Service (weather.gov) | FEMA (fema.gov)',
    'sources': [
        'National Weather Service (weather.gov)',
        'Federal Emergency Management Agency (fema.gov)',
        'Kentucky Climate Center'
    ],
    'risks': data['home_insurance']['risks'],
    'action_alert': data['home_insurance']['action_alert']
})
home_template.save(os.path.join(output_dir, 'kentucky-home-insurance-infographic.png'))

print("\n" + "="*60)
print("✓ All Kentucky infographics generated successfully!")
print("="*60)
