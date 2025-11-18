import re, yaml, difflib
import numpy as np
import matplotlib.pyplot as plt
from typing import List, Optional
from collections import defaultdict
from copy import deepcopy

class StaticMethodMeta(type):
    def __new__(cls, name, bases, namespace):
        for attr_name, attr_value in namespace.items():
            if callable(attr_value) and not attr_name.startswith('__'):
                namespace[attr_name] = staticmethod(attr_value)
        return super().__new__(cls, name, bases, namespace)

class tools(metaclass=StaticMethodMeta):
    def read_yml(filepath):
        with open(filepath, 'r') as f:
            content = f.read()
        return yaml.safe_load(content)
    
    def printdict(data:dict, indent:str=""):
        for k, v in data.items():
            if isinstance(v, (dict, defaultdict)):
                print(f"{indent}{k}:")
                tl.printdict(v, indent+"\t")
            elif isinstance(v, list):
                print(f"{indent}{k}({len(v)}):[")
                tl.printlist(v, indent+'\t')
                print(f"{indent}]")
            else:
                print(f"{indent}{k}:\t{v if v != None else None}")

    def printlist(l, indent:str=""):
        for i, c in enumerate(l):
            print(f"{indent}{i+1}.\t{c}")

    pd = printdict
    pl = printlist
    
    def execute_immediately(r:list):
        def wp(f):
            r.append(f())
        return wp
    execute = execute_immediately

    def find_most_similar_string(input_str: str, string_list: List[str], cutoff: float = 0.1) -> Optional[str]:
        """
        最相似的字符串，如果找不到相似度足够高的则返回None
        """
        if not string_list:return None
        matches = difflib.get_close_matches(input_str, string_list, n=1, cutoff=cutoff)
        return matches[0] if matches else None
    best_match = find_most_similar_string

    def get_nested_dict_v(d, keys):
        """
        递归查找多层字典
        """
        if len(keys) == 1:return d[keys[0]]
        else:return tl.get_nested_dict_v(d[keys[0]], keys[1:])
    gndv = get_nested_dict_v

    def update_nested_dict(d, keys, value):
        """
        递归更新多层字典
        """
        if len(keys) == 1:
            d[keys[0]] = value
        else:
            key = keys[0]
            if key not in d or not isinstance(d[key], dict):
                d[key] = {}
            tl.update_nested_dict(d[key], keys[1:], value)

tl = tools

class math(metaclass=StaticMethodMeta):

    def normal_non_crit_dice_expectation(d):
        return (1+d)/2
    nncde = normal_non_crit_dice_expectation

    def xmds_non_crit_dice_expectation(d):
        return (d+1)*(4*d-1)/(6*d)
    xncde = xmds_non_crit_dice_expectation
    
    def attribute_adjustment_value(attr:int):
        return ((np.asarray(attr) - 10) // 2).astype(int)
    attr_adj_v = attribute_adjustment_value

m = math


passive_skill_list = {
    'xmds': '凶蛮打手', 
    'buff': '3可重击增伤buff', 
    'jwqds':'巨武器大师', 
    'sxts':'属性提升',
    'fsjj':'法术狙击',
    'mfkx1':'魔法抗性1',
    'wlkx1':'物理抗性1',
    'hmkn':'毁灭狂怒',
}
active_skill_list = {
    'na':'普通攻击',
    'hmj': '轰鸣剑', 
    'zsz': '至圣斩', 
    'fyzsz': '反应至圣斩', 
    
}
Vulnerability_list = {
    'wet': '濡湿',
    'freeze': '冻僵',
    'oil': '火易伤',
    'physical': '物理',
    'Radiant': '光耀',
    'psychic': '心灵',
}

cast_types = {'Attack':'攻击骰', 'Saving':'豁免骰'}
Roll_status = {'Advantage':'优势', 'Disadvantage':'劣势', 'Neutral':'均势'}
attributes = {'STR':'力量', 'DEX':'敏捷', 'CON':'体质', 'INT':'智力', 'WIS':'感知', 'CHA':'魅力'}

class dice:
    def __init__(self, n, d) -> None:
        self.n = int(n)
        self.d = int(d)

class function_pack:
    def __init__(self, func, info) -> None:
        self.func = func
        self.info = info

fp = function_pack

def D_exp(params):
    self, foe, cast_type, rollstat, axis, metric = params['self'], params['enemy'], params['cast_type'], params['Roll_status'], params['axis'], params['metric']
    skill_active = lambda s:s in self['Passive_skill_group'][0]
    d = dice(*self['weapon_dice'][0].split('d'))
    print(d.n, d.d)
    D_p_normal = m.nncde(d.d)
    D_p_normal_buffed = m.nncde(d.d) + m.nncde(4) + m.nncde(4) + m.nncde(6)
    D_p_xmds = m.xncde(d.d)
    D_p_xmds_buffed = m.xncde(d.d) + m.xncde(4) + m.xncde(4) + m.xncde(6)
    print(D_p_normal)
    print(D_p_xmds)
    C = self['Crit_Bonus']
    D_p_unablecrit = m.attr_adj_v(self['Attribute'][self['Main_att_attr_physic']])
    B = foe['AC'] - self['Attack_Bonus']
    if skill_active('xmds'):
        if skill_active('buff'):D_p_ablecrit = D_p_xmds_buffed
        else:                   D_p_ablecrit = D_p_xmds
    else:
        if skill_active('buff'):D_p_ablecrit = D_p_normal_buffed
        else:                   D_p_ablecrit = D_p_normal
    if skill_active('jwqds'): 
        B += 5
        D_p_unablecrit += 10

    t = np.maximum(20-C-B, 0)
    hit_chance_special = (2 * (C + 1) + t) / 20
    hit_chance = ((C + 1) + t) / 20
    return D_p_ablecrit * hit_chance_special + D_p_unablecrit * hit_chance

def create_formula_function(cfg, func_Dp):
    """
    创建一个使用参数字典和坐标轴列表的公式函数
    Returns:
        一个函数 func(*l_axis)，该函数返回固定公式的结果
    """
    def func(*axis_values):
        """
        使用坐标轴参数计算固定公式
        Args:*axis_values: 坐标轴参数的值，数量与 l_axis 相同
        Returns:公式结果
        """
        # 检查参数数量是否匹配
        axis = cfg['axis']
        if len(axis_values) != len(axis):raise ValueError(f"期望 {len(axis)} 个坐标轴参数，但得到了 {len(axis_values)} 个")
        
        current_params = deepcopy(cfg)
        
        for i, axis_key in enumerate(axis):
            tl.update_nested_dict(current_params, axis_key.split('-'), axis_values[i])

        # 使用全部参数计算固定公式
        return func_Dp(current_params)
    
    return func


def AttackFunc(cfg:dict):
    """
    攻击骰
    Ph = ∑(k=20-Crit_Bonus->20)Pk
    Pn = ∑(k=(foe.Ac-Attack_Bonus)->20-Crit_Bonus-1)Pk
    D_exp = D_p_ablecrit * (Ph * 2 + Pn) + D_p_unablecrit * (Ph + Pn)
    """
    def gen_singlemetric():
        print(f'single metric mode')
        return create_formula_function(deepcopy(cfg), D_exp)
    
    if cfg['metric']:
        print(f'multi metric mode')
        m_k, m_v = list(metric.items())[0]
        assert len(metric) == 1 and len(m_v) > 1, f'metric size error({metric})'
        gen_multimetric(cfg)
    else:
        return gen_singlemetric()

def SavingFunc(cfg):pass

def factory(cfg):
    axa = tl.gndv(cfg, cfg['axis'][0].split('-'))
    info = {
        'title':'2D 曲线图', 
        'axis':{
            'axa':{
                'label':cfg['axis'][0], 
                'vals':np.arange(axa[0], axa[1] + 1),
            },
        }
    }
    if len(cfg['axis']) == 2: 
        axb = tl.gndv(cfg, cfg['axis'][1].split('-'))
        tl.update_nested_dict(info, ['axis', 'axb'], {
                'label':cfg['axis'][1], 
                'vals':np.arange(axb[0], axb[1] + 1),
        })
        info['title'] = '3D 曲面图'
    if cfg['cast_type'] == "Attack":
        return fp(AttackFunc(deepcopy(cfg)), info)
    else:
        SavingFunc(cfg)
    


def single_function_analysis(funcpack:fp):
    """单函数分析模式"""
    if not funcpack.func:
        print("错误: 没有找到可分析的函数")
        return
    
    func = funcpack.func
    coord_info = funcpack.info
    func_name = coord_info['title']
    print(f"=== 单函数分析: {func_name} ===")
    
    # 创建网格
    axis = coord_info['axis']
    if len(axis) == 1:
        F = func(axis['axa']['vals'])
        fig = plt.figure(figsize=(10, 8))
        ax = fig.add_subplot(111)  # 不需要 projection 参数
        A = axis['axa']['vals']
        F = func(A)

        # 绘制线图
        line = ax.plot(A, F, linewidth=2, color='blue', alpha=0.8)
        ax.set_xlabel(axis['axa']['label'])  # 使用你的 axis 字典
        ax.set_ylabel('伤害期望')
        ax.set_title(f'{coord_info.get("title", "技能")}')

        # 如果需要颜色条，在 2D 图中通常不需要，但可以添加其他元素
        # 例如添加网格
        ax.grid(True, alpha=0.3)

        plt.tight_layout()
        plt.show()

    if len(axis) == 2:
        a_vals, b_vals = axis['axa']['vals'], axis['axb']['vals']
        A, B = np.meshgrid(a_vals, b_vals, indexing='ij')
        
        # 计算函数值
        F = func(A, B)
        
        # 打印函数值矩阵
        print(f"\n{func_name} 函数值矩阵:")
        print(f"行: {axis['axa']['label']}")
        print(f"列: {axis['axb']['label']}")
        print()
        
        header = "--" + "".join([f"{b:>8}" for b in b_vals])
        rows = f'{header}\n{"-" * len(header)}\n'
        
        for i, a in enumerate(a_vals):
            row = f"{a:>11}  "
            for j, b in enumerate(b_vals):
                row += f"{F[i, j]:>8.1f}"
            rows += f'{row}\n'
        
        print(text_to_markdown_table(rows))
        
        # 创建3D图
        fig = plt.figure(figsize=(10, 8))
        ax = fig.add_subplot(111, projection='3d')
        
        surf = ax.plot_surface(A, B, F, cmap='viridis', alpha=0.8)
        ax.set_xlabel(axis['axa']['label'])
        ax.set_ylabel(axis['axb']['label'])
        ax.set_zlabel('伤害期望')
        ax.set_title(f'{coord_info.get("title", "技能")}')
        fig.colorbar(surf, ax=ax, shrink=0.5, label='函数值')
        
        plt.tight_layout()
        plt.show()


def multi_function_compare(func_dict, a_vals, b_vals):
    """多函数对比模式"""
    if len(func_dict) < 2:
        print("错误: 对比模式需要至少2个函数")
        return single_function_analysis(func_dict, coord_info, a_vals, b_vals)
    
    # 获取基础函数和其他函数
    base_func_name = '基础'
    if base_func_name not in func_dict:
        base_func_name = list(func_dict.keys())[0]
    
    base_func = func_dict[base_func_name]
    compare_funcs = {name: func for name, func in func_dict.items() if name != base_func_name}
    
    # 创建网格
    A, B = np.meshgrid(a_vals, b_vals, indexing='ij')
    
    # 计算基础函数值
    F_base = base_func(A, B)
    
    # 为每个对比函数生成分析
    for func_name, func in compare_funcs.items():
        print(f"\n{'='*80}")
        print(f"{func_name} 相对于 {base_func_name} 的对比分析")
        print(f"{'='*80}")
        
        # 计算对比函数值
        F_compare = func(A, B)
        
        # 计算增幅百分比矩阵
        percentage_increase = np.zeros_like(F_base)
        for i in range(len(a_vals)):
            for j in range(len(b_vals)):
                if F_base[i, j] != 0:  # 避免除以零
                    percentage_increase[i, j] = ((F_compare[i, j] - F_base[i, j]) / F_base[i, j]) * 100
                else:
                    percentage_increase[i, j] = 0
        
        # 打印增幅百分比矩阵
        print("行: 重击减值 (0-5)")
        print("列: 实际护甲Ac-Bonus (5-15)")
        print()
        
        header = "重击减值\\护甲" + "".join([f"{b:>18}" for b in b_vals])
        rows = f'{header}\n{"-" * len(header)}\n'
        
        for i, a in enumerate(a_vals):
            row = f"{a:>11}  "
            for j, b in enumerate(b_vals):
                increase = percentage_increase[i, j]
                row += f"{increase:>7.1f}%({F_base[i, j]:.1f}->{F_compare[i, j]:.1f})"
            rows += f'{row}\n'
        
        print(text_to_markdown_table(rows))
        print(f"\n说明：正值表示{func_name} > {base_func_name}（开启{coord_info.get('title', '技能')}更优）")
        print(f"      负值表示{func_name} < {base_func_name}（关闭{coord_info.get('title', '技能')}更优）")
    
    # 创建对比图表
    create_comparison_charts(func_dict, coord_info, A, B, a_vals, b_vals)

def create_comparison_charts(func_dict, coord_info, A, B, a_vals, b_vals):
    """创建对比图表"""
    n_funcs = len(func_dict)
    
    # 计算每个函数的值
    func_values = {}
    for name, func in func_dict.items():
        func_values[name] = func(A, B)
    
    # 创建子图布局
    if n_funcs <= 3:
        fig = plt.figure(figsize=(5 * n_funcs + 5, 5))
        subplot_count = n_funcs + 1  # 每个函数一个图 + 一个组合图
    else:
        fig = plt.figure(figsize=(20, 5 * ((n_funcs + 1) // 2)))
        subplot_count = n_funcs + 1
    
    # 为每个函数创建单独的3D图
    colors = ['viridis', 'plasma', 'coolwarm', 'hot', 'spring', 'summer']
    for idx, (name, values) in enumerate(func_values.items()):
        ax = fig.add_subplot(2, (subplot_count + 1) // 2, idx + 1, projection='3d')
        surf = ax.plot_surface(A, B, values, cmap=colors[idx % len(colors)], alpha=0.8)
        ax.set_xlabel('重击减值')
        ax.set_ylabel('实际护甲Ac-Bonus')
        ax.set_zlabel('伤害期望')
        ax.set_title(f'{name}')
        fig.colorbar(surf, ax=ax, shrink=0.5, label='函数值')
    
    # 创建组合3D图
    ax_combined = fig.add_subplot(2, (subplot_count + 1) // 2, subplot_count, projection='3d')
    for idx, (name, values) in enumerate(func_values.items()):
        surf = ax_combined.plot_surface(A, B, values, cmap=colors[idx % len(colors)], 
                                      alpha=0.6, label=name)
    
    ax_combined.set_xlabel('重击减值')
    ax_combined.set_ylabel('实际护甲Ac-Bonus')
    ax_combined.set_zlabel('伤害期望')
    ax_combined.set_title('所有函数对比')
    ax_combined.legend()
    
    plt.tight_layout()
    plt.show()

def text_to_markdown_table(data_text):
    """
    将文本数据转换为Markdown表格
    
    参数:
    data_text: 包含表格数据的字符串
    
    返回:
    markdown_table: Markdown格式的表格字符串
    """
    
    # 分割文本行
    lines = data_text.strip().split('\n')
    
    # 提取表头（第一行）
    header_line = lines[0]
    # 使用正则表达式分割表头，匹配连续的非空白字符
    headers = re.findall(r'\S+', header_line)
    
    # 处理数据行
    data_rows = []
    for line in lines[2:]:  # 跳过表头和分隔线
        # 使用正则表达式分割数据行
        row_data = re.findall(r'\S+', line)
        if row_data:  # 确保不是空行
            data_rows.append(row_data)
    
    # 构建Markdown表格
    markdown_lines = []
    
    # 添加表头
    header_row = "| | " + " | ".join(headers[1:]) + " |"
    markdown_lines.append(header_row)
    
    # 添加分隔线
    separator_row = "|" + "|".join(["---" for _ in headers]) + "|"
    markdown_lines.append(separator_row)
    
    # 添加数据行
    for row in data_rows:
        data_row = "| " + " | ".join(row) + " |"
        markdown_lines.append(data_row)
    
    # 返回完整的Markdown表格
    return "\n".join(markdown_lines)
