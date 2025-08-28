# Double Pendulum Simulation

A double pendulum simulation program implemented using the Verlet integration algorithm, written in C++ with Python visualization capabilities.

## Features

- **Verlet Integration Algorithm**: High-precision Verlet integration for numerical solution of the double pendulum system
- **Configurable Parameters**: Flexible configuration of initial conditions and physical parameters via config files
- **Data Output**: C++ program outputs time-series data to text files
- **Python Visualization**: Generate high-quality PNG static images and GIF animations using matplotlib
- **Automatic Environment Management**: Automatically create and manage conda virtual environments
- **Chaos System Demonstration**: Showcase the chaotic behavior characteristics of double pendulum systems

## Project Structure

```
DoublePendulum/
├── include/
│   └── DoublePendulum.hpp  # Double pendulum class header
├── src/
│   ├── DoublePendulum.cpp  # Double pendulum class implementation
│   └── main.cpp            # Main program entry point
├── config/
│   └── config              # Configuration file
├── setup_env.sh            # Conda environment setup script
├── visualize.py            # Python visualization script
└── Makefile                # Build configuration
```

## Quick Start

### 1. Environment Setup
Before first use, set up the conda environment and Python dependencies:
```bash
./setup_env.sh
```

### 2. Compile Program
```bash
make gcc
```

### 3. Run Simulation
```bash
# Run C++ program to generate data
make run

# Generate static trajectory plot
make plot

# Generate animation (frame-by-frame mode)
make animate

# Generate animation and keep frame files
make animate-keep

# One-click: generate data and static plot
make all
```

## Configuration File

The configuration file `config/config` uses key-value pairs to define physical parameters and simulation settings for the double pendulum system:

```
L1=1.0          # Length of first pendulum (m)
L2=1.0          # Length of second pendulum (m) 
M1=1.0          # Mass of first pendulum bob (kg)
M2=1.0          # Mass of second pendulum bob (kg)
G=9.8           # Gravitational acceleration (m/s²)
THETA1=0.0      # Initial angle of first pendulum (radians)
THETA2=0.0      # Initial angle of second pendulum (radians)
OMEGA1=3.0      # Initial angular velocity of first pendulum (rad/s)
OMEGA2=0.0      # Initial angular velocity of second pendulum (rad/s)
DT=0.00001      # Time step (s)
TOTAL_TIME=10.0 # Total simulation time (s)
```

### Parameter Description
- **Physical Parameters**: L1, L2 are pendulum lengths; M1, M2 are pendulum bob masses; G is gravitational acceleration
- **Initial Conditions**: THETA1, THETA2 are initial angles; OMEGA1, OMEGA2 are initial angular velocities
- **Numerical Parameters**: DT is time step (affects accuracy and speed); TOTAL_TIME is total simulation duration

## Program Output

### C++ Program Output
The C++ program reads the configuration file, runs the double pendulum simulation, and outputs results to a data file (default: `pendulum_data.txt`) in the following format:
```
# Configuration info: L1=1.00 L2=1.00 M1=1.00 M2=1.00
time x1_coord y1_coord x2_coord y2_coord
0.000000 0.000000 -1.000000 0.000000 -2.000000
0.000010 0.000030 -0.999999 0.000060 -1.999998
...
```

### Python Visualization Output
The Python script can generate two types of visualizations:

1. **Static Trajectory Plot** (PNG format)
   - Shows complete motion trajectories of both pendulum bobs
   - Red trajectory: First pendulum bob
   - Blue trajectory: Second pendulum bob
   - Includes starting points, pivot point, and final pendulum rod positions

2. **Animation** (GIF format)
   - Dynamic display of real-time double pendulum motion
   - Includes pendulum rods, bobs, and trajectory trails
   - Uses frame-by-frame generation for better control and memory efficiency
   - Frame files temporarily saved to `output/` directory during generation
   - Option to keep frame files for inspection or post-processing

## Frame-by-Frame Animation Mode
```bash
# Generate animation (automatically removes frame files)
make animate

# Generate animation and keep frame files
make animate-keep

# Or use Python directly
python visualize.py pendulum_data.txt --animate -o output.gif
python visualize.py pendulum_data.txt --animate --keep-frames -o output.gif
```
Generates individual PNG frames in the `output/` directory, then combines them into a GIF. Provides:
- Better quality control
- Option to keep individual frames
- More customization possibilities

### Keep Frame Files
```bash
make animate-frames-keep
# or
python visualize.py pendulum_data.txt --animate --frame-mode --keep-frames -o output.gif
```
Same as frame-by-frame mode but preserves individual frame files in the `output/` directory for further processing.

## Algorithm Principles

### Verlet Integration Algorithm
The program uses the Verlet algorithm to solve the double pendulum equations of motion. This algorithm has the following advantages:
- **Time Symmetry**: Better numerical stability
- **Energy Conservation**: Energy remains relatively stable during long-term integration
- **High Precision**: Second-order accuracy numerical integration method

Algorithm steps:
1. **Position Update**: `θ(t+dt) = 2*θ(t) - θ(t-dt) + α(t)*dt²`
2. **Velocity Update**: `ω(t) = [θ(t+dt) - θ(t-dt)] / (2*dt)`

### Double Pendulum System Dynamics
The double pendulum is a nonlinear dynamical system with two degrees of freedom. The equations of motion derived from Lagrangian mechanics include:
- **Gravitational Effects**: Gravitational influence on both pendulum bobs
- **Constraint Forces**: Rigid body constraints of pendulum rods
- **Coupling Effects**: Interactions between the two pendulum bobs

Angular acceleration calculations involve complex trigonometric functions and coupling terms, reflecting the system's nonlinear characteristics.

## Chaotic Behavior Characteristics

The double pendulum system is a classic chaotic system with the following features:
- **Sensitivity to Initial Conditions**: Small changes in initial conditions lead to drastically different long-term behavior
- **Unpredictability**: Long-term behavior cannot be precisely predicted
- **Fractal Trajectories**: Forms complex fractal structures in phase space
- **Quasi-periodic Motion**: Exhibits quasi-periodic or chaotic motion under certain parameters

By changing initial angles or angular velocities, you can observe the transition from regular oscillation to complete chaos.

## System Requirements

### C++ Compilation Environment
- **Compiler**: C++11 standard compatible compiler (e.g., GCC 4.8+)
- **Build Tools**: GNU Make
- **Operating System**: Linux, macOS, or Windows (using WSL)

### Python Environment
- **Python Version**: 3.9 or higher
- **Package Manager**: Conda (Miniconda or Anaconda recommended)
- **Dependencies**:
  - `matplotlib`: For graphics plotting and animation generation
  - `numpy`: For numerical computation and data processing
  - `PIL (Pillow)`: For image processing and GIF creation in frame-by-frame mode

*Note: Python dependencies are automatically installed to a local conda environment via the `setup_env.sh` script*

## Usage Tips

### Parameter Tuning Recommendations
1. **Time Step (DT)**:
   - Smaller values (e.g., 0.00001): High precision but slower computation
   - Larger values (e.g., 0.01): Faster computation but potentially unstable
   - Recommended range: 0.0001 - 0.001

2. **Initial Condition Experiments**:
   - Small angles: Approximates linear system, regular oscillation
   - Large angles: Obvious nonlinear effects, possible chaos
   - Different initial velocities: Generate different types of motion patterns

3. **Simulation Time**:
   - Short time (<5s): Observe basic motion patterns
   - Long time (10-30s): Observe chaotic behavior and trajectory complexity

### Troubleshooting
- **Compilation Failure**: Ensure g++ and make tools are installed
- **Python Environment Issues**: Re-run `./setup_env.sh`
- **Empty Data File**: Check configuration file format and parameter validity
- **Animation Generation Failure**: Ensure sufficient disk space, GIF files can be large
- **Frame-by-Frame Mode Issues**: Check that PIL/Pillow is installed; use `make animate` as fallback
- **Individual Frame Files**: Use `--keep-frames` option to preserve frames for manual processing

## Make Command Reference

| Command | Function | Description |
|---------|----------|-------------|
| `make gcc` | Compile C++ program | Generate executable `double_pendulum` |
| `make run` | Run simulation | Generate data file using default configuration |
| `make plot` | Static plot | Generate PNG trajectory plot from data file |
| `make animate` | Animation (frame-by-frame) | Generate GIF animation using frame-by-frame mode |
| `make animate-keep` | Animation (keep frames) | Generate GIF and keep individual frame files |
| `make all` | Complete workflow | Compile → Run → Generate static plot |
| `make clean` | Clean | Delete all generated files and conda environment |
| `make help` | Help | Show all available commands |

## Example Results

### Configuration Example: Small Angle Oscillation
```bash
# Configuration: THETA1=0.5, THETA2=0.3, OMEGA1=0, OMEGA2=0
# Result: Regular elliptical trajectories, quasi-periodic motion
```

### Configuration Example: Large Angle Chaos
```bash
# Configuration: THETA1=3.0, THETA2=2.0, OMEGA1=1, OMEGA2=1  
# Result: Complex fractal trajectories, typical chaotic behavior
```

## Project Extensions

Possible feature extensions to consider:
- Add damping effects (air resistance, friction)
- Implement comparison of different numerical integration algorithms
- Add phase space plots and Poincaré section analysis
- Support batch processing of multiple initial conditions
- Add energy conservation monitoring and analysis

## License

This project is licensed under the MIT License.

## Contributing

Issues and Pull Requests are welcome to improve this project!

---

**Languages**: [English](README.md) | [中文](README_CN.md)
