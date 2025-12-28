"""
EntropyWalker : Comparative Stochastic Visualization
===================================================

A real-time simulation comparing Python's Mersenne Twister properties against 
the 'trueentropy' library using a split-screen random walk visualization.

Usage:
    python main.py

Controls:
    ESC - Quit
    C   - Clear trails
    H   - Toggle heatmap
    R   - Reset statistics
    G   - Show distribution graphs
"""

import sys
import pygame
import random
from typing import NoReturn, Tuple, List

from walker import RandomWalker, Direction
from stats import StatsTracker
from graphs import show_distribution_graphs
import trueentropy

# --- Configuration & Constants ---
ENTROPY_SOURCE_NAME = "TrueEntropy (HYBRID)"
NUM_WALKERS = 15  # Number of walkers per side
CELL_SIZE = 10    # Heatmap cell size in pixels

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
        factor = 0.6 + (i / count) * 0.5
        new_color = tuple(max(0, min(255, int(c * factor))) for c in base_color)
        colors.append(new_color)
    return colors

def get_random_direction_std() -> Direction:
    """Returns a direction using Python's standard random module."""
    return random.choice(['UP', 'DOWN', 'LEFT', 'RIGHT'])

def get_random_direction_true() -> Direction:
    """Returns a direction using the trueentropy library."""
    return trueentropy.choice(['UP', 'DOWN', 'LEFT', 'RIGHT'])

def heat_to_color(value: float) -> Tuple[int, int, int]:
    """Convert heat value (0-1) to color (blue -> green -> yellow -> red)."""
    if value < 0.25:
        t = value / 0.25
        return (0, int(t * 255), 255)  # Blue to Cyan
    elif value < 0.5:
        t = (value - 0.25) / 0.25
        return (0, 255, int(255 * (1 - t)))  # Cyan to Green
    elif value < 0.75:
        t = (value - 0.5) / 0.25
        return (int(t * 255), 255, 0)  # Green to Yellow
    else:
        t = (value - 0.75) / 0.25
        return (255, int(255 * (1 - t)), 0)  # Yellow to Red

def render_heatmap(surface: pygame.Surface, tracker: StatsTracker, offset_x: int = 0, alpha: int = 100) -> None:
    """Render heatmap overlay on surface."""
    max_heat = tracker.get_max_heat()
    
    for row_idx, row in enumerate(tracker.heatmap):
        for col_idx, count in enumerate(row):
            if count > 0:
                # Normalize heat value
                heat = min(count / max_heat, 1.0) if max_heat > 0 else 0
                color = heat_to_color(heat)
                
                # Draw cell
                rect = pygame.Rect(
                    offset_x + col_idx * tracker.cell_size,
                    row_idx * tracker.cell_size,
                    tracker.cell_size,
                    tracker.cell_size
                )
                cell_surface = pygame.Surface((tracker.cell_size, tracker.cell_size))
                cell_surface.fill(color)
                cell_surface.set_alpha(alpha)
                surface.blit(cell_surface, rect)

def main() -> NoReturn:
    """Main application loop."""
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("EntropyWalker : Comparative Stochastic Visualization")
    clock = pygame.time.Clock()

    font = pygame.font.SysFont("Consolas", 14)
    font_small = pygame.font.SysFont("Consolas", 12)
    
    # Calculate screen geometry
    mid_x: int = WIDTH // 2

    # Generate color variants for each side
    left_colors = generate_color_variants(LEFT_BASE_COLOR, NUM_WALKERS)
    right_colors = generate_color_variants(RIGHT_BASE_COLOR, NUM_WALKERS)

    # Initialize Walkers
    walkers_std: List[RandomWalker] = []
    walkers_true: List[RandomWalker] = []
    
    left_origin = (mid_x // 2, HEIGHT // 2)
    right_origin = (mid_x + (mid_x // 2), HEIGHT // 2)
    
    for i in range(NUM_WALKERS):
        walkers_std.append(RandomWalker(
            left_origin[0], left_origin[1], left_colors[i], step_size=3, max_history=5000
        ))
        walkers_true.append(RandomWalker(
            right_origin[0], right_origin[1], right_colors[i], step_size=3, max_history=5000
        ))

    # Initialize Stats Trackers
    stats_std = StatsTracker(left_origin, mid_x, HEIGHT, CELL_SIZE)
    stats_true = StatsTracker((mid_x // 2, HEIGHT // 2), mid_x, HEIGHT, CELL_SIZE)

    # Configure TrueEntropy
    trueentropy.configure(mode="HYBRID", hybrid_reseed_interval=60.0)
    trueentropy.start_collector(interval=10.0)

    # Create surfaces
    trail_surface = pygame.Surface((WIDTH, HEIGHT))
    trail_surface.fill(BG_COLOR)
    pygame.draw.line(trail_surface, DIVIDER_COLOR, (mid_x, 0), (mid_x, HEIGHT), 2)

    # State
    running: bool = True
    show_heatmap: bool = False

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
                        trail_surface.fill(BG_COLOR)
                        pygame.draw.line(trail_surface, DIVIDER_COLOR, (mid_x, 0), (mid_x, HEIGHT), 2)
                    elif event.key == pygame.K_h:
                        show_heatmap = not show_heatmap
                    elif event.key == pygame.K_r:
                        stats_std.reset()
                        stats_true.reset()
                    elif event.key == pygame.K_g:
                        # Show distribution graphs
                        show_distribution_graphs(
                            stats_std, stats_true,
                            "Python Random", ENTROPY_SOURCE_NAME
                        )

            # Update walkers and record stats
            for walker in walkers_std:
                old_x, old_y = walker.x, walker.y
                direction = get_random_direction_std()
                walker.move(direction)
                walker.x = max(0, min(walker.x, mid_x - 1))
                walker.y = max(0, min(walker.y, HEIGHT))
                pygame.draw.line(trail_surface, walker.color, (old_x, old_y), (walker.x, walker.y), 1)
                stats_std.record_move(walker.x, walker.y, direction)

            for walker in walkers_true:
                old_x, old_y = walker.x, walker.y
                direction = get_random_direction_true()
                walker.move(direction)
                walker.x = max(mid_x + 1, min(walker.x, WIDTH))
                walker.y = max(0, min(walker.y, HEIGHT))
                pygame.draw.line(trail_surface, walker.color, (old_x, old_y), (walker.x, walker.y), 1)
                # Adjust x for right-side heatmap (relative to mid_x)
                stats_true.record_move(walker.x - mid_x, walker.y, direction)

            # Drawing
            screen.blit(trail_surface, (0, 0))

            # Heatmap overlay
            if show_heatmap:
                render_heatmap(screen, stats_std, 0, 80)
                render_heatmap(screen, stats_true, mid_x, 80)

            # Draw Walker Heads
            for walker in walkers_std:
                pygame.draw.circle(screen, WHITE, (walker.x, walker.y), 2)
            for walker in walkers_true:
                pygame.draw.circle(screen, WHITE, (walker.x, walker.y), 2)

            # UI / HUD - Top
            text_std = font.render(f"Python random (Mersenne Twister) x{NUM_WALKERS}", True, LEFT_BASE_COLOR)
            screen.blit(text_std, (20, 15))

            text_true = font.render(f"{ENTROPY_SOURCE_NAME} x{NUM_WALKERS}", True, RIGHT_BASE_COLOR)
            screen.blit(text_true, (mid_x + 20, 15))

            # Stats Panel - Left
            left_stats = stats_std.get_stats_dict()
            stats_y = HEIGHT - 80
            screen.blit(font_small.render(f"Dispersão: {left_stats['dispersao']:.1f}px", True, TEXT_COLOR), (20, stats_y))
            screen.blit(font_small.render(f"Retorno: {left_stats['retorno_rate']:.2f}%", True, TEXT_COLOR), (20, stats_y + 15))
            screen.blit(font_small.render(f"Entropia: {left_stats['entropia']:.3f}/2.0", True, TEXT_COLOR), (20, stats_y + 30))
            screen.blit(font_small.render(f"Moves: {left_stats['total_moves']}", True, TEXT_COLOR), (20, stats_y + 45))

            # Stats Panel - Right
            right_stats = stats_true.get_stats_dict()
            screen.blit(font_small.render(f"Dispersão: {right_stats['dispersao']:.1f}px", True, TEXT_COLOR), (mid_x + 20, stats_y))
            screen.blit(font_small.render(f"Retorno: {right_stats['retorno_rate']:.2f}%", True, TEXT_COLOR), (mid_x + 20, stats_y + 15))
            screen.blit(font_small.render(f"Entropia: {right_stats['entropia']:.3f}/2.0", True, TEXT_COLOR), (mid_x + 20, stats_y + 30))
            screen.blit(font_small.render(f"Moves: {right_stats['total_moves']}", True, TEXT_COLOR), (mid_x + 20, stats_y + 45))

            # Health indicator
            health = trueentropy.health()
            health_text = font_small.render(f"Health: {health['score']}/100", True, TEXT_COLOR)
            screen.blit(health_text, (WIDTH - 150, HEIGHT - 25))

            # Heatmap toggle indicator
            heatmap_text = font_small.render(f"[H] Heatmap: {'ON' if show_heatmap else 'OFF'}", True, TEXT_COLOR)
            screen.blit(heatmap_text, (WIDTH // 2 - 60, HEIGHT - 25))

            pygame.display.flip()
            clock.tick(FPS)
    finally:
        trueentropy.stop_collector()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()


