import numpy as np
import el_price

def cost(P_sun, P_wind, P_load, power_tariff, tax_cost, transmission_cost, VAT):
    if P_sun is None:
        P_sun = np.zeros((24, 365))
    else:
        P_sun = P_sun
    if P_wind is None:
        P_wind = np.zeros((24, 365))
    else:
        P_wind = P_wind
    #Calculating the electricity cost
    #Price of electricity in SEK/kWh
    price = el_price.spotprice_2023
    #Calculating the electricity cost for the spot price and the cost of electricity tax
    cost_electricity = np.zeros((24, 365))
    cost_tax = np.zeros((24, 365))
    cost_transmission = np.zeros((24, 365))
    for i in range(24):
        for j in range(365):
            if (P_sun[i, j] + P_wind[i, j]) > P_load[i, j]:
                cost_electricity[i, j] = 0 #Tidigare: (P_self[i, j] - load[j]) * price[i, j]
                cost_tax[i, j] = 0
                cost_transmission[i, j] = 0
            else:
                cost_electricity[i, j] = (P_load[i, j] - (P_sun[i, j] + P_wind[i, j])) * price[i, j]
                cost_tax[i, j] = P_load[i, j] * tax_cost
                cost_transmission[i, j] = P_load[i, j] * transmission_cost
    #Caluclateing the power cost for the peak in each month
    peak_cost = np.zeros(12)
    peak_month = np.array([np.max(P_load[:, 0:31]), np.max(P_load[:, 31:59]), np.max(P_load[:, 59:90]), np.max(P_load[:, 90:120]), np.max(P_load[:, 120:151]), np.max(P_load[:, 151:181]), np.max(P_load[:, 181:212]), np.max(P_load[:, 212:243]), np.max(P_load[:, 243:273]), np.max(P_load[:, 273:304]), np.max(P_load[:, 304:334]), np.max(P_load[:, 334:365])])
    for i in range(12):
        peak_cost[i] = peak_month[i] * power_tariff
    #peak_cost_matrix = np.zeroes((24,365))
    # Deviding the fixed costs for each hour
    # for i in range(12):
    #     if i == 0:
    #         peak_cost_matrix [:, 0:31] = peak_cost[i]/(len(P_load[:, 0:31])*24)
                
    #Calculating the total cost for the year
    #total_cost_matrix = np.zeroes((24,365))
    #total_cost_matrix = (cost_electricity + cost_tax + cost_transmission)*VAT
    # print(total_cost_matrix)
    # print(total_cost_matrix.shape)
    total_cost = (cost_electricity.sum() + cost_tax.sum() + cost_transmission.sum() + peak_cost.sum())*VAT 
    return total_cost