import pygame
from typing import List, Tuple, Literal

# Type alias for directions
Direction = Literal['UP', 'DOWN', 'LEFT', 'RIGHT']

class RandomWalker:
    """
    Represents an autonomous agent that moves on a 2D plane based on stochastic inputs.
    
    Attributes:
        x (int): Current x-coordinate.
        y (int): Current y-coordinate.
        color (Tuple[int, int, int]): RGB color of the walker's trail.
        step_size (int): Checkpoint distance per move.
        path (List[Tuple[int, int]]): History of visited coordinates.
        max_history (int): Maximum number of points to keep in path history.
    """

    def __init__(self, x: int, y: int, color: Tuple[int, int, int], step_size: int = 2, max_history: int = 1000):
        """
        Initialize the RandomWalker.

        Args:
            x: Initial x-coordinate.
            y: Initial y-coordinate.
            color: RGB tuple for the walker's display color.
            step_size: Pixels to move per step.
            max_history: Max points to store in path (deprecated/unused by persistent rendering, but kept for logic).
        """
        self.x = x
        self.y = y
        self.color = color
        self.step_size = step_size
        self.path: List[Tuple[int, int]] = []
        self.max_history = max_history

    def move(self, direction: Direction) -> None:
        """
        Update position based on directional input.

        Args:
            direction: One of 'UP', 'DOWN', 'LEFT', 'RIGHT'.
        """
        if direction == 'UP':
            self.y -= self.step_size
        elif direction == 'DOWN':
            self.y += self.step_size
        elif direction == 'LEFT':
            self.x -= self.step_size
        elif direction == 'RIGHT':
            self.x += self.step_size
        
        # Append to path
        self.path.append((self.x, self.y))
        
        # Limit path history for performance (logic retention)
        if len(self.path) > self.max_history:
            self.path.pop(0)

    def draw(self, surface: pygame.Surface) -> None:
        """
        Draw the walker's current head and immediate path segment.
        
        Args:
            surface: The display surface to draw onto.
        """
        if len(self.path) > 1:
            pygame.draw.lines(surface, self.color, False, self.path, 1)
        
        # Draw head
        pygame.draw.circle(surface, (255, 255, 255), (self.x, self.y), 3)
