import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter
from usage_pattern import usage_pattern
import el_cost
from numpy import *

boat = [0, 2, 4, 6, 8, 10, 20, 50]

#_____Original data___________________________________________________________________________________________________________________________  
old_grid_usage_bj = [145.18, 145.18, 145.18, 145.18, 145.18, 145.18, 145.18, 145.18]

reference_grid_usage_bj = [old_grid_usage_bj[i] + 0.07 *11 * boat[i] for i in range(len(old_grid_usage_bj))]

old_cost_bj = [264804, 264804, 264804, 264804, 264804, 264804, 264804, 264804]

boat_load_cost_bj = []

def boat_load_cost(NUMBOAT):
    USE1, _ = usage_pattern(162, 100, 0.9, 60)  # Example usage pattern for a specific day
    USE2, _ = usage_pattern(183, 100, 0.9, 60)  # Example usage pattern for a specific day
    USE3, _ = usage_pattern(204, 100, 0.9, 60)  # Example usage pattern for a specific day
    BOATLOAD1 = zeros((24, 365))
    BOATLOAD2 = zeros((24, 365))
    BOATLOAD3 = zeros((24, 365))
    NUMBOAT1 = 0
    NUMBOAT2 = 0
    NUMBOAT3 = 0
    for b in range(NUMBOAT):
        if b % 3 == 0:
            NUMBOAT1 += 1
        elif b % 3 == 1:
            NUMBOAT2 += 1
        else:
            NUMBOAT3 += 1
    for d in range(365):
        for h in range(24):
            if h == 23:
                BOATLOAD1[h, d] == 0
                BOATLOAD2[h, d] == 0
                BOATLOAD3[h, d] == 0
            else:
                if USE1[h, d] == 1 and USE1[h+1, d] == 0:
                    BOATLOAD1[23, d-1] = 10 * NUMBOAT1
                    BOATLOAD1[0:6, d] = 10 * NUMBOAT1
                elif USE2[h, d] == 1 and USE2[h+1, d] == 0:
                    BOATLOAD2[23, d-1] = 10 * NUMBOAT2
                    BOATLOAD2[0:6, d] = 10 * NUMBOAT2
                elif USE3[h, d] == 1 and USE3[h+1, d] == 0:
                    BOATLOAD3[23, d-1] = 10 * NUMBOAT3
                    BOATLOAD3[0:6, d] = 10 * NUMBOAT3
                else:
                    BOATLOAD1[h-1, d] = 0
                    BOATLOAD2[h-1, d] = 0
                    BOATLOAD3[h-1, d] = 0
            CHARGECOST1 = el_cost.cost(None, None, BOATLOAD1, 61.55, 0.439, 0.113, 1.25)
            CHARGECOST2 = el_cost.cost(None, None, BOATLOAD2, 61.55, 0.439, 0.113, 1.25)
            CHARGECOST3 = el_cost.cost(None, None, BOATLOAD3, 61.55, 0.439, 0.113, 1.25)
            TOTCOST = CHARGECOST1 + CHARGECOST2 + CHARGECOST3
    return TOTCOST
 
for b in boat:
    if b == 0:
        continue  # Skip the first iteration where b is 0
    else:
        boat_load_cost_bj.append(boat_load_cost(b))
 
print("Boat load cost: ", boat_load_cost_bj)

#_____Case 1____________________________________________________________________________________________________________________________
peak_grid_usage_bj = [123.52, 124.72, 126.15, 127.61, 129.07, 130.53, 137.83, 159.73]
peak_bess_throughput_bj = [41474, 31575, 28408, 23848, 21071, 21863, 14645, 11631]
peak_boat_throughput_bj = [0, 7018, 5038, 4489, 3931, 3223, 2380, 1264]

peak_throughput_bj= [peak_bess_throughput_bj[i] + peak_boat_throughput_bj[i] for i in range(len(peak_bess_throughput_bj))]  
peak_cost_bj = [194084, 192804, 191815, 191118, 190808, 190661, 191888, 206593]

#____Case 2____________________________________________________________________________________________________________________________
# Nord pool: allowing electricity to be sold on Nord pool
nordpool_grid_usage_bj = [134.41, 139.71, 143.07, 147.03, 151.03, 154.08, 167.08, 195.04]
nord_pool_cost_bj = [209919, 212876, 213867, 216216, 219144, 220720, 229540, 252160]
nord_pool_revenue_bj = [19535.4, 27079.3, 30851.9, 35418.3, 40009.6, 42829.3, 53202.5, 64527.1]
nord_bess_throughput_bj = [42418, 35886, 29998, 28647, 27706, 22976, 16166, 12101]
nord_boat_throughput_bj = [0, 7657, 6426, 5265, 4550, 4449, 3129, 1687]

nord_throughput_bj= [nord_bess_throughput_bj[i] + nord_boat_throughput_bj[i] for i in range(len(nord_bess_throughput_bj))]

#New costs
optimized_cost_nordpool_bj = [nord_pool_cost_bj[i] - nord_pool_revenue_bj[i] for i in range(len(nord_pool_cost_bj))]

#_____P_bid 0.1___________________________________________________________________________________________________________________________
#region
# ______Case 3____________________________________________________________________________________________________________________________
LFM_grid_usage_01_bj = [138.0, 143.41, 149.04, 153.65, 159.06, 161.95, 178.54, 214.41]
LFM_bess_throughput_01_bj = [56017, 44632, 34969, 32839, 29370, 26880, 19964, 14045]
LFM_boat_throughput_01_bj = [0, 8968, 8187, 6469,  5829,  5131, 3515, 1842]
LFM_cost_01_bj = [ 212164, 215197 , 219929 , 223294,228758 , 230490,243685 ,282724 ]

LFM_throughput_01_bj= [LFM_bess_throughput_01_bj[i] + LFM_boat_throughput_01_bj[i] for i in range(len(LFM_bess_throughput_01_bj))]

#Revenue
# LFM:
LFM_revenue_01_bj = [(3283+7462), (4515+10262), (5747+13062), (6979+15862), (8211+18662), (9443+21462), (15603+35462), (34083+77462)]
LFM_revenue_Nordpool_01_bj = [25792.6 , 33602.1, 39703, 44047.3, 48474.5, 50437.5, 58789.1, 63132.8]   

LFM_total_revenue_01_bj = [LFM_revenue_01_bj[i] + LFM_revenue_Nordpool_01_bj[i] for i in range(len(LFM_revenue_01_bj))]

#New costs
optimized_cost_LFM_01_bj= [LFM_cost_01_bj[i] - LFM_revenue_01_bj[i] - LFM_revenue_Nordpool_01_bj[i] for i in range(len(LFM_cost_01_bj))]

#______Case 4____________________________________________________________________________________________________________________________
# FCR-D up: 
FCR_D_up_revenue_01_bj = [26009.0, 33969.2, 44092.7,49962.7 , 58410.0, 65553.6,  98361.6, 255452.3]

# FCR-D up: 
FCR_D_down_revenue_01_bj = [87280.6,109815.2, 146115.5,162649,191137.4, 206706.0,333123.1, 696786.6]

#New costs
optimized_cost_FCR_D_up_LFM_01_bj = [optimized_cost_LFM_01_bj[i] - FCR_D_up_revenue_01_bj[i]  for i in range(len(optimized_cost_LFM_01_bj))]
optimized_cost_FCR_D_down_LFM_01_bj = [optimized_cost_LFM_01_bj[i] - FCR_D_down_revenue_01_bj[i]  for i in range(len(optimized_cost_LFM_01_bj))]
optimized_cost_FCR_D_LFM_01_bj = [optimized_cost_LFM_01_bj[i] - FCR_D_up_revenue_01_bj[i] - FCR_D_down_revenue_01_bj[i] for i in range(len(optimized_cost_LFM_01_bj))]

#endregion

#_____P_bid 0.2___________________________________________________________________________________________________________________________
#region
# ______Case 3____________________________________________________________________________________________________________________________
LFM_grid_usage_02_bj = [139.72 , 145.51 , 151.88 ,  157.5, 162.49 ,  166.7, 186.34 , 246.47]
LFM_bess_throughput_02_bj = [55317, 42390, 36394 , 32145 , 27748 , 26643, 23445 , 17048]
LFM_boat_throughput_02_bj = [0,9622 ,7825  , 6594 , 5865,5202 , 3302, 2282]
LFM_cost_02_bj = [215810,220009,225596,  230874 , 236936 ,241127 ,262300 ,343927 ]

LFM_throughput_02_bj= [LFM_bess_throughput_02_bj[i] + LFM_boat_throughput_02_bj[i] for i in range(len(LFM_bess_throughput_02_bj))]

#Revenue
# LFM:
LFM_revenue_02_bj = [(6567+14924), (9031+20524), (11495+26124), (13959+31724 ) , (16423+37324), (18887+42924 ), (42924 +70924), (68167+154924)]
LFM_revenue_Nordpool_02_bj = [ 26031.8  , 31904.4 ,36733.6 , 42344.4 , 45659.3,47626.2 , 54352.4 , 79055.2] 

#New costs
optimized_cost_LFM_02_bj= [LFM_cost_02_bj[i] - LFM_revenue_02_bj[i] - LFM_revenue_Nordpool_02_bj[i] for i in range(len(LFM_cost_02_bj))]

#______Case 4____________________________________________________________________________________________________________________________
# FCR-D up: 
FCR_D_up_revenue_02_bj = [26879.4, 34506.8 ,43744.6 , 54116.9 , 58107.7 , 68805.0,119117.9 , 279061.3 ]

# FCR-D up: 
FCR_D_down_revenue_02_bj = [85090.1, 101055.4,128502.9 ,  148270.1,169312.5,189256.3,248754.3, 545269.0]

#New costs
optimized_cost_FCR_D_up_LFM_02_bj = [optimized_cost_LFM_02_bj[i] - FCR_D_up_revenue_02_bj[i]  for i in range(len(optimized_cost_LFM_02_bj))]
optimized_cost_FCR_D_down_LFM_02_bj = [optimized_cost_LFM_02_bj[i] - FCR_D_down_revenue_02_bj[i]  for i in range(len(optimized_cost_LFM_02_bj))]
optimized_cost_FCR_D_LFM_02_bj = [optimized_cost_LFM_02_bj[i] - FCR_D_up_revenue_02_bj[i] - FCR_D_down_revenue_02_bj[i] for i in range(len(optimized_cost_LFM_02_bj))]
#endregion

#_____P_bid 0.3___________________________________________________________________________________________________________________________
#region
# ______Case 3____________________________________________________________________________________________________________________________
LFM_grid_usage_03_bj = [141.56, 149.02 ,157.0 , 163.76 ,170.7 ,178.02  ,  207.25  , 0]
LFM_bess_throughput_03_bj = [ 55144,44505, 41780, 35094  ,34188 ,31397  ,27445, 0 ]
LFM_boat_throughput_03_bj = [0,10021 , 7645 , 7093 ,6336 ,6128  ,4395  , 0 ]
LFM_cost_03_bj = [222885,229032 ,241311 ,249254 ,260600  , 275761,324169 ,0 ]

LFM_throughput_03_bj= [LFM_bess_throughput_03_bj[i] + LFM_boat_throughput_03_bj[i] for i in range(len(LFM_bess_throughput_03_bj))]

#Revenue
# LFM:
LFM_revenue_03_bj = [(9850+22386),(13546+30786), (17242+39186),(20938+47586) , (24634+55986),(28330+64386) , (46810+ 106386) , (102250+232386)]
LFM_revenue_Nordpool_03_bj = [ 26869.2,  32495.2, 39972.9,45661.5 ,50580.6 ,56623.2  ,73757.0 ,0] 

#New costs
optimized_cost_LFM_03_bj= [LFM_cost_03_bj[i] - LFM_revenue_03_bj[i] - LFM_revenue_Nordpool_03_bj[i] for i in range(len(LFM_cost_03_bj))]

#______Case 4____________________________________________________________________________________________________________________________
# FCR-D up: 
FCR_D_up_revenue_03_bj = [29880.4,40306.8 , 51606.1, 59962.7, 71378.4 ,81765.5 , 131701.4 , 0 ]

# FCR-D up: 
FCR_D_down_revenue_03_bj = [79222.2,102532.1, 119952.5, 151593, 163548.8, 181613.5, 275090.1, 0]

#New costs
optimized_cost_FCR_D_up_LFM_03_bj = [optimized_cost_LFM_03_bj[i] - FCR_D_up_revenue_03_bj[i]  for i in range(len(optimized_cost_LFM_03_bj))]
optimized_cost_FCR_D_down_LFM_03_bj = [optimized_cost_LFM_03_bj[i] - FCR_D_down_revenue_03_bj[i]  for i in range(len(optimized_cost_LFM_03_bj))]
optimized_cost_FCR_D_LFM_03_bj = [optimized_cost_LFM_03_bj[i] - FCR_D_up_revenue_03_bj[i] - FCR_D_down_revenue_03_bj[i] for i in range(len(optimized_cost_LFM_03_bj))]
#endregion


#____Per boat, revenue _____________________________________________________________________________________________________________________________
revenue_per_boat_case1_bj = [
    (old_cost_bj[i] - peak_cost_bj[i])  / boat[i]
    if boat[i] != 0 else old_cost_bj[0] - peak_cost_bj[0]  # Skip division if boat[i] is 0
    for i in range(len(peak_bess_throughput_bj))
]

revenue_per_boat_case2_bj = [
    (old_cost_bj[i] - nord_pool_cost_bj[i] + nord_pool_revenue_bj[i]) / boat[i]
    if boat[i] != 0 else old_cost_bj[0] - nord_pool_cost_bj[0] + nord_pool_revenue_bj[0]  # Skip division if boat[i] is 0
    for i in range(len(nord_pool_revenue_bj))
]

revenue_per_boat_case3_bj = [
    (old_cost_bj[i] - LFM_cost_01_bj[i] + LFM_revenue_01_bj[i] + LFM_revenue_Nordpool_01_bj[i]) / boat[i]
    if boat[i] != 0 else old_cost_bj[0] - LFM_cost_01_bj[0] + LFM_revenue_01_bj[0] + LFM_revenue_Nordpool_01_bj[0]  # Skip division if boat[i] is 0
    for i in range(len(LFM_revenue_01_bj))
]
revenue_per_boat_case4_bj = [
    (old_cost_bj[i] - LFM_cost_01_bj[i] + LFM_revenue_01_bj[i] + LFM_revenue_Nordpool_01_bj[i] + FCR_D_down_revenue_01_bj[i] + FCR_D_up_revenue_01_bj[i]) / boat[i]
    if boat[i] != 0 else old_cost_bj[0] - LFM_cost_01_bj[0] + LFM_revenue_01_bj[0] + LFM_revenue_Nordpool_01_bj[0] + FCR_D_down_revenue_01_bj[0] + FCR_D_up_revenue_01_bj[0]  # Skip division if boat[i] is 0
    for i in range(len(LFM_revenue_01_bj))
]


total_revenue_bj = [LFM_total_revenue_01_bj[i] + FCR_D_up_revenue_01_bj[i] + FCR_D_down_revenue_01_bj[i] for i in range(len(nord_pool_revenue_bj))]

#____Calculating cool stuff___________________________________________________________________________________________________________________________
#region
final_cost = [optimized_cost_FCR_D_LFM_01_bj[i] - LFM_revenue_Nordpool_01_bj[i] - LFM_revenue_01_bj[i] - FCR_D_up_revenue_01_bj[i] - FCR_D_down_revenue_01_bj[i] for i in range(len(optimized_cost_FCR_D_LFM_01_bj))]
final_cost_per_boat = [final_cost[i] / boat[i] if boat[i] != 0 else final_cost[0] for i in range(len(final_cost))]
total_savings = [old_cost_bj[i] - final_cost[i] for i in range(len(old_cost_bj))]
total_savings_per_boat = [total_savings[i] / boat[i] if boat[i] != 0 else total_savings[0] for i in range(len(total_savings))]

bess_throughput_participation_factor = [(LFM_bess_throughput_01_bj[i]) / (LFM_bess_throughput_01_bj[i] + (LFM_boat_throughput_01_bj[i] * boat[i])) * 100 for i in range(len(LFM_bess_throughput_01_bj))]
boat_throughput_participation_factor = [(LFM_boat_throughput_01_bj[i] * boat[i]) / (LFM_bess_throughput_01_bj[i] + (LFM_boat_throughput_01_bj[i] * boat[i])) * 100 for i in range(len(LFM_boat_throughput_01_bj))]

print("Reference grid usage: ", reference_grid_usage_bj)
print("Final cost: ", final_cost)
print("Total savings: ", total_savings)
print("Final cost/boat: ", final_cost_per_boat)
print("Total savings/boat: ", total_savings_per_boat)
print("BESS throughput: ", LFM_bess_throughput_01_bj, "participation factor: ", bess_throughput_participation_factor, "%")
print("Boat throughput: ", LFM_boat_throughput_01_bj, "participation factor: ", boat_throughput_participation_factor, "%")
print("Total savings/boat, allocated:", [total_savings_per_boat[i] * (boat_throughput_participation_factor[i] / 100) for i in range(len(total_savings_per_boat))])
#endregion

#__Plotting___________________________________________________________________________________________________________________________
#Grid usage
#region
plt.figure(figsize=(8, 5))
plt.plot(boat, old_grid_usage_bj, color='orange', linestyle='--')
plt.plot(boat, peak_grid_usage_bj, color='olivedrab', marker='.')
plt.plot(boat, nordpool_grid_usage_bj,color='teal', marker='.')
plt.plot(boat, LFM_grid_usage_01_bj, color='indianred', marker='.')
plt.legend(['Reference Case','Case 1: Peak Shaved', 'Case 2: Spot Price', 'Case 3: LFM'])
plt.xlabel('Number of Electric Leisure Boats')
plt.ylabel('Grid usage [MWh]')
plt.grid(True)
plt.tight_layout()
plt.show()

#Energy throughput BESS
plt.figure(figsize=(7, 6))
plt.plot(boat, peak_bess_throughput_bj , color='olivedrab', marker='.')
plt.plot(boat, nord_bess_throughput_bj, color='teal', marker='.')
plt.plot(boat, LFM_bess_throughput_01_bj , color='indianred', marker='.')
plt.legend(['Case 1: Peak Shaved', 'Case 2: Spot Price', 'Case 3: LFM'])
plt.xlabel('Number of Electric Leisure Boats')
plt.ylabel('Electricity Throughput BESS [kWh]')
plt.grid(True)
plt.tight_layout()
plt.show()

#Energy throughput boat
plt.figure(figsize=(7, 6))
plt.plot(boat[1:], peak_boat_throughput_bj[1:] , color='olivedrab', marker='.')
plt.plot(boat[1:], nord_boat_throughput_bj[1:], color='teal', marker='.')
plt.plot(boat[1:], LFM_boat_throughput_01_bj[1:] , color='indianred' , marker='.')
plt.legend(['Case 1: Peak Shaved', 'Case 2: Spot Price', 'Case 3: LFM'])
plt.xlabel('Number of Electric Leisure Boats')
plt.ylabel('Electricity Throughput per Boat [kWh]')
plt.grid(True)
plt.tight_layout()
plt.show()



#Costs
plt.figure(figsize=(7, 6))
#plt.plot(boat, old_cost_bj, color='orange', linestyle='--')
plt.plot(boat, peak_cost_bj , color='olivedrab', marker='.')
plt.plot(boat, nord_pool_cost_bj, marker='.', color='teal')
plt.plot(boat, LFM_cost_01_bj, marker='.', color='indianred')
# plt.plot(boat, optimized_cost_FCR_D_LFM_kr, marker='o')
plt.legend(['Case 1: Peak Shaved', 'Case 2: Spot Price', 'Case 3: LFM '])
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
#plt.plot(boat, old_cost_bj, color='orange', linestyle='--')
plt.plot(boat, peak_cost_bj , color='olivedrab',  marker='.')
plt.plot(boat, nord_pool_cost_bj, marker='.', color='teal', linestyle='--')
plt.plot(boat, optimized_cost_nordpool_bj, marker='.', color='teal')
plt.plot(boat, LFM_cost_01_bj, marker='.', color='indianred', linestyle='--')
plt.plot(boat, optimized_cost_LFM_01_bj, marker='.', color='indianred')
plt.plot(boat, optimized_cost_FCR_D_up_LFM_01_bj, color='lightsteelblue', marker='.', linestyle='--')
plt.plot(boat, optimized_cost_FCR_D_down_LFM_01_bj, color='cornflowerblue', marker='.', linestyle='--')
plt.plot(boat, optimized_cost_FCR_D_LFM_01_bj, color='royalblue', marker='.')
plt.legend(['Optimized cost Case 1: Peak Shaved', 'Optimized cost Case 2: Spot Price', 'Cost after revenue Case 2: Spot Price ', 'Optimized cost Case 3: LFM ', 'Cost after revenue Case 3: LFM', 'Cost after revenue Case 4: FCR-D up', 'Cost after revenue Case 4: FCR-D down', "Cost after revenue Case 4: FCR-D"])
plt.xlabel('Number of Electric Leisure Boats'), 
plt.ylabel('Cost of Electricity [SEK]')
plt.grid(True)
# Force full numbers on the y-axis
formatter = ScalarFormatter(useOffset=False, useMathText=False)
formatter.set_scientific(False)  # Disable scientific notation
plt.gca().yaxis.set_major_formatter(formatter)
plt.show()


#Revenue
plt.figure(figsize=(7, 6))
#plt.plot(boat, old_cost_be, color='orange', linestyle='--')
plt.plot(boat, nord_pool_revenue_bj, marker='.', color='teal')
plt.plot(boat, LFM_total_revenue_01_bj, marker='.', color='indianred')
plt.plot(boat, FCR_D_up_revenue_01_bj, color='lightsteelblue', marker='.')
plt.plot(boat, FCR_D_down_revenue_01_bj, color='cornflowerblue', marker='.')
plt.plot(boat, total_revenue_bj, color='black', marker='.')
plt.legend(['Case 2: Nord Pool', 'Case 3: LFM', 'FCR-D up ', 'FCR-D down', 'Case 4: FCR-D'])
plt.xlabel('Number of Electric Leisure Boats'), 
plt.ylabel('Revenue [SEK]')
plt.grid(True)
# Force full numbers on the y-axis
formatter = ScalarFormatter(useOffset=False, useMathText=False)
formatter.set_scientific(False)  # Disable scientific notation
plt.gca().yaxis.set_major_formatter(formatter)
plt.show()


#Plot energy and cost together
# Plot grid usage on the primary y-axis
fig, ax1 = plt.subplots(figsize=(8, 5))
#ax1.plot(boat, peak_grid_usage_bj, color='olivedrab', marker='.', label='Electricity usage')
#ax1.plot(boat, nordpool_grid_usage_bj, color='teal', marker='.', label='Electricity usage')
ax1.plot(boat, LFM_grid_usage_01_bj, color='indianred', marker='.', label='Electricity usage')
ax1.set_xlabel('Number of Electric Leisure Boats')
ax1.set_ylabel('Grid usage [MWh]', color='black')
ax1.tick_params(axis='y', labelcolor='black')
ax1.grid(True)
# Add a secondary y-axis for cost
ax2 = ax1.twinx()
#ax2.plot(boat, peak_cost_bj, color='olivedrab', marker='.', linestyle='--', label='Cost')
#x2.plot(boat, nord_pool_cost_bj, color='teal', marker='.', linestyle='--', label='Cost')
#ax2.plot(boat, LFM_cost_01_bj, color='indianred', marker='.', linestyle='--', label='Cost')
ax2.plot(boat, optimized_cost_FCR_D_LFM_01_bj, color='indianred', marker='.', linestyle='--', label='Final Cost')
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
plt.plot(boat, revenue_per_boat_case1_bj, color='olivedrab', marker='.')
plt.plot(boat, revenue_per_boat_case2_bj, color='teal', marker='.')
plt.plot(boat, revenue_per_boat_case3_bj, color='indianred', marker='.')
plt.plot(boat, revenue_per_boat_case4_bj, color='royalblue', marker='.')
plt.legend(['Case 1: Peak Shaved', 'Case 2: Spot Price', 'Case 3: LFM', 'Case 4: FCR-D'])
plt.xlabel('Number of Electric Leisure Boats')
plt.ylabel('Revenue per boat [SEK]')
plt.grid(True)
plt.tight_layout()
plt.show()

#endregion

new_grid_usage_kr = [old_grid_usage_bj[i] + 0.007*11*boat[i] for i in range(len(old_grid_usage_bj))]

print(f"Increased grid usage: {[round(value,2) for value in new_grid_usage_kr]}")