import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import matplotlib.patches as mpatches
import seaborn as sns

# 设置美观的样式
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("husl")

# 路径数据: 每条路径的(时间(小时), 费用)
paths = [
    {"name": "Path 3", "time": 0.67, "cost": 10},  # 费用最低
    {"name": "Path 2", "time": 0.5, "cost": 15},
    {"name": "Dominated A", "time": 0.45, "cost": 25},
    {"name": "Dominated B", "time": 0.6, "cost": 20},
    {"name": "Path 1", "time": 0.33, "cost": 30},
    {"name": "Path 4", "time": 0.25, "cost": 40}   # 费用最高
]

# 按费用排序
paths_sorted = sorted(paths, key=lambda x: x["cost"])

# 重新分配名称，确保编号按费用从小到大
for i, path in enumerate(paths_sorted):
    if "Dominated" not in path["name"]:
        path["name"] = f"Path {i+1}"

# 创建图形和轴
fig, ax = plt.subplots(figsize=(12, 9))
ax.set_xlabel('Time (hours)', fontsize=14, fontweight='bold')
ax.set_ylabel('Cost ($)', fontsize=14, fontweight='bold')
ax.set_title('Optimal Path Selection with Changing Value of Time (VOT)', 
             fontsize=16, fontweight='bold', pad=20)

# 设置背景颜色
ax.set_facecolor('#f8f9fa')
fig.patch.set_facecolor('white')

# 分离Pareto前沿路径和被支配路径
pareto_paths = [path for path in paths_sorted if "Dominated" not in path["name"]]
dominated_paths = [path for path in paths_sorted if "Dominated" in path["name"]]

# 为Pareto前沿上的路径选择更鲜明的颜色
pareto_colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']
for i, path in enumerate(pareto_paths):
    ax.scatter(path["time"], path["cost"], s=150, label=path["name"], 
               alpha=0.9, color=pareto_colors[i], edgecolors='black', linewidth=1.2)

# 绘制被支配的路径点
for i, path in enumerate(dominated_paths):
    ax.scatter(path["time"], path["cost"], s=120, label=path["name"], 
               alpha=0.7, marker='X', color='#7f7f7f', edgecolors='black', linewidth=1)

# 绘制Pareto前沿线
pareto_times = [path["time"] for path in pareto_paths]
pareto_costs = [path["cost"] for path in pareto_paths]

# 按时间排序以便绘制连续的Pareto前沿线
sorted_indices = np.argsort(pareto_times)
sorted_pareto_times = [pareto_times[i] for i in sorted_indices]
sorted_pareto_costs = [pareto_costs[i] for i in sorted_indices]

pareto_line, = ax.plot(sorted_pareto_times, sorted_pareto_costs, 'b-', 
                      alpha=0.8, linewidth=3, label='Pareto Frontier')

# 添加图例
legend = ax.legend(loc='upper right', fontsize=11, frameon=True, 
                  fancybox=True, shadow=True)
legend.get_frame().set_facecolor('white')

# 添加当前VOT文本
vot_text = ax.text(0.05, 0.95, '', transform=ax.transAxes, fontsize=12,
                  bbox=dict(facecolor='white', alpha=0.9, edgecolor='gray', boxstyle='round,pad=0.5'))

# 添加最优路径指示器
optimal_marker, = ax.plot([], [], 'o', markersize=18, alpha=0.9, 
                         color='gold', markeredgecolor='black', markeredgewidth=2)

# 添加当前广义成本线
line, = ax.plot([], [], 'r--', alpha=0.7, linewidth=2.5)

# 为每条路径添加广义成本文本标签
cost_texts = []
for i, path in enumerate(paths_sorted):
    text = ax.text(path["time"] + 0.02, path["cost"] + 1.2, '', fontsize=10,
                  bbox=dict(facecolor='white', alpha=0.8, edgecolor='lightgray', pad=2))
    cost_texts.append(text)

# 添加表格显示所有路径的详细成本信息（放在左下角）
table_data = []
for path in paths_sorted:
    table_data.append([path["name"], f"{path['time']:.2f}", path["cost"], 0])

table = ax.table(cellText=table_data, 
                colLabels=['Path', 'Time (h)', 'Cost ($)', 'Gen. Cost'],
                loc='lower left', 
                cellLoc='center',
                bbox=[0.05, 0.05, 0.35, 0.3])
table.auto_set_font_size(False)
table.set_fontsize(10)

# 设置表格样式
for key, cell in table.get_celld().items():
    cell.set_text_props(fontsize=10)
    if key[0] == 0:  # 表头行
        cell.set_text_props(weight='bold', fontsize=11)
        cell.set_facecolor('#e9ecef')
    cell.set_edgecolor('lightgray')

# 设置坐标轴范围
ax.set_xlim(0.2, 0.75)
ax.set_ylim(5, 45)

# 添加网格
ax.grid(True, linestyle='--', alpha=0.7)

# 动画更新函数
def update(vot):
    # 计算每条路径的广义成本
    generalized_costs = [vot * path["time"] + path["cost"] for path in paths_sorted]
    
    # 找到最优路径
    optimal_idx = np.argmin(generalized_costs)
    optimal_path = paths_sorted[optimal_idx]
    
    # 更新最优路径标记
    optimal_marker.set_data([optimal_path["time"]], [optimal_path["cost"]])
    
    # 更新VOT文本
    vot_text.set_text(f'VOT = {vot:.2f} $/hour\nOptimal Path: {optimal_path["name"]}\nGeneralized Cost: {generalized_costs[optimal_idx]:.2f}')
    
    # 绘制当前广义成本线
    x_vals = np.linspace(0.2, 0.75, 100)
    constant = vot * optimal_path["time"] + optimal_path["cost"]
    y_vals = constant - vot * x_vals
    line.set_data(x_vals, y_vals)
    
    # 更新每条路径的广义成本文本
    for i, text in enumerate(cost_texts):
        text.set_text(f'GC: {generalized_costs[i]:.2f}')
        if i == optimal_idx:
            text.set_bbox(dict(facecolor='lightyellow', alpha=0.9, edgecolor='gold'))
        else:
            text.set_bbox(dict(facecolor='white', alpha=0.8, edgecolor='lightgray'))
    
    # 更新表格中的广义成本数据
    for i, cost in enumerate(generalized_costs):
        table._cells[(i+1, 3)]._text.set_text(f'{cost:.2f}')
        if i == optimal_idx:
            for j in range(4):
                table._cells[(i+1, j)].set_facecolor('#fffacd')  # 淡黄色
        else:
            for j in range(4):
                table._cells[(i+1, j)].set_facecolor('white')
    
    return optimal_marker, vot_text, line, *cost_texts

# 创建动画
vot_values = np.linspace(0, 200, 100)
ani = FuncAnimation(fig, update, frames=vot_values, 
                    interval=100, blit=False, repeat=True)

# 保存为高质量GIF
ani.save('path_selection_animation.gif', writer='pillow', fps=10, dpi=100)

plt.tight_layout()
plt.show()