#______Importing libraries_______________________________________________________________________________________________
#region

# This script requires the following::
# pip install pandas
# pip install matplotlib
# pip install numpy
# pip install scipy
# pip install pyomo
# pip install openpyxl

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import load_krossholmen_2023
import solarpower
import load_björkö
import load_björkö_bessekroken
import el_price
import el_cost
import Optimization
import usage_pattern
from scipy.interpolate import interp1d
from Effekthandel_väst import effekthandel_väst
from Frequency import frequency_price
import windequation

user = 1 #User: Maja = 1, Maria = 2
#endregion
#______Variable and parameters___________________________________________________________________________________________
#region
# load_winter_krossholmen = load_krossholmen_2023.load_winter
# load_summer_krossholmen = load_krossholmen_2023.load_summer

# marinas = ['Björkö', 'Krossholmen', 'Bessekroken']
marinas = ['Krossholmen'] #Choose which marina to simulate

for i in list(marinas):
    if i == 'Björkö':
        load_data = load_björkö.load
        solar_panel_area = (75+50)*0.85 # m^2
        turbines = 0 # Number of wind turbines
        grid_limit = 242.2 #Limitations of grid (abonnerad effekt) [kW]

        bess_capacity = 533 #kWh
        bess_charge_rate = 352 #kW
        bess_discharge_rate = 352 #kW

        boat_capacity = 100 #kWh
        boat_charge_rate = 60 #kW
        boat_discharge_rate = 60 #kW
    elif i == 'Krossholmen':
        load_data = load_krossholmen_2023.load
        solar_panel_area = 167 # m^2
        turbines = 1 # Number of wind turbines
        grid_limit = 1680 #Limitations of grid (abonnerad effekt) [kW]

        bess_capacity = 533 #kWh
        bess_charge_rate = 352 #kW
        bess_discharge_rate = 352 #kW

        boat_capacity = 100 #kWh
        boat_charge_rate = 60 #kW
        boat_discharge_rate = 60 #kW
    elif i == 'Bessekroken':
        load_data = load_björkö_bessekroken.load
        solar_panel_area = 250*0.85 # m^2
        turbines = 1
        grid_limit = 13.8 #Limitations of grid (abonnerad effekt) [kW]

        bess_capacity = 533 #kWh
        bess_charge_rate = 352 #kW
        bess_discharge_rate = 352 #kW

        boat_capacity = 100 #kWh
        boat_charge_rate = 60 #kW
        boat_discharge_rate = 60 #kW
    else:
        raise ValueError("Invalid marina name. Choose from 'Björkö', 'Krossholmen', or 'Bessekroken'.")

spot_price=el_price.spotprice_2023

#Costs for electricity
energy_tax = 0.439 #SEK/kWh
transmission_fee = 0.113 #SEK/kWh 
peak_cost = 61.55 #SEK/kWh

number_boats = 2 #Number of boats in the marina

# Bid size for the boats and BESS on the LFM
bid_size = 0.1 # % of the capacity

# Days for when the boat is unavailable for 14 days in a row
a = 162 # söndag 11 juni
b = 183 # söndag 2 juli
c = 204 # söndag 23 juli

#endregion
#________Reference Case__________________________________________________________________________________________________
#region

#Calculating the sum of the array for the yearly load 1X365
yearly_load=np.zeros((365))
for i in range(365):
    yearly_load[i] = sum(load_data[:, i])

#Calculating the sum of the array for the yearly spot price in SE3 1X365
yearly_spot_price=np.zeros((365))
for i in range(365):
    yearly_spot_price[i] = sum(spot_price[:, i])/len(spot_price[:, i])
#endregion
#_________Plotting Reference Case________________________________________________________________________________________
#region 
# Plotting the daily load
# plt.figure(figsize=(10, 5))
# plt.plot(range(len(yearly_load)), yearly_load, label='Electricity Load')
# plt.plot(range(len(yearly_spot_price)), yearly_spot_price, label='Spot Price')
# plt.fill_between(range(len(yearly_load)), yearly_load, alpha=0.3)
# plt.xlabel('Days')
# plt.ylabel('Daily Load (kWh)')
# plt.title('Electricity Load')
# #plt.legend()
# plt.xlim(0, 364)  # Set x-axis limits to start at 0 and end at 364
# plt.ylim(0, (max(yearly_load)+5)) 
# #plt.grid(True)
# plt.show(block=False)
# plt.show()

# # Create subplots
# fig, axs = plt.subplots(1, 2, figsize=(10, 5))
# fig.suptitle('Seasonal Daily Load')
# # Plot mean winter daily load
# axs[0].plot(sum(load_winter)/len(load_winter))
# axs[0].set_title('Winter')
# axs[0].set_ylabel('kWh')
# axs[0].set_xlabel('Hour of the day')
# axs[0].set_xlim(0, 23)
# #axs[0].grid(True)
# # Plot mean summer daily load
# axs[1].plot(sum(load_summer)/len(load_summer))
# axs[1].set_title('Summer')
# axs[1].set_ylabel('kWh')
# axs[1].set_xlabel('Hour of the day')
# axs[1].set_xlim(0, 23)
# #axs[1].grid(True)

#endregion
#__________________________________________________________________________________________________________________
#region Calculating selfproduced electricity

#Calling on functions for solar production and wind production, change the values to get the desired result
solar_power=solarpower.solar(solar_panel_area, 0.20) #20% efficiency
wind_power=windequation.wind(turbines) # Function set for a turbine rated at 5,5kW

#Calculating the sum of the array for the solar power 1X365
P_solar=np.zeros((365))  
for i in range(365):
    P_solar[i] = sum(solar_power[:, i])

#Calculating the sum of the array for the wind power 1X365
P_wind=np.zeros((365))
for i in range(365):
    P_wind[i]=sum(wind_power[:,i])

#Calculating the self consumed electricity with matrix 24x365
# P_self = np.zeros((24, 365))
# #If the value is negative it will be changed to 0
# for i in range(24):
#     for j in range(365):    
#         if load_bessekroken[i, j] - solar_power[i, j] - wind_power[i,j] < 0:
#             P_self[i, j] = 0
#         else:
#             P_self[i, j] = load_bessekroken[i, j] - solar_power[i, j] - wind_power[i,j]
# #Calculating the sum of the array 1X365
# P_self1=np.zeros((365))
# for i in range(365):
#     P_self1[i] = sum(P_self[:, i])

#Calculating the total electricity production from solar and wind power
total_sum_sun=round(sum(P_solar)*10,1)/10
print(f"The yearly production of solar power is {round(total_sum_sun/1000, 2)} MWh")

total_sum_wind=round(sum(P_wind)*10,1)/10
print(f"The yearly production of wind power is {round(total_sum_wind/1000, 2)} MWh")
#endregion

# plt.figure()
# plt.plot(P_wind)
# plt.plot(P_solar, color='darkorange')
# plt.legend(['Yearly wind production','Yearly solar production'])
# plt.ylabel('Electricity production [kWh]')
# plt.xlabel('Days')
# plt.show()

#______Boat availability and power________________________________________________________________________________________
# Boat availability and power (available = 0, unavailable = 1, power is unused)
boat_availability1, boat_power1 = usage_pattern.usage_pattern(a, 100, 90, 60)  # 24x365
boat_availability2, boat_power2 = usage_pattern.usage_pattern(b, 100, 90, 60)  # 24x365
boat_availability3, boat_power3 = usage_pattern.usage_pattern(c, 100, 90, 60)  # 24x365

battery_lower_limit = 0.1 #Lower limit of the battery SOC
battery_upper_limit = 0.9 #Upper limit of the battery SOC

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

cycl_cost = round((((3000000*0.35) + (9.66 * 150 * boat_capacity * number_boats)) * (1 - 0.3)) / (5380 * (bess_capacity + boat_capacity * number_boats)), 3)
print(f"Cycl cost: {cycl_cost} SEK/kWh")

#Boat load is an array representing electricity need for the boat. This is used to control the SOC och the boat batteries in the optimization code.
#Before a trip SOC = 90 %, during a trip SOC = 10 %, when arriving back SOC = 20 %
boat_load1 = usage_pattern.boat_load(boat_availability1, (battery_upper_limit-battery_lower_limit)*boat_capacity*number_boats1, 0.1*boat_capacity*number_boats1)
boat_load2 = usage_pattern.boat_load(boat_availability2, (battery_upper_limit-battery_lower_limit)*boat_capacity*number_boats2, 0.1*boat_capacity*number_boats2)
boat_load3 = usage_pattern.boat_load(boat_availability3, (battery_upper_limit-battery_lower_limit)*boat_capacity*number_boats3, 0.1*boat_capacity*number_boats3)

#______LCM: Effekthandel väst________________________________________________________________________________________
# LCM: Matrix for bids and activated
bids_effekthandelväst_data = effekthandel_väst.I_bid #  (0 = no bid, 1 = bid)
activated_bids_effekthandelväst_data = effekthandel_väst.I_activated # (0 = no bid or no activation of bid, 1 = bid activated)
# This is used when simulating no the case of no participation on LFM
# bids_effekthandelväst_data = np.zeros((24,365))
# activated_bids_effekthandelväst_data = np.zeros((24,365))

# Matrix with the bids and their sizes for the different batteries
bid_bess = activated_bids_effekthandelväst_data * bess_capacity * bid_size
bid_boat1 = activated_bids_effekthandelväst_data * boat_capacity * number_boats1 * bid_size
bid_boat2 = activated_bids_effekthandelväst_data * boat_capacity * number_boats2 * bid_size
bid_boat3 = activated_bids_effekthandelväst_data * boat_capacity * number_boats3 * bid_size

#Cost of electricity for the reference case
old_cost = el_cost.cost(None, None, load_data, 61.55, 0.439, 0.113, 1.25)

#______Calling optimization function________________________________________________________________________________________
Calling the optimization function
model = Optimization.optimize_microgrid(solar_power, wind_power, load_data, spot_price, grid_limit, bess_capacity, bess_charge_rate, bess_discharge_rate, boat_capacity, boat_charge_rate, boat_discharge_rate, battery_lower_limit, battery_upper_limit, number_boats1, number_boats2, number_boats3, boat_availability1, boat_availability2, boat_availability3, boat_load1, boat_load2, boat_load3, user, energy_tax, transmission_fee, cycl_cost, peak_cost, bids_effekthandelväst_data, activated_bids_effekthandelväst_data, bid_bess, bid_boat1, bid_boat2, bid_boat3, bid_size)

#______Plotting results________________________________________________________________________________________
old_grid_usage = np.zeros((24, 365))  # Initial load data
grid_used_battery = np.zeros((24, 365))  # Grid usage with battery data
grid_used_load = np.zeros((24, 365))  # Grid usage with load data
self_sufficiency = np.zeros((24, 365))  # Self sufficiency data
self_production = np.zeros((24, 365))  # Self production data
self_production_used = np.zeros((24, 365))  # Self production used data
sold_electricity = np.zeros((24, 365))  # Sold electricity data
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
#bidplaced = np.zeros((24, 365))  # Bid placed data
spotprice = np.zeros((24, 365))  # Spot price data

# Now you can access the model and its results
for h in model.HOURS:
    for d in model.DAYS:
        old_grid_usage[h, d] = load_data[h][d]  # Initial load
        grid_used_battery[h, d] = model.grid_used_battery[h, d].value  # Grid usage with battery
        grid_used_load[h, d] = model.grid_used_load[h, d].value  # Grid usage with load
        self_production[h, d] = model.self_production[h, d]  # Self production
        self_production_used[h, d] = model.self_production_used[h, d].value
        sold_electricity[h, d] = model.grid_sold[h, d].value
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
        #bidplaced [h, d] = model.bid_placed[h, d].value  # Bid placed data
        spotprice [h, d] = spot_price[h][d]  # Spot price data

#Calculating the cost of electricity for the opttimized grid usage
opt_cost = el_cost.cost(None, None, grid_used_load + grid_used_battery, 61.55, 0.439, 0.113, 1.25)

total_grid_usage = np.zeros((24, 365))
total_grid_usage = grid_used_battery + grid_used_load

plt.figure()
plt.plot(np.sum(old_grid_usage, axis=0))
plt.plot(np.sum(total_grid_usage, axis=0))
plt.legend(['Old grid usage', 'New grid usage'])
plt.ylabel(['Electricity drawn from the grid [kWh]'])
plt.xlabel(['Days'])
plt.show()

bess_soc_values = np.zeros(8760) 
bess_charge_values = np.zeros( 8760) 
bess_discharge_values = np.zeros(8760)  # Battery discharge data

boat_soc1_values = np.zeros(8760)
boat_soc2_values = np.zeros(8760)
boat_soc3_values = np.zeros(8760)

boat_charge1_values = np.zeros(8760)
boat_charge2_values = np.zeros(8760)
boat_charge3_values = np.zeros(8760)

load_data_hourly = np.zeros(8760)
grid_used_battery_hourly = np.zeros(8760)
grid_used_load_hourly = np.zeros(8760)
self_production_hourly = np.zeros(8760)
self_production_used_hourly = np.zeros(8760)
self_sufficiency_hourly = np.zeros(8760)
sold_electricity_hourly = np.zeros(8760)
sold_electricity_solar_hourly = np.zeros(8760)
spot_price_hourly = np.zeros(8760)

# Function used to calculate the energy throughput
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
energy_throughput = np.zeros(1)

if number_boats == 0:
    boat_charge1_values = np.zeros(8760)
    boat_soc1_values = np.zeros(8760)
    boat_charge2_values = np.zeros(8760)
    boat_soc2_values = np.zeros(8760)
    boat_charge3_values = np.zeros(8760)
    boat_soc3_values = np.zeros(8760)
    energy_throughput = np.zeros(8760).sum()
else:
    boat_charge1_values, boat_soc1_values = hourly_values(boat_soc1, boat_soc1_values, boat_charge1, boat_charge1_values, boat_discharge1, number_boats1)
    boat_charge2_values, boat_soc2_values = hourly_values(boat_soc2, boat_soc2_values, boat_charge2, boat_charge2_values, boat_discharge2, number_boats2)
    boat_charge3_values, boat_soc3_values = hourly_values(boat_soc3, boat_soc3_values, boat_charge3, boat_charge3_values, boat_discharge3, number_boats3)
    energy_throughput = round(((boat_discharge1.sum()+boat_discharge2.sum()+boat_discharge3.sum()+boat_charge1.sum()+boat_charge2.sum()+boat_charge3.sum())/(2*number_boats)))

def hourly_values2(RES, DATA):
    i = 0
    for d in range(365):
        for h in range(24):
            RES[i] = DATA[h, d]
            i += 1
    return RES

load_data_hourly = hourly_values2(load_data_hourly, load_data)
grid_used_battery_hourly = hourly_values2(grid_used_battery_hourly, grid_used_battery)
grid_used_load_hourly = hourly_values2(grid_used_load_hourly, grid_used_load)
self_production_hourly = hourly_values2(self_production_hourly, self_production)
self_production_used_hourly = hourly_values2(self_production_used_hourly, self_production_used)
self_sufficiency_hourly = hourly_values2(self_sufficiency_hourly, self_sufficiency)
sold_electricity_hourly = hourly_values2(sold_electricity_hourly, sold_electricity)
spot_price_hourly = hourly_values2(spot_price_hourly, spotprice)

old_load_winter = old_grid_usage[:, np.concatenate((np.arange(334, 365), np.arange(0, 59)))]
old_load_spring = old_grid_usage[:, 59:151]
old_load_summer = old_grid_usage[:, 151:243]
old_load_autumn = old_grid_usage[:, 243:334]

new_load_winter = total_grid_usage[:, np.concatenate((np.arange(334, 365), np.arange(0, 59)))]
new_load_spring = total_grid_usage[:, 59:151]
new_load_summer = total_grid_usage[:, 151:243]
new_load_autumn = total_grid_usage[:, 243:334]

spot_price_winter = spotprice[:, np.concatenate((np.arange(334, 365), np.arange(0, 59)))]
spot_price_spring = spotprice[:, 59:151]
spot_price_summer = spotprice[:, 151:243]
spot_price_autumn = spotprice[:, 243:334]

for h in range(8760):
    if self_production_used_hourly[h] == 0:
        sold_electricity_solar_hourly[h] = 0 
    else:
        sold_electricity_solar_hourly[h] = self_production_hourly[h] - self_production_used_hourly[h]

print(f"Old cost: {round(old_cost.sum())} SEK, Old grid usage: {round(old_grid_usage.sum()/1000,2)} MWh")
print(f"Optimized cost: {round(opt_cost.sum())} SEK, Optimized grid usage: {round((grid_used_load + grid_used_battery).sum()/1000,2)} MWh")
print(f'Grid to load: {round(grid_used_load.sum()/1000, 2)} MWh, Grid to battery: {round(grid_used_battery.sum()/1000, 2)} MWh')
print(f"Self production: {round(self_production.sum()/1000, 2)} MWh", 
      f"PV+wind electricity sold: {round(np.nansum(sold_electricity_solar_hourly)/1000, 2)} MWh")
print(f"Cycl cost: {round(cycl_cost, 2)} SEK/kWh")
print(f"Energy throughput BESS: {round(((bess_discharge.sum()+bess_charge.sum())/2))} kWh, Energy throughput boat (mean): {energy_throughput} kWh")
print(f"Electricity market revenue, from BESS and boats: {round((sold_electricity*spotprice).sum(),1)} SEK, from solar: {round(np.nansum(sold_electricity_solar_hourly*spot_price_hourly),1)} SEK")
print(f"Power bid revenue: {round((0.2*bid_size*(bess_capacity+boat_capacity*(number_boats1+number_boats2+number_boats3))*bids_effekthandelväst_data).sum())} SEK")
print(f"Power activated revenue: {round(3.5*(bid_bess+bid_boat1+bid_boat2+bid_boat3).sum())} SEK")
#print(f'Power throughput BESS: {round((bess_discharge.sum))}, Power throughput boat (mean): {round(((boat_discharge1+boat_discharge2+boat_discharge3)/number_boats).sum())} MWh')
#print(f"Self sufficiency: {round(((self_sufficiency_hourly/(grid_used_battery_hourly + grid_used_load_hourly))*100).sum())} %")




#Arrays for daytype for each month, 0 = weekday, 1 = weekend
jan_daytype = np.array([1, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0])
feb_daytype = np.array([0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0])
mar_daytype = np.array([0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0])
apr_daytype = np.array([1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1])
may_daytype = np.array([1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0])
jun_daytype = np.array([0, 0, 1, 1, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0])
jul_daytype = np.array([1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0])
aug_daytype = np.array([0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0])
sep_daytype = np.array([0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1])
oct_daytype = np.array([1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0])
nov_daytype = np.array([0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0])
dec_daytype = np.array([0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1, 1])

winter_daytype = np.concatenate((dec_daytype, jan_daytype, feb_daytype))
spring_daytype = np.concatenate((mar_daytype, apr_daytype, may_daytype))
summer_daytype = np.concatenate((jun_daytype, jul_daytype, aug_daytype))
autumn_daytype = np.concatenate((sep_daytype, oct_daytype, nov_daytype))

#Empty matrixes for the next step
old_load_winter_weekday = []
old_load_winter_weekend = []
old_load_spring_weekday = []
old_load_spring_weekend = []
old_load_summer_weekday = []
old_load_summer_weekend = []
old_load_autumn_weekday = []
old_load_autumn_weekend = []
new_load_winter_weekday = []
new_load_winter_weekend = []
new_load_spring_weekday = []
new_load_spring_weekend = []
new_load_summer_weekday = []
new_load_summer_weekend = []
new_load_autumn_weekday = []
new_load_autumn_weekend = []
spot_price_winter_weekday = []
spot_price_winter_weekend = []
spot_price_summer_weekday = []
spot_price_summer_weekend = []

#for-loops positioning the load values for either weekday or weekend in different matrixes
#each row represents the load for one hour in the day

def load_weekday_weekend(DAYTYPE, WEEKDAY, WEEKEND, OLDLOAD):
    for i, value in enumerate(DAYTYPE):
        if value == 0:
            WEEKDAY.append(OLDLOAD[:, i])
        if value == 1:
            WEEKEND.append(OLDLOAD[:, i])
    return WEEKDAY, WEEKEND
old_load_winter_weekday, old_load_winter_weekend = load_weekday_weekend(winter_daytype, old_load_winter_weekday, old_load_winter_weekend, old_load_winter)
old_load_spring_weekday, old_load_spring_weekend = load_weekday_weekend(spring_daytype, old_load_spring_weekday, old_load_spring_weekend, old_load_spring)
old_load_summer_weekday, old_load_summer_weekend = load_weekday_weekend(summer_daytype, old_load_summer_weekday, old_load_summer_weekend, old_load_summer)
old_load_autumn_weekday, old_load_autumn_weekend = load_weekday_weekend(autumn_daytype, old_load_autumn_weekday, old_load_autumn_weekend, old_load_autumn)
new_load_winter_weekday, new_load_winter_weekend = load_weekday_weekend(winter_daytype, new_load_winter_weekday, new_load_winter_weekend, new_load_winter)
new_load_spring_weekday, new_load_spring_weekend = load_weekday_weekend(spring_daytype, new_load_spring_weekday, new_load_spring_weekend, new_load_spring)
new_load_summer_weekday, new_load_summer_weekend = load_weekday_weekend(summer_daytype, new_load_summer_weekday, new_load_summer_weekend, new_load_summer)
new_load_autumn_weekday, new_load_autumn_weekend = load_weekday_weekend(autumn_daytype, new_load_autumn_weekday, new_load_autumn_weekend, new_load_autumn)
spot_price_winter_weekday, spot_price_winter_weekend = load_weekday_weekend(winter_daytype, spot_price_winter_weekday, spot_price_winter_weekend, spot_price_winter)
spot_price_summer_weekday, spot_price_summer_weekend = load_weekday_weekend(summer_daytype, spot_price_summer_weekday, spot_price_summer_weekend, spot_price_summer)




#_____Frequency market: FCR-D_________________________________________________________________________________________________________
#region
#FCR-D up revenue
#total_soc=bess_soc_values + boat_soc1_values + boat_soc2_values + boat_soc3_values
total_boat=boat_soc1 + boat_soc2 + boat_soc3
TOTAL_CAPACITY = bess_capacity + boat_capacity * number_boats
P_bud = 0.5 * TOTAL_CAPACITY - 0.1 * TOTAL_CAPACITY # 50% of the total capacity
P_bud_summer = 0.5 * bess_capacity - 0.1 * bess_capacity #


# Initialize a 24x365 matrix with zeros
total_soc1 = np.zeros((24, 365)) # Battery state of charge data (total charge)
bid_matrix = np.zeros((24, 365))
# Set 1s for hours 0-7 and 19-23
bid_matrix[0:6, :] = 1  # Hours 0-7
bid_matrix[6:19, :] = None
bid_matrix[19:24, :] = 1  # Hours 19-23


# Reshape the matrix to 8760x1 in column-major order
bid_matrix_reshaped = bid_matrix.reshape(-1, order='F')

for i in range(365):
    for j in range(24):
        if  121 <= i <= 273:
            total_soc1[j, i] = bess_soc[j, i]
        else:
            total_soc1[j,i] = bess_soc[j,i] + boat_soc1[j,i] + boat_soc2[j,i] + boat_soc3[j,i]

total_soc2=bid_matrix * total_soc1


#FCR-D up revenue________________________________________________________________________________________________________   
FCR_D_up_price_data=(frequency_price.FCR_D_up_2024)/1000
bid_soc = np.zeros((24,365)) # Battery state of charge data (total charge)
total_fcr_revenue=np.zeros((24,365)) 
# hours=np.zeros(24,365)
count=0

# Iterate over the indices and values of total_soc
for i in range(365):
    for j in range(24):
        if j < 23:
            if 0 <= i <= 120 and total_soc2[j,i] >= 0.6 * TOTAL_CAPACITY and total_soc2[j+1, i] >= 0.6 * TOTAL_CAPACITY:
                count += 1
                total_fcr_revenue[j,i]= FCR_D_up_price_data[j,i].item() * P_bud
                bid_soc[j,i] = total_soc2[j,i]
            elif 121 <= i <= 273 and total_soc2[j,i] >= 0.6 * bess_capacity and total_soc2[j+1,i] >= 0.6 * bess_capacity:
                count += 1
                total_fcr_revenue[j,i]= FCR_D_up_price_data[j,i].item() * P_bud_summer
                bid_soc[j,i] = total_soc2[j,i]
            elif 274 <= i <= 365 and total_soc2[j,i] >= 0.6 * TOTAL_CAPACITY and total_soc2[j+1, i] >= 0.6 * TOTAL_CAPACITY:
                count += 1
                total_fcr_revenue[j,i]= FCR_D_up_price_data[j,i].item() * P_bud
                bid_soc[j,i] = total_soc2[j,i]
        else:  # For hour 23 (last hour of the day)
            if 0 <= i <= 120 and total_soc2[j, i] >= 0.6 * TOTAL_CAPACITY:
                count += 1
                total_fcr_revenue[j, i] = FCR_D_up_price_data[j, i].item() * P_bud
                bid_soc[j, i] = total_soc2[j, i]
            elif 121 <= i <= 273 and total_soc2[j, i] >= 0.6 * bess_capacity:
                count += 1
                total_fcr_revenue[j, i] = FCR_D_up_price_data[j, i].item() * P_bud_summer
                bid_soc[j, i] = total_soc2[j, i]
            elif 274 <= i <= 365 and total_soc2[j, i] >= 0.6 * TOTAL_CAPACITY:
                count += 1
                total_fcr_revenue[j, i] = FCR_D_up_price_data[j, i].item() * P_bud
                bid_soc[j, i] = total_soc2[j, i]



total_fcr_revenue_reshaped=np.zeros((365))  
for i in range(365):
    total_fcr_revenue_reshaped[i] = sum(total_fcr_revenue[:, i])

print(f"FCR-D up revenue: {sum(total_fcr_revenue_reshaped)} SEK")
print(f"FCR-D up participant: {count} h")
#_________________________________________________________________________________________________________________________

#FCR-D down revenue______________________________________________________________________________________________________
FCR_D_down_price_data=(frequency_price.FCR_D_down_2024)/1000
total_fcr_down_revenue=np.zeros((24,365)) 
count_1=0
bid_soc_down = np.zeros((24,365))

# Iterate over the indices and values of total_soc
for i in range(365):
    for j in range(24):
        if j < 23:
            if 0 <= i <= 120 and total_soc2[j,i] < 0.4 * TOTAL_CAPACITY and total_soc2[j+1, i] < 0.4 * TOTAL_CAPACITY:
                count_1 += 1
                total_fcr_down_revenue[j,i]= FCR_D_down_price_data[j,i].item() * P_bud
                bid_soc_down[j,i] = total_soc2[j,i]
            elif 121 <= i <= 273 and total_soc2[j,i] < 0.4 * bess_capacity and total_soc2[j+1,i] < 0.4 * bess_capacity:
                count_1 += 1
                total_fcr_down_revenue[j,i]= FCR_D_down_price_data[j,i].item() * P_bud_summer
                bid_soc_down[j,i] = total_soc2[j,i]
            elif 274 <= i <= 365 and total_soc2[j,i] < 0.4 * TOTAL_CAPACITY and total_soc2[j+1, i] < 0.4 * TOTAL_CAPACITY:
                count_1 += 1
                total_fcr_down_revenue[j,i]= FCR_D_down_price_data[j,i].item() * P_bud
                bid_soc_down[j,i] = total_soc2[j,i]
        else:  # For hour 23 (last hour of the day)
            if 0 <= i <= 120 and total_soc2[j, i] < 0.4 * TOTAL_CAPACITY:
                count_1 += 1
                total_fcr_down_revenue[j, i] = FCR_D_down_price_data[j, i].item() * P_bud
                bid_soc_down[j, i] = total_soc2[j, i]
            elif 121 <= i <= 273 and total_soc2[j, i] < 0.4 * bess_capacity:
                count_1 += 1
                total_fcr_down_revenue[j, i] = FCR_D_down_price_data[j, i].item() * P_bud_summer
                bid_soc_down[j, i] = total_soc2[j, i]
            elif 274 <= i <= 365 and total_soc2[j, i] < 0.4 * TOTAL_CAPACITY:
                count_1 += 1
                total_fcr_down_revenue[j, i] = FCR_D_down_price_data[j, i].item() * P_bud
                bid_soc_down[j, i] = total_soc2[j, i]


total_fcr_down_revenue_reshaped=np.zeros((365))  
for i in range(365):
    total_fcr_down_revenue_reshaped[i] = sum(total_fcr_down_revenue[:, i])

print(f"FCR-D down revenue: {sum(total_fcr_down_revenue_reshaped)} SEK")
print(f"FCR-D down participant: {count_1} h")


# #_____________________________________________________________________________________________
# #PLOT
# Plotting)
plt.figure(figsize=(12, 6))

# Plot old grid usage
plt.plot((load_data_hourly), linewidth=0.5)
plt.plot((grid_used_load_hourly + grid_used_battery_hourly), color='darkseagreen', alpha=0.8, linewidth=0.5)
plt.legend(['Old grid usage', 'New grid usage'])
plt.xlim(0, 8760)  # Set x-axis limits to start at 0 and end at 8760
plt.xlabel('Hour')
plt.ylabel('Electricity drawn from the grid [kWh]')
plt.show()

# plt.figure(figsize=(12, 6))

# # Plot the sold electricity
# plt.plot((sold_electricity_hourly))
# plt.title('Sold electricity')
# plt.xlim(0, 8760)  # Set x-axis limits to start at 0 and end at 8760
# plt.xlabel('Hour')
# plt.ylabel('kWh')
# plt.show()

# # Plot BESS and boat
# plt.figure
# plt.subplot(2, 1, 1)
# plt.plot((bess_soc_values))
# plt.legend(['SOC'])
# plt.ylim(0, 500)
# plt.title('BESS')
# plt.xlabel('Hours')
# plt.ylabel('kW')

# plt.subplot(2, 1, 2)
# plt.plot((bess_charge_values))
# plt.legend(['Charge/Discharge'])
# plt.xlabel('Hours')
# plt.ylabel('kW')
# plt.show()

# #Plot new grid usage
# plt.figure
# plt.subplot(3, 3, 1)
# plt.plot((boat_soc1_values))
# plt.legend(['SOC'])
# plt.ylim(0, 100)
# plt.title('Boattype 1')
# plt.xlabel('Hours')
# plt.ylabel('kWh')

# plt.subplot(3, 3, 2)
# plt.plot((boat_soc2_values))
# plt.legend(['SOC'])
# plt.ylim(0, 100)
# plt.title('Boattype 2')
# plt.xlabel('Hours')
# plt.ylabel('kWh')

# plt.subplot(3, 3, 3)
# plt.plot((boat_soc3_values))
# plt.legend(['SOC'])
# plt.ylim(0, 100)
# plt.title('Boattype 3')
# plt.xlabel('Hours')
# plt.ylabel('kWh')

# plt.subplot(3, 3, 4)
# plt.plot((boat_charge1_values))
# plt.legend(['Charge/Discharge'])
# plt.xlabel('Hours')
# plt.ylabel('kWh')

# plt.subplot(3, 3, 5)
# plt.plot((boat_charge2_values))
# plt.legend(['Charge/Discharge'])
# plt.xlabel('Hours')
# plt.ylabel('kWh')

# plt.subplot(3, 3, 6)
# plt.plot((boat_charge3_values))
# plt.legend(['Charge/Discharge'])
# plt.xlabel('Hours')
# plt.ylabel('kWh')

# plt.subplot(3, 3, 7)
# plt.plot((boat_soc1_values[3024:3048]))
# #plt.plot((boat_soc1_values[3912:4248]))
# plt.legend(['Charge/Discharge'])
# plt.ylim(0, 100)
# plt.xlabel('Hours')
# plt.ylabel('kWh')

# plt.subplot(3, 3, 8)
# # plt.plot((boat_soc2_values[(b*24):(b*24+24*14)]))
# plt.plot((boat_soc2_values[4392:4752]))
# plt.legend(['Charge/Discharge'])
# plt.ylim(0, 100)
# plt.xlabel('Hours')
# plt.ylabel('kWh')

# plt.subplot(3, 3, 9)
# plt.plot((boat_soc3_values[(c*24):(c*24+24*14)]))
# plt.legend(['Charge/Discharge'])
# plt.ylim(0, 100)
# plt.xlabel('Hours')
# plt.ylabel('kWh')

# plt.tight_layout()
# plt.show()

#_________________________________________________________________________________________________________________________________________________________

# #position for the time on the x-axis
tick_locations = [0, 6, 12, 18, 24]

#Winter, weekday
ffig, ax1 = plt.subplots(figsize=(8, 6))

mean_old_load_winter_weekday = np.mean(old_load_winter_weekday, axis=0)
mean_new_load_winter_weekday = np.mean(new_load_winter_weekday, axis=0)
ax1.plot(mean_old_load_winter_weekday, label='Old mean grid usage')
ax1.plot(mean_new_load_winter_weekday, label='New mean grid usage', color='darkseagreen')
ax1.set_ylabel('Electricity drawn from the grid [kWh]')
ax1.set_ylim(78, 238)
ax1.set_xlabel('Hour of day')
ax1.set_xticks(tick_locations)
ax1.set_xticklabels([str(h) for h in tick_locations])

# Horizontal grid lines (match both y-axes)
ax1.grid(True, axis='y', color='lightgray', linewidth=0.7, zorder=1)

# Vertical grid lines only at selected hours
for x in tick_locations:
    ax1.axvline(x=x, color='lightgray', linewidth=0.7, zorder=0)

# Twin y-axis for spot price
ax2 = ax1.twinx()
mean_spot_price_winter_weekday = np.mean(spot_price_winter_weekday, axis=0)
ax2.plot(mean_spot_price_winter_weekday, label='Mean spot price', color='teal', linestyle='dashed', linewidth=1)
ax2.set_ylabel('Spot price [SEK/kWh]', color='teal')
ax2.tick_params(axis='y', which='both', labelcolor='teal')

# Optional: add legends
ax1.legend(loc='upper left')
ax2.legend(loc='upper right')

plt.tight_layout()
plt.show()

#Winter, weekend
ffig, ax1 = plt.subplots(figsize=(8, 6))

mean_old_load_winter_weekend = np.mean(old_load_winter_weekend, axis=0)
mean_new_load_winter_weekend = np.mean(new_load_winter_weekend, axis=0)
ax1.plot(mean_old_load_winter_weekend, label='Old mean grid usage')
ax1.plot(mean_new_load_winter_weekend, label='New mean grid usage', color='darkseagreen')
ax1.set_ylabel('Electricity drawn from the grid [kWh]')
ax1.set_ylim(68, 210)
ax1.set_xlabel('Hour of day')
ax1.set_xticks(tick_locations)
ax1.set_xticklabels([str(h) for h in tick_locations])

# Horizontal grid lines (match both y-axes)
ax1.grid(True, axis='y', color='lightgray', linewidth=0.7, zorder=1)

# Vertical grid lines only at selected hours
for x in tick_locations:
    ax1.axvline(x=x, color='lightgray', linewidth=0.7, zorder=0)

# Twin y-axis for spot price
ax2 = ax1.twinx()
mean_spot_price_winter_weekend = np.mean(spot_price_winter_weekend, axis=0)
ax2.plot(mean_spot_price_winter_weekend, label='Mean spot price', color='teal', linestyle='dashed', linewidth=1)
ax2.set_ylabel('Spot price [SEK/kWh]', color='teal', )
ax2.tick_params(axis='y', which='both', labelcolor='teal')

# Optional: add legends
ax1.legend(loc='upper left')
ax2.legend(loc='upper right')

plt.tight_layout()
plt.show()

#Summer, weekday
ffig, ax1 = plt.subplots(figsize=(8, 6))

mean_old_load_summer_weekday = np.mean(old_load_summer_weekday, axis=0)
mean_new_load_summer_weekday = np.mean(new_load_summer_weekday, axis=0)
ax1.plot(mean_old_load_summer_weekday, label='Old mean grid usage')
ax1.plot(mean_new_load_summer_weekday, label='New mean grid usage', color='darkseagreen')
ax1.set_ylabel('Electricity drawn from the grid [kWh]')
ax1.set_xlabel('Hour of day')
ax1.set_xticks(tick_locations)
ax1.set_xticklabels([str(h) for h in tick_locations])

# Horizontal grid lines (match both y-axes)
ax1.grid(True, axis='y', color='lightgray', linewidth=0.7, zorder=1)

# Vertical grid lines only at selected hours
for x in tick_locations:
    ax1.axvline(x=x, color='lightgray', linewidth=0.7, zorder=0)

# Twin y-axis for spot price
ax2 = ax1.twinx()
mean_spot_price_summer_weekday = np.mean(spot_price_summer_weekday, axis=0)
ax2.plot(mean_spot_price_summer_weekday, label='Mean spot price', color='teal', linestyle='dashed', linewidth=1)
ax2.set_ylabel('Spot price [SEK/kWh]', color='teal', )
ax2.tick_params(axis='y', which='both', labelcolor='teal')

# Optional: add legends
ax1.legend(loc='upper left')
ax2.legend(loc='upper right')

plt.tight_layout()
plt.show()

#Summer, weekend
ffig, ax1 = plt.subplots(figsize=(8, 6))

mean_old_load_summer_weekend = np.mean(old_load_summer_weekend, axis=0)
mean_new_load_summer_weekend = np.mean(new_load_summer_weekend, axis=0)
ax1.plot(mean_old_load_summer_weekend, label='Old mean grid usage')
ax1.plot(mean_new_load_summer_weekend, label='New mean grid usage', color='darkseagreen')
ax1.set_ylabel('Electricity drawn from the grid [kWh]')
ax1.set_xlabel('Hour of day')
ax1.set_xticks(tick_locations)
ax1.set_xticklabels([str(h) for h in tick_locations])

# Horizontal grid lines (match both y-axes)
ax1.grid(True, axis='y', color='lightgray', linewidth=0.7, zorder=1)

# Vertical grid lines only at selected hours
for x in tick_locations:
    ax1.axvline(x=x, color='lightgray', linewidth=0.7, zorder=0)

# Twin y-axis for spot price
ax2 = ax1.twinx()
mean_spot_price_summer_weekend = np.mean(spot_price_summer_weekend, axis=0)
ax2.plot(mean_spot_price_summer_weekend, label='Mean spot price', color='teal', linestyle='dashed', linewidth=1)
ax2.set_ylabel('Spot price [SEK/kWh]', color='teal', )
ax2.tick_params(axis='y', which='both', labelcolor='teal')

# Optional: add legends
ax1.legend(loc='upper left')
ax2.legend(loc='upper right')

plt.tight_layout()
plt.show()

#




