"""
Statistics Tracker for EntropyWalker
=====================================

This module provides real-time metrics and heatmap tracking for random walk
analysis. It calculates statistical measures to compare the quality of
different random number generators.

Metrics tracked:
    - Dispersion (average distance from origin)
    - Entropy (Shannon entropy of direction sequence)
    - Return rate (percentage of moves returning to origin)
    - Direction distribution (histogram of UP/DOWN/LEFT/RIGHT)
    - Heatmap (2D grid of visit frequency)
"""

import math
from typing import Tuple, List, Dict
from collections import Counter


class StatsTracker:
    """
    Tracks statistics and generates heatmap data for random walk analysis.
    
    This class accumulates move data from multiple walkers and provides
    methods to calculate various statistical metrics useful for comparing
    random number generator quality.
    
    Attributes:
        origin: Starting point (x, y) for distance calculations.
        cell_size: Size of each heatmap cell in pixels.
        grid_width: Number of horizontal cells in heatmap.
        grid_height: Number of vertical cells in heatmap.
        heatmap: 2D grid storing visit counts per cell.
        direction_counts: Counter for each direction.
        total_moves: Total number of recorded moves.
    """

    def __init__(self, origin: Tuple[int, int], width: int, height: int, cell_size: int = 10):
        """
        Initialize the statistics tracker.
        
        Args:
            origin: Starting point (x, y) for distance calculations.
            width: Total tracking width in pixels.
            height: Total tracking height in pixels.
            cell_size: Size of each heatmap cell in pixels.
        """
        self.origin = origin
        self.cell_size = cell_size
        self.grid_width = width // cell_size
        self.grid_height = height // cell_size
        
        # Heatmap: 2D grid storing visit count per cell
        self.heatmap: List[List[int]] = [[0] * self.grid_width for _ in range(self.grid_height)]
        
        # Direction tracking for entropy calculation
        # Stored as integers: 0=UP, 1=DOWN, 2=LEFT, 3=RIGHT
        self.direction_history: List[int] = []
        self.max_history = 1000  # Rolling window for entropy
        
        # Direction counts for histogram visualization
        self.direction_counts: Dict[str, int] = {'UP': 0, 'DOWN': 0, 'LEFT': 0, 'RIGHT': 0}
        
        # Distance history for distribution graphs
        self.distance_history: List[float] = []
        self.max_distance_history = 500
        
        # Return to origin tracking
        self.return_count: int = 0
        self.return_threshold: int = 15  # Pixels within origin to count as "returned"
        
        # Aggregate statistics
        self.total_moves: int = 0
        self.distance_sum: float = 0.0

    def record_move(self, x: int, y: int, direction: str) -> None:
        """
        Record a single walker move for statistical analysis.
        
        Args:
            x: New x-coordinate after move.
            y: New y-coordinate after move.
            direction: Direction taken ('UP', 'DOWN', 'LEFT', 'RIGHT').
        """
        self.total_moves += 1
        
        # Update heatmap cell (clamp to grid bounds)
        cell_x = max(0, min(x // self.cell_size, self.grid_width - 1))
        cell_y = max(0, min(y // self.cell_size, self.grid_height - 1))
        self.heatmap[cell_y][cell_x] += 1
        
        # Record direction for entropy calculation
        dir_map = {'UP': 0, 'DOWN': 1, 'LEFT': 2, 'RIGHT': 3}
        self.direction_history.append(dir_map.get(direction, 0))
        if len(self.direction_history) > self.max_history:
            self.direction_history.pop(0)
        
        # Count directions for histogram
        if direction in self.direction_counts:
            self.direction_counts[direction] += 1
        
        # Calculate Euclidean distance from origin
        dist_to_origin = math.sqrt((x - self.origin[0])**2 + (y - self.origin[1])**2)
        
        # Record distance for distribution graph
        self.distance_history.append(dist_to_origin)
        if len(self.distance_history) > self.max_distance_history:
            self.distance_history.pop(0)
        
        # Check if walker returned to origin area
        if dist_to_origin <= self.return_threshold:
            self.return_count += 1
        
        # Accumulate for average distance calculation
        self.distance_sum += dist_to_origin

    def get_dispersao(self) -> float:
        """
        Calculate average distance from origin (Dispersion).
        
        Higher values indicate walkers spread further from center.
        
        Returns:
            Average Euclidean distance from origin in pixels.
        """
        if self.total_moves == 0:
            return 0.0
        return self.distance_sum / self.total_moves

    def get_retorno_rate(self) -> float:
        """
        Calculate return to origin rate.
        
        Returns:
            Percentage of moves where walker was within threshold of origin.
        """
        if self.total_moves == 0:
            return 0.0
        return (self.return_count / self.total_moves) * 100

    def get_entropia(self) -> float:
        """
        Calculate Shannon entropy of direction sequence.
        
        Entropy measures unpredictability of the direction sequence.
        For 4 equally-likely directions, maximum entropy is log2(4) = 2.0.
        Higher entropy indicates better randomness.
        
        Returns:
            Shannon entropy value (0.0 to 2.0).
        """
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
        """
        Calculate direction distribution as percentages.
        
        Ideal distribution for unbiased RNG: 25% each direction.
        
        Returns:
            Dictionary mapping direction to percentage.
        """
        total = sum(self.direction_counts.values())
        if total == 0:
            return {'UP': 25.0, 'DOWN': 25.0, 'LEFT': 25.0, 'RIGHT': 25.0}
        return {k: (v / total) * 100 for k, v in self.direction_counts.items()}

    def get_max_heat(self) -> int:
        """
        Get maximum heat value for heatmap normalization.
        
        Returns:
            Maximum visit count across all cells.
        """
        max_heat = 0
        for row in self.heatmap:
            row_max = max(row) if row else 0
            if row_max > max_heat:
                max_heat = row_max
        return max_heat if max_heat > 0 else 1

    def get_stats_dict(self) -> Dict[str, float]:
        """
        Get all statistics as a dictionary for display.
        
        Returns:
            Dictionary with all computed metrics.
        """
        return {
            'dispersao': self.get_dispersao(),
            'retorno_rate': self.get_retorno_rate(),
            'entropia': self.get_entropia(),
            'total_moves': self.total_moves,
            'return_count': self.return_count
        }

    def reset(self) -> None:
        """Reset all statistics to initial state."""
        self.heatmap = [[0] * self.grid_width for _ in range(self.grid_height)]
        self.direction_history = []
        self.direction_counts = {'UP': 0, 'DOWN': 0, 'LEFT': 0, 'RIGHT': 0}
        self.distance_history = []
        self.return_count = 0
        self.total_moves = 0
        self.distance_sum = 0.0


