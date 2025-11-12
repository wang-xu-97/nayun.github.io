import numpy as np
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['AR PL UMing CN']  # 指定默认字体为黑体[citation:4][citation:6]
plt.rcParams['axes.unicode_minus'] = False   # 解决坐标轴负号显示为方块的问题[citation:4][citation:6]
from mpl_toolkits.mplot3d import Axes3D

tolerance = 0.5  # 容忍度，可以根据需要调整
D_p = 9.5
# 定义你的方程 f1(a,b) 和 f2(a,b)
# 请根据你的具体方程修改这些函数
def f1(C, B):
    """示例方程1，请替换为你的实际方程"""
    # return a**2 + b**2
    t = np.maximum(20-C-B, 0)
    numerator = 2 * (C + 1) + t
    return D_p * numerator / 20

def f2(C, B):
    """示例方程2，请替换为你的实际方程"""
    # return a * b
    t = np.maximum(20-C-B-5, 0)
    numerator = 2 * (C + 1) + t
    return (D_p) * numerator / 20 + 10

# 参数范围
min_val, max_val = 0, 20

# 生成所有可能的整数组合
a_vals = np.arange(0, 5 + 1)
b_vals = np.arange(5, 15 + 1)

# 创建网格
A, B = np.meshgrid(a_vals, b_vals, indexing='ij')

# 计算方程值
F1 = f1(A, B)
F2 = f2(A, B)

# 扁平化数组用于绘图
a_flat = A.flatten()
b_flat = B.flatten()
f1_flat = F1.flatten()
f2_flat = F2.flatten()

# 查找f1和f2的相交点 (f1 ≈ f2)
intersection_points = []

# 按a轴离散点查找相交点
for a in a_vals:
    # 找到当前a值对应的所有点
    mask = (a_flat == a)
    a_subset = a_flat[mask]
    b_subset = b_flat[mask]
    f1_subset = f1_flat[mask]
    f2_subset = f2_flat[mask]
    
    # 查找f1和f2相近的点
    diff = np.abs(f1_subset - f2_subset)
    close_indices = np.where(diff <= tolerance)[0]
    
    for idx in close_indices:
        intersection_points.append({
            '重击减值': a_subset[idx],
            '实际护甲Ac-Bonus': b_subset[idx],
            'f1': f1_subset[idx],
            'f2': f2_subset[idx],
            'diff': diff[idx]
        })

# 创建3D图
fig = plt.figure(figsize=(15, 5))

# 子图1: f1(a,b) 的3D曲面
ax1 = fig.add_subplot(131, projection='3d')
surf1 = ax1.plot_surface(A, B, F1, cmap='viridis', alpha=0.8)
ax1.set_xlabel('重击减值')
ax1.set_ylabel('实际护甲Ac-Bonus')
ax1.set_zlabel('关巨武器大师')
ax1.set_title('关巨武器大师 3D')
fig.colorbar(surf1, ax=ax1, shrink=0.5, label='f1值')

# 子图2: f2(a,b) 的3D曲面
ax2 = fig.add_subplot(132, projection='3d')
surf2 = ax2.plot_surface(A, B, F2, cmap='plasma', alpha=0.8)
ax2.set_xlabel('重击减值')
ax2.set_ylabel('实际护甲Ac-Bonus')
ax2.set_zlabel('开巨武器大师')
ax2.set_title('开巨武器大师 3D')
fig.colorbar(surf2, ax=ax2, shrink=0.5, label='f2值')

# 子图3: 两个曲面和相交线
ax3 = fig.add_subplot(133, projection='3d')
# 绘制f1曲面
surf1_3 = ax3.plot_surface(A, B, F1, cmap='viridis', alpha=0.6, label='f1')
# 绘制f2曲面
surf2_3 = ax3.plot_surface(A, B, F2, cmap='plasma', alpha=0.6, label='f2')

# 绘制相交点
if intersection_points:
    a_int = [p['重击减值'] for p in intersection_points]
    b_int = [p['实际护甲Ac-Bonus'] for p in intersection_points]
    f_int = [p['f1'] for p in intersection_points]  # 因为f1≈f2
    
    # 用红色点标记相交点
    ax3.scatter(a_int, b_int, f_int, color='red', s=5, label='相交点', alpha=1.0)
    
    # 尝试连接相交点形成相交线
    # if len(a_int) > 1:
    #     # 按a值排序
    #     sorted_indices = np.argsort(a_int)
    #     a_int_sorted = [a_int[i] for i in sorted_indices]
    #     b_int_sorted = [b_int[i] for i in sorted_indices]
    #     f_int_sorted = [f_int[i] for i in sorted_indices]
        
    #     # 绘制相交线
    #     ax3.plot(a_int_sorted, b_int_sorted, f_int_sorted, 
    #             color='red', linewidth=3, label='相交线')

# 输出相交点信息
print("=" * 60)
print("相交点分析 (f1 ≈ f2)")
print("=" * 60)
print(f"容忍度: {tolerance}")
print(f"找到 {len(intersection_points)} 个相交点")
print()

if intersection_points:
    # 按a值分组显示
    a_groups = {}
    for point in intersection_points:
        a_val = point['重击减值']
        if a_val not in a_groups:
            a_groups[a_val] = []
        a_groups[a_val].append(point)
    
    print("按a轴离散点的相交点:")
    print("-" * 50)
    for a_val in sorted(a_groups.keys()):
        points = a_groups[a_val]
        print(f"重击减值 = {a_val}:")
        for point in points:
            print(f"  实际护甲 = {point['实际护甲Ac-Bonus']}, 关期望 = {point['f1']:.2f}, 开期望 = {point['f2']:.2f}, 差值 = {point['diff']:.4f}, 显示命中率 = {(21-point['实际护甲Ac-Bonus'])/20:.2f}")
        print()
    
    # 统计信息
    print("相交点统计:")
    print("-" * 30)
    print(f"a值范围: {min(a_int)} - {max(a_int)}")
    print(f"b值范围: {min(b_int)} - {max(b_int)}")
    print(f"函数值范围: {min(f_int):.2f} - {max(f_int):.2f}")
else:
    print("未找到相交点，可以尝试增加容忍度或检查方程定义")

ax3.set_xlabel('重击减值')
ax3.set_ylabel('实际护甲Ac-Bonus')
ax3.set_zlabel('函数值')
ax3.set_title('f1 f2 intersection')
# ax3.legend()

plt.tight_layout()
plt.show()
