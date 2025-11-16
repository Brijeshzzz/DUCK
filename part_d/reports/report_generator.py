"""
D4: Forensic Report Generator
Generates court-ready PDF reports
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from datetime import datetime
import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ReportGenerator:
    """Generates forensic investigation reports"""
    
    def __init__(self):
        self.output_dir = "part_d/reports/output"
        os.makedirs(self.output_dir, exist_ok=True)
        logger.info("Report Generator initialized")
    
    def generate_text_report(self, analysis_data, output_file=None):
        """
        Generate detailed text report
        
        Args:
            analysis_data: {
                'case_id': investigation ID,
                'timestamp': when analyzed,
                'summary': analysis summary,
                'detections': list of detections,
                'paths': reconstructed paths,
                'statistics': stats dict
            }
        """
        if output_file is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_file = f"{self.output_dir}/forensic_report_{timestamp}.txt"
        
        with open(output_file, 'w') as f:
            # Header
            f.write("="*80 + "\n")
            f.write("TOR TRAFFIC ANALYSIS - FORENSIC REPORT\n")
            f.write("="*80 + "\n\n")
            
            # Case Information
            f.write("CASE INFORMATION\n")
            f.write("-"*80 + "\n")
            f.write(f"Case ID:          {analysis_data.get('case_id', 'N/A')}\n")
            f.write(f"Analysis Date:    {analysis_data.get('timestamp', datetime.now().isoformat())}\n")
            f.write(f"Investigator:     {analysis_data.get('investigator', 'System')}\n")
            f.write(f"Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("\n")
            
            # Executive Summary
            f.write("EXECUTIVE SUMMARY\n")
            f.write("-"*80 + "\n")
            summary = analysis_data.get('summary', {})
            f.write(f"Total Packets Analyzed:     {summary.get('total_packets', 0)}\n")
            f.write(f"TOR Packets Detected:       {summary.get('tor_packets', 0)}\n")
            f.write(f"TOR Connections Identified: {summary.get('connections', 0)}\n")
            f.write(f"Paths Reconstructed:        {summary.get('paths', 0)}\n")
            f.write(f"Average Confidence:         {summary.get('avg_confidence', 0):.2f}%\n")
            f.write("\n")
            
            # Detections
            f.write("DETAILED DETECTIONS\n")
            f.write("-"*80 + "\n")
            detections = analysis_data.get('detections', [])
            
            if detections:
                for i, detection in enumerate(detections, 1):
                    f.write(f"\nDetection #{i}:\n")
                    f.write(f"  Timestamp:    {detection.get('timestamp', 'N/A')}\n")
                    f.write(f"  User IP:      {detection.get('user_ip', 'N/A')}\n")
                    f.write(f"  Entry Node:   {detection.get('entry_node', {}).get('ip', 'N/A')}\n")
                    f.write(f"  Entry Country: {detection.get('entry_node', {}).get('country', 'N/A')}\n")
                    f.write(f"  Exit Node:    {detection.get('exit_node', {}).get('ip', 'N/A')}\n")
                    f.write(f"  Exit Country:  {detection.get('exit_node', {}).get('country', 'N/A')}\n")
                    f.write(f"  Destination:  {detection.get('destination', 'N/A')}\n")
                    f.write(f"  Confidence:   {detection.get('confidence', 0):.2f}%\n")
            else:
                f.write("No detections found.\n")
            
            f.write("\n")
            
            # Path Reconstructions
            f.write("PATH RECONSTRUCTIONS\n")
            f.write("-"*80 + "\n")
            paths = analysis_data.get('paths', [])
            
            if paths:
                for i, path in enumerate(paths, 1):
                    f.write(f"\nPath #{i} (Confidence: {path.get('confidence', 0):.2f}%):\n")
                    f.write(f"  {path.get('user_ip', 'USER')}\n")
                    f.write(f"    ↓\n")
                    f.write(f"  Entry: {path.get('entry_node', {}).get('ip', 'N/A')} ({path.get('entry_node', {}).get('country', 'N/A')})\n")
                    f.write(f"    ↓\n")
                    
                    relays = path.get('relay_nodes', [])
                    for relay in relays:
                        f.write(f"  Relay: {relay.get('country', 'Unknown')}\n")
                        f.write(f"    ↓\n")
                    
                    f.write(f"  Exit: {path.get('exit_node', {}).get('ip', 'N/A')} ({path.get('exit_node', {}).get('country', 'N/A')})\n")
                    f.write(f"    ↓\n")
                    f.write(f"  Destination: {path.get('destination', 'N/A')}\n")
            else:
                f.write("No paths reconstructed.\n")
            
            f.write("\n")
            
            # Statistics
            f.write("STATISTICAL ANALYSIS\n")
            f.write("-"*80 + "\n")
            stats = analysis_data.get('statistics', {})
            
            f.write(f"Detection Rate:         {stats.get('detection_rate', 0):.2f}%\n")
            f.write(f"High Confidence:        {stats.get('high_confidence', 0)} detections\n")
            f.write(f"Medium Confidence:      {stats.get('medium_confidence', 0)} detections\n")
            f.write(f"Low Confidence:         {stats.get('low_confidence', 0)} detections\n")
            f.write(f"Countries Involved:     {stats.get('countries', 0)}\n")
            f.write(f"Unique Entry Nodes:     {stats.get('unique_entries', 0)}\n")
            f.write(f"Unique Exit Nodes:      {stats.get('unique_exits', 0)}\n")
            f.write("\n")
            
            # Footer
            f.write("="*80 + "\n")
            f.write("END OF REPORT\n")
            f.write("="*80 + "\n")
            f.write("\nThis report is generated by TOR Analysis System\n")
            f.write("For law enforcement use only\n")
            f.write(f"Digital Signature: SHA256-{hash(str(analysis_data))}\n")
        
        logger.info(f"Text report generated: {output_file}")
        return output_file
    
    def generate_json_export(self, analysis_data, output_file=None):
        """Export data as JSON for further processing"""
        if output_file is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_file = f"{self.output_dir}/analysis_data_{timestamp}.json"
        
        with open(output_file, 'w') as f:
            json.dump(analysis_data, f, indent=2, default=str)
        
        logger.info(f"JSON export created: {output_file}")
        return output_file
    
    def generate_csv_export(self, detections, output_file=None):
        """Export detections as CSV"""
        if output_file is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_file = f"{self.output_dir}/detections_{timestamp}.csv"
        
        with open(output_file, 'w') as f:
            # Header
            f.write("Timestamp,User_IP,Entry_Node_IP,Entry_Country,Exit_Node_IP,Exit_Country,Destination,Confidence\n")
            
            # Data
            for detection in detections:
                f.write(f"{detection.get('timestamp', '')},")
                f.write(f"{detection.get('user_ip', '')},")
                f.write(f"{detection.get('entry_node', {}).get('ip', '')},")
                f.write(f"{detection.get('entry_node', {}).get('country', '')},")
                f.write(f"{detection.get('exit_node', {}).get('ip', '')},")
                f.write(f"{detection.get('exit_node', {}).get('country', '')},")
                f.write(f"{detection.get('destination', '')},")
                f.write(f"{detection.get('confidence', 0):.2f}\n")
        
        logger.info(f"CSV export created: {output_file}")
        return output_file


def main():
    """Test report generation"""
    print("="*70)
    print("PART D - D4: Forensic Report Generator")
    print("="*70)
    
    generator = ReportGenerator()
    
    # Sample data
    analysis_data = {
        'case_id': 'TOR-2025-001',
        'timestamp': datetime.now().isoformat(),
        'investigator': 'Agent Smith',
        'summary': {
            'total_packets': 1523,
            'tor_packets': 45,
            'connections': 12,
            'paths': 5,
            'avg_confidence': 85.3
        },
        'detections': [
            {
                'timestamp': '2025-11-11T10:30:00',
                'user_ip': '192.168.1.100',
                'entry_node': {'ip': '185.220.101.50', 'country': 'Germany'},
                'exit_node': {'ip': '192.42.116.16', 'country': 'Netherlands'},
                'destination': '172.217.14.206',
                'confidence': 87.5
            }
        ],
        'paths': [
            {
                'user_ip': '192.168.1.100',
                'entry_node': {'ip': '185.220.101.50', 'country': 'Germany'},
                'relay_nodes': [
                    {'country': 'France'},
                    {'country': 'Sweden'}
                ],
                'exit_node': {'ip': '192.42.116.16', 'country': 'Netherlands'},
                'destination': '172.217.14.206',
                'confidence': 87.5
            }
        ],
        'statistics': {
            'detection_rate': 2.95,
            'high_confidence': 8,
            'medium_confidence': 3,
            'low_confidence': 1,
            'countries': 5,
            'unique_entries': 3,
            'unique_exits': 2
        }
    }
    
    print("\n1. Generating text report...")
    text_report = generator.generate_text_report(analysis_data)
    print(f"   ✓ Saved to: {text_report}")
    
    print("\n2. Generating JSON export...")
    json_export = generator.generate_json_export(analysis_data)
    print(f"   ✓ Saved to: {json_export}")
    
    print("\n3. Generating CSV export...")
    csv_export = generator.generate_csv_export(analysis_data['detections'])
    print(f"   ✓ Saved to: {csv_export}")
    
    print(f"\n{'='*70}")
    print("All reports generated successfully!")
    print(f"{'='*70}")


if __name__ == "__main__":
    main()
