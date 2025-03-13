from numpy import *
import pandas as pd
from math import *
import matplotlib.pyplot as plt 
from matplotlib.colors import LinearSegmentedColormap

#Different mondays when the boat is used for 14 days in a row
#a=163 #måndag 12 juni
#a=205 #måndag 24 juli
#a=226 #måndag 14 augusti

def usage_pattern(a):
    P_b=zeros((24,365))
    for day in range(365):
        for hour in range(24):
            P_b[hour,day]=0
    #126:e dagen är 6:e maj vilket är 1 helgen då båten används
    
    for day in range(126, 274, 14):  # Start at day 126, end at day 273, step by 14 days
        P_b[range(0,10), day] = 0 #kommer varierar mellan 0 och 1
        P_b[range(10,14), day] = 1
        P_b[range(14,24), day] = 0

    for day in range(a, a+14):  # Start at day 163, end at day 163+14
        P_b[:, day] = 1
    
    return P_b


P_b=usage_pattern(163)

# Create a continuous colormap
cmap = LinearSegmentedColormap.from_list('custom_cmap', ['white', 'blue', 'lightblue'])

# Plotting the usage pattern for verification
plt.figure(figsize=(10, 5))
plt.imshow(P_b, aspect='auto', cmap=cmap, interpolation='none')
plt.colorbar(label='Usage Pattern')
plt.xlabel('Days of the Year')
plt.ylabel('Hours of the Day')
plt.title('Usage Pattern of Leisure Boat')
plt.gca().invert_yaxis()
plt.show()



#________________Anteckningar_______________________________________________________________________________
#Oktober - april båten står still 
#0, båten står alltid i hamnen
#Maj - september båten används en gång varannan vecka
#Används varje dag i två veckor någon gång melan maj och september 
#1, båten kan användas inom vissa tider
#2, båten är borta helt

#FRÅGA! Ska jag simulera tillgänglig energi i batteriet också?
#FRÅGA! Under helgerna på sommaren när båtarna är i hamnen tänkte 
#jag att den kommer vara 0 vissa timmar och 1 vissa (under natten)
#Hur åker de iväg en vanlig dag?

