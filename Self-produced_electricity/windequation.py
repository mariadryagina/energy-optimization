import numpy as np
import math
import matplotlib.pyplot as plt 

watt=np.array([0.1,0.2,0.35,0.5,0.8,1.3,2,2.7,3.7,5,6,6])
m_s=np.array([2,3,4,5,6,7,8,9,10,11,12,13])


# Creating the plot
plt.figure(figsize=(10, 5))
plt.plot(m_s, watt, marker='o', linestyle='-', label='Power Output')
plt.xlabel('Wind Speed (m/s)')
plt.ylabel('Power Output (kW)')
plt.title('Wind turbine power curve')
plt.legend()
plt.grid(True)
plt.show()
