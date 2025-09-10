#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import re
from pathlib import Path

def count_chinese_chars(file_path):
    """统计文件中的中文字符数量"""
    try:
        # 自动检测文件编码
        import chardet
        
        with open(file_path, 'rb') as f:
            raw_data = f.read()
            encoding = chardet.detect(raw_data)['encoding'] or 'utf-8'
        
        # 读取文件并统计中文字符
        with open(file_path, 'r', encoding=encoding, errors='ignore') as f:
            content = f.read()
            
            # 方法1: 使用Unicode范围
            chinese_pattern = r'[\u4e00-\u9fff\u3400-\u4dbf\uf900-\ufaff]'
            chinese_chars = re.findall(chinese_pattern, content)
            
            # 方法2: 使用汉字Unicode块（更全面）
            # 包括：CJK统一表意文字、扩展A、扩展B等
            comprehensive_pattern = r'[\u4e00-\u9fff\u3400-\u4dbf\u20000-\u2a6df\u2a700-\u2b73f\u2b740-\u2b81f\u2b820-\u2ceaf\uf900-\ufaff\u2f800-\u2fa1f]'
            all_chinese_chars = re.findall(comprehensive_pattern, content)
            
            return len(all_chinese_chars), len(chinese_chars)
            
    except FileNotFoundError:
        print(f"错误：文件 '{file_path}' 不存在")
        return 0, 0
    except Exception as e:
        print(f"读取文件时出错: {e}")
        return 0, 0

def count_by_line(file_path):
    """按行统计中文字符，显示每行的数量"""
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            total = 0
            for line_num, line in enumerate(f, 1):
                chinese_count = len(re.findall(r'[\u4e00-\u9fff]', line))
                if chinese_count > 0:
                    print(f"第{line_num:3d}行: {chinese_count:3d}个中文 - {line.strip()[:50]}{'...' if len(line) > 50 else ''}")
                total += chinese_count
            return total
    except Exception as e:
        print(f"错误: {e}")
        return 0

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("用法: python3 count_chinese.py <文件名>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    
    if not Path(file_path).exists():
        print(f"文件 '{file_path}' 不存在")
        sys.exit(1)
    
    print(f"正在分析文件: {file_path}")
    print("=" * 50)
    
    # 统计总中文字符数
    comprehensive_count, basic_count = count_chinese_chars(file_path)
    print(f"基本中文字符数: {basic_count}")
    print(f"全面中文字符数（包含扩展）: {comprehensive_count}")
    
    # print("\n按行统计:")
    # print("-" * 50)
    # total_by_line = count_by_line(file_path)
    # print(f"\n按行统计总数: {total_by_line}")
