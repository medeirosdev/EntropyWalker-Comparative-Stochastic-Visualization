# EntropyWalker

**Comparative Stochastic Visualization**

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg)
![Status](https://img.shields.io/badge/status-stable-green.svg)

A real-time visualization tool for comparing pseudorandom number generators (PRNG) against high-entropy sources using the Random Walk algorithm. The application renders multiple autonomous agents in a split-screen environment, comparing Python's Mersenne Twister against the `trueentropy` library.

## Features

- **Split-Screen Comparison**: Left side uses Python's `random` module, right side uses `trueentropy`
- **Multiple Walkers**: 15 simultaneous agents per side with color-coded trails
- **Persistent Trails**: Accumulated path history for pattern analysis
- **Real-Time Statistics**: Live metrics including dispersion, entropy, and return rate
- **Heatmap Overlay**: Visual density map showing visit frequency per cell
- **Distribution Graphs**: Matplotlib charts for direction and distance analysis
- **Hybrid Mode**: Uses `trueentropy` in HYBRID mode for high-performance simulation

## Installation

Clone the repository:

```bash
git clone https://github.com/medeirosdev/EntropyWalker-Comparative-Stochastic-Visualization.git
cd EntropyWalker-Comparative-Stochastic-Visualization
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

Run the main application:

```bash
python main.py
```

### Keyboard Controls

| Key | Action |
|-----|--------|
| `ESC` | Quit application |
| `C` | Clear trails |
| `H` | Toggle heatmap overlay |
| `R` | Reset statistics |
| `G` | Generate distribution graphs |

## Statistics

The application tracks and displays real-time metrics:

- **Dispersion**: Average distance of walkers from their origin point
- **Entropy**: Shannon entropy of direction sequence (max 2.0 for 4 directions)
- **Return Rate**: Percentage of moves that returned to origin area

## Technical Details

The system uses autonomous agents starting from central coordinates. At each time step, a direction vector is selected from {Up, Down, Left, Right} based on the designated entropy source.

### Architecture

```
main.py          # Application entry point and game loop
walker.py        # RandomWalker class definition
stats.py         # Statistics tracking and heatmap generation
graphs.py        # Matplotlib visualization module
```

### Entropy Sources

- **Left Screen**: Python `random` module (Mersenne Twister PRNG)
- **Right Screen**: `trueentropy` library (hardware/chaos entropy sources)

## Configuration

Key parameters in `main.py`:

```python
NUM_WALKERS = 15      # Agents per side
CELL_SIZE = 10        # Heatmap cell size (pixels)
WIDTH = 1200          # Window width
HEIGHT = 600          # Window height
FPS = 60              # Frame rate
```

## Requirements

- Python 3.8+
- pygame >= 2.6.1
- trueentropy >= 1.0.0
- matplotlib >= 3.7.0

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

## Contributing

Contributions are welcome. Please open an issue or submit a pull request.


