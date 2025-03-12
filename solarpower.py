from numpy import *
import pandas as pd
from math import *
 
#Reading excel file 
path_to_file = "/Users/a517469/Python/solardata_2023.xlsx"
 
df = pd.read_excel(path_to_file)

#Creting a matrix with zeros
I=zeros((24,366))

#Storing values from excel in I
for i in range(366):
    for j in range(24):
         I[j,i]=df.iloc[i*24+j,2]
	
#I_df = pd.DataFrame(I)
#print(I_df)

I_1=zeros((366))

for i in range(366):
      I_1[i]=sum(I[:,i])

print(I_1)

total_sum=nansum(I_1)
print(total_sum)


#I - irradiation in W/m^2
#A - amount of panels in m^2
#eta - efficency of PV farm
def solarpower(A, eta):
	
	P_s=(I*A*eta)/1000
	
	return P_s

P_s1=solarpower(167,0.22)
P_s2=pd.DataFrame(P_s1)
print(P_s2)

