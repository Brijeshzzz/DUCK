"""
Fix: Save volume correlation results to correct file
"""

import json
import os

# Your actual volume correlation result
volume_result = {
    'entry_node_ip': '83.108.59.221',
    'entry_country': 'Norway',
    'exit_node_ip': '204.137.14.106',
    'exit_country': 'United States of America',
    'volume_difference': 0.02,
    'match': True
}

# Save to correct location
os.makedirs('part_b/logs', exist_ok=True)
with open('part_b/logs/volume_correlations.json', 'w') as f:
    json.dump([volume_result], f, indent=4)

print("✓ Volume correlation saved!")
print(f"  Location: part_b/logs/volume_correlations.json")
print(f"  Volume difference: {volume_result['volume_difference']}")
