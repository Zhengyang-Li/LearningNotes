import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
plt.rcParams['font.sans-serif'] = ['STHeiti']  # 显示中文标签
plt.rcParams['axes.unicode_minus'] = False         # 正常显示负号

# 定义矩阵和列向量
A = np.array([[1, 0, 0], [0, 5, 2], [3, 1, 9]])
v1, v2, v3 = A.T  # 提取列向量

# 创建 3D 图形
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

# 绘制向量
ax.quiver(0, 0, 0, v1[0], v1[1], v1[2], color='r', label='v1 = [1, 0, 3]', arrow_length_ratio=0.1)
ax.quiver(0, 0, 0, v2[0], v2[1], v2[2], color='g', label='v2 = [0, 5, 1]', arrow_length_ratio=0.1)
ax.quiver(0, 0, 0, v3[0], v3[1], v3[2], color='b', label='v3 = [0, 2, 9]', arrow_length_ratio=0.1)

# 设置坐标轴
ax.set_xlim([0, 10])
ax.set_ylim([0, 10])
ax.set_zlim([0, 10])
ax.set_xlabel('X轴')
ax.set_ylabel('Y轴')
ax.set_zlabel('Z轴')
ax.set_title('用鼠标拖动旋转视角观察向量')

# 添加图例
ax.legend()

# 显示图形
plt.show()