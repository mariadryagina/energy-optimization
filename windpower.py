from numpy import *
import pandas as pd
from math import *
 
#Reading excel file 
path_to_file = "/Users/a517469/Python/winddata.xlsx"
 
df = pd.read_excel(path_to_file)

#Creting a matrix with zeros
V=zeros((24,366))

for i in range(366):
    for j in range(24):
         V[j,i]=df.iloc[i*24+j,4]
	
for i in range(24):
    for j in range(366):
        if V[i, j] > 12:
            V[i, j] = 12

#V_df = pd.DataFrame(V)
#print(V_df)

# Calculate the mean value of the entire matrix V
mean_value = mean(V)
print(f"The mean value of the matrix V: {mean_value}")



#V - wind speed in m/s
#n - amount of turbines
#The formula for wind power is P_w=4,8653*V^2,9637 and it is in W

def windpower(V,n):
     
     P_wind=(4.8653*V**2.9637)*n/1000

     return P_wind

P_wind1=windpower(V,1)
P_wind2=pd.DataFrame(P_wind1)
print(P_wind2)

V_1=zeros((366))

for i in range(366):
      V_1[i]=sum(P_wind1[:,i])

print(V_1)

total_sum=sum(V_1)
print(total_sum)


