import argparse, traceback
from tool import *
plt.rcParams['font.sans-serif'] = ['AR PL UMing CN']  # 指定默认字体为黑体[citation:4][citation:6]
plt.rcParams['axes.unicode_minus'] = False   # 解决坐标轴负号显示为方块的问题[citation:4][citation:6]

def parse_cfg(c):
    axis = []
    metric = {}
    def axis_metric_determine(k, s:str, s_default, mark='->', v_type=int):
        r = []
        if v_type != int:
            @tl.execute(r)
            def determin_metric():
                if not s:return s_default
                def update_metric():
                    if len(v_type(s)) > 1:
                        if len(metric) > 0:
                            print(f'曲面矩阵已设置{metric}，{k}矩阵({s})设置不生效，重置为默认({s_default})')
                            return s_default
                        else:
                            metric.update({k:s})
                    return s
                
                if 'dice' not in k:return update_metric()
                if 'Active_skill_group' in k:sl = active_skill_list
                elif 'Passive_skill_group' in k:sl = passive_skill_list
                else: sl = Vulnerability_list
                for i, _s in enumerate(s):
                    for __s in _s:
                        if __s not in sl:
                            print(f'{k}->{_s}->{__s} not in skill list{sl}')
                            _s.remove(__s)
                    s[i] = _s
                return update_metric()
        else:
            @tl.execute(r)
            def determine_axis():
                def limited(i:str, low=1, up=30):
                    i = i.strip()
                    if int(i) <= low:
                        print(f'{k}属性值设置低于下限({i})，重置为默认下限({low})')
                        return low
                    if int(i) >= up:
                        print(f'{k}属性值设置高于上限({i})，重置为默认上限({up})')
                        return up
                    return int(i)

                if mark in s:
                    if len(axis) >= 2:
                        print(f'坐标轴已有{axis}，{k}范围设置不生效，重置为默认({s_default})')
                        return s_default
                    axis.append(k)
                    ss = s.split(mark)
                    if len(ss) <= 2:
                        try:return [limited(i) if v_type==int else i.strip() for i in ss]
                        except:print(f'坐标轴解析错误{s}，{k}范围设置不生效，重置为默认({s_default})')
                    else:print(f'坐标轴解析错误{s}，{k}范围设置不生效，重置为默认({s_default})')
                else:
                    try: return int(s)
                    except: return s_default
        return r[0]


    defaults = {
        'AC': 15, 
        'Saving_Bonus': 0, 
        'Spell_Save_DC_Bonus': 0, 
        'Attack_Bonus': 0,
        'Crit_Bonus': 0,
        'weapon_dice': ['1d10'],
        'Passive_skill_group': [[]],
        'Active_skill_group': [['na']],
        'Vulnerability': [[]],
    }
    for fig in ['self_status', 'enemy_status']:
        try:
            for idx, attr in enumerate(c[fig]['Attribute']):c[fig]['Attribute'][idx] = axis_metric_determine(f'{fig}-{list(attributes.keys())[idx]}', str(attr), 10)
            if (cfasize:=len(c[fig]['Attribute'])) < 6:c[fig]['Attribute'].extend([10]*(6-cfasize))
        except: c[fig]['Attribute'] = [10] * 6
        for k, v in defaults.items():c[fig][k] = axis_metric_determine(f'{fig}-{k}', str(c[fig].get(k, None)) if type(v)!=list else c[fig].get(k, None), v, v_type=type(v))
    c['axis'] = axis
    c['metric'] = metric
    c['cast_type'] = 'Attack' if not (bm:=tl.best_match(c['cast_type'], cast_types.keys())) else bm
    c['Roll_status'] = 'Neutral' if not (bm:=tl.best_match(c['Roll_status'], Roll_status.keys())) else bm
    return c


def main():
    c = parse_cfg(tl.read_yml('cfg.yaml'))
    tl.printdict(c)
    func_dict = factory(c)
    exit()
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