import numpy as np
import el_price

def el_cost(P_self, P_grid, load, p_cost, tax_cost, VAT):
    #Calculating the electricity cost
    #Price of electricity in SEK/kWh
    price = el_price.el_price()
    #Calculating the electricity cost for the spot price
    cost = np.zeros((24, 365))
    for i in range(24):
        for j in range(365):
            if P_self[i, j] > load[j]:
                cost[i, j] = 0 #Tidigare: (P_self[i, j] - load[j]) * price[i, j]
            else:
                cost[i, j] = (P_grid[i, j] - P_self[i, j]) * price[i, j]
    #Caluclateing the power cost for the peak in each month
    peak_cost = np.zeros((12))
    peak_month = [max(load[:, 0:31]), max(load[:, 31:59]), max(load[:, 59:90]), max(load[:, 90:120]), max(load[:, 120:151]), max(load[:, 151:181]), max(load[:, 181:212]), max(load[:, 212:243]), max(load[:, 243:273]), max(load[:, 273:304]), max(load[:, 304:334]), max(load[:, 334:365])])]
    for i in range(12):
        peak_cost[i] = peak_month[i] * p_cost
    #Calculating the total cost for the year
    cost_tax = np.zeros((24, 365))
    for i in range(24):
        for j in range(365):
            cost_tax[i, j] = load[i, j] * tax_cost
    #Calculating the total cost for the year
    total_cost = (cost.sum() + peak_cost.sum() + cost_tax.sum())*VAT 
    return total_cost