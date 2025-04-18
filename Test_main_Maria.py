#______Importing libraries_______________________________________________________________________________________________
#region
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import load_krossholmen_2023
import solarpower
import windpower
# import load_björkö
# import load_björkö_bessekroken
import el_price
import el_cost
import Optimization_Maria
import usage_pattern
from Effekthandel_väst import effekthandel_väst
from Frequency import frequency_price
#endregion
#______Variable and parameters___________________________________________________________________________________________
#region
load_krossholmen = load_krossholmen_2023.load
# load_björkö_hamn=load_björkö.load
# load_bessekroken=load_björkö_bessekroken.load 
# load_winter_krossholmen = load_krossholmen_2023.load_winter
# load_summer_krossholmen = load_krossholmen_2023.load_summer

spot_price_2023=el_price.spotprice_2023


#endregion
#________Reference Case__________________________________________________________________________________________________
#region Calculating the sum of the array for the yearly load 1X365 in Besskroken
# yearly_load_bessekroken=np.zeros((365))
# for i in range(365):
#     yearly_load_bessekroken[i] = sum(load_bessekroken[:, i])

#Calculating the sum of the array for the yearly load 1X365 in Krossholmen
yearly_load_krossholmen=np.zeros((365))
for i in range(365):
    yearly_load_krossholmen[i] = sum(load_krossholmen[:, i])

#Calculating the sum of the array for the yearly load 1X365 in Krossholmen
# yearly_load_björkö=np.zeros((365))
# for i in range(365):
#     yearly_load_björkö[i] = sum(load_björkö_hamn[:, i])

#Calculating the sum of the array for the yearly spot price in SE3 1X365
yearly_spot_price_2023=np.zeros((365))
for i in range(365):
    yearly_spot_price_2023[i] = sum(spot_price_2023[:, i])/len(spot_price_2023[:, i])
#endregion
#_________Plotting Reference Case________________________________________________________________________________________
#region Plotting the daily load in Bessekroken
# plt.figure(figsize=(10, 5))
# plt.plot(range(len(yearly_load_bessekroken)), yearly_load_bessekroken, label='Electricity Load')
# plt.plot(range(len(yearly_spot_price_2023)), yearly_spot_price_2023, label='Spot Price')
# plt.fill_between(range(len(yearly_load_bessekroken)), yearly_load_bessekroken, alpha=0.3)
# plt.xlabel('Days')
# plt.ylabel('Daily Load (kWh)')
# plt.title('Electricity Load in 2023 in Bessekroken')
# #plt.legend()
# plt.xlim(0, 364)  # Set x-axis limits to start at 0 and end at 364
# plt.ylim(0, (max(yearly_load_bessekroken)+5)) 
# #plt.grid(True)
# plt.show(block=False)
# plt.show()


# #Plotting the daily load in Krossholmen
# plt.figure(figsize=(10, 5))
# plt.plot(range(len(yearly_load_krossholmen)), yearly_load_krossholmen, label='Electricity Load')
# plt.fill_between(range(len(yearly_load_krossholmen)), yearly_load_krossholmen, alpha=0.3)
# plt.xlabel('Days')
# plt.ylabel('Daily Load (kWh)')
# plt.title('Electricity Load in 2023 in Krossholmen')
# #plt.legend()
# plt.xlim(0, 364)  # Set x-axis limits to start at 0 and end at 364
# plt.ylim(0, (max(yearly_load_krossholmen)+100)) 
# #plt.grid(True)
# plt.show(block=False)
# plt.show()

# # Create subplots
# fig, axs = plt.subplots(1, 2, figsize=(10, 5))
# fig.suptitle('Seasonal Daily Load in Krossholmen')
# # Plot mean winter daily load in Krossholmen
# axs[0].plot(sum(load_winter_krossholmen)/len(load_winter_krossholmen))
# axs[0].set_title('Winter')
# axs[0].set_ylabel('kWh')
# axs[0].set_xlabel('Hour of the day')
# axs[0].set_xlim(0, 23)
# #axs[0].grid(True)
# # Plot mean summer daily load in Krossholmen
# axs[1].plot(sum(load_summer_krossholmen)/len(load_summer_krossholmen))
# axs[1].set_title('Summer')
# axs[1].set_ylabel('kWh')
# axs[1].set_xlabel('Hour of the day')
# axs[1].set_xlim(0, 23)
# #axs[1].grid(True)

# #Plotting the daily load in Björkö marina
# plt.figure(figsize=(10, 5))
# plt.plot(range(len(yearly_load_björkö)), yearly_load_björkö, label='Electricity Load')
# plt.fill_between(range(len(yearly_load_björkö)), yearly_load_björkö, alpha=0.3)
# plt.xlabel('Days of the Year')
# plt.ylabel('Daily Load (kWh)')
# plt.title('Electricity Load in 2023 in Björkö')
# #plt.legend()
# plt.xlim(0, 364)  # Set x-axis limits to start at 0 and end at 364
# plt.ylim(0, (max(yearly_load_björkö)+100)) 
# #plt.grid(True)
# plt.show(block=False)
# plt.show()
#endregion
#_________Case 1_________________________________________________________________________________________________________
#region Calculating selfproduced electricity
#Calling on function, change the values to get the desired result

P_s2=solarpower.solar(167,0.20) #167m^2, 20% efficiency, which is the values of Krossholmen
P_wind2=windpower.wind(1) #1 turbine rated 5,5kW

#Calculating the sum of the array for the solar power 1X365
P_s3=np.zeros((365))  
for i in range(365):
    P_s3[i] = sum(P_s2[:, i])

#Calculating the sum of the array for the wind power 1X365
P_wind3=np.zeros((365))
for i in range(365):
    P_wind3[i]=sum(P_wind2[:,i])

#Calculating the self consumed electricity with matrix 24x365
# P_self = np.zeros((24, 365))
# #If the value is negative it will be changed to 0
# for i in range(24):
#     for j in range(365):    
#         if load_bessekroken[i, j] - P_s2[i, j] - P_wind2[i,j] < 0:
#             P_self[i, j] = 0
#         else:
#             P_self[i, j] = load_bessekroken[i, j] - P_s2[i, j] - P_wind2[i,j]
# #Calculating the sum of the array 1X365
# P_self1=np.zeros((365))
# for i in range(365):
#     P_self1[i] = sum(P_self[:, i])

#Calculating the total 
total_sum_sun=round(sum(P_s3)*10,1)/10
print(f"The yearly production of solar power is {total_sum_sun/1000}MWh")

total_sum_wind=round(sum(P_wind3)*10)/10
print(f"The yearly production of wind power is {total_sum_wind/1000}MWh")
#endregion


#______Plotting Case 1___________________________________________________________________________________________________
#region Plotting the daily electricity load
# plt.figure(figsize=(10, 5))
# #plt.plot(range(len(P_s3)), P_s3, label='Solar Power Production')
# plt.plot(range(len(yearly_load_bessekroken)), yearly_load_bessekroken, label='The load of Bessekroken')
# plt.fill_between(range(len(yearly_load_bessekroken)), yearly_load_bessekroken, alpha=1)
# plt.plot(range(len(P_self1)), P_self1, label='The load of Bessekroken after self-produced electricity')
# plt.fill_between(range(len(P_self1)), P_self1, alpha=1)

# #plt.plot(range(len(P_wind3)), P_wind3, label='Wind Power Production')
# plt.xlabel('Days of the year')
# plt.ylabel('kWh')
# plt.title('Self-produced electricity and load of Bessekroken')
# plt.legend()
# plt.xlim(0, 364)  # Set x-axis limits to start at 0 and end at 364
# plt.ylim(0, (max(max(yearly_load_bessekroken), max(P_self1))+5)) 
# #plt.grid(True)
# plt.show(block=False)
# plt.show()

# #Plotting the selfproduced electricity of wind and solar power
# plt.figure(figsize=(10, 5))
# plt.plot(range(len(P_wind3)), P_wind3, label='Wind Power Production')
# plt.plot(range(len(P_s3)), P_s3, label='Solar Power Production')
# plt.xlabel('Days of the year')
# plt.ylabel('kWh')
# plt.title('Self-produced electricity')
# plt.legend()
# plt.xlim(0, 364)  # Set x-axis limits to start at 0 and end at 364
# plt.ylim(0, (max(max(P_wind3), max(P_s3))+5)) 
# #plt.grid(True)
# plt.show(block=False)
# plt.show()
#endregion
#region
a = 163
b = 205
c = 226


solar_data = solarpower.solar(100,0.20)                         # 24x365
wind_data = windpower.wind(1)                                   # 24x365
load_data = load_krossholmen                                    # 24x365
spot_price_data = el_price.spotprice_2023  
grid_limit = 1680 #Limitations of grid, abbonerad effekt [kW]                     # 24x365
boat_availability1, boat_power1 = usage_pattern.usage_pattern(a, 100, 90, 60)  # 24x365
boat_availability2, boat_power2 = usage_pattern.usage_pattern(b, 100, 90, 60)  # 24x365
boat_availability3, boat_power3 = usage_pattern.usage_pattern(c, 100, 90, 60)  # 24x365

bids_effekthandelväst_data = effekthandel_väst.I_bid
activated_bids_effekthandelväst_data = effekthandel_väst.I_activated

market_availability = np.ones((24, 365))

for i in range(24):
    for j in range(365):
        if bids_effekthandelväst_data[i, j] == 1:
            market_availability[i, j] = 0
        else:
            market_availability[i, j] = 1


# charge_required1 = usage_pattern.soc_target(boat_availability1)
# charge_required2 = usage_pattern.soc_target(boat_availability2)
# charge_required3 = usage_pattern.soc_target(boat_availability3)

number_boats = 3
bess_capacity = 500 #kWh
bess_charge_rate = 350 #kW
bess_discharge_rate = 350 #kW
bess_battery_cost = 500000 #SEK
bess_cycling = 10000 #numbers of cycles
boat_capacity = 100 
boat_charge_rate = 60 #kW
boat_discharge_rate = 60
boat_battery_cost = 100000 #SEK
boat_cycling = 5000 #numbers of cycles
user = 2 #User: Maja = 1, Maria = 2
energy_tax = 0.439 #SEK/kWh
transmission_fee = 0.113 #SEK/kWh 
peak_cost = 61.55 #SEK/kWh

bess_cycling_cost = bess_battery_cost/(bess_cycling*bess_capacity)
boat_cycling_cost = boat_battery_cost/(boat_cycling*boat_capacity)

number_boats1 = 0
number_boats2 = 0
number_boats3 = 0

for b in range(number_boats):
    if b % 3 == 0:
        number_boats1 += 1
    elif b % 3 == 1:
        number_boats2 += 1
    else:
        number_boats3 += 1

boat_load1 = usage_pattern.boat_load(boat_availability1, boat_capacity*number_boats1, 0.2*boat_capacity*number_boats1)
boat_load2 = usage_pattern.boat_load(boat_availability2, boat_capacity*number_boats2, 0.2*boat_capacity*number_boats2)
boat_load3 = usage_pattern.boat_load(boat_availability3, boat_capacity*number_boats3, 0.2*boat_capacity*number_boats3)

bid_size = 0.01 # % of the capacity

bid_bess = activated_bids_effekthandelväst_data * bess_capacity * bid_size
bid_boat1 = activated_bids_effekthandelväst_data * boat_capacity * number_boats1 * bid_size
bid_boat2 = activated_bids_effekthandelväst_data * boat_capacity * number_boats2 * bid_size
bid_boat3 = activated_bids_effekthandelväst_data * boat_capacity * number_boats3 * bid_size
# bid_bess_pd = pd.DataFrame(bid_bess)
# bid_bess_pd.to_csv('bid_bess.csv', index=False)

model = Optimization_Maria.optimize_microgrid(solar_data, wind_data, load_data, spot_price_data, grid_limit, bess_capacity, bess_charge_rate, bess_discharge_rate, boat_capacity, boat_charge_rate, boat_discharge_rate, number_boats1, number_boats2, number_boats3, boat_availability1, boat_availability2, boat_availability3, boat_load1, boat_load2, boat_load3, user, energy_tax, transmission_fee, peak_cost, bids_effekthandelväst_data, activated_bids_effekthandelväst_data, market_availability, bid_bess, bid_boat1, bid_boat2, bid_boat3)

old_grid_usage = np.zeros((24, 365))  # Initial load data
new_grid_usage = np.zeros((24, 365))  # Optimized grid usage data
self_sufficiency = np.zeros((24, 365))  # Self sufficiency data
self_production = np.zeros((24, 365))  # Self production data
bess_charge = np.zeros((24, 365))  # Battery charge data
bess_discharge = np.zeros((24, 365))  # Battery discharge data
bess_soc = np.zeros((24, 365))  # Battery state of charge data
boat_charge1 = np.zeros((24, 365))  # Boat charge data
boat_charge2 = np.zeros((24, 365))
boat_charge3 = np.zeros((24, 365))
boat_discharge1 = np.zeros((24, 365))  # Boat discharge data
boat_discharge2 = np.zeros((24, 365))  # Boat discharge data
boat_discharge3 = np.zeros((24, 365))  # Boat discharge data
boat_soc1 = np.zeros((24, 365)) # Boat state of charge data (total charge)
boat_soc2 = np.zeros((24, 365)) # Boat state of charge data (total charge)
boat_soc3 = np.zeros((24, 365)) # Boat state of charge data (total charge)
spot_price = np.zeros((24, 365))  # Spot price data



# Now you can access the model and its results
for h in model.HOURS:
    for d in model.DAYS:
        #print(f"Hour: {h}, Day: {d}, Load: {model.load_param[h, d]}, Self sufficiency: {model.self_sufficiency[h, d].value}, Grid usage: {model.grid_used[h, d].value}")
        #print(f"BESS: SOC: {model.bess_soc[h, d].value}, Discharge: {model.bess_discharge[h, d].value}, Charge: {model.bess_charge[h, d].value}")
        #print(f"Boat: SOC: {model.boat_soc[h, d].value}, Discharge: {model.boat_discharge[h, d].value}, Charge: {model.boat_charge[h, d].value}")
        old_grid_usage[h, d] = load_data[h][d]  # Initial load
        new_grid_usage[h, d] = model.grid_used[h, d].value  # Optimized grid usage
        self_sufficiency[h, d] = model.self_sufficiency[h, d].value  # Self sufficiency
        self_production[h, d] = solar_data[h][d] + wind_data[h][d]  # Self production
        bess_charge [h, d] = model.bess_charge[h, d].value
        bess_discharge [h, d] = model.bess_discharge[h, d].value
        bess_soc [h, d] = model.bess_soc[h, d].value
        boat_charge1 [h, d] = model.boat_charge1[h, d].value
        boat_charge2 [h, d] = model.boat_charge2[h, d].value
        boat_charge3 [h, d] = model.boat_charge3[h, d].value
        boat_discharge1 [h, d] = model.boat_discharge1[h, d].value
        boat_discharge2 [h, d] = model.boat_discharge2[h, d].value
        boat_discharge3 [h, d] = model.boat_discharge3[h, d].value
        boat_soc1 [h, d] = model.boat_soc1[h, d].value
        boat_soc2 [h, d] = model.boat_soc2[h, d].value
        boat_soc3 [h, d] = model.boat_soc3[h, d].value
        spot_price [h, d] = spot_price_data[h][d]

old_cost = el_cost.cost(None, None, old_grid_usage, 61.55, 0.439, 0.113, 1.25)
opt_cost = el_cost.cost(None, None, new_grid_usage, 61.55, 0.439, 0.113, 1.25)

bess_soc_values = np.zeros(8760) # Battery state of charge data (total charge)
bess_charge_values = np.zeros( 8760) # Battery charge data
bess_discharge_values = np.zeros(8760)  # Battery discharge data
 
boat_soc1_values = np.zeros(8760)
boat_soc2_values = np.zeros(8760)
boat_soc3_values = np.zeros(8760)
boat_charge1_values = np.zeros(8760)
boat_charge2_values = np.zeros(8760)
boat_charge3_values = np.zeros(8760)
 
load_data_hourly = np.zeros(8760)
new_grid_usage_hourly = np.zeros(8760)
self_production_hourly = np.zeros(8760)
self_sufficiency_hourly = np.zeros(8760)
sold_electricity_hourly = np.zeros(8760)
 
 
def hourly_values(SOC, SOCRES, CHR, CHRRES, DIS, BOAT):
    i = 0
    for d in range(365):
        for h in range(24):
            #Hourly charging data for plotting
            if DIS[h, d] > 0:
                CHRRES[i] = -DIS[h, d]
            elif CHR[h, d] > 0:
                CHRRES[i] = CHR[h, d]
            else:
                CHRRES[i] = 0
 
            #Hourly SoC-data for plotting
            if BOAT == 0:
                SOCRES[i] = 0
            else:
                SOCRES[i] = SOC[h, d]/BOAT
 
            i += 1
    return CHRRES, SOCRES
       
bess_charge_values, bess_soc_values = hourly_values(bess_soc, bess_soc_values, bess_charge, bess_charge_values, bess_discharge, 1)
boat_charge1_values, boat_soc1_values = hourly_values(boat_soc1, boat_soc1_values, boat_charge1, boat_charge1_values, boat_discharge1, number_boats1)
boat_charge2_values, boat_soc2_values = hourly_values(boat_soc2, boat_soc2_values, boat_charge2, boat_charge2_values, boat_discharge2, number_boats2)
boat_charge3_values, boat_soc3_values = hourly_values(boat_soc3, boat_soc3_values, boat_charge3, boat_charge3_values, boat_discharge3, number_boats3)
 

 
 
def hourly_values2(RES, DATA):
    i = 0
    for d in range(365):
        for h in range(24):
            RES[i] = DATA[h, d]
            i += 1
    return RES
 
load_data_hourly = hourly_values2(load_data_hourly, load_data)
new_grid_usage_hourly = hourly_values2(new_grid_usage_hourly, new_grid_usage)
self_production_hourly = hourly_values2(self_production_hourly, self_production)
self_sufficiency_hourly = hourly_values2(self_sufficiency_hourly, self_sufficiency)




print(f"Old cost: {old_cost.sum()}")
print(f"Optimized cost: {opt_cost.sum()}")

# Plotting
plt.figure(figsize=(12, 6))

# Plot old grid usage
plt.subplot(2, 1, 1)
plt.plot((load_data_hourly))
plt.title('Old Grid Usage (Initial Load)')
plt.xlabel('Day')
plt.ylabel('kWh')

# Plot new grid usage
plt.subplot(2, 1, 2)
plt.plot((new_grid_usage_hourly))
plt.plot((self_production_hourly))
plt.plot((self_sufficiency_hourly))
plt.legend(['Grid usage', 'Self production', 'Self sufficiency'])
plt.title('New Grid Usage (Optimized)')
plt.xlabel('Days')
plt.ylabel('kWh')
plt.show()

# Plot BESS and boat
plt.figure
plt.subplot(2, 1, 1)
plt.plot((bess_soc_values))
plt.legend(['SOC'])
plt.title('BESS')
plt.xlabel('Hours')
plt.ylabel('kW')

plt.subplot(2, 1, 2)
plt.plot((bess_charge_values))
plt.legend(['Charge/Discharge'])
plt.xlabel('Hours')
plt.ylabel('kW')
plt.show()

#Plot new grid usage
plt.figure
plt.subplot(3, 3, 1)
plt.plot((boat_soc1_values))
plt.legend(['SOC'])
plt.title('Boattype 1')
plt.xlabel('Hours')
plt.ylabel('kWh')

plt.subplot(3, 3, 2)
plt.plot((boat_soc2_values))
plt.legend(['SOC'])
plt.title('Boattype 2')
plt.xlabel('Hours')
plt.ylabel('kWh')

plt.subplot(3, 3, 3)
plt.plot((boat_soc3_values))
plt.legend(['SOC'])
plt.title('Boattype 3')
plt.xlabel('Hours')
plt.ylabel('kWh')

plt.subplot(3, 3, 4)
plt.plot((boat_charge1_values))
plt.legend(['Charge/Discharge'])
plt.xlabel('Hours')
plt.ylabel('kWh')

plt.subplot(3, 3, 5)
plt.plot((boat_charge2_values))
plt.legend(['Charge/Discharge'])
plt.xlabel('Hours')
plt.ylabel('kWh')

plt.subplot(3, 3, 6)
plt.plot((boat_charge3_values))
plt.legend(['Charge/Discharge'])
plt.xlabel('Hours')
plt.ylabel('kWh')

plt.subplot(3, 3, 7)
plt.plot((boat_soc1_values[3912:4248]))
plt.legend(['Charge/Discharge'])
plt.xlabel('Hours')
plt.ylabel('kWh')

plt.subplot(3, 3, 8)
plt.plot((boat_soc2_values[4920:5256]))
plt.legend(['Charge/Discharge'])
plt.xlabel('Hours')
plt.ylabel('kWh')

plt.subplot(3, 3, 9)
plt.plot((boat_soc3_values[5424:5760]))
plt.legend(['Charge/Discharge'])
plt.xlabel('Hours')
plt.ylabel('kWh')

plt.tight_layout()
plt.show()
#endregion
#______Case 2__Frekvens FCR-D_________________________________________________________________________________________________________
#region
#FCR-D up revenue
#total_soc=bess_soc_values + boat_soc1_values + boat_soc2_values + boat_soc3_values
total_boat=boat_soc1_values + boat_soc2_values + boat_soc3_values
TOTAL_CAPACITY = bess_capacity + boat_capacity * number_boats
P_bud = 0.5 * TOTAL_CAPACITY - 0.1 * TOTAL_CAPACITY # 50% of the total capacity
P_bud_summer = 0.5 * bess_capacity - 0.1 * bess_capacity #

total_soc1 = np.zeros(8760) # Battery state of charge data (total charge)
bid_soc = np.zeros(8760) # Battery state of charge data (total charge)
total_fcr_revenue=np.zeros(8760) 
hours=np.zeros(8760)
count=0

# Initialize a 24x365 matrix with zeros
bid_matrix = np.zeros((24, 365))
# Set 1s for hours 0-7 and 19-23
bid_matrix[0:6, :] = 1  # Hours 0-7
bid_matrix[6:19, :] = None
bid_matrix[19:24, :] = 1  # Hours 19-23

# Reshape the matrix to 8760x1 in column-major order
bid_matrix_reshaped = bid_matrix.reshape(-1, order='F')

for i in range(len(total_soc1)):
    if  2880 <= i <= 6551:
        total_soc1[i] = bess_soc_values[i]
    else:
        total_soc1[i] = bess_soc_values[i] + boat_soc1_values[i] + boat_soc2_values[i] + boat_soc3_values[i]

total_soc2=bid_matrix_reshaped * total_soc1

#FCR-D revenue   
FCR_D_up_price_data=(frequency_price.FCR_D_up_1)/1000

# Iterate over the indices and values of total_soc
for i in range(len(total_soc2)-1):
    if total_soc2[i] >= 0.5 * TOTAL_CAPACITY and total_soc2[i + 1] >= 0.5 * TOTAL_CAPACITY:
        hours[i] = i  # Store the index in hours
        count += 1
        total_fcr_revenue[i]= FCR_D_up_price_data[i].item() * P_bud
        bid_soc[i] = total_soc2[i]
    elif 2880 <= i <= 6551 and total_soc2[i] >= 0.5 * bess_capacity and total_soc2[i + 1] >= 0.5 * bess_capacity:
        hours[i] = i
        count += 1
        total_fcr_revenue[i]= FCR_D_up_price_data[i].item() * P_bud_summer
        bid_soc[i] = total_soc2[i]

print(f"FCR-D up revenue: {total_fcr_revenue.sum()} SEK")
print(f"FCR-D up participant: {count} h")

#FCR-D down revenue
FCR_D_down_price_data=(frequency_price.FCR_D_down_1)/1000
total_fcr_down_revenue=np.zeros(8760) 
count_1=0
bid_soc_down = np.zeros(8760)
hours_1=np.zeros(8760)

# Iterate over the indices and values of total_soc
for i in range(len(total_soc2)-1):
    if  total_soc2[i] < 0.5 * TOTAL_CAPACITY and total_soc2[i + 1] < 0.5 * TOTAL_CAPACITY:
        hours_1[i] = i  # Store the index in hours
        count_1 += 1
        total_fcr_down_revenue[i]= FCR_D_down_price_data[i].item() * P_bud
        bid_soc_down[i] = total_soc2[i]
    elif 2880 <= i <= 6551 and total_soc2[i] < 0.5 * bess_capacity and total_soc2[i + 1] < 0.5 * bess_capacity:
        hours_1[i] = i
        count_1 += 1
        total_fcr_down_revenue[i]= FCR_D_down_price_data[i].item() * P_bud_summer
        bid_soc_down[i] = total_soc2[i]

print(f"FCR-D down revenue: {total_fcr_down_revenue.sum()} SEK")
print(f"FCR-D down participant: {count_1} h")


# Creating csv files
hours_pd = pd.DataFrame(hours_1)
hours_pd.to_csv('Hours_soc.csv', index=False)

# bess_soc_pd = pd.DataFrame(bess_soc)
# bess_soc_pd.to_csv('bess_soc.csv', index=False)

# boat_soc1_pd = pd.DataFrame(boat_soc1)
# boat_soc1_pd.to_csv('boat_soc1.csv', index=False)

# boat_discharge1_pd = pd.DataFrame(boat_discharge1)
# boat_discharge1_pd.to_csv('boat_discharge1.csv', index=False)

# boat_charge1_pd = pd.DataFrame(boat_charge1)
# boat_charge1_pd.to_csv('boat_charge1.csv', index=False)

# boat_soc2_pd = pd.DataFrame(boat_soc2)
# boat_soc2_pd.to_csv('boat_soc2.csv', index=False)

# boat_soc3_pd = pd.DataFrame(boat_soc3)
# boat_soc3_pd.to_csv('boat_soc3.csv', index=False)

total_soc2_pd = pd.DataFrame(total_soc2)
total_soc2_pd.to_csv('total_soc2.csv', index=False)

bid_soc_pd = pd.DataFrame(bid_soc)
bid_soc_pd.to_csv('bid_soc.csv', index=False)

bid_soc_down_pd = pd.DataFrame(bid_soc_down)
bid_soc_down_pd.to_csv('bid_soc_down.csv', index=False)

# total_boat_pd = pd.DataFrame(total_boat)
# total_boat_pd.to_csv('total_boat_soc.csv', index=False)

# FCR_D_up_price_data_pd = pd.DataFrame(FCR_D_up_price_data)
# FCR_D_up_price_data_pd.to_csv('FCR_D_up_price_data.csv', index=False)

# total_fcr_revenue_pd = pd.DataFrame(total_fcr_revenue)
# total_fcr_revenue_pd.to_csv('total_fcr_revenue.csv', index=False)

#endregion