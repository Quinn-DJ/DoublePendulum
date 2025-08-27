#!/usr/bin/env python3
"""
双摆数据可视化脚本
读取C++程序输出的数据文件并生成可视化图像
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import argparse
import sys

def read_pendulum_data(filename):
    """读取双摆数据文件"""
    data = []
    config_info = {}
    
    try:
        with open(filename, 'r') as f:
            for line in f:
                line = line.strip()
                if line.startswith('#'):
                    # 解析配置信息
                    if 'L1=' in line and 'L2=' in line:
                        parts = line.replace('#', '').strip().split()
                        for part in parts:
                            if '=' in part:
                                key, value = part.split('=')
                                config_info[key] = float(value)
                    continue
                
                if line:
                    # 解析数据行: time x1 y1 x2 y2
                    values = list(map(float, line.split()))
                    data.append(values)
    
    except FileNotFoundError:
        print(f"错误: 无法找到数据文件 {filename}")
        sys.exit(1)
    except Exception as e:
        print(f"错误: 读取数据文件时出错: {e}")
        sys.exit(1)
    
    return np.array(data), config_info

def plot_static_trajectories(data, config_info, output_file):
    """绘制静态轨迹图"""
    times = data[:, 0]
    x1, y1 = data[:, 1], data[:, 2]
    x2, y2 = data[:, 3], data[:, 4]
    
    plt.figure(figsize=(12, 8))
    
    # 绘制轨迹
    plt.plot(x1, y1, 'r-', linewidth=2, alpha=0.7, label='第一个摆球轨迹')
    plt.plot(x2, y2, 'lightblue', linewidth=2, alpha=0.7, label='第二个摆球轨迹')
    
    # 绘制起始点
    plt.plot(x1[0], y1[0], 'ro', markersize=8, label='起始位置1')
    plt.plot(x2[0], y2[0], 'bo', markersize=8, label='起始位置2')
    
    # 绘制固定点
    plt.plot(0, 0, 'ko', markersize=10, label='固定点')
    
    # 绘制最终摆杆位置
    plt.plot([0, x1[-1], x2[-1]], [0, y1[-1], y2[-1]], 'k-', linewidth=1, alpha=0.5)
    
    plt.axis('equal')
    plt.grid(True, alpha=0.3)
    plt.xlabel('X 位置 (m)')
    plt.ylabel('Y 位置 (m)')
    plt.title(f'双摆轨迹 - L1={config_info.get("L1", "?"):.2f}m, L2={config_info.get("L2", "?"):.2f}m')
    plt.legend()
    
    plt.tight_layout()
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"静态轨迹图已保存为: {output_file}")

def create_animation(data, config_info, output_file):
    """创建动画"""
    times = data[:, 0]
    x1, y1 = data[:, 1], data[:, 2]
    x2, y2 = data[:, 3], data[:, 4]
    
    fig, ax = plt.subplots(figsize=(10, 8))
    
    # 设置坐标轴范围
    max_range = max(np.max(np.abs(x1)), np.max(np.abs(y1)), np.max(np.abs(x2)), np.max(np.abs(y2))) * 1.1
    ax.set_xlim(-max_range, max_range)
    ax.set_ylim(-max_range, max_range)
    ax.set_aspect('equal')
    ax.grid(True, alpha=0.3)
    ax.set_xlabel('X 位置 (m)')
    ax.set_ylabel('Y 位置 (m)')
    ax.set_title(f'双摆动画 - L1={config_info.get("L1", "?"):.2f}m, L2={config_info.get("L2", "?"):.2f}m')
    
    # 初始化绘图元素
    line_pendulum, = ax.plot([], [], 'k-', linewidth=3)
    ball1, = ax.plot([], [], 'ro', markersize=10)
    ball2, = ax.plot([], [], 'bo', markersize=10)
    pivot, = ax.plot([0], [0], 'ko', markersize=8)
    trail1, = ax.plot([], [], 'r-', alpha=0.3, linewidth=1)
    trail2, = ax.plot([], [], 'b-', alpha=0.3, linewidth=1)
    
    # 存储轨迹
    trail1_x, trail1_y = [], []
    trail2_x, trail2_y = [], []
    
    def animate(frame):
        if frame < len(data):
            # 更新摆杆
            pendulum_x = [0, x1[frame], x2[frame]]
            pendulum_y = [0, y1[frame], y2[frame]]
            line_pendulum.set_data(pendulum_x, pendulum_y)
            
            # 更新摆球
            ball1.set_data([x1[frame]], [y1[frame]])
            ball2.set_data([x2[frame]], [y2[frame]])
            
            # 更新轨迹
            trail1_x.append(x1[frame])
            trail1_y.append(y1[frame])
            trail2_x.append(x2[frame])
            trail2_y.append(y2[frame])
            
            # 限制轨迹长度以提高性能
            if len(trail1_x) > 500:
                trail1_x.pop(0)
                trail1_y.pop(0)
                trail2_x.pop(0)
                trail2_y.pop(0)
            
            trail1.set_data(trail1_x, trail1_y)
            trail2.set_data(trail2_x, trail2_y)
        
        return line_pendulum, ball1, ball2, trail1, trail2
    
    # 创建动画
    anim = animation.FuncAnimation(fig, animate, frames=len(data), 
                                 interval=50, blit=True, repeat=True)
    
    # 保存动画
    if output_file.endswith('.gif'):
        anim.save(output_file, writer='pillow', fps=20)
    else:
        anim.save(output_file, writer='ffmpeg', fps=20, bitrate=1800)
    
    print(f"动画已保存为: {output_file}")

def main():
    parser = argparse.ArgumentParser(description='双摆数据可视化')
    parser.add_argument('data_file', help='数据文件路径')
    parser.add_argument('-o', '--output', default='pendulum_plot.png', 
                       help='输出文件名 (默认: pendulum_plot.png)')
    parser.add_argument('-a', '--animate', action='store_true', 
                       help='创建动画而不是静态图')
    parser.add_argument('--show', action='store_true', 
                       help='显示图像而不保存')
    
    args = parser.parse_args()
    
    print("双摆数据可视化工具")
    print("==================")
    print(f"数据文件: {args.data_file}")
    print(f"输出文件: {args.output}")
    print(f"模式: {'动画' if args.animate else '静态图'}")
    
    # 读取数据
    data, config_info = read_pendulum_data(args.data_file)
    print(f"数据点数: {len(data)}")
    
    if len(data) == 0:
        print("错误: 数据文件为空")
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
