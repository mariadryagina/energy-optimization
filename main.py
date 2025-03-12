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
#Load_2023 = load_krossholmen_2023.load_aug
yearly_load = load_krossholmen_2023.yearly_load
yearly_load_bessekroken = load_björkö_bessekroken.yearly_load
load_bessekroken=load_björkö_bessekroken.load

#___________________________________________________________________________________________________________________________
#Calculating selfproduced electricity
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
P_self = np.zeros((24, 365))
#If the value is negative it will be changed to 0
for i in range(24):
    for j in range(365):    
        if load_bessekroken[i, j] - P_s2[i, j] - P_wind2[i,j] < 0:
            P_self[i, j] = 0
        else:
            P_self[i, j] = load_bessekroken[i, j] - P_s2[i, j] - P_wind2[i,j]
#Calculating the sum of the array 1X365
P_self1=np.zeros((365))  # Initialize P_s1 as an array
for i in range(365):
    P_self1[i] = sum(P_self[:, i])

#Calculating the total 
total_sum_sun=round(sum(P_s3)*10,1)/10
print(f"The yearly production of solar power is {total_sum_sun/1000}MWh")

total_sum_wind=round(sum(P_wind3)*10)/10
print(f"The yearly production of wind power is {total_sum_wind/1000}MWh")



#______Plotting_____________________________________________________________________________________________________________
# Plotting the daily electricity load
plt.figure(figsize=(10, 5))
#plt.plot(range(len(P_s3)), P_s3, label='Solar Power Production')
plt.plot(range(len(P_self1)), P_self1, label='The load of Bessekroken after self-produced electricity')
plt.fill_between(range(len(P_self1)), P_self1, alpha=0.3)
plt.plot(range(len(yearly_load_bessekroken)), yearly_load_bessekroken, label='The load of Bessekroken')
#plt.fill_between(range(len(yearly_load_bessekroken)), yearly_load_bessekroken, alpha=0.3, label='Daily Load Area')
#plt.plot(range(len(P_wind3)), P_wind3, label='Wind Power Production')
plt.xlabel('Days of the year')
plt.ylabel('kWh')
plt.title('Self-produced electricity and load of Bessekroken')
plt.legend()
plt.grid(True)
plt.show(block=False)
plt.show()

#Plotting the selfproduced electricity of wind and solar power
plt.figure(figsize=(10, 5))
plt.plot(range(len(P_wind3)), P_wind3, label='Wind Power Production')
plt.plot(range(len(P_s3)), P_s3, label='Solar Power Production')
plt.xlabel('Days of the year')
plt.ylabel('kWh')
plt.title('Self-produced electricity')
plt.legend()
plt.grid(True)
plt.show(block=False)
plt.show()

# #Plotting the daily load in krossholmen
# plt.figure(figsize=(10, 5))
# plt.plot(range(len(yearly_load)), yearly_load, label='Daily Electricity Load')
# plt.fill_between(range(len(yearly_load)), yearly_load, alpha=0.3, label='Daily Load Area')
# plt.xlabel('Day of the Year')
# plt.ylabel('Daily Load (kWh)')
# plt.title('Daily Electricity Load in 2023')
# plt.legend()
# plt.grid(True)
# plt.show(block=False)
# plt.show()


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
