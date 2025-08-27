CXX = g++
CXXFLAGS = -std=c++11 -Wall -Wextra -O2
INCLUDES = -Iinclude
SRCDIR = src
OBJDIR = obj
SOURCES = $(wildcard $(SRCDIR)/*.cpp)
OBJECTS = $(SOURCES:$(SRCDIR)/%.cpp=$(OBJDIR)/%.o)
TARGET = double_pendulum

PYTHON_WRAPPER = ./.conda/bin/python

# 默认目标：编译、运行、生成图像
all: gcc run plot

# 编译目标：gcc
gcc: $(TARGET)

# 创建目标文件夹
$(OBJDIR):
	mkdir -p $(OBJDIR)

# 编译目标文件
$(OBJDIR)/%.o: $(SRCDIR)/%.cpp | $(OBJDIR)
	$(CXX) $(CXXFLAGS) $(INCLUDES) -c $< -o $@

# 链接生成可执行文件
$(TARGET): $(OBJECTS)
	$(CXX) $(CXXFLAGS) $(OBJECTS) -o $(TARGET)

# 运行目标：输出数据
run: $(TARGET)
	./$(TARGET) ./config/config pendulum_data.txt

# 清理所有生成的文件
clean:
	rm -rf $(OBJDIR) $(TARGET) *.bmp *.txt *.png *.gif

# Python静态可视化
plot: 
	$(PYTHON_WRAPPER) visualize.py pendulum_data.txt -o pendulum_plot.png

# Python动画
animate: 
	$(PYTHON_WRAPPER) visualize.py pendulum_data.txt -o pendulum_animation.gif -a

# 环境设置：创建并激活Python环境（如果需要）
setup:
	@echo "如果需要Python环境，请运行: ./setup_env.sh"

# 显示帮助
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
