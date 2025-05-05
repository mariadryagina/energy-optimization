import matplotlib.pyplot as plt

boat = [0, 2, 4, 6, 8, 10, 20, 50]


old_grid_usage_be = 13.09 # MWh
old_grid_usage_kr = [906.8, 906.8, 906.8, 906.8, 906.8, 906.8, 906.8, 906.8]
old_grid_usage_bj = 145.18

old_cost_be = 24269
old_cost_bj = 264804
old_cost_kr = 1608118

peak_grid_usage_kr = [859.56, 860.46, 861.87, 863.29, 864.75, 866.21, 873.51, 895.41]
peak_grid_usage_be = [0, 0.02, 0.02, 0.09, 0.17, 0.17, 0, 0]
peak_grid_usage_bj = [123.52, 124.72, 126.15, 127.61, 129.07, 130.53, 137.83, 159.73]

peak_bess_throughput_kr = [101740, 95537, 87362, 80747, 73730, 70761, 55495, 40327]
peak_bess_throughput_be = [6764, 3490, 2454, 2312, 2170, 2723]
peak_bess_throughput_bj = [41474, 31575, 28408, 23848, 21071, 21863, 14645, 11631]

peak_boat_throughput_kr = [0, 14376, 12882, 11509, 10526, 9369, 6673, 3771]
peak_boat_throughput_be = [0, 1916, 1402, 1082, 922, 756, 0, 0]
peak_boat_throughput_bj = [0, 7018, 5038, 4489, 3931, 3223, 2380, 1264]

peak_cost_kr = [1440970, 1422105, 1409541, 1400206, 1392958, 1386754, 1364202, 1339059]
peak_cost_be = [0, 271, 271, 387, 722, 722, 0, 0]
peak_cost_bj = [194084, 192804, 191815, 191118, 190808, 190661, 191888, 206593]


# Nord pool: allowing electricity to be sold on Nord pool
nordpool_grid_usage_kr = [864.16, 867.91, 871.45, 875.62, 879.51, 882.86, 898.21, 928.8]
nordpool_grid_usage_be = [1.14, 1.3, 1.38, 1.54, 1.86, 2.16, 0, 0]
nordpool_grid_usage_bj = [134.41, 139.71, 143.07, 147.03, 151.03, 154.08, 167.08, 195.04]

nord_pool_cost_kr = [1452559, 1437663, 1428023, 1422321, 1417250, 1413486, 1400043, 1384664]
nord_pool_cost_be = [3213, 3815, 4204, 4529, 5313, 5635, 0, 0]
nord_pool_cost_bj = [209919, 212876, 213867, 216216, 219144, 220720, 229540, 252160]

nord_pool_revenue_kr = [8296.7, 13231.2, 17355.1, 22790.3, 26966.1, 31044.7, 46942.2, 64605]
nord_pool_revenue_be = [17069.2, 17477.0, 17369.4, 17134.5, 16840.1, 16362.1, 0, 0]
nord_pool_revenue_bj = [19535.4, 27079.3, 30851.9, 35418.3, 40009.6, 42829.3, 53202.5, 64527.1]

nord_bess_throughput_kr = [86941, 82073, 76140, 72248, 67943, 65292, 55829, 44974]
nord_bess_throughput_be = [21757, 11594, 9666, 9233, 7707, 6160, 0, 0]
nord_bess_throughput_bj = [42418, 35886, 29998, 28647, 27706, 22976, 16166, 12101]

nord_boat_throughput_kr = [0, 13185, 11618, 10463, 9581, 8751, 6473, 3798]
nord_boat_throughput_be = [0, 5614, 3284, 2234, 1832, 1569, 0, 0]
nord_boat_throughput_bj = [0, 7657, 6426, 5265, 4550, 4449, 3129, 1687]


# Peak shave
#Grid usage
plt.figure(figsize=(8, 5))
plt.plot(boat, peak_grid_usage_kr, marker='o')
plt.plot(boat, old_grid_usage_kr, color='orange', linestyle='--')
plt.legend('New grid usage', 'Old grid usage')
plt.xlabel('Number of Boats')
plt.ylabel('MWh')
plt.grid(True)
plt.tight_layout()
plt.show()

#Costs
