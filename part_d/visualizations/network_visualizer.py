import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class NetworkVisualizer:
    """Creates visual representations of TOR paths"""
    
    def __init__(self):
        self.output_dir = "part_d/visualizations/output"
        os.makedirs(self.output_dir, exist_ok=True)
        logger.info("Network Visualizer initialized")
    
    def draw_tor_path(self, path_data, output_file=None):
        """
        Draw a TOR path visualization
        """
        fig, ax = plt.subplots(figsize=(14, 8))
        positions = {
            'user': (0, 2),
            'entry': (2, 2),
            'relay1': (4, 3),
            'relay2': (6, 2),
            'relay3': (8, 3),
            'exit': (10, 2),
            'destination': (12, 2)
        }
        confidence = path_data.get('confidence', 0)
        if confidence >= 80:
            path_color = '#22c55e'
            confidence_text = 'HIGH'
        elif confidence >= 60:
            path_color = '#f97316'
            confidence_text = 'MEDIUM'
        else:
            path_color = '#ef4444'
            confidence_text = 'LOW'
        
        # Draw nodes with plain text labels
        ax.text(positions['user'][0], positions['user'][1], 
                f"USER\n{path_data.get('user_ip', 'N/A')}", 
                bbox=dict(boxstyle='round,pad=0.5', facecolor='#93c5fd', edgecolor='black', linewidth=2),
                ha='center', va='center', fontsize=10, weight='bold')
        
        entry = path_data.get('entry_node', {})
        ax.text(positions['entry'][0], positions['entry'][1],
                f"ENTRY NODE\n{entry.get('ip', 'N/A')}\n{entry.get('country', 'N/A')}",
                bbox=dict(boxstyle='round,pad=0.5', facecolor='#86efac', edgecolor='black', linewidth=2),
                ha='center', va='center', fontsize=9, weight='bold')

        relay_nodes = path_data.get('relay_nodes', [])
        for i, relay in enumerate(relay_nodes[:3], 1):
            pos_key = f'relay{i}'
            ax.text(positions[pos_key][0], positions[pos_key][1],
                    f"RELAY {i}\n{relay.get('country', 'Unknown')}",
                    bbox=dict(boxstyle='round,pad=0.5', facecolor='#fde047', edgecolor='black', linewidth=2),
                    ha='center', va='center', fontsize=9)

        exit_node = path_data.get('exit_node', {})
        ax.text(positions['exit'][0], positions['exit'][1],
                f"EXIT NODE\n{exit_node.get('ip', 'N/A')}\n{exit_node.get('country', 'N/A')}",
                bbox=dict(boxstyle='round,pad=0.5', facecolor='#86efac', edgecolor='black', linewidth=2),
                ha='center', va='center', fontsize=9, weight='bold')

        ax.text(positions['destination'][0], positions['destination'][1],
                f"DESTINATION\n{path_data.get('destination', 'N/A')}",
                bbox=dict(boxstyle='round,pad=0.5', facecolor='#fca5a5', edgecolor='black', linewidth=2),
                ha='center', va='center', fontsize=10, weight='bold')

        # Draw connections
        connections = [
            ('user', 'entry'),
            ('entry', 'relay1'),
            ('relay1', 'relay2'),
            ('relay2', 'relay3'),
            ('relay3', 'exit'),
            ('exit', 'destination')
        ]
        for start, end in connections:
            if start in positions and end in positions:
                ax.annotate('', xy=positions[end], xytext=positions[start],
                            arrowprops=dict(arrowstyle='->', lw=3, color=path_color))
        
        # Title and confidence
        ax.text(6, 5, f'TOR PATH RECONSTRUCTION', ha='center', fontsize=16, weight='bold')
        ax.text(6, 4.5, f'Confidence: {confidence}% ({confidence_text})', ha='center', fontsize=14, weight='bold', color=path_color)

        # Timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ax.text(6, 0.5, f'Generated: {timestamp}', ha='center', fontsize=9, style='italic', color='gray')
        
        ax.set_xlim(-1, 13)
        ax.set_ylim(0, 6)
        ax.axis('off')
        if output_file is None:
            output_file = f"{self.output_dir}/tor_path_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        plt.tight_layout()
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        plt.close()
        logger.info(f"Path visualization saved to {output_file}")
        return output_file

    # Timeline and statistics functions: do similarly if you used emojis.

    # Add your main() function at the end to run tests if desired.
