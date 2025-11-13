import numpy as np
from tool import *

coord_info = {
    'title': '巨武器大师', 
    'x': '重击减值', 
    'y': '实际护甲Ac-Bonus', 
    'z': '伤害期望'
}

D_p_normal = nncde(12)
D_p_normal_buffed = nncde(12) + nncde(4) + nncde(4) + nncde(6)
print(D_p_normal)
print(D_p_normal_buffed)
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
    return D_p_normal_buffed * hit_chance_special + 13 * hit_chance