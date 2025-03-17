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
#______Variable and parameters___________________________________________________________________________________________
#region
load_krossholmen = load_krossholmen_2023.load
load_björkö_hamn=load_björkö.load
load_bessekroken=load_björkö_bessekroken.load 
load_winter_krossholmen = load_krossholmen_2023.load_winter
#endregion
#________Reference Case__________________________________________________________________________________________________
#region Calculating the sum of the array for the yearly load 1X365 in Besskroken
yearly_load_bessekroken=np.zeros((365))
for i in range(365):
    yearly_load_bessekroken[i] = sum(load_bessekroken[:, i])

#Calculating the sum of the array for the yearly load 1X365 in Krossholmen
yearly_load_krossholmen=np.zeros((365))
for i in range(365):
    yearly_load_krossholmen[i] = sum(load_krossholmen[:, i])

#Calculating the sum of the array for the yearly load 1X365 in Krossholmen
yearly_load_björkö=np.zeros((365))
for i in range(365):
    yearly_load_björkö[i] = sum(load_björkö_hamn[:, i])
#endregion
#_________Plotting Reference Case________________________________________________________________________________________
#region Plotting the daily load in Bessekroken
plt.figure(figsize=(10, 5))
plt.plot(range(len(yearly_load_bessekroken)), yearly_load_bessekroken, label='Electricity Load')
plt.fill_between(range(len(yearly_load_bessekroken)), yearly_load_bessekroken, alpha=0.3)
plt.xlabel('Days')
plt.ylabel('Daily Load (kWh)')
plt.title('Electricity Load in 2023 in Bessekroken')
#plt.legend()
plt.xlim(0, 364)  # Set x-axis limits to start at 0 and end at 364
plt.ylim(0, (max(yearly_load_bessekroken)+5)) 
#plt.grid(True)
plt.show(block=False)
plt.show()


#Plotting the daily load in Krossholmen
plt.figure(figsize=(10, 5))
plt.plot(range(len(yearly_load_krossholmen)), yearly_load_krossholmen, label='Electricity Load')
plt.fill_between(range(len(yearly_load_krossholmen)), yearly_load_krossholmen, alpha=0.3)
plt.xlabel('Days')
plt.ylabel('Daily Load (kWh)')
plt.title('Electricity Load in 2023 in Krossholmen')
#plt.legend()
plt.xlim(0, 364)  # Set x-axis limits to start at 0 and end at 364
plt.ylim(0, (max(yearly_load_krossholmen)+100)) 
#plt.grid(True)
plt.show(block=False)
plt.show()

# Create subplots
fig, axs = plt.subplots(1, 2, figsize=(10, 5))
fig.suptitle('Mean FCR-D up Prices During Different Seasons')
# Plot mean winter daily load in Krossholmen
axs[0].plot(sum(load_winter_krossholmen)/len(load_winter_krossholmen))
axs[0].set_title('Winter')
axs[0].set_ylabel('SEK/MWh')
axs[0].set_xlabel('Hour of the day')
axs[0].set_xlim(0, 23)
axs[0].grid(True)
# Plot mean summer daily load in Krossholmen
axs[1].plot(price_summer_mean_FCR_D_up)
axs[1].set_title('Summer')
axs[1].set_ylabel('SEK/MWh')
axs[1].set_xlabel('Hour of the day')
axs[1].set_xlim(0, 23)
axs[1].grid(True)

#Plotting the daily load in Björkö marina
plt.figure(figsize=(10, 5))
plt.plot(range(len(yearly_load_björkö)), yearly_load_björkö, label='Electricity Load')
plt.fill_between(range(len(yearly_load_björkö)), yearly_load_björkö, alpha=0.3)
plt.xlabel('Days of the Year')
plt.ylabel('Daily Load (kWh)')
plt.title('Electricity Load in 2023 in Björkö')
#plt.legend()
plt.xlim(0, 364)  # Set x-axis limits to start at 0 and end at 364
plt.ylim(0, (max(yearly_load_björkö)+100)) 
#plt.grid(True)
plt.show(block=False)
plt.show()
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
P_self = np.zeros((24, 365))
#If the value is negative it will be changed to 0
for i in range(24):
    for j in range(365):    
        if load_bessekroken[i, j] - P_s2[i, j] - P_wind2[i,j] < 0:
            P_self[i, j] = 0
        else:
            P_self[i, j] = load_bessekroken[i, j] - P_s2[i, j] - P_wind2[i,j]
#Calculating the sum of the array 1X365
P_self1=np.zeros((365))
for i in range(365):
    P_self1[i] = sum(P_self[:, i])

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
plt.plot(range(len(yearly_load_bessekroken)), yearly_load_bessekroken, label='The load of Bessekroken')
plt.fill_between(range(len(yearly_load_bessekroken)), yearly_load_bessekroken, alpha=1)
plt.plot(range(len(P_self1)), P_self1, label='The load of Bessekroken after self-produced electricity')
plt.fill_between(range(len(P_self1)), P_self1, alpha=1)

#plt.plot(range(len(P_wind3)), P_wind3, label='Wind Power Production')
plt.xlabel('Days of the year')
plt.ylabel('kWh')
plt.title('Self-produced electricity and load of Bessekroken')
plt.legend()
plt.xlim(0, 364)  # Set x-axis limits to start at 0 and end at 364
plt.ylim(0, (max(max(yearly_load_bessekroken), max(P_self1))+5)) 
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
