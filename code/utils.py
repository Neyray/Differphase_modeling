import matplotlib.pyplot as plt
import seaborn as sns
import os
import platform

def set_style():
    """设置科研绘图风格，支持中文"""
    sns.set_theme(style="whitegrid")
    
    system_name = platform.system()
    if system_name == "Windows":
        plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei']
    elif system_name == "Darwin": 
        plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']
    elif system_name == "Linux":
        plt.rcParams['font.sans-serif'] = ['WenQuanYi Zen Hei', 'Droid Sans Fallback']
    
    plt.rcParams['axes.unicode_minus'] = False
    plt.rcParams['font.size'] = 12

def save_fig(fig, filename):
    """
    保存图片到项目根目录的figures文件夹
    
    保存到 Differphase_Modeling/figures/
    """
    # 获取当前文件所在目录（code目录）
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 构建根目录路径（code的上一级）
    root_dir = os.path.dirname(current_dir)
    
    # 构建figures目录路径
    figures_dir = os.path.join(root_dir, 'figures')
    
    # 确保目录存在
    if not os.path.exists(figures_dir):
        os.makedirs(figures_dir)
    
    # 保存图片
    path = os.path.join(figures_dir, filename)
    fig.savefig(path, dpi=300, bbox_inches='tight')
    print(f"✅ 图片已保存至: {path}")