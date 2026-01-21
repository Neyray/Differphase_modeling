from configs import ModelParams

# 实例化参数
p = ModelParams()

def model_differphase(y, t, k_rev_dynamic):
    """
    A组 Differphase 系统的三态动力学模型
    y: [Stem, Buffer, Producer, Yield]
    k_rev_dynamic: 动态传入的回补率
    """
    N_S, N_B, N_P, P_yield = y
    N_Total = N_S + N_B + N_P
    
    # Logistic 生长限制因子 (1 - N/K)
    limit = 1 - (N_Total / p.K)
    if limit < 0: limit = 0

    # --- 微分方程组 ---
    
    # 1. 干细胞 (Stem): 生长 - 分化 + 回补
    dN_S = p.mu_stem * N_S * limit - p.k_diff * N_S + k_rev_dynamic * N_B
    
    # 2. 缓冲细胞 (Buffer): 来源分化 - 成熟流失 - 回补流失
    dN_B = p.k_diff * N_S - p.k_mature * N_B - k_rev_dynamic * N_B
    
    # 3. 生产细胞 (Producer): 来源成熟 + 自我生长 (带负担)
    dN_P = p.k_mature * N_B + p.mu_prod * N_P * limit
    
    # 4. 橡胶产量 (累计积分)
    dYield = p.q_rubber_dol * N_P
    
    return [dN_S, dN_B, dN_P, dYield]

def model_monoculture(y, t):
    """
    对照组: 传统单菌发酵模型
    y: [N_Mono, Yield]
    """
    N_M, P_yield = y
    
    # Logistic 限制
    limit = 1 - (N_M / p.K)
    if limit < 0: limit = 0
    
    # 1. 菌体生长 (高代谢负担，生长慢)
    dN_M = p.mu_mono * N_M * limit
    
    # 2. 产量 (低效率)
    dYield = p.q_rubber_mono * N_M
    
    return [dN_M, dYield]