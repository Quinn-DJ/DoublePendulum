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
import os
from PIL import Image
import glob

def read_pendulum_data(filename):
    """Read double pendulum position data file"""
    data = []
    config_info = {}
    
    try:
        print("Reading position data file...")
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
        print(f"Position data reading completed! Total data points: {len(data)}")
    
    except FileNotFoundError:
        print(f"Error: Cannot find data file {filename}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: Error occurred while reading data file: {e}")
        sys.exit(1)
    
    return np.array(data), config_info

def read_angle_data(filename):
    """Read double pendulum angle data file"""
    data = []
    config_info = {}
    
    try:
        print("Reading angle data file...")
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
                # Parse data line: time theta1 theta2
                values = list(map(float, line.split()))
                data.append(values)
        
        print(f"\rReading progress: 100%")
        print(f"Angle data reading completed! Total data points: {len(data)}")
    
    except FileNotFoundError:
        print(f"Warning: Cannot find angle data file {filename}, skipping angle trajectory plot")
        return None, {}
    except Exception as e:
        print(f"Warning: Error occurred while reading angle data file: {e}, skipping angle trajectory plot")
        return None, {}
    
    return np.array(data), config_info

def plot_static_trajectories(data, angle_data, config_info, output_file):
    """Plot static trajectory diagram with position and angle trajectories"""
    print("Creating static trajectory plot...")
    
    times = data[:, 0]
    x1, y1 = data[:, 1], data[:, 2]
    x2, y2 = data[:, 3], data[:, 4]
    
    print("Progress: 10% - Setting up plot...")
    
    # Create subplots
    if angle_data is not None:
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))
    else:
        fig, ax1 = plt.subplots(figsize=(12, 8))
    
    print("Progress: 20% - Drawing position trajectories...")
    # Draw position trajectories
    ax1.plot(x1, y1, 'r-', linewidth=2, alpha=0.7, label='The first pendulum path')
    ax1.plot(x2, y2, 'lightblue', linewidth=2, alpha=0.7, label='The second pendulum path')
    
    print("Progress: 40% - Adding markers and points...")
    # Draw starting points
    ax1.plot(x1[0], y1[0], 'ro', markersize=8, label='Starting point 1')
    ax1.plot(x2[0], y2[0], 'bo', markersize=8, label='Starting point 2')
    
    # Draw fixed point
    ax1.plot(0, 0, 'ko', markersize=10, label='Fixed point')
    
    # Draw final pendulum position
    ax1.plot([0, x1[-1], x2[-1]], [0, y1[-1], y2[-1]], 'k-', linewidth=1, alpha=0.5)
    
    print("Progress: 60% - Configuring position plot settings...")
    ax1.set_aspect('equal')
    ax1.grid(True, alpha=0.3)
    ax1.set_xlabel('X Position (m)')
    ax1.set_ylabel('Y Position (m)')
    ax1.set_title(f'Double Pendulum Position Trajectory\nL1={config_info.get("L1", "?"):.2f}m, L2={config_info.get("L2", "?"):.2f}m')
    ax1.legend()
    
    # Plot angle trajectory if available
    if angle_data is not None:
        print("Progress: 70% - Drawing angle trajectory...")
        angle_times = angle_data[:, 0]
        theta1, theta2 = angle_data[:, 1], angle_data[:, 2]
        
        ax2.plot(theta1, theta2, 'g-', linewidth=2, alpha=0.7, label='Angle trajectory (θ₁, θ₂)')
        ax2.plot(theta1[0], theta2[0], 'go', markersize=8, label='Starting point')
        ax2.plot(theta1[-1], theta2[-1], 'rs', markersize=8, label='End point')
        
        ax2.grid(True, alpha=0.3)
        ax2.set_xlabel('θ₁ (radians)')
        ax2.set_ylabel('θ₂ (radians)')
        ax2.set_title('Phase Space Trajectory (θ₁ vs θ₂)')
        ax2.legend()
        
        print("Progress: 80% - Configuring angle plot settings...")
    
    print("Progress: 90% - Saving plot...")
    plt.tight_layout()
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print("Progress: 100% - Plot creation completed!")
    print(f"Static trajectory plot saved as: {output_file}")
    
    if angle_data is not None:
        print("Both position and angle trajectories have been plotted.")

def create_animation(data, config_info, output_file, keep_frames=False):
    """Create animation by saving individual frames and converting to GIF"""
    print("Creating animation by saving individual frames...")
    
    times = data[:, 0]
    x1, y1 = data[:, 1], data[:, 2]
    x2, y2 = data[:, 3], data[:, 4]
    
    # Create output directory for frames
    frames_dir = "output"
    if not os.path.exists(frames_dir):
        os.makedirs(frames_dir)
    
    print("Progress: 10% - Setting up canvas...")
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
    
    # Store trajectories
    trail1_x, trail1_y = [], []
    trail2_x, trail2_y = [], []
    
    print("Progress: 20% - Generating frames...")
    total_frames = len(data)
    
    # Skip frames to reduce total number (every 30th frame)
    frame_skip = 5  # Take 1 frame every 30 data points
    
    frame_files = []
    for i in range(0, total_frames, frame_skip):
        # Clear the plot
        ax.clear()
        
        # Reset plot properties
        ax.set_xlim(-max_range, max_range)
        ax.set_ylim(-max_range, max_range)
        ax.set_aspect('equal')
        ax.grid(True, alpha=0.3)
        ax.set_xlabel('X Position (m)')
        ax.set_ylabel('Y Position (m)')
        ax.set_title(f'Double Pendulum Animation - L1={config_info.get("L1", "?"):.2f}m, L2={config_info.get("L2", "?"):.2f}m')
        
        # Update trajectories
        trail1_x.append(x1[i])
        trail1_y.append(y1[i])
        trail2_x.append(x2[i])
        trail2_y.append(y2[i])
        
        # Limit trajectory length for better performance
        if len(trail1_x) > 200:
            trail1_x.pop(0)
            trail1_y.pop(0)
            trail2_x.pop(0)
            trail2_y.pop(0)
        
        # Draw trajectories
        if len(trail1_x) > 1:
            ax.plot(trail1_x, trail1_y, 'r-', alpha=0.3, linewidth=1)
            ax.plot(trail2_x, trail2_y, 'b-', alpha=0.3, linewidth=1)
        
        # Draw pendulum structure
        ax.plot([0, x1[i], x2[i]], [0, y1[i], y2[i]], 'k-', linewidth=3)
        ax.plot([0], [0], 'ko', markersize=8)  # Pivot point
        ax.plot([x1[i]], [y1[i]], 'ro', markersize=10)  # Ball 1
        ax.plot([x2[i]], [y2[i]], 'bo', markersize=10)  # Ball 2
        
        # Save frame
        frame_filename = f"{frames_dir}/frame_{i//frame_skip:06d}.png"
        plt.savefig(frame_filename, dpi=100, bbox_inches='tight')
        frame_files.append(frame_filename)
        
        # Show progress
        progress = int((i * 50) / total_frames) + 20
        if i % (max(1, total_frames // 20)) == 0:
            print(f"Progress: {progress}% - Generated frame {i//frame_skip + 1}/{total_frames//frame_skip}")
    
    plt.close(fig)
    
    print("Progress: 70% - Converting frames to GIF...")
    
    # Convert frames to GIF using PIL
    images = []
    for frame_file in frame_files:
        img = Image.open(frame_file)
        images.append(img)
    
    print("Progress: 80% - Saving GIF...")
    # Save as GIF
    if images:
        images[0].save(
            output_file,
            save_all=True,
            append_images=images[1:],
            duration=80,  # milliseconds per frame
            loop=0
        )
    
    print("Progress: 90% - Cleaning up frame files...")
    # Optionally clean up frame files
    if not keep_frames:
        for frame_file in frame_files:
            os.remove(frame_file)
        print(f"Cleaned up {len(frame_files)} frame files")
    else:
        print(f"Kept {len(frame_files)} frame files in {frames_dir}/ directory")
    
    print("Progress: 100% - Animation creation completed!")
    print(f"Generated {len(images)} frames")
    print(f"Animation saved as: {output_file}")

def main():
    parser = argparse.ArgumentParser(description='Double Pendulum Data Visualization')
    parser.add_argument('data_file', help='Position data file path')
    parser.add_argument('-a', '--angle-file', help='Angle data file path (optional)')
    parser.add_argument('-o', '--output', default='pendulum_plot.png', 
                       help='Output file name (default: pendulum_plot.png)')
    parser.add_argument('--animate', action='store_true', 
                       help='Create animation instead of static plot')
    parser.add_argument('--keep-frames', action='store_true', 
                       help='Keep individual frame files after creating GIF')
    parser.add_argument('--show', action='store_true', 
                       help='Show image instead of saving')
    
    args = parser.parse_args()
    
    print("Double Pendulum Data Visualization Tool")
    print("=====================================")
    print(f"Position data file: {args.data_file}")
    if args.angle_file:
        print(f"Angle data file: {args.angle_file}")
    else:
        # Try to guess angle file name from position file name
        base_name = args.data_file
        if '.' in base_name:
            base_name = base_name.rsplit('.', 1)[0]
        angle_file = base_name + '_angles.txt'
        args.angle_file = angle_file
        print(f"Angle data file (auto-detected): {args.angle_file}")
    
    print(f"Output file: {args.output}")
    print(f"Mode: {'Animation' if args.animate else 'Static plot'}")
    
    # Read position data
    data, config_info = read_pendulum_data(args.data_file)
    print(f"Number of position data points: {len(data)}")
    
    # Read angle data (optional)
    angle_data = None
    if args.angle_file:
        angle_data, angle_config_info = read_angle_data(args.angle_file)
        if angle_data is not None:
            print(f"Number of angle data points: {len(angle_data)}")
    
    if len(data) == 0:
        print("Error: Position data file is empty")
        return
    
    if args.animate:
        if args.output.endswith(('.png', '.jpg', '.jpeg')):
            args.output = args.output.rsplit('.', 1)[0] + '.gif'
        
        create_animation(data, config_info, args.output, args.keep_frames)
    else:
        plot_static_trajectories(data, angle_data, config_info, args.output)
    
    if args.show:
        plt.show()

if __name__ == '__main__':
    main()
