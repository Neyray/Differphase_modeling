import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
from configs import ModelParams
from model_core import model_differphase, model_monoculture
from utils import set_style, save_fig
import pandas as pd
import os

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
    
    # 合并为一个DataFrame
    df_yield = pd.DataFrame({
        'Time_hours': time_h,
        'DOL_total_cells': sol_dol[:, 0] + sol_dol[:, 1] + sol_dol[:, 2],
        'DOL_stem_cells': sol_dol[:, 0],
        'DOL_buffer_cells': sol_dol[:, 1],
        'DOL_producer_cells': sol_dol[:, 2],
        'DOL_yield': yield_dol,
        'Mono_cells': sol_mono[:, 0],
        'Mono_yield': yield_mono
    })
    
    # 保存CSV
    csv_path = os.path.join(data_dir, 'yield_comparison.csv')
    df_yield.to_csv(csv_path, index=False)
    print(f"✅ 数据已导出: {csv_path}")
    
    # 计算并保存关键指标
    final_dol = yield_dol[-1]
    final_mono = yield_mono[-1]
    increase = ((final_dol - final_mono) / final_mono) * 100
    
    summary = pd.DataFrame({
        '指标': ['DOL最终产量', '单菌最终产量', '产量提升百分比'],
        '数值': [final_dol, final_mono, f'{increase:.2f}%']
    })
    summary_path = os.path.join(data_dir, 'yield_summary.csv')
    summary.to_csv(summary_path, index=False)
    print(f"✅ 汇总指标已导出: {summary_path}")
    print(f"   产量提升: {increase:.1f}%")
    





    # === 绘图：产量累计曲线 ===
    fig, ax = plt.subplots(figsize=(10, 6))
    
    ax.plot(time_h, yield_dol, color='#e74c3c', linewidth=3, label='Differphase (DOL分工)')
    ax.plot(time_h, yield_mono, color='gray', linestyle='--', linewidth=2, label='传统单菌 (Monoculture)')
    
    # 填充颜色差异区域
    ax.fill_between(time_h, yield_dol, yield_mono, color='#e74c3c', alpha=0.1)
    
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