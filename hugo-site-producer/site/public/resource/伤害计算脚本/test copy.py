import argparse
from tool import *
plt.rcParams['font.sans-serif'] = ['AR PL UMing CN']  # 指定默认字体为黑体[citation:4][citation:6]
plt.rcParams['axes.unicode_minus'] = False   # 解决坐标轴负号显示为方块的问题[citation:4][citation:6]

def parse_skillgroup(v):
    v.replace('，', ',')
    def in_preset(s):
        if s in supported_skill_list:return True
        print(f'{s} not in supported skill list({supported_skill_list})')
        return False

    if ',' in v:return [s for s in v.split(',') if in_preset(s)]
    elif in_preset(v):[v]
    return []

def parse_cfg(c):
    # axes = 
    def range_determine(s):
        return s.split('-')
    for fig in ['self_status', 'enemy_status']:
        try:
            for idx, attr in enumerate(c[fig]['Attribute']):
                try:   c[fig]['Attribute'][idx] = int(attr)
                except:c[fig]['Attribute'][idx] = 10
            if (cfasize:=len(c[fig]['Attribute'])) < 6:c[fig]['Attribute'].extend([10]*(6-cfasize))
        except: c[fig]['Attribute'] = [10] * 6
        defaults = {
            'AC': 15, 
            'Saving_Bonus': 0, 
            'Spell_Save_DC_Bonus': 0, 
            'Attack_Bonus': 0,
        }
        for k, v in defaults.items():
            try:    c[fig][k] = int(c[fig][k])
            except: c[fig][k] = v
    return c

def parse_args():
    parser = argparse.ArgumentParser(description='测试.')
    parser.add_argument('-e', '--enable', type=parse_skillgroup, default=[],          nargs='+',           help='启用技能，默认启用巨武器大师')
    parser.add_argument('-d', '--dice',   type=lambda v:dice(*v.split('d')) ,      default="1d12",      help='武器伤害骰')
    parser.add_argument('-b', '--bonus',   type=int ,      default=3,      help='武器伤害固定加值')
    return parser.parse_args()


def main():
    args = parse_args()
    print(args.enable)
    c = tl.read_yml('cfg.yaml')
    tl.printdict(parse_cfg(c))
    # tl.printdict(c)
    exit()
    func_dict = factory(args)
    singlefuncpack = None
    for v in func_dict.values():
        print(v)
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