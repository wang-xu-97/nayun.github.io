import re
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
