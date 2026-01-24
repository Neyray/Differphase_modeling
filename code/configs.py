import numpy as np

class ModelParams:
    """
    Differphase 项目核心参数库
    核心逻辑：通过代谢分工(DOL)，降低单个细胞的代谢负担，从而提高总产量。
    """
    #时间设置
    t_total = 48 * 60  # 模拟 48 小时 (分钟)
    t_span = np.linspace(0, t_total, 1000) # 1000个时间采样点



    #基础生长参数
    # 干细胞 (Stem) 生长最快 (负担最小)
    # 来源: 文档提到 Stem 倍增时间 ~35min
    mu_stem = np.log(2) / 35.0  
    
    # 缓冲细胞 (Buffer) & 生产细胞 (Producer)
    # 来源: 文档提到普通细胞 ~29min (由于质粒负担，实际会慢)
    mu_prod = np.log(2) / 45.0  # 假设：生产细胞因合成橡胶，生长变慢
    
    # [关键对比] 传统单菌 (Monoculture)
    # 逻辑: 单菌要同时维持所有质粒和代谢通路，负担极重，生长最慢，且容易到达毒性阈值
    mu_mono = np.log(2) / 60.0  




    #系统参数
    K = 1e9  # 环境承载力 (最大细胞密度)
    



    #转化率参数
    # 干细胞 -> 缓冲细胞 (分化)
    k_diff = 0.01 
    
    # 缓冲细胞 -> 干细胞 (回补 - Reversion)
    # 这里的数值将在 run_stability.py 中被动态修改以测试灵敏度
    k_rev_base = 0.05 
    
    # 缓冲细胞 -> 生产细胞 (成熟)
    k_mature = 0.02




    #产量参数
    # 单位: g/cell/min (假设值，通过相对大小体现优势)
    q_rubber_dol = 1.2e-8  # DOL系统的生产效率 (专职生产)
    q_rubber_mono = 0.8e-8 # 单菌系统的生产效率 (受代谢干扰)