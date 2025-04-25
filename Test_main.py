#______Importing libraries_______________________________________________________________________________________________
#region
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import load_krossholmen_2023
import solarpower
import windpower
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

user = 2 #User: Maja = 1, Maria = 2
#endregion
#______Variable and parameters___________________________________________________________________________________________
#region
# load_winter_krossholmen = load_krossholmen_2023.load_winter
# load_summer_krossholmen = load_krossholmen_2023.load_summer

# marinas = ['Björkö', 'Krossholmen', 'Bessekroken']
marinas = ['Björkö'] #, 'Krossholmen', 'Bessekroken']

for i in list(marinas):
    if i == 'Björkö':
        load_data = load_björkö.load
        solar_panel_area = 100 # m^2
        turbines = 0 # Number of wind turbines
        grid_limit = 242.2 #Limitations of grid, abbonerad effekt [kW]

        bess_capacity = 500 #kWh
        bess_charge_rate = 350 #kW
        bess_discharge_rate = 350 #kW

        boat_capacity = 100 #kWh
        boat_charge_rate = 60 #kW
        boat_discharge_rate = 60 #kW
    elif i == 'Krossholmen':
        load_data = load_krossholmen_2023.load
        solar_panel_area = 100 # m^2
        turbines = 1 # Number of wind turbines
        grid_limit = 1680 #Limitations of grid, abbonerad effekt [kW]

        bess_capacity = 500 #kWh
        bess_charge_rate = 350 #kW
        bess_discharge_rate = 350 #kW

        boat_capacity = 100 #kWh
        boat_charge_rate = 60 #kW
        boat_discharge_rate = 60 #kW
    elif i == 'Bessekroken':
        load_data = load_björkö_bessekroken.load
        solar_panel_area = 100 # m^2
        turbines = 1
        grid_limit = 13.8 #Limitations of grid, abbonerad effekt [kW]

        bess_capacity = 500 #kWh
        bess_charge_rate = 350 #kW
        bess_discharge_rate = 350 #kW

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

number_boats = 3 #Number of boats in the marina

# Bid size for the boats and BESS on the LFM
bid_size = 0.2 # % of the capacity

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
#_________Case 1_________________________________________________________________________________________________________
#region Calculating selfproduced electricity
#Calling on function, change the values to get the desired result

solar_power=solarpower.solar(solar_panel_area,0.20) #20% efficiency
#wind_power=windpower.wind(turbines) # Function set for a turbine rated at 5,5kW
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

#Calculating the total 
total_sum_sun=round(sum(P_solar)*10,1)/10
print(f"The yearly production of solar power is {round(total_sum_sun/1000)} MWh")

total_sum_wind=round(sum(P_wind)*10,1)/10
print(f"The yearly production of wind power is {round(total_sum_wind/1000)} MWh")
#endregion


#______Plotting Case 1___________________________________________________________________________________________________
#region Maybe remove??
# Plotting the daily electricity load
# plt.figure(figsize=(10, 5))
# #plt.plot(range(len(P_solar)), P_solar, label='Solar Power Production')
# plt.plot(range(len(yearly_load_bessekroken)), yearly_load_bessekroken, label='The load of Bessekroken')
# plt.fill_between(range(len(yearly_load_bessekroken)), yearly_load_bessekroken, alpha=1)
# plt.plot(range(len(P_self1)), P_self1, label='The load of Bessekroken after self-produced electricity')
# plt.fill_between(range(len(P_self1)), P_self1, alpha=1)

# #plt.plot(range(len(P_wind)), P_wind, label='Wind Power Production')
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
# plt.plot(range(len(P_wind)), P_wind, label='Wind Power Production')
# plt.plot(range(len(P_solar)), P_solar, label='Solar Power Production')
# plt.xlabel('Days of the year')
# plt.ylabel('kWh')
# plt.title('Self-produced electricity')
# plt.legend()
# plt.xlim(0, 364)  # Set x-axis limits to start at 0 and end at 364
# plt.ylim(0, (max(max(P_wind), max(P_solar))+5)) 
# #plt.grid(True)
# plt.show(block=False)
# plt.show()
#endregion

#______Boat availability and power________________________________________________________________________________________
# Boat availability and power
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

boat_load1 = usage_pattern.boat_load(boat_availability1, (battery_upper_limit-battery_lower_limit)*boat_capacity*number_boats1, 0.1*boat_capacity*number_boats1)
boat_load2 = usage_pattern.boat_load(boat_availability2, (battery_upper_limit-battery_lower_limit)*boat_capacity*number_boats2, 0.1*boat_capacity*number_boats2)
boat_load3 = usage_pattern.boat_load(boat_availability3, (battery_upper_limit-battery_lower_limit)*boat_capacity*number_boats3, 0.1*boat_capacity*number_boats3)

#______LCM: Effekthandel väst________________________________________________________________________________________
# LCM: Matrix for bids and activation
bids_effekthandelväst_data = effekthandel_väst.I_bid
activated_bids_effekthandelväst_data = effekthandel_väst.I_activated

# Matrix with bids for the different batteries
bid_bess = activated_bids_effekthandelväst_data * bess_capacity * bid_size
bid_boat1 = activated_bids_effekthandelväst_data * boat_capacity * number_boats1 * bid_size
bid_boat2 = activated_bids_effekthandelväst_data * boat_capacity * number_boats2 * bid_size
bid_boat3 = activated_bids_effekthandelväst_data * boat_capacity * number_boats3 * bid_size

#______Calling optimization function________________________________________________________________________________________
model = Optimization.optimize_microgrid(solar_power, wind_power, load_data, spot_price, grid_limit, bess_capacity, bess_charge_rate, bess_discharge_rate, boat_capacity, boat_charge_rate, boat_discharge_rate, battery_lower_limit, battery_upper_limit, number_boats1, number_boats2, number_boats3, boat_availability1, boat_availability2, boat_availability3, boat_load1, boat_load2, boat_load3, user, energy_tax, transmission_fee, peak_cost, bids_effekthandelväst_data, activated_bids_effekthandelväst_data, bid_bess, bid_boat1, bid_boat2, bid_boat3, bid_size)

#______Plotting results________________________________________________________________________________________
old_grid_usage = np.zeros((24, 365))  # Initial load data
grid_used_battery = np.zeros((24, 365))  # Grid usage with battery data
grid_used_load = np.zeros((24, 365))  # Grid usage with load data
self_sufficiency = np.zeros((24, 365))  # Self sufficiency data
self_production = np.zeros((24, 365))  # Self production data
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
spotprice = np.zeros((24, 365))  # Spot price data

# Now you can access the model and its results
for h in model.HOURS:
    for d in model.DAYS:
        old_grid_usage[h, d] = load_data[h][d]  # Initial load
        grid_used_battery[h, d] = model.grid_used_battery[h, d].value  # Grid usage with battery
        grid_used_load[h, d] = model.grid_used_load[h, d].value  # Grid usage with load
        self_production[h, d] = solar_power[h][d] + wind_power[h][d]  # Self production
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
        spotprice [h, d] = spot_price[h][d]  # Spot price data

old_cost = el_cost.cost(None, None, old_grid_usage, 61.55, 0.439, 0.113, 1.25)
opt_cost = el_cost.cost(None, None, grid_used_load + grid_used_battery, 61.55, 0.439, 0.113, 1.25)

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
grid_used_battery_hourly = hourly_values2(grid_used_battery_hourly, grid_used_battery)
grid_used_load_hourly = hourly_values2(grid_used_load_hourly, grid_used_load)
self_production_hourly = hourly_values2(self_production_hourly, self_production)
self_sufficiency_hourly = hourly_values2(self_sufficiency_hourly, self_sufficiency)
sold_electricity_hourly = hourly_values2(sold_electricity_hourly, sold_electricity)

print(f"Old cost: {round(old_cost.sum())} SEK, Old grid usage: {round(old_grid_usage.sum())} MWh")
print(f"Optimized cost: {round(opt_cost.sum())} SEK, Optimized grid usage: {round((grid_used_load + grid_used_battery).sum())} MWh")
print(f'Grid to load: {round(grid_used_load.sum())} MWh, Grid to battery: {round(grid_used_battery.sum())} MWh')
print(f"Electricity market revenue: {round((sold_electricity*spotprice).sum(),1)} SEK")
print(f"Power bid revenue: {round((0.2*bid_size*(bess_capacity+boat_capacity*(number_boats1+number_boats2+number_boats3))*bids_effekthandelväst_data).sum())} SEK")
print(f"Power activated revenue: {round(3.5*(bid_bess+bid_boat1+bid_boat2+bid_boat3).sum())} SEK")
#print(f"Self sufficiency: {round(((self_sufficiency_hourly/(grid_used_battery_hourly + grid_used_load_hourly))*100).sum())} %")

# Plotting)
plt.figure(figsize=(12, 6))

# Plot old grid usage
plt.subplot(3, 1, 1)
plt.plot((load_data_hourly))
plt.title('Old Grid Usage (Initial Load)')
plt.xlabel('Day')
plt.ylabel('kWh')

# Plot new grid usage
plt.subplot(3, 1, 2)
plt.plot((grid_used_battery_hourly + grid_used_load_hourly + self_production_hourly))
plt.plot((grid_used_battery_hourly))
plt.plot((self_production_hourly))
plt.legend(['Grid usage', 'Grid usage to the battery', 'Self production'])
plt.title('New Grid Usage (Optimized)')
plt.xlabel('Days')
plt.ylabel('kWh')

plt.subplot(3, 1, 3)
plt.plot((sold_electricity_hourly))
plt.title('Sold Electricity')
plt.xlabel('Days')
plt.ylabel('kWh')
plt.show()

# Plot BESS and boat
plt.figure
plt.subplot(2, 1, 1)
plt.plot((bess_soc_values))
plt.legend(['SOC'])
plt.ylim(0, 500)
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
plt.ylim(0, 100)
plt.title('Boattype 1')
plt.xlabel('Hours')
plt.ylabel('kWh')

plt.subplot(3, 3, 2)
plt.plot((boat_soc2_values))
plt.legend(['SOC'])
plt.ylim(0, 100)
plt.title('Boattype 2')
plt.xlabel('Hours')
plt.ylabel('kWh')

plt.subplot(3, 3, 3)
plt.plot((boat_soc3_values))
plt.legend(['SOC'])
plt.ylim(0, 100)
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
plt.plot((boat_soc1_values[3024:3048]))
#plt.plot((boat_soc1_values[3912:4248]))
plt.legend(['Charge/Discharge'])
plt.ylim(0, 100)
plt.xlabel('Hours')
plt.ylabel('kWh')

plt.subplot(3, 3, 8)
# plt.plot((boat_soc2_values[(b*24):(b*24+24*14)]))
plt.plot((boat_soc2_values[4392:4752]))
plt.legend(['Charge/Discharge'])
plt.ylim(0, 100)
plt.xlabel('Hours')
plt.ylabel('kWh')

plt.subplot(3, 3, 9)
plt.plot((boat_soc3_values[(c*24):(c*24+24*14)]))
plt.legend(['Charge/Discharge'])
plt.ylim(0, 100)
plt.xlabel('Hours')
plt.ylabel('kWh')

plt.tight_layout()
plt.show()

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


#FCR-D revenue   
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


#FCR-D down revenue
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


#region
# # Creating csv files
# boat_load1_pd = pd.DataFrame(boat_load1)
# boat_load1_pd.to_csv('BOAT_LOAD.csv', index=False)

# boat_soc1_pd = pd.DataFrame(boat_soc1)
# boat_soc1_pd.to_csv('BOAT_SOC_1.csv', index=False)

# boat_soc2_pd = pd.DataFrame(boat_soc2)
# boat_soc2_pd.to_csv('BOAT_SOC_2.csv', index=False)

# boat_soc3_pd = pd.DataFrame(boat_soc3)
# boat_soc3_pd.to_csv('BOAT_SOC_3.csv', index=False)

# spot_price_pd = pd.DataFrame(spot_price)
# spot_price_pd.to_csv('spot_price.csv', index=False)

# sold_electricity_pd = pd.DataFrame(sold_electricity)
# sold_electricity_pd.to_csv('sold_electricity.csv', index=False)

# self_production_pd = pd.DataFrame(self_production)
# self_production_pd.to_csv('self_production.csv', index=False)

# spot_price_pd = pd.DataFrame(spot_price)
# spot_price_pd.to_csv('spot_price.csv', index=False)

# sold_electricity_pd = pd.DataFrame(sold_electricity)
# sold_electricity_pd.to_csv('sold_electricity.csv', index=False)

# grid_used_battery_pd = pd.DataFrame(grid_used_battery)
# grid_used_battery_pd.to_csv('grid_used_battery.csv', index=False)

# grid_used_load_pd = pd.DataFrame(grid_used_load)
# grid_used_load_pd.to_csv('grid_used_load.csv', index=False)

# grid_total_pd = pd.DataFrame(grid_used_battery + grid_used_load)
# grid_total_pd.to_csv('grid_total.csv', index=False)

# old_grid_usage_pd = pd.DataFrame(old_grid_usage)
# old_grid_usage_pd.to_csv('old_grid_usage.csv', index=False)

# hours_pd = pd.DataFrame(hours_1)
# hours_pd.to_csv('Hours_soc.csv', index=False)

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

# bid_soc_down_pd = pd.DataFrame(bid_soc_down)
# bid_soc_down_pd.to_csv('bid_soc_down.csv', index=False)

# total_boat_pd = pd.DataFrame(total_boat)
# total_boat_pd.to_csv('total_boat_soc.csv', index=False)

# FCR_D_down_price_data_pd = pd.DataFrame(FCR_D_down_price_data)
# FCR_D_down_price_data_pd.to_csv('FCR_D_down_price_data.csv', index=False)

total_fcr_revenue_pd = pd.DataFrame(total_fcr_revenue)
total_fcr_revenue_pd.to_csv('total_fcr_revenue.csv', index=False)

# total_fcr_down_revenue_pd = pd.DataFrame(total_fcr_down_revenue)
# total_fcr_down_revenue_pd.to_csv('total_fcr_down_revenue.csv', index=False)
#endregion
#endregion