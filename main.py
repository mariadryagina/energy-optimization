# Reference case

import numpy as np
import matplotlib.pyplot as plt
import load_krossholmen_2023
import load_björkö_bessekroken
import el_price

Load_2023 = load_krossholmen_2023.load_aug
print("Load August 2023",Load_2023)

#Load_2024 = load_krossholmen_2024.load_aug
#print("Load August 2024",Load_2024)

Load_2024_b = load_björkö_bessekroken.load_aug

spotprice=el_price.spotprice_2024[:, 213:244]

electricity_price= Load_2023 * spotprice 
print("Spotprice August 2024", electricity_price)

yearly_electricityprice = electricity_price.sum(axis=0)
print("Total:", yearly_electricityprice.sum(axis=0))

plt.figure(figsize=(10, 5))
plt.plot(yearly_electricityprice)
plt.grid(True)
plt.show()
