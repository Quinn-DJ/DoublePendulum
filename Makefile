CXX = g++
CXXFLAGS = -std=c++11 -Wall -Wextra -O2
INCLUDES = -Iinclude
SRCDIR = src
OBJDIR = obj
SOURCES = $(wildcard $(SRCDIR)/*.cpp)
OBJECTS = $(SOURCES:$(SRCDIR)/%.cpp=$(OBJDIR)/%.o)
TARGET = double_pendulum

PYTHON_WRAPPER = ./.conda/bin/python

# Default target: build, run, and generate plots
all: gcc run plot

# Build target: gcc
gcc: $(TARGET)

# Create object directory
$(OBJDIR):
	mkdir -p $(OBJDIR)

# Compile object files
$(OBJDIR)/%.o: $(SRCDIR)/%.cpp | $(OBJDIR)
	$(CXX) $(CXXFLAGS) $(INCLUDES) -c $< -o $@

# Link to create executable
$(TARGET): $(OBJECTS)
	$(CXX) $(CXXFLAGS) $(OBJECTS) -o $(TARGET)

# Run target: output data
run: $(TARGET)
	./$(TARGET) ./config/config pendulum_data.txt

# Clean all generated files
clean:
	rm -rf $(OBJDIR) $(TARGET) *.bmp *.txt *.png *.gif

# Python static visualization
plot: 
	$(PYTHON_WRAPPER) visualize.py pendulum_data.txt -o pendulum_plot.png

# Python animation
animate: 
	$(PYTHON_WRAPPER) visualize.py pendulum_data.txt -o pendulum_animation.gif -a

# Environment setup: create and activate Python environment (if needed)
setup:
	@echo "如果需要Python环境，请运行: ./setup_env.sh"

# Help target: display available make targets
help:
	@echo "可用的目标："
	@echo "  all         - 编译程序 + 运行模拟 + 生成静态图"
	@echo "  gcc         - 编译程序"
	@echo "  run         - 运行模拟输出数据"
	@echo "  plot        - Python静态可视化"
	@echo "  animate     - Python动画"
	@echo "  clean       - 清理所有生成的文件（包括conda环境）"
	@echo "  setup       - 设置Python环境"
	@echo "  help        - 显示此帮助信息"

.PHONY: all gcc run plot animate clean setup help
