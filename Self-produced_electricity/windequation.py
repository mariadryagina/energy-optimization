import numpy as np
import math
import matplotlib.pyplot as plt 

watt=np.array([40,122,290,560,980,1550,2300,3300,4500,6000,7800,7800,7800,7800])/1000
m_s=np.array([2,3,4,5,6,7,8,9,10,11,12,13,14,15])


# Creating the plot
plt.figure(figsize=(10, 5))
plt.plot(m_s, watt, marker='o', linestyle='-', label='Power Output')
plt.xlabel('Wind Speed (m/s)')
plt.ylabel('Power Output (kW)')
plt.title('Wind turbine power curve')
plt.legend()
plt.grid(True)
plt.show()
