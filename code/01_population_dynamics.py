import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
from configs import ModelParams
from utils import set_style, save_fig

# 初始化
set_style()
params = ModelParams()

def differphase_model(y, t, k_rev_val):
    """
    y: [Stem, Buffer, Producer, Rubber_Yield]
    k_rev_val: 当前的回补率 (Reversion Rate)
    """
    N_S, N_B, N_P, Rubber = y
    Total_N = N_S + N_B + N_P
    
    # Logistic 生长抑制项
    limit = 1 - (Total_N / params.K)
    if limit < 0: limit = 0

    # --- 微分方程组 (Based on A Group Logic) ---
    
    # 1. 干细胞 (S)
    # 增长: 自我复制
    # 流失: 不对称分裂产生Buffer (此处简化为分裂后一个S一个B，或者S转为B)
    # 回补: Buffer 在特定条件下变回 S
    dN_S = params.mu_stem * N_S * limit - params.k_diff * N_S + k_rev_val * N_B
    
    # 2. 缓冲细胞 (B - Buffer/Progenitor)
    # 来源: 干细胞分化
    # 去向: 成熟为生产细胞 (P) 或 回补为干细胞 (S)
    # 假设 Buffer 也有一定分裂能力，但较弱（此处忽略其分裂，专注分化逻辑）
    k_mature = 0.02 # Buffer成熟为Producer的速率
    dN_B = params.k_diff * N_S - k_mature * N_B - k_rev_val * N_B
    
    # 3. 生产细胞 (P - Rubber Producers)
    # 来源: Buffer成熟
    # 生长: 自身分裂 (带代谢负担)
    dN_P = k_mature * N_B + params.mu_prod * N_P * limit
    
    # 4. 橡胶产量 (Yield)
    # 只有 P 细胞生产
    dRubber = params.q_rubber * N_P
    
    return [dN_S, dN_B, dN_P, dRubber]

# --- 执行模拟 ---
def run_simulation():
    # 初始状态: 100个干细胞开始
    y0 = [100, 0, 0, 0] 
    
    # 场景对比：有回补系统 vs 无回补系统
    # High Reversion (Project Design)
    sol_high = odeint(differphase_model, y0, params.t_span, args=(params.k_reversion_base,))
    
    # No Reversion (Control Group)
    sol_zero = odeint(differphase_model, y0, params.t_span, args=(0.0,))

    # --- 绘图 1: 细胞种群动态 ---
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # 绘制有回补系统的曲线
    ax.plot(params.t_span/60, sol_high[:, 0], label='干细胞 (Stem)', color='#2ecc71', linewidth=2.5)
    ax.plot(params.t_span/60, sol_high[:, 2], label='生产细胞 (Producer)', color='#e74c3c', linewidth=2.5)
    ax.plot(params.t_span/60, sol_high[:, 1], label='缓冲细胞 (Buffer)', color='#f1c40f', linestyle='--')
    
    ax.set_title('Differphase系统种群动态模拟 (Population Dynamics)', fontsize=14, fontweight='bold')
    ax.set_xlabel('时间 (Hours)')
    ax.set_ylabel('细胞数量 (Cells)')
    ax.set_yscale('log') # 对数坐标看数量级差异
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    save_fig(fig, '01_population_dynamics.png')
    
    # --- 绘图 2: 干细胞池稳定性对比 ---
    fig2, ax2 = plt.subplots(figsize=(8, 5))
    ax2.plot(params.t_span/60, sol_high[:, 0], label='Differphase (有回补)', color='blue')
    ax2.plot(params.t_span/60, sol_zero[:, 0], label='Control (无回补)', color='gray', linestyle='--')
    
    ax2.set_title('回补系统对干细胞池稳定性的影响', fontsize=14)
    ax2.set_xlabel('时间 (Hours)')
    ax2.set_ylabel('干细胞数量')
    ax2.legend()
    
    save_fig(fig2, '02_stem_stability.png')

if __name__ == "__main__":
    run_simulation()