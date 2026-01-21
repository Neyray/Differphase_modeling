import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
from configs import ModelParams
from model_core import model_differphase, model_monoculture
from utils import set_style, save_fig

def run():
    set_style()
    p = ModelParams()
    
    # 初始条件
    y0_dol = [1e7, 0, 0, 0] # Differphase: 接种干细胞
    y0_mono = [1e7, 0]      # Monoculture: 接种普通菌
    
    # === 运行模拟 ===
    # 1. DOL 系统
    sol_dol = odeint(model_differphase, y0_dol, p.t_span, args=(p.k_rev_base,))
    yield_dol = sol_dol[:, 3] # 第4列是产量
    
    # 2. 单菌系统
    sol_mono = odeint(model_monoculture, y0_mono, p.t_span)
    yield_mono = sol_mono[:, 1] # 第2列是产量
    
    # === 绘图：产量累计曲线 ===
    fig, ax = plt.subplots(figsize=(10, 6))
    
    time_h = p.t_span / 60
    ax.plot(time_h, yield_dol, color='#e74c3c', linewidth=3, label='Differphase (DOL分工)')
    ax.plot(time_h, yield_mono, color='gray', linestyle='--', linewidth=2, label='传统单菌 (Monoculture)')
    
    # 填充颜色差异区域
    ax.fill_between(time_h, yield_dol, yield_mono, color='#e74c3c', alpha=0.1)
    
    # 计算提升百分比
    final_dol = yield_dol[-1]
    final_mono = yield_mono[-1]
    increase = ((final_dol - final_mono) / final_mono) * 100
    
    # 在图上标注结论
    ax.text(30, final_dol * 0.8, 
            f'最终产量提升: {increase:.1f}%\n(Model Prediction)', 
            fontsize=14, color='#c0392b', fontweight='bold', 
            bbox=dict(facecolor='white', alpha=0.8, edgecolor='red'))

    ax.set_title('橡胶生产效率对比: 分工 vs 单菌', fontsize=16)
    ax.set_xlabel('发酵时间 (Hours)')
    ax.set_ylabel('累积橡胶产量 (Arbitrary Units)')
    ax.legend(fontsize=12)
    
    save_fig(fig, '02_yield_comparison.png')

if __name__ == "__main__":
    run()