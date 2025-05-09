import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter
from usage_pattern import usage_pattern
import el_price
from numpy import *
import pandas as pd
spotprice = el_price.spotprice_2023

boat = [0, 2, 4, 6, 8, 10, 20, 50]

#_____Original data___________________________________________________________________________________________________________________________  
old_grid_usage_kr = [906.8, 906.8, 906.8, 906.8, 906.8, 906.8, 906.8, 906.8]

old_cost_kr = [1608118, 1608118, 1608118, 1608118, 1608118, 1608118, 1608118, 1608118]
boat_load_cost_kr = []
reference_grid_usage_kr = [old_grid_usage_kr[i] + 0.07 *11 * boat[i] for i in range(len(old_grid_usage_kr))]

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
        boat_load_cost_kr.append(0)
    else:
        total_cost, _, _, _, _, _, _ = boat_load_cost(b, spotprice)
        boat_load_cost_kr.append(float(total_cost))

reference_cost_kr = [old_cost_kr[i] + boat_load_cost_kr[i] for i in range(len(old_cost_kr))]
print("Boat load cost: ", boat_load_cost_kr)
print("Reference cost: ", reference_cost_kr)

#_____Case 1____________________________________________________________________________________________________________________________
peak_grid_usage_kr = [859.56, 860.46, 861.87, 863.29, 864.75, 866.21, 873.51, 895.41]
peak_bess_throughput_kr = [101740, 95537, 87362, 80747, 73730, 70761, 55495, 40327]
peak_boat_throughput_kr = [0, 14376, 12882, 11509, 10526, 9369, 6673, 3771]


peak_throughput_kr= [peak_bess_throughput_kr[i] + peak_boat_throughput_kr[i] for i in range(len(peak_bess_throughput_kr))]

peak_cost_kr = [1440970, 1422105, 1409541, 1400206, 1392958, 1386754, 1364202, 1339059]


#____Case 2____________________________________________________________________________________________________________________________
# Nord pool: allowing electricity to be sold on Nord pool
nordpool_grid_usage_kr = [864.16, 867.91, 871.45, 875.62, 879.51, 882.86, 898.21, 928.8]
nord_pool_cost_kr = [1452559, 1437663, 1428023, 1422321, 1417250, 1413486, 1400043, 1384664]
nord_pool_revenue_kr = [8296.7, 13231.2, 17355.1, 22790.3, 26966.1, 31044.7, 46942.2, 64605]
nord_bess_throughput_kr = [86941, 82073, 76140, 72248, 67943, 65292, 55829, 44974]
nord_boat_throughput_kr = [0, 13185, 11618, 10463, 9581, 8751, 6473, 3798]

nord_throughput_kr= [nord_bess_throughput_kr[i] + nord_boat_throughput_kr[i] for i in range(len(nord_bess_throughput_kr))]

#New costs
optimized_cost_nordpool_kr = [nord_pool_cost_kr[i] - nord_pool_revenue_kr[i] for i in range(len(nord_pool_cost_kr))]


#_____P_bid 0.1___________________________________________________________________________________________________________________________
#region
# ______Case 3____________________________________________________________________________________________________________________________
LFM_grid_usage_01_kr = [860.55,  864.9 , 870.72, 875.53, 880.84, 885.72, 905.48, 947.77]
LFM_bess_throughput_01_kr = [114142, 106131, 96510, 87003, 83137, 77825, 63501, 40565]
LFM_boat_throughput_01_kr = [0, 16515, 14499, 13565, 12198, 11388, 7923 , 4464]
LFM_cost_01_kr = [1440170 , 1425957, 1420173, 1415729, 1413978, 1411829, 1408106, 1419099]

LFM_throughput_01_kr= [LFM_bess_throughput_01_kr[i] + LFM_boat_throughput_01_kr[i] for i in range(len(LFM_bess_throughput_01_kr))]  

#Revenue
# LFM:
LFM_revenue_01_kr = [(3283+7462), (4515+10262), (5747+13062), (6979+15862) , (8211+18662), (9443+21462), (15603+35462), (34083+77462)]

#Nordpool:
LFM_revenue_Nordpool_01_kr = [15689.4, 24150.6, 36722.0, 47535.2 , 53817.2, 60691.1, 87115.7, 107199.7]

LFM_total_revenue_01_kr = [LFM_revenue_01_kr[i] + LFM_revenue_Nordpool_01_kr[i] for i in range(len(LFM_revenue_01_kr))] 

#New costs
optimized_cost_LFM_01_kr= [LFM_cost_01_kr[i] - LFM_revenue_01_kr[i] - LFM_revenue_Nordpool_01_kr[i] for i in range(len(LFM_cost_01_kr))]

#______Case 4____________________________________________________________________________________________________________________________
# FCR-D up: 
FCR_D_up_revenue_01_kr = [22671.5, 28914.1, 35422.9,  43437.3, 52581.0, 61113.0, 98670.5, 197662.2]


# FCR-D up: 
FCR_D_down_revenue_01_kr = [92152, 115428.1, 136467.5, 165199.1, 187236.4, 224826.7, 389319.6,  854701.1]


#New costs
optimized_cost_FCR_D_up_LFM_01_kr = [optimized_cost_LFM_01_kr[i] - FCR_D_up_revenue_01_kr[i]  for i in range(len(optimized_cost_LFM_01_kr))]
optimized_cost_FCR_D_down_LFM_01_kr = [optimized_cost_LFM_01_kr[i] - FCR_D_down_revenue_01_kr[i]  for i in range(len(optimized_cost_LFM_01_kr))]
optimized_cost_FCR_D_LFM_01_kr = [optimized_cost_LFM_01_kr[i] - FCR_D_up_revenue_01_kr[i] - FCR_D_down_revenue_01_kr[i] for i in range(len(optimized_cost_LFM_01_kr))]

#endregion

#_____P_bid 0.2___________________________________________________________________________________________________________________________
#region
# ______Case 3____________________________________________________________________________________________________________________________
LFM_grid_usage_02_kr = [862.25,  868.2  , 873.96 , 880.18,  887.14 , 891.9 , 915.3, 970.61 ]
LFM_bess_throughput_02_kr = [114291, 104619, 95491, 86090, 83420 , 79648, 59175 , 45829]
LFM_boat_throughput_02_kr = [0, 16344 , 14772,  13875 , 12252 , 11005 ,7994, 4541]
LFM_cost_02_kr = [1443234 , 1433550 ,1427009 , 1426009, 1426214 ,  1427093 , 1430323 , 1471090 ]

LFM_throughput_02_kr= [LFM_bess_throughput_02_kr[i] + LFM_boat_throughput_02_kr[i] for i in range(len(LFM_bess_throughput_02_kr))]  

#Revenue
# LFM:
LFM_revenue_02_kr = [(6567+14924), (9031+20524), (11495+26124), (13959+31724 ) , (16423+37324), (18887+42924 ), (42924 +70924), (68167+154924)]

#Nordpool:
LFM_revenue_Nordpool_02_kr = [16737.6 , 26884.0,  38736.5, 50192.7 ,  50950.5,63554.6 , 85613.9 ,101710.3]

#New costs
optimized_cost_LFM_02_kr= [LFM_cost_02_kr[i] - LFM_revenue_02_kr[i] - LFM_revenue_Nordpool_02_kr[i] for i in range(len(LFM_cost_02_kr))]

#______Case 4____________________________________________________________________________________________________________________________
# FCR-D up: 
FCR_D_up_revenue_02_kr = [22638.1,30389.1 ,35245.4 ,45048.4 , 53155.5, 62797.9 , 100682.5 , 215814]

# FCR-D up: 
FCR_D_down_revenue_02_kr = [91597.4,111764.6 ,129560.2 , 155571.2 , 178078.3 , 209068.6 , 364260.1,757333.8 ]

#New costs
optimized_cost_FCR_D_up_LFM_02_kr = [optimized_cost_LFM_02_kr[i] - FCR_D_up_revenue_02_kr[i]  for i in range(len(optimized_cost_LFM_02_kr))]
optimized_cost_FCR_D_down_LFM_02_kr = [optimized_cost_LFM_02_kr[i] - FCR_D_down_revenue_02_kr[i]  for i in range(len(optimized_cost_LFM_02_kr))]
optimized_cost_FCR_D_LFM_02_kr = [optimized_cost_LFM_02_kr[i] - FCR_D_up_revenue_02_kr[i] - FCR_D_down_revenue_02_kr[i] for i in range(len(optimized_cost_LFM_02_kr))]

#endregion

#_____P_bid 0.3___________________________________________________________________________________________________________________________
#region
# ______Case 3____________________________________________________________________________________________________________________________
LFM_grid_usage_03_kr = [864.37, 870.69,877.84,886.09, 891.98,898.7,928.27 ,1012.71  ]
LFM_bess_throughput_03_kr = [115440 ,108076 , 99536 ,94949 , 90699 ,86428 , 77703 , 57789 ]
LFM_boat_throughput_03_kr = [0,16378 ,15002 ,14432 , 13920  ,12648  ,10178 ,6798]
LFM_cost_03_kr = [ 1449482 ,1441912  , 1439232 ,1439296 ,1439412 ,  1437796, 1451786 ,1577048  ]

LFM_throughput_03_kr= [LFM_bess_throughput_03_kr[i] + LFM_boat_throughput_03_kr[i] for i in range(len(LFM_bess_throughput_03_kr))]  

#Revenue
# LFM:
LFM_revenue_03_kr = [(9850+22386),(13546+30786), (17242+39186),(20938+47586) , (24634+55986),(28330+64386) , (46810+ 106386) , (102250+232386)]

#Nordpool:
LFM_revenue_Nordpool_03_kr = [14865.0,27251.5 ,38325.9  ,46934.4 ,62051.3 ,63855.7 , 90369.4  , 149817.0 ]

#New costs
optimized_cost_LFM_03_kr= [LFM_cost_03_kr[i] - LFM_revenue_03_kr[i] - LFM_revenue_Nordpool_03_kr[i] for i in range(len(LFM_cost_03_kr))]


#______Case 4____________________________________________________________________________________________________________________________
# FCR-D up: 
FCR_D_up_revenue_03_kr = [23241.7, 30426.7,36825.9, 43466.0 , 49066.2, 57736.7, 91675.6, 208541.8]

# FCR-D up: 
FCR_D_down_revenue_03_kr = [90755.9, 110218.8,130218,147492.0,174919.3, 206877.7, 320102.4, 721503.6]

#New costs
optimized_cost_FCR_D_up_LFM_03_kr = [optimized_cost_LFM_03_kr[i] - FCR_D_up_revenue_03_kr[i]  for i in range(len(optimized_cost_LFM_03_kr))]
optimized_cost_FCR_D_down_LFM_03_kr = [optimized_cost_LFM_03_kr[i] - FCR_D_down_revenue_03_kr[i]  for i in range(len(optimized_cost_LFM_03_kr))]
optimized_cost_FCR_D_LFM_03_kr = [optimized_cost_LFM_03_kr[i] - FCR_D_up_revenue_03_kr[i] - FCR_D_down_revenue_03_kr[i] for i in range(len(optimized_cost_LFM_03_kr))]

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

#Total revenue
total_revenue_kr = [FCR_D_up_revenue_01_kr[i] + FCR_D_down_revenue_01_kr[i] +LFM_revenue_01_kr[i] + LFM_revenue_Nordpool_01_kr[i] for i in range(len(LFM_revenue_01_kr))]

final_cost = [optimized_cost_FCR_D_LFM_01_kr[i] - LFM_revenue_Nordpool_01_kr[i] - LFM_revenue_01_kr[i] - FCR_D_up_revenue_01_kr[i] - FCR_D_down_revenue_01_kr[i] for i in range(len(optimized_cost_FCR_D_LFM_01_kr))]
final_cost_per_boat = [final_cost[i] / boat[i] if boat[i] != 0 else final_cost[0] for i in range(len(final_cost))]
total_savings = [reference_cost_kr[i] - final_cost[i] for i in range(len(old_cost_kr))]
total_savings_per_boat = [total_savings[i] / boat[i] if boat[i] != 0 else total_savings[0] for i in range(len(total_savings))]

bess_throughput_participation_factor = [(LFM_bess_throughput_01_kr[i]) / (LFM_bess_throughput_01_kr[i] + (LFM_boat_throughput_01_kr[i] * boat[i])) * 100 for i in range(len(LFM_bess_throughput_01_kr))]
boat_throughput_participation_factor = [(LFM_boat_throughput_01_kr[i] * boat[i]) / (LFM_bess_throughput_01_kr[i] + (LFM_boat_throughput_01_kr[i] * boat[i])) * 100 for i in range(len(LFM_boat_throughput_01_kr))]

print("Reference grid usage: ", reference_grid_usage_kr)
print("Final cost: ", final_cost)
print("Total savings: ", total_savings)
print("Final cost/boat: ", final_cost_per_boat)
print("Total savings/boat: ", total_savings_per_boat)
print("BESS throughput: ", LFM_bess_throughput_01_kr, "participation factor: ", bess_throughput_participation_factor, "%")
print("Boat throughput: ", LFM_boat_throughput_01_kr, "participation factor: ", boat_throughput_participation_factor, "%")
print("Total savings/boat, allocated:", [total_savings_per_boat[i] * (boat_throughput_participation_factor[i] / 100) for i in range(len(total_savings_per_boat))])



# #__Plotting___________________________________________________________________________________________________________________________
# #region
# # Grid usage
# plt.figure(figsize=(8, 5))
# plt.plot(boat, old_grid_usage_kr, color='orange', linestyle='--')
# plt.plot(boat, peak_grid_usage_kr, color='olivedrab', marker='.')
# plt.plot(boat, nordpool_grid_usage_kr,color='teal', marker='.')
# plt.plot(boat, LFM_grid_usage_01_kr, color='indianred', marker='.')
# plt.legend(['Reference Case','Case 1: Peak Shaved', 'Case 2: Spot Price', 'Case 3: LFM'])
# plt.xlabel('Number of Electric Leisure Boats')
# plt.ylabel('Grid usage [MWh]')
# plt.grid(True)
# plt.tight_layout()
# plt.show()

# #Energy throughput BESS
# plt.figure(figsize=(7, 6))
# plt.plot(boat, peak_bess_throughput_kr , color='olivedrab', marker='.')
# plt.plot(boat, nord_bess_throughput_kr, color='teal', marker='.')
# plt.plot(boat, LFM_bess_throughput_01_kr , color='indianred', marker='.')
# plt.legend(['Case 1: Peak Shaved', 'Case 2: Spot Price', 'Case 3: LFM'])
# plt.xlabel('Number of Electric Leisure Boats')
# plt.ylabel('Electricity Throughput BESS [kWh]')
# plt.grid(True)
# plt.tight_layout()
# plt.show()

# #Energy throughput boat
# plt.figure(figsize=(7, 6))
# plt.plot(boat[1:], peak_boat_throughput_kr[1:] , color='olivedrab', marker='.')
# plt.plot(boat[1:], nord_boat_throughput_kr[1:], color='teal', marker='.')
# plt.plot(boat[1:], LFM_boat_throughput_01_kr[1:] , color='indianred' , marker='.')
# plt.legend(['Case 1: Peak Shaved', 'Case 2: Spot Price', 'Case 3: LFM'])
# plt.xlabel('Number of Electric Leisure Boats')
# plt.ylabel('Electricity Throughput per Boat [kWh]')
# plt.grid(True)
# plt.tight_layout()
# plt.show()



# #Costs
# plt.figure(figsize=(7, 6))
# #plt.plot(boat, old_cost_kr, color='orange', linestyle='--')
# plt.plot(boat, peak_cost_kr , color='olivedrab', marker='.')
# plt.plot(boat, nord_pool_cost_kr, marker='.', color='teal')
# plt.plot(boat, LFM_cost_01_kr, marker='.', color='indianred')
# # plt.plot(boat, optimized_cost_FCR_D_LFM_kr, marker='o')
# plt.legend(['Case 1: Peak Shaved', 'Case 2: Spot Price', 'Case 3: LFM '])
# plt.xlabel('Number of Electric Leisure Boats')
# plt.ylabel('Cost of Electricity [SEK]')
# plt.grid(True)
# # Force full numbers on the y-axis
# formatter = ScalarFormatter(useOffset=False, useMathText=False)
# formatter.set_scientific(False)  # Disable scientific notation
# plt.gca().yaxis.set_major_formatter(formatter)
# plt.show()

# #Case 4
# #Costs
# plt.figure(figsize=(8, 5))
# plt.plot(boat, old_cost_kr, color='orange', linestyle='--')
# plt.plot(boat, peak_cost_kr , color='olivedrab',  marker='.')
# plt.plot(boat, nord_pool_cost_kr, marker='.', color='teal', linestyle='--')
# plt.plot(boat, optimized_cost_nordpool_kr, marker='.', color='teal')
# plt.plot(boat, LFM_cost_01_kr, marker='.', color='indianred', linestyle='--')
# plt.plot(boat, optimized_cost_LFM_01_kr, marker='.', color='indianred')
# plt.plot(boat, optimized_cost_FCR_D_up_LFM_01_kr, color='lightsteelblue', marker='.', linestyle='--')
# plt.plot(boat, optimized_cost_FCR_D_down_LFM_01_kr, color='cornflowerblue', marker='.', linestyle='--')
# plt.plot(boat, optimized_cost_FCR_D_LFM_01_kr, color='royalblue', marker='.')
# plt.legend(['Optimized cost Case 1: Peak Shaved', 'Optimized cost Case 2: Spot Price', 'Cost after revenue Case 2: Spot Price ', 'Optimized cost Case 3: LFM ', 'Cost after revenue Case 3: LFM', 'Cost after revenue Case 4: FCR-D up', 'Cost after revenue Case 4: FCR-D down', "Cost after revenue Case 4: FCR-D"])
# plt.xlabel('Number of Electric Leisure Boats'), 
# plt.ylabel('Cost of Electricity [SEK]')
# plt.grid(True)
# # Force full numbers on the y-axis
# formatter = ScalarFormatter(useOffset=False, useMathText=False)
# formatter.set_scientific(False)  # Disable scientific notation
# plt.gca().yaxis.set_major_formatter(formatter)
# plt.show()

# #Revenue
# plt.figure(figsize=(7, 6))
# #plt.plot(boat, old_cost_be, color='orange', linestyle='--')
# plt.plot(boat, nord_pool_revenue_kr, marker='.', color='teal')
# plt.plot(boat, LFM_total_revenue_01_kr, marker='.', color='indianred')
# plt.plot(boat, FCR_D_up_revenue_01_kr, color='lightsteelblue', marker='.')
# plt.plot(boat, FCR_D_down_revenue_01_kr, color='cornflowerblue', marker='.')
# plt.plot(boat, total_revenue_kr, color='black', marker='.')
# plt.legend(['Case 2: Nord Pool', 'Case 3: LFM', 'FCR-D up ', 'FCR-D down', 'Case 4: FCR-D'])
# plt.xlabel('Number of Electric Leisure Boats'), 
# plt.ylabel('Revenue [SEK]')
# plt.grid(True)
# # Force full numbers on the y-axis
# formatter = ScalarFormatter(useOffset=False, useMathText=False)
# formatter.set_scientific(False)  # Disable scientific notation
# plt.gca().yaxis.set_major_formatter(formatter)
# plt.show()

# #Plot energy and cost together
# # Plot grid usage on the primary y-axis
# fig, ax1 = plt.subplots(figsize=(8, 5))
# #ax1.plot(boat, peak_grid_usage_kr, color='olivedrab', marker='.', label='Electricity usage')
# #ax1.plot(boat, nordpool_grid_usage_kr, color='teal', marker='.', label='Electricity usage')
# ax1.plot(boat, LFM_grid_usage_01_kr, color='indianred', marker='.', label='Electricity usage')
# ax1.set_xlabel('Number of Electric Leisure Boats')
# ax1.set_ylabel('Grid usage [MWh]', color='black')
# ax1.tick_params(axis='y', labelcolor='black')
# ax1.grid(True)
# # Add a secondary y-axis for cost
# ax2 = ax1.twinx()
# #ax2.plot(boat, peak_cost_kr, color='olivedrab', marker='.', linestyle='--', label='Final Cost')
# #ax2.plot(boat, nord_pool_cost_kr, color='teal', marker='.', linestyle='--', label='Final Cost')
# # ax2.plot(boat, optimized_cost_LFM_01_kr, color='indianred', marker='.', linestyle='--', label='Final Cost LFM')
# # ax2.plot(boat, optimized_cost_FCR_D_up_LFM_01_kr, color='olivedrab', marker='.', linestyle='--', label='Final Cost FCR-D up')
# # ax2.plot(boat, optimized_cost_FCR_D_down_LFM_01_kr, color='teal', marker='.', linestyle='--', label='Final Cost FCR-D down')
# ax2.plot(boat, optimized_cost_FCR_D_LFM_01_kr, color='teal', marker='.', linestyle='--', label='Final Cost')
# ax2.set_ylabel('Cost of Electricity [SEK]', color='dimgrey')
# ax2.tick_params(axis='y', labelcolor='dimgrey')
# # Force full numbers on the y-axis
# formatter = ScalarFormatter(useOffset=False, useMathText=False)
# formatter.set_scientific(False)  # Disable scientific notation
# plt.gca().yaxis.set_major_formatter(formatter)
# # Combine legends from both axes
# lines_1, labels_1 = ax1.get_legend_handles_labels()
# lines_2, labels_2 = ax2.get_legend_handles_labels()
# ax1.legend(lines_1 + lines_2, labels_1 + labels_2, loc='upper left')
# plt.tight_layout()
# plt.show()


# #Plot revenue per boat
# plt.figure(figsize=(8, 5))
# plt.plot(boat, revenue_per_boat_case1_kr, color='olivedrab', marker='.')
# plt.plot(boat, revenue_per_boat_case2_kr, color='teal', marker='.')
# plt.plot(boat, revenue_per_boat_case3_kr, color='indianred', marker='.')
# plt.plot(boat, revenue_per_boat_case4_kr, color='royalblue', marker='.')
# plt.legend(['Case 1: Peak Shaved', 'Case 2: Spot Price', 'Case 3: LFM', 'Case 4: FCR-D'])
# plt.xlabel('Number of Electric Leisure Boats')
# plt.ylabel('Revenue per boat [SEK]')
# plt.grid(True)
# plt.tight_layout()
# plt.show()

# #endregion

# #____Esay calculation of increased grid usage without any cool stuff____________________________________________________________________________________________________________________________
# new_grid_usage_kr = [old_grid_usage_kr[i] + 0.007*11*boat[i] for i in range(len(old_grid_usage_kr))]

# print(f"Increased grid usage: {[round(value,2) for value in new_grid_usage_kr]}")