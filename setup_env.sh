#!/bin/bash
# 双摆项目环境管理脚本
# 功能：创建/激活虚拟环境，安装依赖，可选运行Python脚本

# 获取脚本所在目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONDA_ENV="${SCRIPT_DIR}/.conda"

echo "双摆项目环境管理"
echo "=================="

# 检查conda是否可用
if ! command -v conda &> /dev/null; then
    echo "错误: conda未找到，请先安装Miniconda或Anaconda"
    exit 1
fi

# 检查并创建环境
if [ ! -d "$CONDA_ENV" ]; then
    echo "本地conda环境不存在，正在创建..."
    echo "环境路径: $CONDA_ENV"
    
    # 创建新的conda环境
    source ~/miniconda3/bin/activate
    conda create --prefix "$CONDA_ENV" python=3.9 -y
    
    if [ $? -ne 0 ]; then
        echo "错误: 创建conda环境失败"
        exit 1
    fi
    
    echo "✓ 环境创建成功"
else
    echo "✓ 找到现有环境: $CONDA_ENV"
fi

# 激活环境
echo "正在激活环境..."
source ~/miniconda3/bin/activate
conda activate "$CONDA_ENV"

if [ $? -ne 0 ]; then
    echo "错误: 激活环境失败"
    exit 1
fi

echo "✓ 环境已激活"

# 检查并安装必要的包
echo "检查Python依赖..."
python -c "import matplotlib, numpy" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "安装必要的Python包..."
    conda install matplotlib numpy -y
    
    if [ $? -ne 0 ]; then
        echo "错误: 安装依赖失败"
        exit 1
    fi
    echo "✓ 依赖安装完成"
else
    echo "✓ 所有依赖已安装"
fi

# 显示环境信息
echo ""
echo "环境信息"
echo "========"
echo "Python路径: $(which python)"
echo "Python版本: $(python --version)"
echo "可用的包:"
python -c "
try:
    import matplotlib
    import numpy
    print(f'  matplotlib: {matplotlib.__version__}')
    print(f'  numpy: {numpy.__version__}')
except ImportError as e:
    print(f'  导入错误: {e}')
"

echo "环境准备完毕！"
