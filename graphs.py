"""
Graph Visualization for EntropyWalker
=====================================

Generates matplotlib charts for comparing random generator performance.
Saves to file to avoid pygame/matplotlib threading conflicts.
"""

import matplotlib
matplotlib.use('Agg')  # Non-interactive backend (file output only)
import matplotlib.pyplot as plt
import os
import subprocess
import sys

from stats import StatsTracker


def show_distribution_graphs(stats_left: StatsTracker, stats_right: StatsTracker,
                              left_name: str = "Python Random", 
                              right_name: str = "TrueEntropy") -> None:
    """
    Generate distribution graphs and open them in the default image viewer.
    """
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    fig.suptitle('EntropyWalker: Distribution Comparison', fontsize=14, fontweight='bold')
    
    # Colors
    left_color = '#00ffc8'
    right_color = '#ff6432'
    
    # 1. Direction Distribution - Left
    ax1 = axes[0, 0]
    left_dist = stats_left.get_direction_distribution()
    directions = ['UP', 'DOWN', 'LEFT', 'RIGHT']
    values_left = [left_dist[d] for d in directions]
    bars1 = ax1.bar(directions, values_left, color=left_color, edgecolor='white', alpha=0.8)
    ax1.axhline(y=25, color='red', linestyle='--', label='Ideal (25%)')
    ax1.set_title(f'{left_name} - Direction Distribution')
    ax1.set_ylabel('Percentage (%)')
    ax1.set_ylim(0, 35)
    ax1.legend()
    for bar, val in zip(bars1, values_left):
        ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5, 
                f'{val:.1f}%', ha='center', va='bottom', fontsize=9)
    
    # 2. Direction Distribution - Right
    ax2 = axes[0, 1]
    right_dist = stats_right.get_direction_distribution()
    values_right = [right_dist[d] for d in directions]
    bars2 = ax2.bar(directions, values_right, color=right_color, edgecolor='white', alpha=0.8)
    ax2.axhline(y=25, color='red', linestyle='--', label='Ideal (25%)')
    ax2.set_title(f'{right_name} - Direction Distribution')
    ax2.set_ylabel('Percentage (%)')
    ax2.set_ylim(0, 35)
    ax2.legend()
    for bar, val in zip(bars2, values_right):
        ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5, 
                f'{val:.1f}%', ha='center', va='bottom', fontsize=9)
    
    # 3. Distance Distribution - Comparison
    ax3 = axes[1, 0]
    if stats_left.distance_history and stats_right.distance_history:
        ax3.hist(stats_left.distance_history, bins=30, alpha=0.6, color=left_color, 
                 label=left_name, edgecolor='white')
        ax3.hist(stats_right.distance_history, bins=30, alpha=0.6, color=right_color, 
                 label=right_name, edgecolor='white')
    ax3.set_title('Distance from Origin Distribution')
    ax3.set_xlabel('Distance (pixels)')
    ax3.set_ylabel('Frequency')
    ax3.legend()
    
    # 4. Summary Stats Comparison
    ax4 = axes[1, 1]
    metrics = ['Dispersão\n(avg dist)', 'Entropia\n(max 2.0)', 'Retorno\n(%)']
    left_stats = stats_left.get_stats_dict()
    right_stats = stats_right.get_stats_dict()
    
    left_values = [left_stats['dispersao'], left_stats['entropia'], left_stats['retorno_rate']]
    right_values = [right_stats['dispersao'], right_stats['entropia'], right_stats['retorno_rate']]
    
    max_disp = max(left_values[0], right_values[0], 1)
    left_normalized = [left_values[0]/max_disp * 100, left_values[1] * 50, left_values[2]]
    right_normalized = [right_values[0]/max_disp * 100, right_values[1] * 50, right_values[2]]
    
    x = range(len(metrics))
    width = 0.35
    ax4.bar([i - width/2 for i in x], left_normalized, width, label=left_name, 
            color=left_color, edgecolor='white', alpha=0.8)
    ax4.bar([i + width/2 for i in x], right_normalized, width, label=right_name, 
            color=right_color, edgecolor='white', alpha=0.8)
    ax4.set_xticks(x)
    ax4.set_xticklabels(metrics)
    ax4.set_title('Metrics Comparison (Normalized)')
    ax4.set_ylabel('Normalized Value')
    ax4.legend()
    
    for i, (lv, rv) in enumerate(zip(left_values, right_values)):
        if i == 0:
            ax4.text(i - width/2, left_normalized[i] + 2, f'{lv:.0f}px', ha='center', fontsize=8)
            ax4.text(i + width/2, right_normalized[i] + 2, f'{rv:.0f}px', ha='center', fontsize=8)
        elif i == 1:
            ax4.text(i - width/2, left_normalized[i] + 2, f'{lv:.2f}', ha='center', fontsize=8)
            ax4.text(i + width/2, right_normalized[i] + 2, f'{rv:.2f}', ha='center', fontsize=8)
        else:
            ax4.text(i - width/2, left_normalized[i] + 2, f'{lv:.1f}%', ha='center', fontsize=8)
            ax4.text(i + width/2, right_normalized[i] + 2, f'{rv:.1f}%', ha='center', fontsize=8)
    
    plt.tight_layout()
    
    # Save to file
    output_path = os.path.join(os.path.dirname(__file__), 'distribution_graphs.png')
    plt.savefig(output_path, dpi=150, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    
    # Open the image with default viewer
    if sys.platform == 'win32':
        os.startfile(output_path)
    elif sys.platform == 'darwin':
        subprocess.run(['open', output_path])
    else:
        subprocess.run(['xdg-open', output_path])
    
    print(f"Graph saved to: {output_path}")

