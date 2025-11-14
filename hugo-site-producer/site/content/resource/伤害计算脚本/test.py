import numpy as np
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['AR PL UMing CN']  # 指定默认字体为黑体[citation:4][citation:6]
plt.rcParams['axes.unicode_minus'] = False   # 解决坐标轴负号显示为方块的问题[citation:4][citation:6]

from tool import *
import argparse

def parse_skillgroup(v):
    v.replace('，', ',')
    if ',' in v:
        return v.split(',')
    elif v not in supported_skill_list:
        print(f'{v} not in supported skill list({supported_skill_list})')
        return []
    else:
        return [v]

def parse_args():
    parser = argparse.ArgumentParser(description='测试.')
    parser.add_argument('-e', '--enable', type=parse_skillgroup, default=[],          nargs='+',           help='启用技能，默认启用巨武器大师')
    parser.add_argument('-d', '--dice',   type=lambda v:dice(*v.split('d')) ,      default="1d12",      help='武器伤害骰')
    parser.add_argument('-b', '--bonus',   type=int ,      default=3,      help='武器伤害固定加值')
    parser.add_argument('-m', '--mode', choices=['single', 'compare'], default='compare', help='分析模式: single-单函数分析, compare-多函数对比')
    return parser.parse_args()


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
    ax.set_title(f'{func_name} - {coord_info.get("title", "技能")}')
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

def main():
    args = parse_args()
    func_dict = factory(args)
    singlefuncpack = None
    for v in func_dict.values():
        if not singlefuncpack and (tt:=v.info['title']) and  tt!= 'default':
            singlefuncpack = v
    
    # 参数范围
    a_vals = np.arange(0, 5 + 1)    # 重击减值
    b_vals = np.arange(5, 15 + 1)   # 实际护甲Ac-Bonus
    
    # 根据模式选择分析方式
    if args.mode == 'single':
        single_function_analysis(singlefuncpack, a_vals, b_vals)
    else:  # compare mode
        multi_function_compare(func_dict, coord_info, a_vals, b_vals)

if __name__ == "__main__":
    main()