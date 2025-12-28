# EntropyWalker: Comparative Stochastic Visualization

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg)
![Status](https://img.shields.io/badge/status-stable-green.svg)

**EntropyWalker : Comparative Stochastic Visualization** is a real-time stochastic visualization tool designed to compare the statistical properties of pseudorandom number generators (PRNG) against high-entropy sources. It renders "Random Walks" in a split-screen environment, pitting Python's standard Marsenne Twister against the `trueentropy` library.

## Features

- **Split-Screen Visualization**: Real-time comparison with persistent trails.
- **Infinite Canvas**: Trails remain on screen to form a complete history of the walk.
- **Entropy Analytics**: Live health monitoring of the entropy source.
- **Persistent Mode**: Trails are drawn to a persistent surface, allowing for long-running accumulation of data without performance loss.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/EntropyWalker.git
   cd EntropyWalker
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the main application script:

```bash
python main.py
```

### Controls

- **ESC**: Quit the application.
- **C**: Clear the screen (reset trails).

## Technical Details

The system utilizes two autonomous agents starting from central coordinates in isolated domains. At each time step ($t$), a direction vector $d \in \{Up, Down, Left, Right\}$ is calculated based on the designated entropy source.

- **Left Screen**: `random` module (Mersenne Twister).
- **Right Screen**: `trueentropy` custom library (Hardware/Chaos sources).

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

