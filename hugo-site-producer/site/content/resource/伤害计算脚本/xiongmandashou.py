import numpy as np

D_p_normal = 6.5 # 可重击非重击伤害期望
def f1(C, B):
    """关闭巨武器大师 均势伤害期望公式"""
    # return a**2 + b**2
    t = np.maximum(20-C-B, 0)
    hit_chance_special = (2 * (C + 1) + t) / 20
    hit_chance = ((C + 1) + t) / 20
    return D_p_normal * hit_chance_special + 3 * hit_chance

def f2(C, B):
    """打开巨武器大师 均势伤害期望公式"""
    # return a * b
    t = np.maximum(20-C-B-5, 0)
    hit_chance_special = (2 * (C + 1) + t) / 20
    hit_chance = ((C + 1) + t) / 20
    return D_p_normal * hit_chance_special + 10 * hit_chance
