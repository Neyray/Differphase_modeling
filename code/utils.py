"""
Differphase项目工具函数库
提供绘图、文件管理、数据处理等通用功能
"""

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os
import platform
import sys
from datetime import datetime

# ==================== 绘图设置 ====================

def set_style():
    """
    设置科研级绘图风格，支持中文显示
    
    解决问题：
    - Matplotlib默认不显示中文
    - 负号显示为方块
    """
    # 使用seaborn的科研风格
    sns.set_theme(style="ticks", context="paper")
    
    # 字体设置（防止中文乱码）
    system_name = platform.system()
    
    if system_name == "Windows":
        # Windows系统使用SimHei（黑体）
        plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei']
    elif system_name == "Darwin":  # macOS
        # Mac系统使用Arial Unicode MS
        plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'PingFang SC']
    else:  # Linux
        # Linux系统使用WenQuanYi
        plt.rcParams['font.sans-serif'] = ['WenQuanYi Zen Hei', 'Droid Sans Fallback']
    
    # 解决负号显示问题
    plt.rcParams['axes.unicode_minus'] = False
    
    # 字体大小
    plt.rcParams['font.size'] = 12
    plt.rcParams['axes.labelsize'] = 12
    plt.rcParams['axes.titlesize'] = 14
    plt.rcParams['xtick.labelsize'] = 10
    plt.rcParams['ytick.labelsize'] = 10
    plt.rcParams['legend.fontsize'] = 11
    
    # 图表边框
    plt.rcParams['axes.linewidth'] = 1.5
    plt.rcParams['xtick.major.width'] = 1.5
    plt.rcParams['ytick.major.width'] = 1.5
    
    # 网格线
    plt.rcParams['grid.alpha'] = 0.3
    plt.rcParams['grid.linestyle'] = '--'
    
    print("✅ 绘图风格已设置（支持中文）")

def test_chinese_font():
    """测试中文字体是否正常显示"""
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.text(0.5, 0.5, '中文测试 Test 123', 
            ha='center', va='center', fontsize=16)
    ax.set_title('字体测试')
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    
    save_fig(fig, 'font_test.png')
    plt.close()
    print("✅ 字体测试完成，请检查 figures/font_test.png")

# ==================== 文件管理 ====================

def ensure_dir(directory):
    """
    确保目录存在，不存在则创建
    
    Args:
        directory (str): 目录路径
    """
    if not os.path.exists(directory):
        os.makedirs(directory)
        print(f"📁 创建目录: {directory}")

def save_fig(fig, filename, dpi=300, tight=True):
    """
    保存图片到figures目录
    
    Args:
        fig: matplotlib figure对象
        filename (str): 文件名（包含扩展名）
        dpi (int): 分辨率，默认300（适合论文）
        tight (bool): 是否使用tight_layout
    """
    # 确保figures目录存在
    figures_dir = '../figures'
    ensure_dir(figures_dir)
    
    # 构建完整路径
    path = os.path.join(figures_dir, filename)
    
    # 保存图片
    if tight:
        fig.savefig(path, dpi=dpi, bbox_inches='tight')
    else:
        fig.savefig(path, dpi=dpi)
    
    print(f"✅ 图片已保存: {path} (DPI={dpi})")

def save_data(data, filename, fmt='%.6e'):
    """
    保存数值数据到data目录
    
    Args:
        data: numpy数组或列表
        filename (str): 文件名
        fmt (str): 数据格式
    """
    data_dir = '../data'
    ensure_dir(data_dir)
    
    path = os.path.join(data_dir, filename)
    np.savetxt(path, data, fmt=fmt, delimiter=',')
    
    print(f"💾 数据已保存: {path}")

def load_data(filename):
    """
    从data目录加载数据
    
    Args:
        filename (str): 文件名
        
    Returns:
        numpy数组
    """
    path = os.path.join('../data', filename)
    
    if not os.path.exists(path):
        print(f"❌ 文件不存在: {path}")
        return None
    
    data = np.loadtxt(path, delimiter=',')
    print(f"📂 数据已加载: {path}")
    return data

# ==================== 数据处理 ====================

def calculate_relative_change(value_new, value_old):
    """
    计算相对变化百分比
    
    Args:
        value_new: 新值
        value_old: 旧值（基准）
        
    Returns:
        float: 变化百分比
    """
    if value_old == 0:
        return float('inf')
    
    return ((value_new - value_old) / value_old) * 100

def find_steady_state(time_series, value_series, threshold=0.01):
    """
    寻找稳态时间点
    
    Args:
        time_series: 时间数组
        value_series: 数值数组
        threshold: 变化率阈值（默认1%）
        
    Returns:
        float: 达到稳态的时间
    """
    # 计算变化率
    rate_of_change = np.abs(np.diff(value_series) / value_series[:-1])
    
    # 找到第一个变化率小于阈值的点
    steady_indices = np.where(rate_of_change < threshold)[0]
    
    if len(steady_indices) > 0:
        steady_time = time_series[steady_indices[0]]
        return steady_time
    else:
        return None

# ==================== 分析函数 ====================

def calculate_doubling_time(growth_rate):
    """
    从生长率计算倍增时间
    
    Args:
        growth_rate (float): 生长率 μ (min^-1)
        
    Returns:
        float: 倍增时间（分钟）
    """
    return np.log(2) / growth_rate

def calculate_growth_rate(doubling_time):
    """
    从倍增时间计算生长率
    
    Args:
        doubling_time (float): 倍增时间（分钟）
        
    Returns:
        float: 生长率 μ (min^-1)
    """
    return np.log(2) / doubling_time

def logistic_growth(N0, mu, K, t):
    """
    Logistic生长方程解析解
    
    Args:
        N0: 初始数量
        mu: 生长率
        K: 承载力
        t: 时间
        
    Returns:
        N(t): t时刻的数量
    """
    return K / (1 + (K - N0) / N0 * np.exp(-mu * t))

# ==================== 可视化增强 ====================

def add_annotation(ax, x, y, text, color='red'):
    """
    在图上添加注释
    
    Args:
        ax: matplotlib axes对象
        x, y: 注释位置
        text: 注释文本
        color: 颜色
    """
    ax.annotate(text, xy=(x, y), xytext=(x, y*1.1),
                arrowprops=dict(arrowstyle='->', color=color),
                fontsize=12, color=color, fontweight='bold')

def add_shaded_region(ax, x_start, x_end, color='gray', alpha=0.2, label=None):
    """
    添加阴影区域（用于标注时间段）
    
    Args:
        ax: matplotlib axes对象
        x_start, x_end: 区域范围
        color: 颜色
        alpha: 透明度
        label: 标签
    """
    ax.axvspan(x_start, x_end, color=color, alpha=alpha, label=label)

def create_comparison_table(data_dict, save_path='../results/comparison_table.txt'):
    """
    创建对比表格
    
    Args:
        data_dict (dict): 数据字典，格式 {'名称': 值}
        save_path (str): 保存路径
    """
    ensure_dir(os.path.dirname(save_path))
    
    with open(save_path, 'w', encoding='utf-8') as f:
        f.write("=" * 60 + "\n")
        f.write("对比表格\n")
        f.write("=" * 60 + "\n\n")
        
        for key, value in data_dict.items():
            f.write(f"{key:30s}: {value}\n")
        
        f.write("\n" + "=" * 60 + "\n")
    
    print(f"📊 对比表格已保存: {save_path}")

# ==================== 日志记录 ====================

def log_message(message, level='INFO'):
    """
    记录日志消息
    
    Args:
        message (str): 消息内容
        level (str): 日志级别 (INFO/WARNING/ERROR)
    """
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # 颜色编码（仅在终端支持时有效）
    colors = {
        'INFO': '\033[92m',     # 绿色
        'WARNING': '\033[93m',  # 黄色
        'ERROR': '\033[91m',    # 红色
        'RESET': '\033[0m'
    }
    
    color = colors.get(level, colors['RESET'])
    reset = colors['RESET']
    
    log_msg = f"{color}[{level}] {timestamp}: {message}{reset}"
    print(log_msg)
    
    # 同时写入日志文件
    log_dir = '../results'
    ensure_dir(log_dir)
    log_file = os.path.join(log_dir, 'simulation.log')
    
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(f"[{level}] {timestamp}: {message}\n")

# ==================== 进度显示 ====================

def progress_bar(current, total, bar_length=50):
    """
    显示进度条
    
    Args:
        current (int): 当前进度
        total (int): 总数
        bar_length (int): 进度条长度
    """
    percent = float(current) / total
    arrow = '=' * int(round(percent * bar_length) - 1) + '>'
    spaces = ' ' * (bar_length - len(arrow))
    
    sys.stdout.write(f"\r[{arrow}{spaces}] {int(percent * 100)}%")
    sys.stdout.flush()
    
    if current == total:
        print()  # 完成后换行

# ==================== 参数验证 ====================

def validate_ode_solution(sol, y0):
    """
    验证ODE求解结果的合理性
    
    Args:
        sol: ODE求解结果
        y0: 初始条件
        
    Returns:
        bool: 是否通过验证
    """
    issues = []
    
    # 检查是否有NaN或Inf
    if np.any(np.isnan(sol)) or np.any(np.isinf(sol)):
        issues.append("⚠️ 解中包含NaN或Inf值")
    
    # 检查是否有负值（细胞数量不能为负）
    if np.any(sol < 0):
        issues.append("⚠️ 解中包含负值（物理上不合理）")
    
    # 检查初始条件是否匹配
    if not np.allclose(sol[0, :len(y0)], y0, rtol=1e-3):
        issues.append("⚠️ 初始条件不匹配")
    
    if issues:
        for issue in issues:
            log_message(issue, 'WARNING')
        return False
    else:
        log_message("ODE求解结果验证通过", 'INFO')
        return True

# ==================== 快速绘图函数 ====================

def quick_plot(x, y, xlabel='x', ylabel='y', title='Plot', 
               filename=None, color='blue'):
    """
    快速绘制简单曲线图
    
    Args:
        x, y: 数据
        xlabel, ylabel, title: 标签和标题
        filename: 保存文件名（可选）
        color: 线条颜色
    """
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(x, y, color=color, linewidth=2)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title, fontweight='bold')
    ax.grid(True, alpha=0.3)
    
    if filename:
        save_fig(fig, filename)
    else:
        plt.show()
    
    plt.close()

# ==================== 主函数（测试用） ====================

if __name__ == "__main__":
    print("=" * 60)
    print("工具函数库测试")
    print("=" * 60)
    
    # 测试1：设置绘图风格
    print("\n1. 测试绘图风格设置...")
    set_style()
    
    # 测试2：测试中文字体
    print("\n2. 测试中文字体...")
    test_chinese_font()
    
    # 测试3：测试目录创建
    print("\n3. 测试目录管理...")
    ensure_dir('../test_dir')
    
    # 测试4：测试数据保存和加载
    print("\n4. 测试数据保存和加载...")
    test_data = np.random.rand(10, 3)
    save_data(test_data, 'test_data.csv')
    loaded_data = load_data('test_data.csv')
    print(f"   数据形状: {loaded_data.shape}")
    
    # 测试5：测试日志
    print("\n5. 测试日志记录...")
    log_message("这是一条INFO消息", 'INFO')
    log_message("这是一条WARNING消息", 'WARNING')
    log_message("这是一条ERROR消息", 'ERROR')
    
    # 测试6：测试进度条
    print("\n6. 测试进度条...")
    import time
    for i in range(101):
        progress_bar(i, 100)
        time.sleep(0.01)
    
    print("\n" + "=" * 60)
    print("✅ 所有测试完成！")
    print("=" * 60)