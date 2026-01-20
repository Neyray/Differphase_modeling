"""
Differphase项目参数配置文件
包含所有生物学参数和模拟设置

参数来源标注：
[DOC] - 来自立项文档实验数据
[LIT] - 来自文献查询
[EST] - 估计值，需湿实验测定
"""

import numpy as np

class ModelParams:
    """模型参数类"""
    
    # ==================== 基础生长参数 ====================
    
    # [DOC] 干细胞倍增时间 35min
    # 生长率 μ = ln(2) / 倍增时间
    mu_stem = np.log(2) / 35.0  # min^-1
    
    # [DOC] 普通大肠杆菌倍增时间 29min
    mu_wild = np.log(2) / 29.0  # min^-1
    
    # [EST] 代谢负担因子
    # 文档提到："额外的复杂代谢通路会对宿主细胞带来很大的代谢负担"
    # 生产菌因表达多酶系统，生长率下降
    # 0.7表示生长率降至野生型的70%
    burden_factor = 0.7
    mu_prod = mu_wild * burden_factor
    
    # 传统单菌的代谢负担更重（承担所有酶系统）
    heavy_burden_factor = 0.5
    mu_mono = mu_wild * heavy_burden_factor
    
    # ==================== 环境参数 ====================
    
    # [LIT] 大肠杆菌培养的环境承载力
    # 基于OD600 ~ 1.0 对应约10^9 cells/mL
    K = 1e9  # cells
    
    # ==================== 细胞分化参数 ====================
    
    # [EST] 分化率 (Stem -> Buffer)
    # 基于不对称分裂假设：每次分裂产生1个干细胞 + 1个缓冲细胞
    # 简化为转化速率，设为干细胞生长率的一半
    k_diff = 0.5 * mu_stem  # min^-1
    
    # [EST] 缓冲细胞成熟率 (Buffer -> Producer)
    # 文档未给出具体数据，估计成熟过程需约50分钟
    k_mature = np.log(2) / 50.0  # min^-1
    
    # ==================== 回补系统参数 ====================
    
    # [EST] 基础回补率 (Buffer -> Stem)
    # 这是项目的核心参数：光控/c-di-GMP调节的去分化
    # 文档提到FleQ和Light-on系统，但未给出定量数据
    # 设为可调参数，用于灵敏度分析
    k_reversion_base = 0.05  # min^-1
    
    # 不同光照强度下的回补率（用于后续扩展）
    k_reversion_high_light = 0.10   # 强光照
    k_reversion_low_light = 0.02    # 弱光照
    k_reversion_no_light = 0.0      # 无光照（对照组）
    
    # ==================== 生产参数 ====================
    
    # [EST] 单个细胞的橡胶生产速率
    # 需要根据Imperial College 2024的数据或湿实验测定
    # 此处为占位值
    q_rubber = 1e-4  # g/cell/min (arbitrary units)
    
    # ==================== 模拟时间设置 ====================
    
    # 默认模拟24小时（以分钟为单位）
    t_span_24h = np.linspace(0, 24*60, 1000)  # 1000个时间点
    
    # 长时间模拟48小时（用于产量对比）
    t_span_48h = np.linspace(0, 48*60, 1000)
    
    # 短时间模拟6小时（用于快速测试）
    t_span_6h = np.linspace(0, 6*60, 500)
    
    # 默认使用24小时
    t_span = t_span_24h
    
    # ==================== 初始条件 ====================
    
    # 初始干细胞数量
    N_S_init = 100
    
    # 初始缓冲细胞数量
    N_B_init = 0
    
    # 初始生产细胞数量
    N_P_init = 0
    
    # 初始橡胶产量
    Rubber_init = 0
    
    # 组合为初始状态向量
    y0 = [N_S_init, N_B_init, N_P_init, Rubber_init]
    
    # ==================== 灵敏度分析设置 ====================
    
    # 回补率扫描范围 (0% - 20%)
    reversion_scan_min = 0.0
    reversion_scan_max = 0.2
    reversion_scan_points = 20
    
    # 代谢负担因子扫描范围
    burden_scan_min = 0.3
    burden_scan_max = 0.9
    burden_scan_points = 15
    
    # ==================== 物理常数 ====================
    
    # 阿伏伽德罗常数（如果需要分子数计算）
    N_A = 6.022e23  # mol^-1
    
    # 细胞体积（大肠杆菌平均值）
    V_cell = 1e-15  # L (约1 μm^3)
    
    # ==================== 文献参考值 ====================
    
    # 以下为从文献中可能获取的参考数据
    # [LIT] c-di-GMP浓度范围（从文献Inducible asymmetric cell division...）
    cdGMP_high = 10.0   # μM (高c-di-GMP，分化细胞)
    cdGMP_low = 1.0     # μM (低c-di-GMP，干细胞)
    
    # [LIT] YhjH酶的催化效率（假设值，需查文献）
    k_cat_YhjH = 1.0    # s^-1
    
    # ==================== 模型验证阈值 ====================
    
    # 干细胞池最低阈值（低于此值认为系统不稳定）
    stem_threshold_min = 0.10  # 10%
    
    # 干细胞池理想范围
    stem_threshold_ideal = 0.20  # 20%
    
    # 产量提升最低要求（相比单菌）
    yield_improvement_min = 1.20  # 提升20%
    
    # ==================== 绘图参数 ====================
    
    # 颜色方案（基于色彩心理学）
    color_stem = '#2ecc71'      # 绿色 - 生命力（干细胞）
    color_buffer = '#f1c40f'    # 黄色 - 过渡（缓冲细胞）
    color_producer = '#e74c3c'  # 红色 - 活跃（生产细胞）
    color_control = 'gray'      # 灰色 - 对照组
    color_highlight = '#3498db' # 蓝色 - 强调
    
    # 线条宽度
    linewidth_main = 2.5
    linewidth_secondary = 2.0
    linewidth_dashed = 1.5
    
    # 图片分辨率
    dpi = 300
    
    # 图片大小（英寸）
    figsize_default = (10, 6)
    figsize_comparison = (8, 5)
    figsize_bar = (7, 6)
    
    # ==================== 调试开关 ====================
    
    # 是否打印详细日志
    verbose = True
    
    # 是否保存中间结果
    save_intermediate = False
    
    # ==================== 帮助函数 ====================
    
    @classmethod
    def get_parameter_summary(cls):
        """返回参数摘要字符串"""
        summary = f"""
        ========================================
        Differphase 模型参数摘要
        ========================================
        
        1. 生长参数
           干细胞生长率:     {cls.mu_stem:.4f} min^-1 (倍增时间 35min)
           生产菌生长率:     {cls.mu_prod:.4f} min^-1 (考虑代谢负担)
           单菌生长率:       {cls.mu_mono:.4f} min^-1 (重代谢负担)
        
        2. 分化参数
           分化率:          {cls.k_diff:.4f} min^-1
           成熟率:          {cls.k_mature:.4f} min^-1
           回补率:          {cls.k_reversion_base:.4f} min^-1
        
        3. 环境参数
           承载力:          {cls.K:.2e} cells
           
        4. 生产参数
           单细胞产胶速率:  {cls.q_rubber:.2e} g/cell/min
        
        5. 初始条件
           初始干细胞:      {cls.N_S_init} cells
        
        ========================================
        """
        return summary
    
    @classmethod
    def validate_parameters(cls):
        """验证参数合理性"""
        issues = []
        
        # 检查生长率
        if cls.mu_stem <= 0 or cls.mu_prod <= 0:
            issues.append("⚠️ 生长率必须为正值")
        
        # 检查代谢负担
        if cls.burden_factor <= 0 or cls.burden_factor > 1:
            issues.append("⚠️ 代谢负担因子应在 (0, 1] 区间")
        
        # 检查回补率
        if cls.k_reversion_base < 0:
            issues.append("⚠️ 回补率不能为负")
        
        # 检查承载力
        if cls.K <= 0:
            issues.append("⚠️ 承载力必须为正值")
        
        if issues:
            print("\n".join(issues))
            return False
        else:
            print("✅ 所有参数验证通过")
            return True

# 使用示例
if __name__ == "__main__":
    params = ModelParams()
    
    # 打印参数摘要
    print(params.get_parameter_summary())
    
    # 验证参数
    params.validate_parameters()