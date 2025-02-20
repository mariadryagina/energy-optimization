from numpy import *
import pandas as pd
from math import *
import matplotlib.pyplot as plt
 
#Reading excel file 
path_to_file = "/Users/a517469/Python/energy-optimization/winddata1.xlsx"
df = pd.read_excel(path_to_file)

#Creting a matrix with zeros
V=zeros((24,366))

for i in range(366):
    for j in range(24):
         V[j,i]=df.iloc[i*24+j,4]


#If a value is greater than 12 it will be changed to 12	
for i in range(24):
    for j in range(366):
        if V[i, j] > 12:
            V[i, j] = 12


#_Function begins_______________________________________________________________#
#V - wind speed in m/s
#n - amount of turbines
#The formula for wind power is P_w=4,8653*V^2,9637 and it is in W

def windpower(V,n):
     
     P_wind=(4.8653*V**2.9637*n)/(1000*1000)

     return P_wind
#_______________________________________________________________________________#

#Calling on function
P_wind1=windpower(V,1)

#Creating an array
P_wind2=zeros((366))

#Storing the sum of each column in the array
for i in range(366):
      P_wind2[i]=sum(P_wind1[:,i])

#Calculating the sum of the array
total_sum=ceil(sum(P_wind2)*10)/10
print(f"The yearly production of wind power 2024 is {total_sum}MWh")

#_______________________________________________________________________________#
# Creating a plot
plt.figure(figsize=(10, 5))
plt.plot(range(1, 367), P_wind2*1000, label='Daily Wind Power Production')
plt.xlabel('Day of the Year')
plt.ylabel('Wind Power Production (kWh)')
plt.title('Daily Wind Power Production in 2024')
plt.legend()
plt.grid(True)
plt.show()


