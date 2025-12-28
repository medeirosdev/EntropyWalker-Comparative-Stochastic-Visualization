"""
Statistics Tracker for EntropyWalker
====================================

Provides real-time metrics and heatmap tracking for random walk analysis.
"""

import math
from typing import Tuple, List, Dict
from collections import Counter

class StatsTracker:
    """
    Tracks statistics and generates heatmap data for a group of random walkers.
    """

    def __init__(self, origin: Tuple[int, int], width: int, height: int, cell_size: int = 10):
        self.origin = origin
        self.cell_size = cell_size
        self.grid_width = width // cell_size
        self.grid_height = height // cell_size
        
        # Heatmap grid (visit counts)
        self.heatmap: List[List[int]] = [[0] * self.grid_width for _ in range(self.grid_height)]
        
        # Direction history for entropy (0=UP, 1=DOWN, 2=LEFT, 3=RIGHT)
        self.direction_history: List[int] = []
        self.max_history = 1000
        
        # Direction counts for histogram
        self.direction_counts: Dict[str, int] = {'UP': 0, 'DOWN': 0, 'LEFT': 0, 'RIGHT': 0}
        
        # Distance history for distribution graph
        self.distance_history: List[float] = []
        self.max_distance_history = 500
        
        # Return to origin tracking
        self.return_count: int = 0
        self.return_threshold: int = 15
        
        # Total moves
        self.total_moves: int = 0
        
        # Distance tracking
        self.distance_sum: float = 0.0

    def record_move(self, x: int, y: int, direction: str) -> None:
        """Record a walker's move."""
        self.total_moves += 1
        
        # Update heatmap
        cell_x = min(x // self.cell_size, self.grid_width - 1)
        cell_y = min(y // self.cell_size, self.grid_height - 1)
        cell_x = max(0, cell_x)
        cell_y = max(0, cell_y)
        self.heatmap[cell_y][cell_x] += 1
        
        # Record direction for entropy
        dir_map = {'UP': 0, 'DOWN': 1, 'LEFT': 2, 'RIGHT': 3}
        self.direction_history.append(dir_map.get(direction, 0))
        if len(self.direction_history) > self.max_history:
            self.direction_history.pop(0)
        
        # Count directions for histogram
        if direction in self.direction_counts:
            self.direction_counts[direction] += 1
        
        # Calculate distance
        dist_to_origin = math.sqrt((x - self.origin[0])**2 + (y - self.origin[1])**2)
        
        # Record distance history
        self.distance_history.append(dist_to_origin)
        if len(self.distance_history) > self.max_distance_history:
            self.distance_history.pop(0)
        
        # Check return to origin
        if dist_to_origin <= self.return_threshold:
            self.return_count += 1
        
        # Accumulate distance for average
        self.distance_sum += dist_to_origin

    def get_dispersao(self) -> float:
        """Calculate average distance from origin (Dispersão)."""
        if self.total_moves == 0:
            return 0.0
        return self.distance_sum / self.total_moves

    def get_retorno_rate(self) -> float:
        """Calculate return to origin rate (percentage)."""
        if self.total_moves == 0:
            return 0.0
        return (self.return_count / self.total_moves) * 100

    def get_entropia(self) -> float:
        """Calculate Shannon entropy of direction sequence."""
        if len(self.direction_history) < 10:
            return 0.0
        
        counts = Counter(self.direction_history)
        total = len(self.direction_history)
        
        entropy = 0.0
        for count in counts.values():
            if count > 0:
                p = count / total
                entropy -= p * math.log2(p)
        
        return entropy

    def get_direction_distribution(self) -> Dict[str, float]:
        """Get direction distribution as percentages."""
        total = sum(self.direction_counts.values())
        if total == 0:
            return {'UP': 25.0, 'DOWN': 25.0, 'LEFT': 25.0, 'RIGHT': 25.0}
        return {k: (v / total) * 100 for k, v in self.direction_counts.items()}

    def get_max_heat(self) -> int:
        """Get maximum heat value for normalization."""
        max_heat = 0
        for row in self.heatmap:
            row_max = max(row) if row else 0
            if row_max > max_heat:
                max_heat = row_max
        return max_heat if max_heat > 0 else 1

    def get_stats_dict(self) -> Dict[str, float]:
        """Get all stats as a dictionary."""
        return {
            'dispersao': self.get_dispersao(),
            'retorno_rate': self.get_retorno_rate(),
            'entropia': self.get_entropia(),
            'total_moves': self.total_moves,
            'return_count': self.return_count
        }

    def reset(self) -> None:
        """Reset all statistics."""
        self.heatmap = [[0] * self.grid_width for _ in range(self.grid_height)]
        self.direction_history = []
        self.direction_counts = {'UP': 0, 'DOWN': 0, 'LEFT': 0, 'RIGHT': 0}
        self.distance_history = []
        self.return_count = 0
        self.total_moves = 0
        self.distance_sum = 0.0

