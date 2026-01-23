import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
from configs import ModelParams
from model_core import model_differphase
from utils import set_style, save_fig
import pandas as pd
import os

def run():
    set_style()
    p = ModelParams()
    
    # 初始条件: 接种 10^7 个干细胞
    y0 = [1e7, 0, 0, 0]
    
    # === 模拟两种情况 ===
    # 1. 有回补 (Our Project): k_rev = 0.05
    sol_with_rev = odeint(model_differphase, y0, p.t_span, args=(p.k_rev_base,))
    
    # 2. 无回补 (Control): k_rev = 0
    sol_no_rev = odeint(model_differphase, y0, p.t_span, args=(0.0,))
    
    # === 导出数据到CSV ===
    # 构建data目录路径
    current_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.dirname(current_dir)
    data_dir = os.path.join(root_dir, 'data')
    
    # 确保目录存在
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    
    # 准备数据
    time_h = p.t_span / 60  # 转换为小时
    
    # DataFrame 1: 有回补系统
    df_with_rev = pd.DataFrame({
        'Time_hours': time_h,
        'Stem_cells': sol_with_rev[:, 0],
        'Buffer_cells': sol_with_rev[:, 1],
        'Producer_cells': sol_with_rev[:, 2],
        'Cumulative_yield': sol_with_rev[:, 3]
    })
    
    # DataFrame 2: 无回补系统
    df_no_rev = pd.DataFrame({
        'Time_hours': time_h,
        'Stem_cells': sol_no_rev[:, 0],
        'Buffer_cells': sol_no_rev[:, 1],
        'Producer_cells': sol_no_rev[:, 2],
        'Cumulative_yield': sol_no_rev[:, 3]
    })
    
    # 保存CSV
    df_with_rev.to_csv(os.path.join(data_dir, 'stability_with_reversion.csv'), index=False)
    df_no_rev.to_csv(os.path.join(data_dir, 'stability_no_reversion.csv'), index=False)
    
    print(f"✅ 数据已导出:")
    print(f"   - {os.path.join(data_dir, 'stability_with_reversion.csv')}")
    print(f"   - {os.path.join(data_dir, 'stability_no_reversion.csv')}")
    
    # === 绘图：细胞比例堆叠图 (展示种群动态) ===
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    
    # 左图：我们的系统 (有回补)
    ax1.stackplot(time_h, 
                  sol_with_rev[:, 0], sol_with_rev[:, 1], sol_with_rev[:, 2],
                  labels=['干细胞 (Stem)', '缓冲细胞 (Buffer)', '生产细胞 (Producer)'],
                  colors=['#2ecc71', '#f1c40f', '#e74c3c'], alpha=0.8)
    ax1.set_title('Differphase系统: 种群结构维持稳定', fontsize=14, fontweight='bold')
    ax1.set_xlabel('发酵时间 (Hours)')
    ax1.set_ylabel('细胞数量 (Cells)')
    ax1.legend(loc='upper left')
    
    # 右图：干细胞池枯竭对比 (核心论点)
    ax2.plot(time_h, sol_with_rev[:, 0], 'g-', linewidth=3, label='有回补 (Our Design)')
    ax2.plot(time_h, sol_no_rev[:, 0], 'k--', linewidth=2, label='无回补 (Control)')
    ax2.set_title('核心优势: 干细胞池防止枯竭', fontsize=14, fontweight='bold')
    ax2.set_xlabel('发酵时间 (Hours)')
    ax2.set_ylabel('干细胞数量 (Stem Cells)')
    ax2.set_yscale('log') # 关键：用对数坐标显示差异
    ax2.legend()
    
    plt.tight_layout()
    save_fig(fig, '01_stability_analysis.png')

if __name__ == "__main__":
    run()