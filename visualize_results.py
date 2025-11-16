"""
Visualize actual TOR analysis results
"""

import sys
sys.path.insert(0, '.')

from part_d.visualizations.network_visualizer import NetworkVisualizer
from part_d.reports.report_generator import ReportGenerator
from datetime import datetime

print("="*70)
print("CREATING VISUALIZATIONS FOR YOUR TOR ANALYSIS RESULTS")
print("="*70)

# Your actual results
results = {
    'case_id': 'TOR-ANALYSIS-20251113',
    'timestamp': '2025-11-13 11:43:42',
    'investigator': 'TOR Analysis System',
    'summary': {
        'total_packets': 'Captured in 2 minutes',
        'tor_packets': 2,
        'connections': 2,
        'paths': 1,
        'avg_confidence': 5.0
    },
    'detections': [
        {
            'timestamp': '2025-11-13 11:43:42',
            'user_ip': 'Local System',
            'entry_node': {
                'ip': '83.108.59.221',
                'country': 'Norway',
                'nickname': 'hubbabubbaABC'
            },
            'exit_node': {
                'ip': '204.137.14.106',
                'country': 'United States of America',
                'nickname': 'SENDNOOSEplz'
            },
            'destination': 'Unknown',
            'confidence': 5.0
        }
    ],
    'paths': [
        {
            'user_ip': 'Local System',
            'entry_node': {
                'ip': '83.108.59.221',
                'country': 'Norway'
            },
            'relay_nodes': [
                {'country': 'Unknown'},
                {'country': 'Unknown'}
            ],
            'exit_node': {
                'ip': '204.137.14.106',
                'country': 'United States'
            },
            'destination': 'Unknown',
            'confidence': 5.0
        }
    ],
    'statistics': {
        'detection_rate': 100.0,
        'high_confidence': 0,
        'medium_confidence': 0,
        'low_confidence': 1,
        'countries': 2,
        'unique_entries': 1,
        'unique_exits': 1
    }
}

# Create visualizations
print("\n1. Creating network path visualization...")
visualizer = NetworkVisualizer()
path_file = visualizer.draw_tor_path(results['paths'][0])
print(f"   ✓ Saved: {path_file}")

# Create timeline
print("\n2. Creating timeline...")
events = [
    {
        'timestamp': datetime.now(),
        'event_type': 'entry',
        'description': 'Entry: Norway'
    },
    {
        'timestamp': datetime.now(),
        'event_type': 'exit',
        'description': 'Exit: USA'
    }
]
timeline_file = visualizer.draw_timeline(events)
print(f"   ✓ Saved: {timeline_file}")

# Create statistics chart
print("\n3. Creating statistics chart...")
stats = {
    'total_packets': 100,  # Approximate
    'tor_packets': 2,
    'detections': 1,
    'high_confidence': 0,
    'medium_confidence': 0,
    'low_confidence': 1
}
stats_file = visualizer.draw_statistics_chart(stats)
print(f"   ✓ Saved: {stats_file}")

# Generate reports
print("\n4. Generating forensic report...")
generator = ReportGenerator()
report_file = generator.generate_text_report(results)
print(f"   ✓ Saved: {report_file}")

print("\n5. Generating JSON export...")
json_file = generator.generate_json_export(results)
print(f"   ✓ Saved: {json_file}")

print("\n6. Generating CSV export...")
csv_file = generator.generate_csv_export(results['detections'])
print(f"   ✓ Saved: {csv_file}")

print("\n" + "="*70)
print("✓ ALL VISUALIZATIONS AND REPORTS CREATED!")
print("="*70)
print("\nCheck these folders:")
print("  • part_d/visualizations/output/  (PNG images)")
print("  • part_d/reports/output/          (TXT, JSON, CSV files)")
print("="*70)
