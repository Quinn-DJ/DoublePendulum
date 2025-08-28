#!/usr/bin/env python3
"""
Double Pendulum Data Visualization Script
Read data files output by C++ program and generate visualization images
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import argparse
import sys

def read_pendulum_data(filename):
    """Read double pendulum data file"""
    data = []
    config_info = {}
    
    try:
        print("Reading data file...")
        with open(filename, 'r') as f:
            lines = f.readlines()
            
        total_lines = len(lines)
        last_reported_progress = -1
        
        for i, line in enumerate(lines):
            # Calculate and display progress percentage
            current_progress = int((i * 100.0) / total_lines)
            if current_progress > last_reported_progress:
                last_reported_progress = current_progress
                print(f"\rReading progress: {current_progress}%", end="", flush=True)
            
            line = line.strip()
            if line.startswith('#'):
                # Parse configuration information
                if 'L1=' in line and 'L2=' in line:
                    parts = line.replace('#', '').strip().split()
                    for part in parts:
                        if '=' in part:
                            key, value = part.split('=')
                            config_info[key] = float(value)
                continue
            
            if line:
                # Parse data line: time x1 y1 x2 y2
                values = list(map(float, line.split()))
                data.append(values)
        
        print(f"\rReading progress: 100%")
        print(f"Data reading completed! Total data points: {len(data)}")
    
    except FileNotFoundError:
        print(f"Error: Cannot find data file {filename}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: Error occurred while reading data file: {e}")
        sys.exit(1)
    
    return np.array(data), config_info

def plot_static_trajectories(data, config_info, output_file):
    """Plot static trajectory diagram"""
    print("Creating static trajectory plot...")
    
    times = data[:, 0]
    x1, y1 = data[:, 1], data[:, 2]
    x2, y2 = data[:, 3], data[:, 4]
    
    print("Progress: 20% - Setting up plot...")
    plt.figure(figsize=(12, 8))
    
    print("Progress: 40% - Drawing trajectories...")
    # Draw trajectories
    plt.plot(x1, y1, 'r-', linewidth=2, alpha=0.7, label='The first pendulum path')
    plt.plot(x2, y2, 'lightblue', linewidth=2, alpha=0.7, label='The second pendulum path')
    
    print("Progress: 60% - Adding markers and points...")
    # Draw starting points
    plt.plot(x1[0], y1[0], 'ro', markersize=8, label='Starting point 1')
    plt.plot(x2[0], y2[0], 'bo', markersize=8, label='Starting point 2')
    
    # Draw fixed point
    plt.plot(0, 0, 'ko', markersize=10, label='Fixed point')
    
    # Draw final pendulum position
    plt.plot([0, x1[-1], x2[-1]], [0, y1[-1], y2[-1]], 'k-', linewidth=1, alpha=0.5)
    
    print("Progress: 80% - Configuring plot settings...")
    plt.axis('equal')
    plt.grid(True, alpha=0.3)
    plt.xlabel('X Position (m)')
    plt.ylabel('Y Position (m)')
    plt.title(f'Double Pendulum Trajectory - L1={config_info.get("L1", "?"):.2f}m, L2={config_info.get("L2", "?"):.2f}m')
    plt.legend()
    
    print("Progress: 90% - Saving plot...")
    plt.tight_layout()
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print("Progress: 100% - Plot creation completed!")
    print(f"Static trajectory plot saved as: {output_file}")

def create_animation(data, config_info, output_file):
    """Create animation"""
    print("Creating animation...")
    
    times = data[:, 0]
    x1, y1 = data[:, 1], data[:, 2]
    x2, y2 = data[:, 3], data[:, 4]
    
    print("Progress: 10% - Setting up animation canvas...")
    fig, ax = plt.subplots(figsize=(10, 8))
    
    # Set coordinate axis range
    max_range = max(np.max(np.abs(x1)), np.max(np.abs(y1)), np.max(np.abs(x2)), np.max(np.abs(y2))) * 1.1
    ax.set_xlim(-max_range, max_range)
    ax.set_ylim(-max_range, max_range)
    ax.set_aspect('equal')
    ax.grid(True, alpha=0.3)
    ax.set_xlabel('X Position (m)')
    ax.set_ylabel('Y Position (m)')
    ax.set_title(f'Double Pendulum Animation - L1={config_info.get("L1", "?"):.2f}m, L2={config_info.get("L2", "?"):.2f}m')
    
    print("Progress: 30% - Initializing plot elements...")
    # Initialize plot elements
    line_pendulum, = ax.plot([], [], 'k-', linewidth=3)
    ball1, = ax.plot([], [], 'ro', markersize=10)
    ball2, = ax.plot([], [], 'bo', markersize=10)
    pivot, = ax.plot([0], [0], 'ko', markersize=8)
    trail1, = ax.plot([], [], 'r-', alpha=0.3, linewidth=1)
    trail2, = ax.plot([], [], 'b-', alpha=0.3, linewidth=1)
    
    # Store trajectories
    trail1_x, trail1_y = [], []
    trail2_x, trail2_y = [], []
    
    print("Progress: 50% - Defining animation function...")
    def animate(frame):
        if frame < len(data):
            # Update pendulum rods
            pendulum_x = [0, x1[frame], x2[frame]]
            pendulum_y = [0, y1[frame], y2[frame]]
            line_pendulum.set_data(pendulum_x, pendulum_y)
            
            # Update pendulum balls
            ball1.set_data([x1[frame]], [y1[frame]])
            ball2.set_data([x2[frame]], [y2[frame]])
            
            # Update trajectories
            trail1_x.append(x1[frame])
            trail1_y.append(y1[frame])
            trail2_x.append(x2[frame])
            trail2_y.append(y2[frame])
            
            # Limit trajectory length for better performance
            if len(trail1_x) > 500:
                trail1_x.pop(0)
                trail1_y.pop(0)
                trail2_x.pop(0)
                trail2_y.pop(0)
            
            trail1.set_data(trail1_x, trail1_y)
            trail2.set_data(trail2_x, trail2_y)
        
        return line_pendulum, ball1, ball2, trail1, trail2
    
    print("Progress: 70% - Creating animation object...")
    # Create animation
    anim = animation.FuncAnimation(fig, animate, frames=len(data), 
                                 interval=50, blit=True, repeat=True)
    
    print("Progress: 80% - Saving animation (this may take a while)...")
    # Save animation
    if output_file.endswith('.gif'):
        anim.save(output_file, writer='pillow', fps=60)
    else:
        anim.save(output_file, writer='ffmpeg', fps=60, bitrate=1800)
    
    print("Progress: 100% - Animation creation completed!")
    print(f"Animation saved as: {output_file}")

def main():
    parser = argparse.ArgumentParser(description='Double Pendulum Data Visualization')
    parser.add_argument('data_file', help='Data file path')
    parser.add_argument('-o', '--output', default='pendulum_plot.png', 
                       help='Output file name (default: pendulum_plot.png)')
    parser.add_argument('-a', '--animate', action='store_true', 
                       help='Create animation instead of static plot')
    parser.add_argument('--show', action='store_true', 
                       help='Show image instead of saving')
    
    args = parser.parse_args()
    
    print("Double Pendulum Data Visualization Tool")
    print("=====================================")
    print(f"Data file: {args.data_file}")
    print(f"Output file: {args.output}")
    print(f"Mode: {'Animation' if args.animate else 'Static plot'}")
    
    # Read data
    data, config_info = read_pendulum_data(args.data_file)
    print(f"Number of data points: {len(data)}")
    
    if len(data) == 0:
        print("Error: Data file is empty")
        return
    
    if args.animate:
        if args.output.endswith(('.png', '.jpg', '.jpeg')):
            args.output = args.output.rsplit('.', 1)[0] + '.gif'
        create_animation(data, config_info, args.output)
    else:
        plot_static_trajectories(data, config_info, args.output)
    
    if args.show:
        plt.show()

if __name__ == '__main__':
    main()
