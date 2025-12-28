"""
EntropyWalker : Comparative Stochastic Visualization
===================================================

A real-time simulation comparing Python's Mersenne Twister properties against 
the 'trueentropy' library using a split-screen random walk visualization.

Usage:
    python main.py
"""

import sys
import pygame
import random
from typing import NoReturn, Tuple, List

from walker import RandomWalker, Direction
import trueentropy

# --- Configuration & Constants ---
ENTROPY_SOURCE_NAME = "TrueEntropy (HYBRID)"
NUM_WALKERS = 15  # Number of walkers per side

WIDTH: int = 1200
HEIGHT: int = 600
FPS: int = 60

# Colors (R, G, B)
BG_COLOR: Tuple[int, int, int] = (10, 10, 15)
DIVIDER_COLOR: Tuple[int, int, int] = (50, 50, 50)
TEXT_COLOR: Tuple[int, int, int] = (150, 150, 150)
WHITE: Tuple[int, int, int] = (255, 255, 255)

# Base colors for each side
LEFT_BASE_COLOR: Tuple[int, int, int] = (0, 255, 200)   # Cyan for Python Random
RIGHT_BASE_COLOR: Tuple[int, int, int] = (255, 100, 50) # Orange for TrueEntropy

def generate_color_variants(base_color: Tuple[int, int, int], count: int) -> List[Tuple[int, int, int]]:
    """Generate color variants with slight hue/saturation shifts."""
    colors = []
    for i in range(count):
        # Vary brightness slightly
        factor = 0.6 + (i / count) * 0.5  # Range from 0.6 to 1.1
        new_color = tuple(max(0, min(255, int(c * factor))) for c in base_color)
        colors.append(new_color)
    return colors

def get_random_direction_std() -> Direction:
    """Returns a direction using Python's standard random module."""
    return random.choice(['UP', 'DOWN', 'LEFT', 'RIGHT'])

def get_random_direction_true() -> Direction:
    """Returns a direction using the trueentropy library."""
    return trueentropy.choice(['UP', 'DOWN', 'LEFT', 'RIGHT'])

def main() -> NoReturn:
    """Main application loop."""
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("EntropyWalker : Comparative Stochastic Visualization")
    clock = pygame.time.Clock()

    font = pygame.font.SysFont("Consolas", 16)
    
    # Calculate screen geometry
    mid_x: int = WIDTH // 2

    # Generate color variants for each side
    left_colors = generate_color_variants(LEFT_BASE_COLOR, NUM_WALKERS)
    right_colors = generate_color_variants(RIGHT_BASE_COLOR, NUM_WALKERS)

    # Initialize Walkers - 15 per side
    walkers_std: List[RandomWalker] = []
    walkers_true: List[RandomWalker] = []
    
    for i in range(NUM_WALKERS):
        # Standard Random Walkers (Left Half) - spread around center
        walkers_std.append(RandomWalker(
            mid_x // 2, 
            HEIGHT // 2, 
            left_colors[i], 
            step_size=3, 
            max_history=5000
        ))
        
        # TrueEntropy Walkers (Right Half) - spread around center
        walkers_true.append(RandomWalker(
            mid_x + (mid_x // 2), 
            HEIGHT // 2, 
            right_colors[i], 
            step_size=3, 
            max_history=5000
        ))

    # Configure TrueEntropy in HYBRID mode for high-performance simulation
    trueentropy.configure(mode="HYBRID", hybrid_reseed_interval=60.0)

    # Start Background Collector (keeps the entropy pool filled)
    trueentropy.start_collector(interval=10.0)

    # Create a persistent surface for trails
    trail_surface = pygame.Surface((WIDTH, HEIGHT))
    trail_surface.fill(BG_COLOR)

    # Divider on persistent surface
    pygame.draw.line(trail_surface, DIVIDER_COLOR, (mid_x, 0), (mid_x, HEIGHT), 2)

    running: bool = True
    try:
        while running:
            # Event Handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    elif event.key == pygame.K_c:
                        # Clear screen
                        trail_surface.fill(BG_COLOR)
                        pygame.draw.line(trail_surface, DIVIDER_COLOR, (mid_x, 0), (mid_x, HEIGHT), 2)

            # Update and draw all walkers
            for walker in walkers_std:
                old_x, old_y = walker.x, walker.y
                walker.move(get_random_direction_std())
                # Boundary Check Left
                walker.x = max(0, min(walker.x, mid_x - 1))
                walker.y = max(0, min(walker.y, HEIGHT))
                # Draw trail
                pygame.draw.line(trail_surface, walker.color, (old_x, old_y), (walker.x, walker.y), 1)

            for walker in walkers_true:
                old_x, old_y = walker.x, walker.y
                walker.move(get_random_direction_true())
                # Boundary Check Right
                walker.x = max(mid_x + 1, min(walker.x, WIDTH))
                walker.y = max(0, min(walker.y, HEIGHT))
                # Draw trail
                pygame.draw.line(trail_surface, walker.color, (old_x, old_y), (walker.x, walker.y), 1)

            # Blit persistent surface to screen
            screen.blit(trail_surface, (0, 0))

            # Draw Walker Heads
            for walker in walkers_std:
                pygame.draw.circle(screen, WHITE, (walker.x, walker.y), 2)
            for walker in walkers_true:
                pygame.draw.circle(screen, WHITE, (walker.x, walker.y), 2)

            # UI / HUD
            text_std = font.render(f"Python random (Mersenne Twister) x{NUM_WALKERS}", True, LEFT_BASE_COLOR)
            screen.blit(text_std, (20, 20))

            text_true = font.render(f"{ENTROPY_SOURCE_NAME} x{NUM_WALKERS}", True, RIGHT_BASE_COLOR)
            screen.blit(text_true, (mid_x + 20, 20))

            # Stats
            health = trueentropy.health()
            stats_text = font.render(f"Health: {health['score']}/100 [{health['status']}]", True, TEXT_COLOR)
            screen.blit(stats_text, (WIDTH - 250, HEIGHT - 30))

            pygame.display.flip()
            clock.tick(FPS)
    finally:
        # Stop Background Collector on exit
        trueentropy.stop_collector()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()

