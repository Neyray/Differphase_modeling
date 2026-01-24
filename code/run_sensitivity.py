import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.integrate import odeint
import pandas as pd
import os

# 导入你现有的核心模型和参数对象
# 注意：我们直接导入 model_core 中的 p 对象，以便动态修改参数
from model_core import model_differphase, model_monoculture, p 
from utils import set_style, save_fig

def run_sensitivity_analysis():
    set_style()
    print("🚀 开始灵敏度分析 (Sensitivity Analysis)...")
    
    # 建立保存路径
    current_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.dirname(current_dir)
    data_dir = os.path.join(root_dir, 'data')
    if not os.path.exists(data_dir): os.makedirs(data_dir)

    # 初始条件
    y0_dol = [1e7, 0, 0, 0]
    y0_mono = [1e7, 0]
    




    
    # ==========================================
    # 分析 1: 回补率 (k_rev) 的鲁棒性扫描
    # 目的: 找到干细胞维持的“生死线”
    # ==========================================
    print("正在进行分析 1: 回补率扫描...")
    
    k_rev_values = np.linspace(0.0, 0.10, 50) # 从 0 到 0.1 扫描 50 个点
    stem_counts_48h = []
    yield_dol_48h = []

    # 原始参数备份
    original_q_rubber = p.q_rubber_dol

    for k in k_rev_values:
        # 运行模型
        sol = odeint(model_differphase, y0_dol, p.t_span, args=(k,))
        stem_counts_48h.append(sol[-1, 0]) # 记录 48h 干细胞数
        yield_dol_48h.append(sol[-1, 3])   # 记录 48h 产量



    # --- 绘图 1: 回补率对稳定性的影响 ---（图四）
    fig1, ax1 = plt.subplots(figsize=(8, 6))
    
    # 绘制干细胞数量曲线
    ax1.plot(k_rev_values, stem_counts_48h, color='#2ecc71', linewidth=3, label='干细胞数量 (48h)')
    ax1.axhline(y=1e6, color='gray', linestyle='--', alpha=0.7, label='生存阈值 (1e6)')
    
    # 标注现有方案的位置
    ax1.scatter([0.05], [stem_counts_48h[np.abs(k_rev_values - 0.05).argmin()]], 
                color='red', s=100, zorder=5, label='当前方案 (k=0.05)')

    ax1.set_yscale('log')
    ax1.set_xlabel('回补率 $k_{rev}$')
    ax1.set_ylabel('48h 干细胞数量 (Log Scale)')
    ax1.set_title('系统稳定性分析：回补率的临界阈值')
    ax1.legend()
    ax1.grid(True, which="both", ls="-", alpha=0.2)
    
    save_fig(fig1, 'sensitivity_k_rev_stability.png')








    # ==========================================
    # 分析 2: 生产效率优势 (Efficiency Ratio) 扫描
    # 目的: 证明即使 DOL 优势不明显 (1.2倍)，依然优于单菌
    # ==========================================
    print("正在进行分析 2: 产量优势比扫描...")
    
    # 定义单菌产量作为基准
    sol_mono = odeint(model_monoculture, y0_mono, p.t_span)
    final_yield_mono = sol_mono[-1, 1]

    # 扫描不同的优势倍数：从 1.0 (无优势) 到 2.0 (2倍优势)
    ratios = np.linspace(1.0, 2.0, 20)
    improvements = []

    for r in ratios:
        # 动态修改 DOL 的产胶速率： q_dol = r * q_mono
        p.q_rubber_dol = r * p.q_rubber_mono
        
        # 运行 DOL 模型 (使用基准 k_rev = 0.05)
        sol_dol = odeint(model_differphase, y0_dol, p.t_span, args=(0.05,))
        final_yield_dol = sol_dol[-1, 3]
        
        # 计算提升百分比
        imp = ((final_yield_dol - final_yield_mono) / final_yield_mono) * 100
        improvements.append(imp)

    # 恢复原始参数
    p.q_rubber_dol = original_q_rubber



    # --- 绘图 2: 提升比例 vs 效率倍数 ---（图五）
    fig2, ax2 = plt.subplots(figsize=(8, 6))
    ax2.plot(ratios, improvements, color='#e74c3c', linewidth=3)
    
    # 填充正收益区域
    ax2.fill_between(ratios, 0, improvements, where=(np.array(improvements)>0), 
                     color='#e74c3c', alpha=0.1)
    
    # 标注关键点
    ax2.axvline(x=1.5, color='gray', linestyle='--', label='当前假设 (1.5倍)')
    ax2.axhline(y=0, color='black', linewidth=1)
    
    ax2.set_xlabel('DOL / 单菌 单细胞产胶效率比 ($q_{ratio}$)')
    ax2.set_ylabel('DOL 总产量提升百分比 (%)')
    ax2.set_title('鲁棒性验证：核心结论不依赖于激进假设')
    ax2.legend()
    
    save_fig(fig2, 'sensitivity_yield_ratio.png')







    # ==========================================
    # 分析 3: 双参数热图 (Heatmap)
    # 目的: 全局视角，k_rev (回补) vs k_diff (分化)
    # ==========================================
    print("正在进行分析 3: 双参数热图扫描...")
    
    # 定义网格
    rev_range = np.linspace(0.01, 0.10, 20)  # y轴：回补率
    diff_range = np.linspace(0.005, 0.025, 20) # x轴：分化率
    
    yield_matrix = np.zeros((len(rev_range), len(diff_range)))

    # 原始 k_diff 备份
    original_k_diff = p.k_diff

    for i, k_rev_val in enumerate(rev_range):
        for j, k_diff_val in enumerate(diff_range):
            # 动态修改参数
            p.k_diff = k_diff_val
            
            # 运行
            sol = odeint(model_differphase, y0_dol, p.t_span, args=(k_rev_val,))
            
            # 记录产量 (如果干细胞死绝了，产量视为0或惩罚，这里直接取产量即可)
            # 额外逻辑：如果 Stem < 1000，视为系统崩溃，标记为 NaN 以便绘图区分
            if sol[-1, 0] < 1000:
                yield_matrix[i, j] = np.nan
            else:
                yield_matrix[i, j] = sol[-1, 3]

    # 恢复参数
    p.k_diff = original_k_diff



    # --- 绘图 3: 热图 ---（图三）
    fig3, ax3 = plt.subplots(figsize=(10, 8))
    
    # 使用 DataFrame 方便绘图
    df_heatmap = pd.DataFrame(yield_matrix, index=np.round(rev_range, 3), columns=np.round(diff_range, 3))
    
    # 绘制热图 (颜色越红产量越高，灰色代表崩溃)
    sns.heatmap(df_heatmap, cmap='YlOrRd', ax=ax3, cbar_kws={'label': '最终产量 (Units)'})
    
    # 反转Y轴让坐标原点在左下角
    ax3.invert_yaxis()
    
    ax3.set_xlabel('分化速率 $k_{diff}$')
    ax3.set_ylabel('回补速率 $k_{rev}$')
    ax3.set_title('参数空间全景图：寻找最佳工作区')
    
    save_fig(fig3, 'sensitivity_heatmap.png')

    print("✅ 所有灵敏度分析已完成，图片保存在 figures/ 目录。")

if __name__ == "__main__":
    run_sensitivity_analysis()