import argparse
from tool import *
plt.rcParams['font.sans-serif'] = ['AR PL UMing CN']  # 指定默认字体为黑体[citation:4][citation:6]
plt.rcParams['axes.unicode_minus'] = False   # 解决坐标轴负号显示为方块的问题[citation:4][citation:6]

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