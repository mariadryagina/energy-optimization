import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter

boat = [0, 2, 4, 6, 8, 10, 20, 50]

#_____Original data___________________________________________________________________________________________________________________________  
old_grid_usage_be = 13.09 # MWh
old_grid_usage_kr = [906.8, 906.8, 906.8, 906.8, 906.8, 906.8, 906.8, 906.8]
old_grid_usage_bj = 145.18

old_cost_be = 24269
old_cost_bj = 264804
old_cost_kr = [1608118, 1608118, 1608118, 1608118, 1608118, 1608118, 1608118, 1608118]


#_____Case 1____________________________________________________________________________________________________________________________
peak_grid_usage_kr = [859.56, 860.46, 861.87, 863.29, 864.75, 866.21, 873.51, 895.41]
peak_grid_usage_be = [0, 0.02, 0.02, 0.09, 0.17, 0.17, 0, 0]
peak_grid_usage_bj = [123.52, 124.72, 126.15, 127.61, 129.07, 130.53, 137.83, 159.73]

peak_bess_throughput_kr = [101740, 95537, 87362, 80747, 73730, 70761, 55495, 40327]
peak_bess_throughput_be = [6764, 3490, 2454, 2312, 2170, 2723]
peak_bess_throughput_bj = [41474, 31575, 28408, 23848, 21071, 21863, 14645, 11631]

peak_boat_throughput_kr = [0, 14376, 12882, 11509, 10526, 9369, 6673, 3771]
peak_boat_throughput_be = [0, 1916, 1402, 1082, 922, 756, 0, 0]
peak_boat_throughput_bj = [0, 7018, 5038, 4489, 3931, 3223, 2380, 1264]

peak_throughput_kr= [peak_bess_throughput_kr[i] + peak_boat_throughput_kr[i] for i in range(len(peak_bess_throughput_kr))]
peak_throughput_be= [peak_bess_throughput_be[i] + peak_boat_throughput_be[i] for i in range(len(peak_bess_throughput_be))] 
peak_throughput_bj= [peak_bess_throughput_bj[i] + peak_boat_throughput_bj[i] for i in range(len(peak_bess_throughput_bj))]  

peak_cost_kr = [1440970, 1422105, 1409541, 1400206, 1392958, 1386754, 1364202, 1339059]
peak_cost_be = [0, 271, 271, 387, 722, 722, 0, 0]
peak_cost_bj = [194084, 192804, 191815, 191118, 190808, 190661, 191888, 206593]

#____Case 2____________________________________________________________________________________________________________________________
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

nord_throughput_kr= [nord_bess_throughput_kr[i] + nord_boat_throughput_kr[i] for i in range(len(nord_bess_throughput_kr))]
nord_throughput_be= [nord_bess_throughput_be[i] + nord_boat_throughput_be[i] for i in range(len(nord_bess_throughput_be))]
nord_throughput_bj= [nord_bess_throughput_bj[i] + nord_boat_throughput_bj[i] for i in range(len(nord_bess_throughput_bj))]

#New costs
optimized_cost_nordpool_kr = [nord_pool_cost_kr[i] - nord_pool_revenue_kr[i] for i in range(len(nord_pool_cost_kr))]
optimized_cost_nordpool_be = [nord_pool_cost_be[i] - nord_pool_revenue_be[i] for i in range(len(nord_pool_cost_be))]
optimized_cost_nordpool_bj = [nord_pool_cost_bj[i] - nord_pool_revenue_bj[i] for i in range(len(nord_pool_cost_bj))]

#_____P_bid 0.1___________________________________________________________________________________________________________________________
#region
# ______Case 3____________________________________________________________________________________________________________________________
LFM_grid_usage_01_kr = [860.55,  864.9 , 870.72, 875.53, 880.84, 885.72, 905.48, 947.77]
LFM_grid_usage_01_be = [2.42, 2.9, 3.32, 4.2, 5.04, 5.52, 0, 0]
LFM_grid_usage_01_bj = [138.0, 143.41, 149.04, 153.65, 159.06, 161.95, 178.54, 214.41]

LFM_bess_throughput_01_kr = [114142, 106131, 96510, 87003, 83137, 77825, 63501, 40565]
LFM_bess_throughput_01_be = [23854, 14333, 9946, 9887, 8230 , 7389 ]
LFM_bess_throughput_01_bj = [56017, 44632, 34969, 32839, 29370, 26880, 19964, 14045]

LFM_boat_throughput_01_kr = [0, 16515, 14499, 13565, 12198, 11388, 7923 , 4464]
LFM_boat_throughput_01_be = [0, 4576, 3306, 2184 , 1831, 1456, 0, 0]
LFM_boat_throughput_01_bj = [0, 8968, 8187, 6469,  5829,  5131, 3515, 1842]

LFM_cost_01_kr = [1440170 , 1425957, 1420173, 1415729, 1413978, 1411829, 1408106, 1419099]
LFM_cost_01_be = [5085, 5780, 6194, 7476, 8996, 9955, 0, 0]
LFM_cost_01_bj = [194084, 192804, 191815, 191118, 190808, 190661, 191888, 206593]

LFM_throughput_01_kr= [LFM_bess_throughput_01_kr[i] + LFM_boat_throughput_01_kr[i] for i in range(len(LFM_bess_throughput_01_kr))]  
LFM_throughput_01_be= [LFM_bess_throughput_01_be[i] + LFM_boat_throughput_01_be[i] for i in range(len(LFM_bess_throughput_01_be))]
LFM_throughput_01_bj= [LFM_bess_throughput_01_bj[i] + LFM_boat_throughput_01_bj[i] for i in range(len(LFM_bess_throughput_01_bj))]

#Revenue
# LFM:
LFM_revenue_01_kr = [(3283+7462), (4515+10262), (5747+13062), (6979+15862) , (8211+18662), (9443+21462), (15603+35462), (34083+77462)]
LFM_revenue_01_be = [(3283+7462), (4515+10262), (5747+13062), (6979+15862), (8211+18662), (9443+21462), 0, 0]
LFM_revenue_01_bj = [(3283+7462), (4515+10262), (5747+13062), (6979+15862), (8211+18662), (9443+21462), (15603+35462), (34083+77462)]

LFM_revenue_Nordpool_01_kr = [15689.4, 24150.6, 36722.0, 47535.2 , 53817.2, 60691.1, 87115.7, 107199.7]
LFM_revenue_Nordpool_01_be = [16809.0, 16075.2 , 15426.8 , 14923.6, 14191.7 , 12750.6, 0, 0] 
LFM_revenue_Nordpool_01_bj = [25792.6 , 33602.1, 39703, 44047.3, 48474.5, 50437.5, 58789.1, 63132.8]   

#New costs
optimized_cost_LFM_01_kr= [LFM_cost_01_kr[i] - LFM_revenue_01_kr[i] - LFM_revenue_Nordpool_01_kr[i] for i in range(len(LFM_cost_01_kr))]
optimized_cost_LFM_01_be= [LFM_cost_01_be[i] - LFM_revenue_01_be[i] - LFM_revenue_Nordpool_01_be[i] for i in range(len(LFM_cost_01_be))]
optimized_cost_LFM_01_bj= [LFM_cost_01_bj[i] - LFM_revenue_01_bj[i] - LFM_revenue_Nordpool_01_bj[i] for i in range(len(LFM_cost_01_bj))]

#______Case 4____________________________________________________________________________________________________________________________
# FCR-D up: 
FCR_D_up_revenue_01_kr = [22671.5, 28914.1, 35422.9,  43437.3, 52581.0, 61113.0, 98670.5, 197662.2]
FCR_D_up_revenue_01_be = [22756.2,30517.5,31623.4,28296.4, 41305.3, 49801.3, 0, 0]
FCR_D_up_revenue_01_bj = [26009.0, 33969.2, 44092.7,49962.7 , 58410.0, 65553.6,  98361.6, 255452.3]

# FCR-D up: 
FCR_D_down_revenue_01_kr = [92152, 115428.1, 136467.5, 165199.1, 187236.4, 224826.7, 389319.6,  854701.1]
FCR_D_down_revenue_01_be = [97729.6,132102.8,192188.9,289707.5, 336921.9,366774.0, 0, 0]
FCR_D_down_revenue_01_bj = [87280.6,109815.2, 146115.5,162649,191137.4, 206706.0,333123.1, 696786.6]

#New costs
optimized_cost_FCR_D_up_LFM_01_kr = [optimized_cost_LFM_01_kr[i] - FCR_D_up_revenue_01_kr[i]  for i in range(len(optimized_cost_LFM_01_kr))]
optimized_cost_FCR_D_up_LFM_01_be = [optimized_cost_LFM_01_be[i] - FCR_D_up_revenue_01_be[i]  for i in range(len(optimized_cost_LFM_01_be))]
optimized_cost_FCR_D_up_LFM_01_bj = [optimized_cost_LFM_01_bj[i] - FCR_D_up_revenue_01_bj[i]  for i in range(len(optimized_cost_LFM_01_bj))]

optimized_cost_FCR_D_down_LFM_01_kr = [optimized_cost_LFM_01_kr[i] - FCR_D_down_revenue_01_kr[i]  for i in range(len(optimized_cost_LFM_01_kr))]
optimized_cost_FCR_D_down_LFM_01_be = [optimized_cost_LFM_01_be[i] - FCR_D_down_revenue_01_be[i]  for i in range(len(optimized_cost_LFM_01_be))]
optimized_cost_FCR_D_down_LFM_01_bj = [optimized_cost_LFM_01_bj[i] - FCR_D_down_revenue_01_bj[i]  for i in range(len(optimized_cost_LFM_01_bj))]

optimized_cost_FCR_D_LFM_01_kr = [optimized_cost_LFM_01_kr[i] - FCR_D_up_revenue_01_kr[i] - FCR_D_down_revenue_01_kr[i] for i in range(len(optimized_cost_LFM_01_kr))]
optimized_cost_FCR_D_LFM_01_be = [optimized_cost_LFM_01_be[i] - FCR_D_up_revenue_01_be[i] - FCR_D_down_revenue_01_be[i] for i in range(len(optimized_cost_LFM_01_be))]
optimized_cost_FCR_D_LFM_01_bj = [optimized_cost_LFM_01_bj[i] - FCR_D_up_revenue_01_bj[i] - FCR_D_down_revenue_01_bj[i] for i in range(len(optimized_cost_LFM_01_bj))]

#endregion

#_____P_bid 0.2___________________________________________________________________________________________________________________________
#region
# ______Case 3____________________________________________________________________________________________________________________________
LFM_grid_usage_02_kr = [862.25,  868.2  , 873.96 , 880.18,  887.14 , 891.9 , 915.3, 970.61 ]
LFM_grid_usage_02_be = [3.62,4.82,6.25,0,0,0,0,0]
LFM_grid_usage_02_bj = [139.72 , 145.51 , 151.88 ,  157.5, 162.49 ,  166.7, 186.34 , 246.47]

LFM_bess_throughput_02_kr = [114291, 104619, 95491, 86090, 83420 , 79648, 59175 , 45829]
LFM_bess_throughput_02_be = [23865, 13645, 11595,0,0,0,0,0]
LFM_bess_throughput_02_bj = [55317, 42390, 36394 , 32145 , 27748 , 26643, 23445 , 17048]

LFM_boat_throughput_02_kr = [0, 16344 , 14772,  13875 , 12252 , 11005 ,7994, 4541]
LFM_boat_throughput_02_be = [0, 4757, 3076,0,0,0,0,0]
LFM_boat_throughput_02_bj = [0,9622 ,7825  , 6594 , 5865,5202 , 3302, 2282]

LFM_cost_02_kr = [1443234 , 1433550 ,1427009 , 1426009, 1426214 ,  1427093 , 1430323 , 1471090 ]
LFM_cost_02_be = [7768, 9222, 12372,0,0,0,0,0]
LFM_cost_02_bj = [215810,220009,225596,  230874 , 236936 ,241127 ,262300 ,343927 ]

LFM_throughput_02_kr= [LFM_bess_throughput_02_kr[i] + LFM_boat_throughput_02_kr[i] for i in range(len(LFM_bess_throughput_02_kr))]  
LFM_throughput_02_be= [LFM_bess_throughput_02_be[i] + LFM_boat_throughput_02_be[i] for i in range(len(LFM_bess_throughput_02_be))]
LFM_throughput_02_bj= [LFM_bess_throughput_02_bj[i] + LFM_boat_throughput_02_bj[i] for i in range(len(LFM_bess_throughput_02_bj))]

#Revenue
# LFM:
LFM_revenue_02_kr = [(6567+14924), (9031+20524), (11495+26124), (13959+31724 ) , (16423+37324), (18887+42924 ), (42924 +70924), (68167+154924)]
LFM_revenue_02_be = [(6567+14924), (9031+20524), (11495+26124), 0, 0, 0, 0, 0]
LFM_revenue_02_bj = [(6567+14924), (9031+20524), (11495+26124), (13959+31724 ) , (16423+37324), (18887+42924 ), (42924 +70924), (68167+154924)]

#New costs
optimized_cost_LFM_02_kr= [LFM_cost_02_kr[i] - LFM_revenue_02_kr[i] for i in range(len(LFM_cost_02_kr))]
optimized_cost_LFM_02_be= [LFM_cost_02_be[i] - LFM_revenue_02_be[i] for i in range(len(LFM_cost_02_be))]
optimized_cost_LFM_02_bj= [LFM_cost_02_bj[i] - LFM_revenue_02_bj[i] for i in range(len(LFM_cost_02_bj))]

#______Case 4____________________________________________________________________________________________________________________________
# FCR-D up: 
FCR_D_up_revenue_02_kr = [22638.1,30389.1 ,35245.4 ,45048.4 , 53155.5, 62797.9 , 100682.5 , 215814]
FCR_D_up_revenue_02_be = [27209.1,42185.5, 49218.4,0,0,0,0,0]
FCR_D_up_revenue_02_bj = [26879.4, 34506.8 ,43744.6 , 54116.9 , 58107.7 , 68805.0,119117.9 , 279061.3 ]

# FCR-D up: 
FCR_D_down_revenue_02_kr = [91597.4,111764.6 ,129560.2 , 155571.2 , 178078.3 , 209068.6 , 364260.1,757333.8 ]
FCR_D_down_revenue_02_be = [76158.0,88418.9, 151125.8,0,0,0,0,0]
FCR_D_down_revenue_02_bj = [85090.1, 101055.4,128502.9 ,  148270.1,169312.5,189256.3,248754.3, 545269.0]

#New costs
optimized_cost_FCR_D_LFM_02_kr = [optimized_cost_LFM_02_kr[i] - FCR_D_up_revenue_02_kr[i] - FCR_D_down_revenue_02_kr[i] for i in range(len(optimized_cost_LFM_02_kr))]
optimized_cost_FCR_D_LFM_02_be = [optimized_cost_LFM_02_be[i] - FCR_D_up_revenue_02_be[i] - FCR_D_down_revenue_02_be[i] for i in range(len(optimized_cost_LFM_02_be))]
optimized_cost_FCR_D_LFM_02_bj = [optimized_cost_LFM_02_bj[i] - FCR_D_up_revenue_02_bj[i] - FCR_D_down_revenue_02_bj[i] for i in range(len(optimized_cost_LFM_02_bj))]
#endregion


#____Per boat, revenue _____________________________________________________________________________________________________________________________
revenue_per_boat_case1_kr = [
    (old_cost_kr[i] - peak_cost_kr[i])  / boat[i]
    if boat[i] != 0 else old_cost_kr[0] - peak_cost_kr[0]  # Skip division if boat[i] is 0
    for i in range(len(peak_bess_throughput_kr))
]

revenue_per_boat_case2_kr = [
    (old_cost_kr[i] - nord_pool_cost_kr[i] + nord_pool_revenue_kr[i]) / boat[i]
    if boat[i] != 0 else old_cost_kr[0] - nord_pool_cost_kr[0] + nord_pool_revenue_kr[0]  # Skip division if boat[i] is 0
    for i in range(len(nord_pool_revenue_kr))
]

revenue_per_boat_case3_kr = [
    (old_cost_kr[i] - LFM_cost_01_kr[i] + LFM_revenue_01_kr[i] + LFM_revenue_Nordpool_01_kr[i]) / boat[i]
    if boat[i] != 0 else old_cost_kr[0] - LFM_cost_01_kr[0] + LFM_revenue_01_kr[0] + LFM_revenue_Nordpool_01_kr[0]  # Skip division if boat[i] is 0
    for i in range(len(LFM_revenue_01_kr))
]
revenue_per_boat_case4_kr = [
    (old_cost_kr[i] - LFM_cost_01_kr[i] + LFM_revenue_01_kr[i] + LFM_revenue_Nordpool_01_kr[i] + FCR_D_down_revenue_01_kr[i] + FCR_D_up_revenue_01_kr[i]) / boat[i]
    if boat[i] != 0 else old_cost_kr[0] - LFM_cost_01_kr[0] + LFM_revenue_01_kr[0] + LFM_revenue_Nordpool_01_kr[0] + FCR_D_down_revenue_01_kr[0] + FCR_D_up_revenue_01_kr[0]  # Skip division if boat[i] is 0
    for i in range(len(LFM_revenue_01_kr))
]

#__Plotting___________________________________________________________________________________________________________________________
#Grid usage
plt.figure(figsize=(8, 5))
plt.plot(boat, old_grid_usage_kr, color='orange', linestyle='--')
plt.plot(boat, peak_grid_usage_kr, color='olivedrab', marker='.')
plt.plot(boat, nordpool_grid_usage_kr,color='teal', marker='.')
plt.plot(boat, LFM_grid_usage_01_kr, color='indianred', marker='.')
plt.legend(['Reference Case','Case 1: Peak Shaved', 'Case 2: Spot Price', 'Case 3: LFM'])
plt.xlabel('Number of Electric Leisure Boats')
plt.ylabel('Grid usage [MWh]')
plt.grid(True)
plt.tight_layout()
plt.show()

#Energy throughput BESS
plt.figure(figsize=(8, 5))
plt.plot(boat, peak_bess_throughput_kr , color='olivedrab', marker='.')
plt.plot(boat, nord_bess_throughput_kr, color='teal', marker='.')
plt.plot(boat, LFM_bess_throughput_01_kr , color='indianred', marker='.')
plt.legend(['Case 1: Peak Shaved', 'Case 2: Spot Price', 'Case 3: LFM'])
plt.xlabel('Number of Electric Leisure Boats')
plt.ylabel('Electricity Throughput BESS [kWh]')
plt.grid(True)
plt.tight_layout()
plt.show()

#Energy throughput boat
plt.figure(figsize=(8, 5))
plt.plot(boat[1:], peak_boat_throughput_kr[1:] , color='olivedrab', marker='.')
plt.plot(boat[1:], nord_boat_throughput_kr[1:], color='teal', marker='.')
plt.plot(boat[1:], LFM_boat_throughput_01_kr[1:] , color='indianred' , marker='.')
plt.legend(['Case 1: Peak Shaved', 'Case 2: Spot Price', 'Case 3: LFM'])
plt.xlabel('Number of Electric Leisure Boats')
plt.ylabel('Electricity Throughput per Boat [kWh]')
plt.grid(True)
plt.tight_layout()
plt.show()



#Costs
plt.figure(figsize=(8, 5))
#plt.plot(boat, old_cost_kr, color='orange', linestyle='--')
plt.plot(boat, peak_cost_kr , color='olivedrab', marker='.')
plt.plot(boat, nord_pool_cost_kr, marker='.', color='teal', linestyle='--')
plt.plot(boat, optimized_cost_nordpool_kr, marker='.', color='teal')
plt.plot(boat, LFM_cost_01_kr, marker='.', color='indianred', linestyle='--')
plt.plot(boat, optimized_cost_LFM_01_kr, marker='.', color='indianred')
# plt.plot(boat, optimized_cost_FCR_D_LFM_kr, marker='o')
plt.legend(['Optimized cost Case 1: Peak Shaved', 'Optimized cost Case 2: Spot Price', 'Cost after revenue Case 2: Spot Price ', 'Optimized cost Case 3: LFM ', 'Cost after revenue Case 3: LFM'])
plt.xlabel('Number of Electric Leisure Boats')
plt.ylabel('Cost of Electricity [SEK]')
plt.grid(True)
# Force full numbers on the y-axis
formatter = ScalarFormatter(useOffset=False, useMathText=False)
formatter.set_scientific(False)  # Disable scientific notation
plt.gca().yaxis.set_major_formatter(formatter)
plt.show()

#Case 4
#Costs
plt.figure(figsize=(8, 5))
#plt.plot(boat, old_cost_kr, color='orange', linestyle='--')
plt.plot(boat, peak_cost_kr , color='olivedrab',  marker='.')
plt.plot(boat, nord_pool_cost_kr, marker='.', color='teal', linestyle='--')
plt.plot(boat, optimized_cost_nordpool_kr, marker='.', color='teal')
plt.plot(boat, LFM_cost_01_kr, marker='.', color='indianred', linestyle='--')
plt.plot(boat, optimized_cost_LFM_01_kr, marker='.', color='indianred')
plt.plot(boat, optimized_cost_FCR_D_up_LFM_01_kr, color='lightsteelblue', marker='.', linestyle='--')
plt.plot(boat, optimized_cost_FCR_D_down_LFM_01_kr, color='cornflowerblue', marker='.', linestyle='--')
plt.plot(boat, optimized_cost_FCR_D_LFM_01_kr, color='royalblue', marker='.')
plt.legend(['Optimized cost Case 1: Peak Shaved', 'Optimized cost Case 2: Spot Price', 'Cost after revenue Case 2: Spot Price ', 'Optimized cost Case 3: LFM ', 'Cost after revenue Case 3: LFM', 'Cost after revenue Case 4: FCR-D up', 'Cost after revenue Case 4: FCR-D down', "Cost after revenue Case 4: FCR-D"])
plt.xlabel('Number of Electric Leisure Boats'), 
plt.ylabel('Cost of Electricity [SEK]')
plt.grid(True)
# Force full numbers on the y-axis
formatter = ScalarFormatter(useOffset=False, useMathText=False)
formatter.set_scientific(False)  # Disable scientific notation
plt.gca().yaxis.set_major_formatter(formatter)
plt.show()

#Plot energy and cost together
# Plot grid usage on the primary y-axis
fig, ax1 = plt.subplots(figsize=(8, 5))
#ax1.plot(boat, peak_grid_usage_kr, color='olivedrab', marker='.', label='Electricity usage')
ax1.plot(boat, nordpool_grid_usage_kr, color='teal', marker='.', label='Elelctricity usage')
#ax1.plot(boat, LFM_grid_usage_01_kr, color='indianred', marker='.', label='Case 3')
ax1.set_xlabel('Number of Electric Leisure Boats')
ax1.set_ylabel('Grid usage [MWh]', color='black')
ax1.tick_params(axis='y', labelcolor='black')
ax1.grid(True)

# Add a secondary y-axis for cost
ax2 = ax1.twinx()
#ax2.plot(boat, peak_cost_kr, color='olivedrab', marker='.', linestyle='--', label='Cost')
ax2.plot(boat, optimized_cost_nordpool_kr, color='teal', marker='.', linestyle='--', label='Cost of Electricity')
#ax2.plot(boat, optimized_cost_LFM_01_bj, color='indianred', marker='.', linestyle='--', label='Cost')
ax2.set_ylabel('Cost of Electricity [SEK]', color='dimgrey')
ax2.tick_params(axis='y', labelcolor='dimgrey')

# Force full numbers on the y-axis
formatter = ScalarFormatter(useOffset=False, useMathText=False)
formatter.set_scientific(False)  # Disable scientific notation
plt.gca().yaxis.set_major_formatter(formatter)

# Combine legends from both axes
lines_1, labels_1 = ax1.get_legend_handles_labels()
lines_2, labels_2 = ax2.get_legend_handles_labels()
ax1.legend(lines_1 + lines_2, labels_1 + labels_2, loc='upper left')
plt.tight_layout()
plt.show()


#Plot revenue per boat
plt.figure(figsize=(8, 5))
plt.plot(boat, revenue_per_boat_case1_kr, color='olivedrab', marker='.')
plt.plot(boat, revenue_per_boat_case2_kr, color='teal', marker='.')
plt.plot(boat, revenue_per_boat_case3_kr, color='indianred', marker='.')
plt.plot(boat, revenue_per_boat_case4_kr, color='royalblue', marker='.')
plt.legend(['Case 1: Peak Shaved', 'Case 2: Spot Price', 'Case 3: LFM', 'Case 4: FCR-D'])
plt.xlabel('Number of Electric Leisure Boats')
plt.ylabel('Revenue per boat [SEK]')
plt.grid(True)
plt.tight_layout()
plt.show()

