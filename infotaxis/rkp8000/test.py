import matplotlib.pyplot as plt
import numpy as np



# labels = []
# infotaxis = [744,395,374,407,410,252,243,349,174,485,524,165,453,367,632,434,259,604,348,613]
# dijkstra = [328,322,374,263,410,252,243,349,174,485,524,165,453,367,433,313,259,626,324,613]

# for i in range(20):
#     labels.append("Trial " + str(i+1))

# x = np.arange(len(labels))  # the label locations
# width = 0.4  # the width of the bars

# fig, ax = plt.subplots()
# rects1 = ax.bar(x - width/2, infotaxis, width, label='Infotaxis')
# rects2 = ax.bar(x + width/2, dijkstra, width, label='Infotaxis & Dijkstra')

# # Add some text for labels, title and custom x-axis tick labels, etc.
# ax.set_ylabel('Time steps')
# ax.set_title('10 cell Tunnel shape obstacle with starting point is (1.9, 0.4)')
# ax.set_xticks(x)
# ax.set_xticklabels(labels)
# ax.legend()

# ax.bar_label(rects1, padding=3)
# ax.bar_label(rects2, padding=3)

# fig.tight_layout()

# plt.show()




# Fixing random state for reproducibility
np.random.seed(19680801)


# x = np.array([0.36,1.02,1.02,1.02,1.02,0.2,1.02,1.02,1.0,0.98,1.02,1.02,1.02,1.32,1.02,1.02,1.02,1.02,1.0,1.02,1.02,1.02,1.02,1.0,1.02,1.0,1.26,1.0,1.14,1.02,1.02,0.06,1.02,1.02,1.02,1.02,1.32])
# y = np.array([0.78,0,0.24,0.58,0.31,0.7,0.08,0.04,0,0.82,0.4,0.56,0,0.02,0.06,0,0.56,0.56,0.56,0,0.14,0.02,0,0,0.56,0.56,0.04,0,0.56,0.56,0,0.46,0,1.16,0.54,0,0.02])

# x = np.array([1.32,0.2,1.02,1.02,1.0,0.1,1.32,1.02,0.02,1.26,1.0])
# y = np.array([0.02,0.24,0,0.2,1.0,0.72,0.02,1,0.72,0.04,0])

x = np.array([1.02,1.32,1.02,1.02,1.02,1.02,1.02,1.02,1.02,1.32,1.02,1.02,1.26])
y = np.array([0.12,0.02,0,1,0.96,1,0.94,0.14,0.94,0.02,1,0.72,0.04])

area = 100  # 0 to 15 point radii

plt.scatter(x, y, s=area, alpha=0.5)
plt.show()