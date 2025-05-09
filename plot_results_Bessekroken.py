import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter
from usage_pattern import usage_pattern
import el_price
from numpy import *
import pandas as pd
spotprice = el_price.spotprice_2023

boat = [0, 2, 4, 6, 8, 10]

#_____Original data___________________________________________________________________________________________________________________________  
old_grid_usage_be = [13.09, 13.09, 13.09, 13.09, 13.09, 13.09] # MWh
reference_grid_usage_be = [old_grid_usage_be[i] + 0.07 *11 * boat[i] for i in range(len(old_grid_usage_be))]

boat_load_cost_be = []

old_cost_be = [24269, 24269, 24269, 24269, 24269, 24269] # SEK

def boat_load_cost(NUMBOAT, SPOTPRICE):
    USE1, _ = usage_pattern(162, 100, 0.9, 60)  # Example usage pattern for a specific day
    USE2, _ = usage_pattern(183, 100, 0.9, 60)  # Example usage pattern for a specific day
    USE3, _ = usage_pattern(204, 100, 0.9, 60)  # Example usage pattern for a specific day
    BOATLOAD1 = zeros((24, 365))
    BOATLOAD2 = zeros((24, 365))
    BOATLOAD3 = zeros((24, 365))
    BOATCOST1 = zeros((24, 365))
    BOATCOST2 = zeros((24, 365))
    BOATCOST3 = zeros((24, 365))
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
                BOATLOAD1[h, d] = 0
                BOATLOAD2[h, d] = 0
                BOATLOAD3[h, d] = 0
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
    for d in range(365):
        for h in range(24):
            BOATCOST1[h, d] = (SPOTPRICE[h, d] + 0.439 + 0.113) * BOATLOAD1[h, d] * 1.25
            BOATCOST2[h, d] = (SPOTPRICE[h, d] + 0.439 + 0.113) * BOATLOAD2[h, d] * 1.25
            BOATCOST3[h, d] = (SPOTPRICE[h, d] + 0.439 + 0.113) * BOATLOAD3[h, d] * 1.25
    TOTCOST = BOATCOST1.sum() + BOATCOST2.sum() + BOATCOST3.sum()
    return TOTCOST, BOATCOST1, BOATCOST2, BOATCOST3, BOATLOAD1, BOATLOAD2, BOATLOAD3

for b in boat:
    if b == 0:
        boat_load_cost_be.append(0)
    else:
        total_cost, _, _, _, _, _, _ = boat_load_cost(b, spotprice)
        boat_load_cost_be.append(float(total_cost))

reference_cost_be = [old_cost_be[i] + boat_load_cost_be[i] for i in range(len(old_cost_be))]
print("Boat load cost: ", boat_load_cost_be)
print("Reference cost: ", reference_cost_be)


#_____Case 1____________________________________________________________________________________________________________________________

peak_grid_usage_be = [0, 0.02, 0.02, 0.09, 0.17, 0.17]
peak_bess_throughput_be = [6764, 3490, 2454, 2312, 2170, 2723]
peak_boat_throughput_be = [0, 1916, 1402, 1082, 922, 756]

peak_throughput_be= [peak_bess_throughput_be[i] + peak_boat_throughput_be[i] for i in range(len(peak_bess_throughput_be))] 

peak_cost_be = [0, 271, 271, 387, 722, 722]


#____Case 2____________________________________________________________________________________________________________________________
# Nord pool: allowing electricity to be sold on Nord pool
nordpool_grid_usage_be = [1.14, 1.3, 1.38, 1.54, 1.86, 2.16]
nord_pool_cost_be = [3213, 3815, 4204, 4529, 5313, 5635]
nord_pool_revenue_be = [17069.2, 17477.0, 17369.4, 17134.5, 16840.1, 16362.1]
nord_bess_throughput_be = [21757, 11594, 9666, 9233, 7707, 6160]
nord_boat_throughput_be = [0, 5614, 3284, 2234, 1832, 1569]

nord_throughput_be= [nord_bess_throughput_be[i] + nord_boat_throughput_be[i] for i in range(len(nord_bess_throughput_be))]


#New costs
optimized_cost_nordpool_be = [nord_pool_cost_be[i] - nord_pool_revenue_be[i] for i in range(len(nord_pool_cost_be))]


#_____P_bid 0.1___________________________________________________________________________________________________________________________
#region
# ______Case 3____________________________________________________________________________________________________________________________
LFM_grid_usage_01_be = [2.42, 2.9, 3.32, 4.2, 5.04, 5.52]
LFM_bess_throughput_01_be = [23854, 14333, 9946, 9887, 8230 , 7389]
LFM_boat_throughput_01_be = [0, 4576, 3306, 2184 , 1831, 1456]
LFM_cost_01_be = [5085, 5780, 6194, 7476, 8996, 9955]

LFM_throughput_01_be= [LFM_bess_throughput_01_be[i] + LFM_boat_throughput_01_be[i] for i in range(len(LFM_bess_throughput_01_be))]

#Revenue
# LFM:
LFM_revenue_01_be = [(3283+7462), (4515+10262), (5747+13062), (6979+15862), (8211+18662), (9443+21462)]
LFM_revenue_Nordpool_01_be = [16809.0, 16075.2 , 15426.8 , 14923.6, 14191.7 , 12750.6] 
LFM_total_revenue_01_be = [LFM_revenue_01_be[i] + LFM_revenue_Nordpool_01_be[i] for i in range(len(LFM_revenue_01_be))]


#New costs
optimized_cost_LFM_01_be= [LFM_cost_01_be[i] - LFM_revenue_01_be[i] - LFM_revenue_Nordpool_01_be[i] for i in range(len(LFM_cost_01_be))]


#______Case 4____________________________________________________________________________________________________________________________
# FCR-D up: 
FCR_D_up_revenue_01_be = [22756.2,30517.5,31623.4,28296.4, 41305.3, 49801.3]

# FCR-D up: 
FCR_D_down_revenue_01_be = [97729.6,132102.8,192188.9,289707.5, 336921.9,366774.0]


#New costs
optimized_cost_FCR_D_up_LFM_01_be = [optimized_cost_LFM_01_be[i] - FCR_D_up_revenue_01_be[i]  for i in range(len(optimized_cost_LFM_01_be))]
optimized_cost_FCR_D_down_LFM_01_be = [optimized_cost_LFM_01_be[i] - FCR_D_down_revenue_01_be[i]  for i in range(len(optimized_cost_LFM_01_be))]
optimized_cost_FCR_D_LFM_01_be = [optimized_cost_LFM_01_be[i] - FCR_D_up_revenue_01_be[i] - FCR_D_down_revenue_01_be[i] for i in range(len(optimized_cost_LFM_01_be))]

#endregion

#_____P_bid 0.2___________________________________________________________________________________________________________________________
#region
# ______Case 3____________________________________________________________________________________________________________________________
LFM_grid_usage_02_be = [3.62,4.82,6.25,0,0,0,0,0]
LFM_bess_throughput_02_be = [23865, 13645, 11595,0,0,0,0,0]
LFM_boat_throughput_02_be = [0, 4757, 3076,0,0,0,0,0]
LFM_cost_02_be = [7768, 9222, 12372,0,0,0,0,0]

LFM_throughput_02_be= [LFM_bess_throughput_02_be[i] + LFM_boat_throughput_02_be[i] for i in range(len(LFM_bess_throughput_02_be))]


#Revenue
# LFM:
LFM_revenue_02_be = [(6567+14924), (9031+20524), (11495+26124), 0, 0, 0, 0, 0]
LFM_revenue_Nordpool_02_be = [15306.2,  14232.4  , 13803.9 , 12813.7 , 0 , 0, 0, 0] 

#New costs
optimized_cost_LFM_02_be= [LFM_cost_02_be[i] - LFM_revenue_02_be[i] - LFM_revenue_Nordpool_02_be[i] for i in range(len(LFM_cost_02_be))]


#______Case 4____________________________________________________________________________________________________________________________
# FCR-D up: 
FCR_D_up_revenue_02_be = [27209.1,42185.5, 49218.4,0,0,0,0,0]

# FCR-D up: 
FCR_D_down_revenue_02_be = [76158.0,88418.9, 151125.8,0,0,0,0,0]

#New costs
optimized_cost_FCR_D_up_LFM_02_be = [optimized_cost_LFM_02_be[i] - FCR_D_up_revenue_02_be[i]  for i in range(len(optimized_cost_LFM_02_be))]
optimized_cost_FCR_D_down_LFM_02_be = [optimized_cost_LFM_02_be[i] - FCR_D_down_revenue_02_be[i]  for i in range(len(optimized_cost_LFM_02_be))]
optimized_cost_FCR_D_LFM_02_be = [optimized_cost_LFM_02_be[i] - FCR_D_up_revenue_02_be[i] - FCR_D_down_revenue_02_be[i] for i in range(len(optimized_cost_LFM_02_be))]

#endregion



#____Per boat, revenue _____________________________________________________________________________________________________________________________
revenue_per_boat_case1_be = [
    (old_cost_be[i] - peak_cost_be[i])  / boat[i]
    if boat[i] != 0 else old_cost_be[0] - peak_cost_be[0]  # Skip division if boat[i] is 0
    for i in range(len(peak_bess_throughput_be))
]

revenue_per_boat_case2_be = [
    (old_cost_be[i] - nord_pool_cost_be[i] + nord_pool_revenue_be[i]) / boat[i]
    if boat[i] != 0 else old_cost_be[0] - nord_pool_cost_be[0] + nord_pool_revenue_be[0]  # Skip division if boat[i] is 0
    for i in range(len(nord_pool_revenue_be))
]

revenue_per_boat_case3_be = [
    (old_cost_be[i] - LFM_cost_01_be[i] + LFM_revenue_01_be[i] + LFM_revenue_Nordpool_01_be[i]) / boat[i]
    if boat[i] != 0 else old_cost_be[0] - LFM_cost_01_be[0] + LFM_revenue_01_be[0] + LFM_revenue_Nordpool_01_be[0]  # Skip division if boat[i] is 0
    for i in range(len(LFM_revenue_01_be))
]
revenue_per_boat_case4_be = [
    (old_cost_be[i] - LFM_cost_01_be[i] + LFM_revenue_01_be[i] + LFM_revenue_Nordpool_01_be[i] + FCR_D_down_revenue_01_be[i] + FCR_D_up_revenue_01_be[i]) / boat[i]
    if boat[i] != 0 else old_cost_be[0] - LFM_cost_01_be[0] + LFM_revenue_01_be[0] + LFM_revenue_Nordpool_01_be[0] + FCR_D_down_revenue_01_be[0] + FCR_D_up_revenue_01_be[0]  # Skip division if boat[i] is 0
    for i in range(len(LFM_revenue_01_be))
]

#Total revenue
total_revenue_be = [LFM_total_revenue_01_be[i] + FCR_D_up_revenue_01_be[i] + FCR_D_down_revenue_01_be[i] for i in range(len(nord_pool_revenue_be))]

final_cost = [optimized_cost_FCR_D_LFM_01_be[i] - LFM_revenue_Nordpool_01_be[i] - LFM_revenue_01_be[i] - FCR_D_up_revenue_01_be[i] - FCR_D_down_revenue_01_be[i] for i in range(len(optimized_cost_FCR_D_LFM_01_be))]
final_cost_per_boat = [final_cost[i] / boat[i] if boat[i] != 0 else final_cost[0] for i in range(len(final_cost))]
total_savings = [reference_cost_be[i] - final_cost[i] for i in range(len(old_cost_be))]
total_savings_per_boat = [total_savings[i] / boat[i] if boat[i] != 0 else total_savings[0] for i in range(len(total_savings))]

bess_throughput_participation_factor = [(LFM_bess_throughput_01_be[i]) / (LFM_bess_throughput_01_be[i] + (LFM_boat_throughput_01_be[i] * boat[i])) * 100 for i in range(len(LFM_bess_throughput_01_be))]
boat_throughput_participation_factor = [(LFM_boat_throughput_01_be[i] * boat[i]) / (LFM_bess_throughput_01_be[i] + (LFM_boat_throughput_01_be[i] * boat[i])) * 100 for i in range(len(LFM_boat_throughput_01_be))]

print("Reference grid usage: ", reference_grid_usage_be)
print("Final cost: ", final_cost)
print("Total savings: ", total_savings)
print("Final cost/boat: ", final_cost_per_boat)
print("Total savings/boat: ", total_savings_per_boat)
print("BESS throughput: ", LFM_bess_throughput_01_be, "participation factor: ", bess_throughput_participation_factor, "%")
print("Boat throughput: ", LFM_boat_throughput_01_be, "participation factor: ", boat_throughput_participation_factor, "%")
print("Total savings/boat, allocated:", [total_savings_per_boat[i] * (boat_throughput_participation_factor[i] / 100) for i in range(len(total_savings_per_boat))])



#__Plotting___________________________________________________________________________________________________________________________
#Grid usage
#region
plt.figure(figsize=(8, 5))
plt.plot(boat, old_grid_usage_be, color='orange', linestyle='--')
plt.plot(boat, peak_grid_usage_be, color='olivedrab', marker='.')
plt.plot(boat, nordpool_grid_usage_be,color='teal', marker='.')
plt.plot(boat, LFM_grid_usage_01_be, color='indianred', marker='.')
plt.legend(['Reference Case','Case 1: Peak Shaved', 'Case 2: Spot Price', 'Case 3: LFM'])
plt.xlabel('Number of Electric Leisure Boats')
plt.ylabel('Grid usage [MWh]')
plt.grid(True)
plt.tight_layout()
plt.show()

#Energy throughput BESS
plt.figure(figsize=(7, 6))
plt.plot(boat, peak_bess_throughput_be , color='olivedrab', marker='.')
plt.plot(boat, nord_bess_throughput_be, color='teal', marker='.')
plt.plot(boat, LFM_bess_throughput_01_be , color='indianred', marker='.')
plt.legend(['Case 1: Peak Shaved', 'Case 2: Spot Price', 'Case 3: LFM'])
plt.xlabel('Number of Electric Leisure Boats')
plt.ylabel('Electricity Throughput BESS [kWh]')
plt.grid(True)
plt.tight_layout()
plt.show()

#Energy throughput boat
plt.figure(figsize=(7, 6))
plt.plot(boat[1:], peak_boat_throughput_be[1:] , color='olivedrab', marker='.')
plt.plot(boat[1:], nord_boat_throughput_be[1:], color='teal', marker='.')
plt.plot(boat[1:], LFM_boat_throughput_01_be[1:] , color='indianred' , marker='.')
plt.legend(['Case 1: Peak Shaved', 'Case 2: Spot Price', 'Case 3: LFM'])
plt.xlabel('Number of Electric Leisure Boats')
plt.ylabel('Electricity Throughput per Boat [kWh]')
plt.grid(True)
plt.tight_layout()
plt.show()



#Costs
plt.figure(figsize=(7, 6))
#plt.plot(boat, old_cost_kr, color='orange', linestyle='--')
plt.plot(boat, peak_cost_be , color='olivedrab', marker='.')
plt.plot(boat, nord_pool_cost_be, marker='.', color='teal')
plt.plot(boat, LFM_cost_01_be, marker='.', color='indianred')
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
#plt.plot(boat, old_cost_be, color='orange', linestyle='--')
plt.plot(boat, peak_cost_be , color='olivedrab',  marker='.')
plt.plot(boat, nord_pool_cost_be, marker='.', color='teal', linestyle='--')
plt.plot(boat, optimized_cost_nordpool_be, marker='.', color='teal')
plt.plot(boat, LFM_cost_01_be, marker='.', color='indianred', linestyle='--')
plt.plot(boat, optimized_cost_LFM_01_be, marker='.', color='indianred')
plt.plot(boat, optimized_cost_FCR_D_up_LFM_01_be, color='lightsteelblue', marker='.', linestyle='--')
plt.plot(boat, optimized_cost_FCR_D_down_LFM_01_be, color='cornflowerblue', marker='.', linestyle='--')
plt.plot(boat, optimized_cost_FCR_D_LFM_01_be, color='royalblue', marker='.')
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
plt.plot(boat, nord_pool_revenue_be, marker='.', color='teal')
plt.plot(boat, LFM_total_revenue_01_be, marker='.', color='indianred')
plt.plot(boat, FCR_D_up_revenue_01_be, color='lightsteelblue', marker='.')
plt.plot(boat, FCR_D_down_revenue_01_be, color='cornflowerblue', marker='.')
plt.plot(boat, total_revenue_be, color='black', marker='.')
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
#ax1.plot(boat, peak_grid_usage_be, color='olivedrab', marker='.', label='Electricity usage')
#ax1.plot(boat, nordpool_grid_usage_be, color='teal', marker='.', label='Electricity usage')
ax1.plot(boat, LFM_grid_usage_01_be, color='indianred', marker='.', label='Electricity usage')
ax1.set_xlabel('Number of Electric Leisure Boats')
ax1.set_ylabel('Grid usage [MWh]', color='black')
ax1.tick_params(axis='y', labelcolor='black')
ax1.grid(True)
# Add a secondary y-axis for cost
ax2 = ax1.twinx()
#ax2.plot(boat, peak_cost_be, color='olivedrab', marker='.', linestyle='--', label='Cost')
#ax2.plot(boat, nord_pool_cost_be, color='teal', marker='.', linestyle='--', label='Cost')
#ax2.plot(boat, LFM_revenue_01_be, color='indianred', marker='.', linestyle='--', label='Cost')
ax2.plot(boat, optimized_cost_FCR_D_LFM_01_be, color='indianred', marker='.', linestyle='--', label='Final Cost')
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
plt.plot(boat, revenue_per_boat_case1_be, color='olivedrab', marker='.')
plt.plot(boat, revenue_per_boat_case2_be, color='teal', marker='.')
plt.plot(boat, revenue_per_boat_case3_be, color='indianred', marker='.')
plt.plot(boat, revenue_per_boat_case4_be, color='royalblue', marker='.')
plt.legend(['Case 1: Peak Shaved', 'Case 2: Spot Price', 'Case 3: LFM', 'Case 4: FCR-D'])
plt.xlabel('Number of Electric Leisure Boats')
plt.ylabel('Revenue per boat [SEK]')
plt.grid(True)
plt.tight_layout()
plt.show()

#endregion

#____Esay calculation of increased grid usage without any cool stuff____________________________________________________________________________________________________________________________
new_grid_usage_be = [old_grid_usage_be[i] + 0.007*11*boat[i] for i in range(len(old_grid_usage_be))]

print(f"Increased grid usage: {[round(value,2) for value in new_grid_usage_be]}")