#______Importing libraries_______________________________________________________________________________________________
#region
import numpy as np
import matplotlib.pyplot as plt
import load_krossholmen_2023
import solarpower
import windpower
import load_björkö
import load_björkö_bessekroken
import el_price
#endregion
#______Importing data___________________________________________________________________________________________
#region
load_krossholmen = load_krossholmen_2023.load
load_björkö_hamn=load_björkö.load
load_bessekroken=load_björkö_bessekroken.load 
load_winter_krossholmen = load_krossholmen_2023.load_winter
load_summer_krossholmen = load_krossholmen_2023.load_summer

spot_price_2023=el_price.spotprice_2023
spot_price_2023_winter=el_price.spotprice_2023_winter
spot_price_2023_summer=el_price.spotprice_2023_summer

#endregion
#________Paramters_______________________________________________________________________________________________________
#region
load = load_bessekroken
load_winter=load_winter_krossholmen
load_summer=load_summer_krossholmen

A=100
eta=0.2
n=1
#endregion
#________Reference Case__________________________________________________________________________________________________
#region Calculating the sum of the array for the yearly load 1X365 in Besskroken
yearly_load=np.zeros((365))
for i in range(365):
    yearly_load[i] = sum(load[:, i])

#Calculating the sum of the array for the yearly spot price in SE3 1X365
spot_price_2023_winter_1=np.zeros(24)
for i in range(24):
    spot_price_2023_winter_1[i] = sum(spot_price_2023_winter[i])/len(spot_price_2023_winter[i])

#Calculating the sum of the array for the yearly spot price in SE3 1X365
spot_price_2023_summer_1=np.zeros(24)
for i in range(24):
    spot_price_2023_summer_1[i] = sum(spot_price_2023_summer[i])/len(spot_price_2023_summer[i])
#endregion
#_________Plotting Reference Case________________________________________________________________________________________
#region Plotting the daily load in Bessekroken
plt.figure(figsize=(10, 5))
plt.plot(range(len(yearly_load)), yearly_load, label='Electricity Load')
plt.fill_between(range(len(yearly_load)), yearly_load, alpha=0.3)
plt.xlabel('Days')
plt.ylabel('Daily Load (kWh)')
plt.title('Electricity Load in 2023 in Krossholmen')
#plt.legend()
plt.xlim(0, 364)  # Set x-axis limits to start at 0 and end at 364
plt.ylim(0, (max(yearly_load))) 
#plt.grid(True)
plt.show(block=False)
plt.show()



# Create subplots for mean winter and summer daily load in Krossholmen with two y-axes
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))
fig.suptitle('Seasonal Daily Load in Krossholmen and Spot Price in SE3')

# Plot mean winter daily load in Krossholmen
ax1.plot(range(24), sum(load_winter)/len(load_winter), label='Mean Winter Load', color='tab:blue')
ax1.set_title('Winter')
ax1.set_ylabel('Load (kWh)', color='tab:blue')
ax1.set_xlabel('Time')
ax1.set_xlim(0, 23)
ax1.tick_params(axis='y', labelcolor='tab:blue')

# Create a second y-axis for the spot price in winter
ax1_2 = ax1.twinx()
ax1_2.plot(range(24), spot_price_2023_winter_1, label='Mean Winter Spot Price', color='tab:orange')
ax1_2.set_ylabel('Spot Price (SEK/kWh)', color='tab:orange')
ax1_2.tick_params(axis='y', labelcolor='tab:orange')

# Plot mean summer daily load in Krossholmen
ax2.plot(range(24), sum(load_summer)/len(load_summer), label='Mean Summer Load', color='tab:blue')
ax2.set_title('Summer')
ax2.set_ylabel('Load (kWh)', color='tab:blue')
ax2.set_xlabel('Time')
ax2.set_xlim(0, 23)
ax2.tick_params(axis='y', labelcolor='tab:blue')

# Create a second y-axis for the spot price in summer
ax2_2 = ax2.twinx()
ax2_2.plot(range(24), spot_price_2023_summer_1, label='Mean Summer Spot Price', color='tab:orange')
ax2_2.set_ylabel('Spot Price (SEK/kWh)', color='tab:orange')
ax2_2.tick_params(axis='y', labelcolor='tab:orange')

# Adjust layout
fig.tight_layout(rect=[0, 0, 1, 0.96])  # Adjust layout to make room for the main title
plt.show()


#endregion
#_________Case 1_________________________________________________________________________________________________________
#region Calculating selfproduced electricity
#Calling on function, change the values to get the desired result

P_s2=solarpower.solar(A,eta) #167m^2, 20% efficiency, which is the values of Krossholmen
P_wind2=windpower.wind(n) #1 turbine rated 5,5kW

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
P_SS=[]
P_Not_SS=[]
#If the value is negative it will be changed to 0
for i in range(24):
    for j in range(365):    
        if load[i, j] - P_s2[i, j] - P_wind2[i,j] < 0:
            P_self[i, j] = 0
            P_Not_SS.append(P_s2[i, j] + P_wind2[i,j])
        else:
            P_self[i, j] = load[i, j] - P_s2[i, j] - P_wind2[i,j]
            P_SS.append(P_s2[i, j] + P_wind2[i,j])
#Calculating the sum of the array 1X365
P_self1=np.zeros((365))
for i in range(365):
    P_self1[i] = sum(P_self[:, i])


print(f"Self consumed electricity {sum(P_SS)}")
print(f"Not used slef-produced electricity {sum(P_Not_SS)}")



#Calculating the total 
total_sum_sun=round(sum(P_s3)*10,1)/10
print(f"The yearly production of solar power is {total_sum_sun/1000}MWh")

total_sum_wind=round(sum(P_wind3)*10)/10
print(f"The yearly production of wind power is {total_sum_wind/1000}MWh")
#endregion
#______Plotting Case 1___________________________________________________________________________________________________
#region Plotting the daily electricity load
plt.figure(figsize=(10, 5))
#plt.plot(range(len(P_s3)), P_s3, label='Solar Power Production')
plt.plot(range(len(yearly_load)), yearly_load, label='The load of Bessekroken')
plt.fill_between(range(len(yearly_load)), yearly_load, alpha=1)
plt.plot(range(len(P_self1)), P_self1, label='The load of Bessekroken after self-produced electricity')
plt.fill_between(range(len(P_self1)), P_self1, alpha=1)
#plt.plot(range(len(P_wind3)), P_wind3, label='Wind Power Production')
plt.xlabel('Days of the year')
plt.ylabel('kWh')
plt.title('Self-produced electricity and load of Bessekroken')
plt.legend()
plt.xlim(0, 364)  # Set x-axis limits to start at 0 and end at 364
plt.ylim(0, (max(max(yearly_load), max(P_self1))+5)) 
#plt.grid(True)
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
plt.xlim(0, 364)  # Set x-axis limits to start at 0 and end at 364
plt.ylim(0, (max(max(P_wind3), max(P_s3))+5)) 
#plt.grid(True)
plt.show(block=False)
plt.show()
#endregion
