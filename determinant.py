
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection, Line3DCollection
plt.rcParams['font.sans-serif'] = ['STHeiti']  # 显示中文标签

# 定义矩阵
A = np.array([[1, 0, 0], 
              [0, 5, 2], 
              [3, 1, 9]])

# 计算行列式
det_A = np.linalg.det(A)
volume = abs(det_A)  # 平行六面体体积

print(f"行列式值 det(A) = {det_A:.2f}")
print(f"列向量张成的体积 = {volume:.2f}")

# 定义矩阵
A = np.array([[1, 0, 0], 
              [0, 5, 2], 
              [3, 1, 9]])

# 计算行列式和体积
det_A = np.linalg.det(A)
volume = abs(det_A)

# 提取列向量
v1, v2, v3 = A.T

# 创建图形
fig = plt.figure(figsize=(12, 8))
ax = fig.add_subplot(111, projection='3d')

# 绘制向量（彩色箭头）
ax.quiver(0, 0, 0, v1[0], v1[1], v1[2], color='r', label='$v_1$=[1,0,3]', arrow_length_ratio=0.1, linewidth=2)
ax.quiver(0, 0, 0, v2[0], v2[1], v2[2], color='g', label='$v_2$=[0,5,1]', arrow_length_ratio=0.1, linewidth=2)
ax.quiver(0, 0, 0, v3[0], v3[1], v3[2], color='b', label='$v_3$=[0,2,9]', arrow_length_ratio=0.1, linewidth=2)

# 计算平行六面体顶点
vertices = np.array([
    [0, 0, 0],  # 原点
    v1,         # v1
    v2,         # v2
    v3,         # v3
    v1 + v2,    # v1 + v2
    v1 + v3,    # v1 + v3
    v2 + v3,    # v2 + v3
    v1 + v2 + v3  # v1 + v2 + v3
])

# 定义六面体的12条边（顶点索引对）
edges = [
    [vertices[0], vertices[1]],  # 0 -> v1
    [vertices[0], vertices[2]],  # 0 -> v2
    [vertices[0], vertices[3]],  # 0 -> v3
    [vertices[1], vertices[4]],  # v1 -> v1+v2
    [vertices[1], vertices[5]],  # v1 -> v1+v3
    [vertices[2], vertices[4]],  # v2 -> v1+v2
    [vertices[2], vertices[6]],  # v2 -> v2+v3
    [vertices[3], vertices[5]],  # v3 -> v1+v3
    [vertices[3], vertices[6]],  # v3 -> v2+v3
    [vertices[4], vertices[7]],  # v1+v2 -> v1+v2+v3
    [vertices[5], vertices[7]],  # v1+v3 -> v1+v2+v3
    [vertices[6], vertices[7]]   # v2+v3 -> v1+v2+v3
]

# 绘制黑色边线
edge_collection = Line3DCollection(edges, colors='black', linewidths=1.5, linestyle='solid')
ax.add_collection3d(edge_collection)

# 定义六面体的6个面（顶点索引组）
faces = [
    [vertices[0], vertices[1], vertices[4], vertices[2]],  # 底面
    [vertices[0], vertices[1], vertices[5], vertices[3]],  # 侧面1
    [vertices[0], vertices[2], vertices[6], vertices[3]],  # 侧面2
    [vertices[1], vertices[4], vertices[7], vertices[5]],  # 顶面
    [vertices[2], vertices[4], vertices[7], vertices[6]],  # 侧面3
    [vertices[3], vertices[5], vertices[7], vertices[6]]   # 背面
]

# 绘制半透明蓝色面
ax.add_collection3d(Poly3DCollection(faces, alpha=0.2, color='blue'))

# 标注体积
ax.text(0, 0, 0, f'体积 = {volume:.1f}', color='black', fontsize=12, ha='center')

# 设置图形属性
ax.set_xlim([0, 10])
ax.set_ylim([0, 10])
ax.set_zlim([0, 15])
ax.set_xlabel('X轴')
ax.set_ylabel('Y轴')
ax.set_zlabel('Z轴')
ax.set_title(f'矩阵A的列向量张成的平行六面体 (det(A) = {det_A:.1f})')
ax.legend()

plt.tight_layout()
plt.show()