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
    USE1_pd = pd.DataFrame(USE1)
    USE2_pd = pd.DataFrame(USE2)
    USE3_pd = pd.DataFrame(USE3)
    USE1_pd.to_csv('USE1.csv', index=False)
    USE2_pd.to_csv('USE2.csv', index=False)
    USE3_pd.to_csv('USE3.csv', index=False)
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
                else:
                    BOATLOAD1[h-1, d] = 0
                if USE2[h, d] == 1 and USE2[h+1, d] == 0:
                    BOATLOAD2[23, d-1] = 10 * NUMBOAT2
                    BOATLOAD2[0:6, d] = 10 * NUMBOAT2
                else:
                    BOATLOAD2[h-1, d] = 0
                if USE3[h, d] == 1 and USE3[h+1, d] == 0:
                    BOATLOAD3[23, d-1] = 10 * NUMBOAT3
                    BOATLOAD3[0:6, d] = 10 * NUMBOAT3
                else:
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
#Peak Shaving
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
#Adding LFM
LFM_grid_usage_01_kr = [860.55,  864.9 , 870.72, 875.53, 880.84, 885.72, 905.48, 947.77]
LFM_bess_throughput_01_kr = [114142, 106131, 96510, 87003, 83137, 77825, 63501, 40565]
LFM_boat_throughput_01_before_kr = [0, 16515, 14499, 13565, 12198, 11388, 7923 , 4464]
LFM_boat_throughput_01_kr = [(LFM_boat_throughput_01_before_kr[i] * 2 - 0.07*11*boat[i])/2 for i in range(len(LFM_boat_throughput_01_before_kr))]
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

#Total revenue
total_revenue_kr = [FCR_D_up_revenue_01_kr[i] + FCR_D_down_revenue_01_kr[i] +LFM_revenue_01_kr[i] + LFM_revenue_Nordpool_01_kr[i] for i in range(len(LFM_revenue_01_kr))]

#endregion

#_____P_bid 0.2___________________________________________________________________________________________________________________________
#region
# ______Case 3____________________________________________________________________________________________________________________________
#Adding LFM
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

LFM_total_revenue_02_kr = [LFM_revenue_02_kr[i] + LFM_revenue_Nordpool_02_kr[i] for i in range(len(LFM_revenue_02_kr))]

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

#Total revenue
total_revenue_02_kr = [FCR_D_up_revenue_02_kr[i] + FCR_D_down_revenue_02_kr[i] +LFM_revenue_02_kr[i] + LFM_revenue_Nordpool_02_kr[i] for i in range(len(LFM_revenue_01_kr))]

#endregion

#_____P_bid 0.3___________________________________________________________________________________________________________________________
#region
# ______Case 3____________________________________________________________________________________________________________________________
#Adding LFM
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

LFM_total_revenue_03_kr = [LFM_revenue_03_kr[i] + LFM_revenue_Nordpool_03_kr[i] for i in range(len(LFM_revenue_03_kr))]

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

#Total revenue
total_revenue_03_kr = [FCR_D_up_revenue_03_kr[i] + FCR_D_down_revenue_03_kr[i] +LFM_revenue_03_kr[i] + LFM_revenue_Nordpool_03_kr[i] for i in range(len(LFM_revenue_03_kr))]

#endregion

#_____P_bid 0.35___________________________________________________________________________________________________________________________
#region
# ______Case 3____________________________________________________________________________________________________________________________
#Adding LFM
LFM_grid_usage_35_kr = [865.65, 872.71, 879.91,  887.64,  894.82, 903.26, 936.88, 1027.26 ]
LFM_bess_throughput_35_kr = [117116, 111663, 104804, 101543, 95692, 91316, 84166, 62071  ]
LFM_boat_throughput_35_kr = [0, 16491, 15539, 14543, 14350, 14165, 10628, 6732 ]
LFM_cost_35_kr = [1455648, 1448659, 1447959, 1454160, 1454754, 1464444, 1496297, 1638697 ]

LFM_throughput_35_kr= [LFM_bess_throughput_35_kr[i] + LFM_boat_throughput_35_kr[i] for i in range(len(LFM_bess_throughput_35_kr))]  

#Revenue
# LFM:
LFM_revenue_35_kr = [(11491+26117), (15803+35917), (20115+45717), (24427+55517), (28739+65317), (33051+75117), (54611+124117), (119291+271117)]

#Nordpool:
LFM_revenue_Nordpool_35_kr = [15443.7, 24934.6, 35390.8, 48196.0, 60281.7, 71582.7, 95018.5, 153255.3]

LFM_total_revenue_35_kr = [LFM_revenue_35_kr[i] + LFM_revenue_Nordpool_35_kr[i] for i in range(len(LFM_revenue_35_kr))]

#New costs
optimized_cost_LFM_35_kr= [LFM_cost_35_kr[i] - LFM_revenue_35_kr[i] - LFM_revenue_Nordpool_35_kr[i] for i in range(len(LFM_cost_35_kr))]


#______Case 4____________________________________________________________________________________________________________________________
# FCR-D up: 
FCR_D_up_revenue_35_kr = [22930.4, 30454.7, 35676.0, 43804.3, 49548.7, 58079.6, 96545.1, 254465.1]

# FCR-D up: 
FCR_D_down_revenue_35_kr = [90924.5, 109294.2, 132645, 155603.4, 177589.9, 203821.0, 300064.7, 708645.8]

#New costs
optimized_cost_FCR_D_up_LFM_35_kr = [optimized_cost_LFM_35_kr[i] - FCR_D_up_revenue_35_kr[i]  for i in range(len(optimized_cost_LFM_35_kr))]
optimized_cost_FCR_D_down_LFM_35_kr = [optimized_cost_LFM_35_kr[i] - FCR_D_down_revenue_35_kr[i]  for i in range(len(optimized_cost_LFM_35_kr))]
optimized_cost_FCR_D_LFM_35_kr = [optimized_cost_LFM_35_kr[i] - FCR_D_up_revenue_35_kr[i] - FCR_D_down_revenue_35_kr[i] for i in range(len(optimized_cost_LFM_35_kr))]

#Total revenue
total_revenue_35_kr = [FCR_D_up_revenue_35_kr[i] + FCR_D_down_revenue_35_kr[i] +LFM_revenue_35_kr[i] + LFM_revenue_Nordpool_35_kr[i] for i in range(len(LFM_revenue_35_kr))]

#endregion


#____Per boat, revenue _____________________________________________________________________________________________________________________________
#region
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
#endregion



final_cost = [LFM_cost_01_kr[i] - LFM_revenue_Nordpool_01_kr[i] - LFM_revenue_01_kr[i] - FCR_D_up_revenue_01_kr[i] - FCR_D_down_revenue_01_kr[i] for i in range(len(optimized_cost_FCR_D_LFM_01_kr))]
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
#region
#Costs
plt.figure(figsize=(7, 6))
#plt.plot(boat, old_cost_kr, color='orange', linestyle='--')
plt.plot(boat, array(peak_cost_kr)/1000 , color='olivedrab', marker='.')
plt.plot(boat, array(nord_pool_cost_kr)/1000, marker='.', color='teal')
plt.plot(boat, array(LFM_cost_01_kr)/1000, marker='.', color='indianred')
# plt.plot(boat, optimized_cost_FCR_D_LFM_kr, marker='o')
plt.legend(['Case 1: Peak Shaved', 'Case 2: Spot Price', 'Case 3: LFM '])
plt.xlabel('Number of Electric Leisure Boats')
plt.ylabel('Optimized Grid Usage Cost [kSEK]')
plt.grid(True)
# Force full numbers on the y-axis
formatter = ScalarFormatter(useOffset=False, useMathText=False)
formatter.set_scientific(False)  # Disable scientific notation
plt.gca().yaxis.set_major_formatter(formatter)
plt.show()



#Revenue
plt.figure(figsize=(7, 6))
#plt.plot(boat, old_cost_be, color='orange', linestyle='--')
plt.plot(boat, array(nord_pool_revenue_kr)/1000, marker='.', color='teal')
plt.plot(boat, array(LFM_total_revenue_01_kr)/1000, marker='.', color='indianred')
plt.plot(boat, array(FCR_D_up_revenue_01_kr)/1000, color='lightsteelblue', marker='.')
plt.plot(boat, array(FCR_D_down_revenue_01_kr)/1000, color='cornflowerblue', marker='.')
plt.plot(boat, array(total_revenue_kr)/1000, color='black', marker='.')
plt.legend(['Case 2: Nord Pool', 'Case 3: LFM', 'FCR-D up ', 'FCR-D down', 'Case 4: FCR-D'])
plt.xlabel('Number of Electric Leisure Boats'), 
plt.ylabel('Revenue [kSEK]')
plt.grid(True)
# Force full numbers on the y-axis
formatter = ScalarFormatter(useOffset=False, useMathText=False)
formatter.set_scientific(False)  # Disable scientific notation
plt.gca().yaxis.set_major_formatter(formatter)
plt.show()

#Plot energy and cost together
# Plot grid usage on the primary y-axis
fig, ax1 = plt.subplots(figsize=(8, 5))
ax1.plot(boat, peak_grid_usage_kr, color='olivedrab', marker='.', label='Electricity usage')
#ax1.plot(boat, nordpool_grid_usage_kr, color='teal', marker='.', label='Electricity usage')
#ax1.plot(boat, LFM_grid_usage_01_kr, color='indianred', marker='.', label='Electricity usage')
#ax1.plot(boat, LFM_grid_usage_01_kr, color='black', marker='.', label='Electricity usage')
ax1.set_xlabel('Number of Electric Leisure Boats')
ax1.set_ylabel('Grid Usage [MWh]', color='black')
ax1.tick_params(axis='y', labelcolor='black')
ax1.grid(True)
# Add a secondary y-axis for cost
ax2 = ax1.twinx()
ax2.plot(boat, array(peak_cost_kr)/1000, color='olivedrab', marker='.', linestyle='--', label='Optimized Girud Usage Cost')
#ax2.plot(boat, array(optimized_cost_nordpool_kr)/1000, color='teal', marker='.', linestyle='--', label='Final Cost')
#ax2.plot(boat, array(optimized_cost_LFM_01_kr)/1000, color='indianred', marker='.', linestyle='--', label='Final Cost')
#ax2.plot(boat, array(optimized_cost_FCR_D_LFM_01_kr)/1000, color='black', marker='.', linestyle='--', label='Final Cost')
ax2.set_ylabel('Optimized Girud Usage Cost [kSEK]', color='dimgrey')
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

#endregion


#_____Plotting Sensitivity analysis______________________________________________________________________________________________________
# Grid usage
plt.figure(figsize=(7, 6))
plt.plot(boat, old_grid_usage_kr, color='orange', linestyle='--')
plt.plot(boat, LFM_grid_usage_01_kr, color='firebrick', marker='.')
plt.plot(boat, LFM_grid_usage_02_kr,  color='indianred', marker='.')
plt.plot(boat, LFM_grid_usage_03_kr, color='lightcoral', marker='.')
plt.plot(boat, LFM_grid_usage_35_kr, color='rosybrown', marker='.')
plt.legend(['Reference Case','Bid size: 0.1', 'Bid size: 0.2', 'Bid size: 0.3', 'Bid size: 0.35'])
plt.xlabel('Number of Electric Leisure Boats')
plt.ylabel('Grid usage [MWh]')
plt.grid(True)
plt.tight_layout()
plt.show()

#Costs
plt.figure(figsize=(7, 6))
plt.plot(boat, array(old_cost_kr)/1000, color='orange', linestyle='--')
plt.plot(boat, array(LFM_cost_01_kr)/1000 , color='firebrick', marker='.')
plt.plot(boat, array(LFM_cost_02_kr)/1000, marker='.', color='indianred')
plt.plot(boat, array(LFM_cost_03_kr)/1000, marker='.', color='lightcoral')
plt.plot(boat, array(LFM_cost_35_kr)/1000, marker='.', color='rosybrown')
plt.legend(['Reference case','Bid size: 0.1', 'Bid size: 0.2', 'Bid size: 0.3', 'Bid size: 0.35'])
plt.xlabel('Number of Electric Leisure Boats')
plt.ylabel('Optimized Grid Usage Cost [kSEK]')
plt.grid(True)
# Force full numbers on the y-axis
formatter = ScalarFormatter(useOffset=False, useMathText=False)
formatter.set_scientific(False)  # Disable scientific notation
plt.gca().yaxis.set_major_formatter(formatter)
plt.show()

#Revenue
plt.figure(figsize=(7, 6))
plt.plot(boat, array(LFM_total_revenue_01_kr)/1000, marker='.', color='firebrick')
plt.plot(boat, array(LFM_total_revenue_02_kr)/1000, marker='.', color='indianred')
plt.plot(boat, array(LFM_total_revenue_03_kr)/1000, color='lightcoral', marker='.')
plt.plot(boat, array(LFM_total_revenue_35_kr)/1000, color='rosybrown', marker='.')
plt.legend(['Bid size: 0.1', 'Bid size: 0.2', 'Bid size: 0.3', 'Bis size: 0.35'])
plt.xlabel('Number of Electric Leisure Boats'), 
plt.ylabel('Revenue [kSEK]')
plt.grid(True)
# Force full numbers on the y-axis
formatter = ScalarFormatter(useOffset=False, useMathText=False)
formatter.set_scientific(False)  # Disable scientific notation
plt.gca().yaxis.set_major_formatter(formatter)
plt.show()

#Revenue
plt.figure(figsize=(7, 6))
plt.plot(boat, (array(FCR_D_down_revenue_01_kr) + array(FCR_D_up_revenue_01_kr))/1000, marker='.', color='black')
plt.plot(boat, (array(FCR_D_down_revenue_02_kr) + array(FCR_D_up_revenue_02_kr))/1000, marker='.', color='dimgrey')
plt.plot(boat, (array(FCR_D_down_revenue_03_kr) + array(FCR_D_up_revenue_03_kr))/1000, color='darkgrey', marker='.')
plt.plot(boat, (array(FCR_D_down_revenue_35_kr) + array(FCR_D_up_revenue_35_kr))/1000, color='silver', marker='.')
plt.legend(['Bid size: 0.1', 'Bid size: 0.2', 'Bid size: 0.3', 'Bis size: 0.35'])
plt.xlabel('Number of Electric Leisure Boats'), 
plt.ylabel('Revenue [kSEK]')
plt.grid(True)
# Force full numbers on the y-axis
formatter = ScalarFormatter(useOffset=False, useMathText=False)
formatter.set_scientific(False)  # Disable scientific notation
plt.gca().yaxis.set_major_formatter(formatter)
plt.show()

#Final cost Case 4
plt.figure(figsize=(7, 6))
plt.plot(boat, array(optimized_cost_LFM_01_kr)/1000 , color='firebrick', marker='.')
plt.plot(boat, array(optimized_cost_LFM_02_kr)/1000, marker='.', color='indianred')
plt.plot(boat, array(optimized_cost_LFM_03_kr)/1000, marker='.', color='lightcoral')
plt.plot(boat, array(optimized_cost_LFM_35_kr)/1000, marker='.', color='rosybrown')
plt.legend(['Bid size: 0.1', 'Bid size: 0.2', 'Bid size: 0.3', 'Bid size: 0.35'])
plt.xlabel('Number of Electric Leisure Boats')
plt.ylabel('Final cost [kSEK]')
plt.grid(True)
# Force full numbers on the y-axis
formatter = ScalarFormatter(useOffset=False, useMathText=False)
formatter.set_scientific(False)  # Disable scientific notation
plt.gca().yaxis.set_major_formatter(formatter)
plt.show()

#Final cost Case 5
plt.figure(figsize=(7, 6))
plt.plot(boat, array(optimized_cost_FCR_D_LFM_01_kr)/1000 , color='black', marker='.')
plt.plot(boat, array(optimized_cost_FCR_D_LFM_02_kr)/1000, marker='.', color='dimgrey')
plt.plot(boat, array(optimized_cost_FCR_D_LFM_03_kr)/1000, marker='.', color='darkgrey')
plt.plot(boat, array(optimized_cost_FCR_D_LFM_35_kr)/1000, marker='.', color='silver')
plt.legend(['Bid size: 0.1', 'Bid size: 0.2', 'Bid size: 0.3', 'Bid size: 0.35'])
plt.xlabel('Number of Electric Leisure Boats')
plt.ylabel('Final cost [kSEK]')
plt.grid(True)
# Force full numbers on the y-axis
formatter = ScalarFormatter(useOffset=False, useMathText=False)
formatter.set_scientific(False)  # Disable scientific notation
plt.gca().yaxis.set_major_formatter(formatter)
plt.show()


