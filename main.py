# Reference case

#______Importing libraries_______________________________________________________#
import numpy as np
import matplotlib.pyplot as plt
import load_krossholmen_2023
import solarpower
import windpower
#import load_krossholmen_2024
import load_björkö_bessekroken
import el_price
#__________________________________________________________________________________________________________________________

#______Variables____________________________________________________________________________________________________________
Load_2023 = load_krossholmen_2023.load_aug
yearly_load = load_krossholmen_2023.yearly_load
yearly_load_bessekroken = load_björkö_bessekroken.yearly_load
#___________________________________________________________________________________________________________________________
#Calculating selfproduced electricity
#Calling on function, change the values to get the desired result
#Krossholmeen
P_s2=solarpower.solar(167,0.20) #167m^2, 20% efficiency
P_wind2=windpower.wind(1) #1 turbine rated 5,5kW

#Calculating the total 
total_sum_sun=round(sum(P_s2)*10,1)/10
print(f"The yearly production of solar power is {total_sum_sun}MWh")

total_sum_wind=round(sum(P_wind2)*10)/10
print(f"The yearly production of wind power is {total_sum_wind}MWh")

#______Plotting_____________________________________________________________________________________________________________
# Plotting the daily electricity load
plt.figure(figsize=(10, 5))
plt.plot(P_s2*1000, label='Solar Power Production')
plt.plot(yearly_load_bessekroken, label='Bessekroken')
plt.plot(P_wind2*1000, label='Wind Power Production')
plt.fill_between(range(len(yearly_load_bessekroken)), yearly_load_bessekroken, alpha=0.3, label='Daily Load Area')
plt.xlabel('Days of the year')
plt.ylabel('kWh')
plt.title('Self-produced electricity and load of Bessekroken')
plt.legend()
plt.grid(True)
plt.show()

#Plotting the daily load in krossholmen
plt.figure(figsize=(10, 5))
plt.plot(range(1, 365), yearly_load, label='Daily Electricity Load')
plt.fill_between(range(1, 365), yearly_load, alpha=0.3, label='Daily Load Area')
plt.xlabel('Day of the Year')
plt.ylabel('Daily Load (kWh)')
plt.title('Daily Electricity Load in 2023')
plt.legend()
plt.grid(True)
plt.show(block=False)
plt.show()


#______Maja's stuff__________________________________________________________________________________________________________
# Load_2024 = load_krossholmen_2024.load_aug
# print("Load August 2024",Load_2024)

#Load_2024_b = load_björkö_bessekroken.load_aug

# spotprice=el_price.spotprice_2024[:, 213:244]

# electricity_price= Load_2023 * spotprice 
# print("Spotprice August 2023", electricity_price)

# yearly_electricityprice = electricity_price.sum(axis=0)
# print("Total:", yearly_electricityprice.sum(axis=0))

# plt.figure(figsize=(10, 5))
# plt.plot(yearly_electricityprice)
# plt.grid(True)
# plt.show()
