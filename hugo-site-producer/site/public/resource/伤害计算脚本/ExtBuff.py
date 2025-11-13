import numpy as np
from tool import *
coord_info = {
    'title': '增伤buff', 
}
dice_n = 1
dice_d = 12

D_p_normal = nncde(dice_d)
D_p_normal_buffed = nncde(dice_d) + nncde(4) + nncde(4) + nncde(6)
print(D_p_normal)
def f1(C, B):
    """无增伤buff"""
    # return a**2 + b**2
    t = np.maximum(20-C-B, 0)
    hit_chance_special = (2 * (C + 1) + t) / 20
    hit_chance = ((C + 1) + t) / 20
    return D_p_normal * hit_chance_special + 3 * hit_chance

def f2(C, B):
    """有增伤buff"""
    # return a * b
    t = np.maximum(20-C-B, 0)
    hit_chance_special = (2 * (C + 1) + t) / 20
    hit_chance = ((C + 1) + t) / 20
    return D_p_normal_buffed * hit_chance_special + 3 * hit_chance
