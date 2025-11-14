import re
import numpy as np
import matplotlib.pyplot as plt
import numpy as np

def normal_non_crit_dice_expectation(d):
    return (1+d)/2

def xmds_non_crit_dice_expectation(d):
    return (d+1)*(4*d-1)/(6*d)

nncde = normal_non_crit_dice_expectation
xncde = xmds_non_crit_dice_expectation

supported_skill_list = ['jwqds', 'xmds', 'buff']

class dice:
    def __init__(self, n, d) -> None:
        self.n = int(n)
        self.d = int(d)

class function_pack:
    def __init__(self, func, info) -> None:
        self.func = func
        self.info = info

fp = function_pack

def factory(args):
    skill_group = [[]] + [i for i in args.enable if i]
    print(skill_group)
    d = args.dice
    print(d.n)
    print(d.d)
    D_p_normal = nncde(d.d)
    D_p_normal_buffed = nncde(d.d) + nncde(4) + nncde(4) + nncde(6)
    D_p_xmds = xncde(d.d)
    D_p_xmds_buffed = xncde(d.d) + xncde(4) + xncde(4) + xncde(6)
    print(D_p_normal)
    print(D_p_xmds)
    
    def maker(skill_status):
        def f(C, B):
            if skill_status['xmds']:
                if skill_status['buff']:D_p_ablecrit = D_p_xmds_buffed
                else:                   D_p_ablecrit = D_p_xmds
            else:
                if skill_status['buff']:D_p_ablecrit = D_p_normal_buffed
                else:                   D_p_ablecrit = D_p_normal
            D_p_unablecrit = args.bonus
            if skill_status['jwqds']: 
                B += 5
                D_p_unablecrit += 10

            t = np.maximum(20-C-B, 0)
            hit_chance_special = (2 * (C + 1) + t) / 20
            hit_chance = ((C + 1) + t) / 20
            return D_p_ablecrit * hit_chance_special + D_p_unablecrit * hit_chance

        return f

    def tt(skills):
        ttmap = {'xmds': '凶蛮打手', 'buff': '3可重击增伤buff', 'jwqds':'巨武器大师'}
        return '+'.join([
            ttmap.get(sk, '')
            for sk in skills
        ])
    
    func_dict = {
        '+'.join(skills) if skills != [] else 'default': fp(maker({
            skill: skill in skills
            for skill in supported_skill_list
        }), {'title':tt(skills)})
        for skills in skill_group
    }

    return func_dict

def single_function_analysis(funcpack:fp, a_vals, b_vals):
    """单函数分析模式"""
    if not funcpack.func:
        print("错误: 没有找到可分析的函数")
        return
    
    func = funcpack.func
    coord_info = funcpack.info
    func_name = coord_info['title']
    print(f"=== 单函数分析: {func_name} ===")
    
    # 创建网格
    A, B = np.meshgrid(a_vals, b_vals, indexing='ij')
    
    # 计算函数值
    F = func(A, B)
    
    # 打印函数值矩阵
    print(f"\n{func_name} 函数值矩阵:")
    print("行: 重击减值 (0-5)")
    print("列: 实际护甲Ac-Bonus (5-15)")
    print()
    
    header = "重击减值\\护甲" + "".join([f"{b:>8}" for b in b_vals])
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
    ax.set_xlabel('重击减值')
    ax.set_ylabel('实际护甲Ac-Bonus')
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
