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
import Optimization
import usage_pattern
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
# boat_load1 = usage_pattern.boat_load(boat_availability1, 0.8)
# boat_load2 = usage_pattern.boat_load(boat_availability2, 0.8)
# boat_load3 = usage_pattern.boat_load(boat_availability3, 0.8)
charge_required1 = usage_pattern.soc_target(boat_availability1)
charge_required2 = usage_pattern.soc_target(boat_availability2)
charge_required3 = usage_pattern.soc_target(boat_availability3)

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
user = 1 #User: Maja = 1, Maria = 2
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

model = Optimization.optimize_microgrid(solar_data, wind_data, load_data, spot_price_data, grid_limit, bess_capacity, bess_charge_rate, bess_discharge_rate, bess_cycling_cost, boat_capacity, boat_charge_rate, boat_discharge_rate, boat_cycling_cost, number_boats1, number_boats2, number_boats3, boat_availability1, boat_availability2, boat_availability3, charge_required1, charge_required2, charge_required3, user, energy_tax, transmission_fee, peak_cost)

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

bess_soc_values = []
bess_charge_values = []
bess_discharge_values = []

boat_soc1_values = []
boat_soc2_values = []
boat_soc3_values = []
boat_charge1_values = []
boat_charge2_values = []
boat_charge3_values = []

load_data_hourly = []
new_grid_usage_hourly = []
self_production_hourly = []
self_sufficiency_hourly = []

def hourly_values(SOC, SOCRES, CHR, CHRRES, DIS, BOAT):
    for d in range(365):
        for h in range(24):
            #Hourly charging data for plotting
            if DIS[h, d] > 0:
                CHRRES.append(float(-DIS[h, d]))
            elif CHR[h, d] > 0:
                CHRRES.append(float(CHR[h, d]))
            else:
                CHRRES.append(float(0))

            #Hourly SoC-data for plotting
            if BOAT == 0:
                SOCRES.append(0)
            else:
                SOCRES.append(float(SOC[h, d]/BOAT))
    return CHRRES, SOCRES
        
bess_charge_values, bess_soc_values = hourly_values(bess_soc, bess_soc_values, bess_charge, bess_charge_values, bess_discharge, 1)
boat_charge1_values, boat_soc1_values = hourly_values(boat_soc1, boat_soc1_values, boat_charge1, boat_charge1_values, boat_discharge1, number_boats1)
boat_charge2_values, boat_soc2_values = hourly_values(boat_soc2, boat_soc2_values, boat_charge2, boat_charge2_values, boat_discharge2, number_boats2)
boat_charge3_values, boat_soc3_values = hourly_values(boat_soc3, boat_soc3_values, boat_charge3, boat_charge3_values, boat_discharge3, number_boats3)

boat_soc3_pd = pd.DataFrame(boat_soc3)
boat_soc3_pd.to_csv('Boat_SOC_24x365.csv', index=False)
boat_soc3_values_pd = pd.DataFrame(boat_soc3_values)
boat_soc3_values_pd.to_csv('Boat_SOC_8760.csv', index=False)

for d in range(365):
    for h in range(24):
        load_data_hourly.append(float(load_data[h, d]))
        new_grid_usage_hourly.append(float(new_grid_usage[h, d]))
        self_production_hourly.append(float(self_production[h, d]))
        self_sufficiency_hourly.append(float(self_sufficiency[h, d]))

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
plt.plot((boat_soc1_values[a*24:a*24+23]))
plt.legend(['Charge/Discharge'])
plt.xlabel('Hours')
plt.ylabel('kWh')

plt.subplot(3, 3, 8)
plt.plot((boat_soc2_values[b*24:b*24+23]))
plt.legend(['Charge/Discharge'])
plt.xlabel('Hours')
plt.ylabel('kWh')

plt.subplot(3, 3, 9)
plt.plot((boat_soc3_values[c*24:c*24+23]))
plt.legend(['Charge/Discharge'])
plt.xlabel('Hours')
plt.ylabel('kWh')

plt.tight_layout()
plt.show()