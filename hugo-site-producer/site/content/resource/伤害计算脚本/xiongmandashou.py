import numpy as np
coord_info = {
    'title': '凶蛮打手', 
    'x': '重击减值', 
    'y': '实际护甲Ac-Bonus', 
    'z': '伤害期望'
}
dice_n = 1
dice_d = 12
def normal_non_crit_dice_expectation(d):
    return (1+d)/2

def xmds_non_crit_dice_expectation(d):
    return (d+1)*(4*d-1)/(6*d)

nncde = normal_non_crit_dice_expectation
xncde = xmds_non_crit_dice_expectation

D_p_normal = nncde(dice_d)
D_p_xmds = xncde(dice_d)
print(D_p_normal)
print(D_p_xmds)
def f1(C, B):
    """无凶蛮打手"""
    # return a**2 + b**2
    t = np.maximum(20-C-B, 0)
    hit_chance_special = (2 * (C + 1) + t) / 20
    hit_chance = ((C + 1) + t) / 20
    return D_p_normal * hit_chance_special + 3 * hit_chance

def f2(C, B):
    """有凶蛮打手"""
    # return a * b
    t = np.maximum(20-C-B, 0)
    hit_chance_special = (2 * (C + 1) + t) / 20
    hit_chance = ((C + 1) + t) / 20
    return D_p_xmds * hit_chance_special + 3 * hit_chance
