from numpy import *
import pandas as pd
from math import *
import matplotlib.pyplot as plt 
from matplotlib.colors import LinearSegmentedColormap
import el_cost

#Different mondays when the boat is used for 14 days in a row
#a=163 #måndag 12 juni
#a=205 #måndag 24 juli
#a=226 #måndag 14 augusti

#Plug in the capcaity of the boat batteryin kWh [P_battery]
#Plug in the SOC_upper 90%
#Plug in the SOC_lower 10%
#Plug in the capacity of the charger in kW [P_charger]

#Sets the usage pattern for a boat(1 = on a trip, 0 = available for B2G)
def usage_pattern(a, P_battery, SOC_upper, P_charger):
    P_b = zeros((24, 365))
    P_b_power = zeros((24, 365))  # kWh
    for day in range(365):
        for hour in range(24):
            P_b[hour, day] = 1
            P_b_power[hour, day] = P_battery * SOC_upper

    for day in range(126, 274, 14):  # Start at day 126, end at day 273, step by 14 days
        P_b[0:9, day] = 1  # Set the first 9 hours to 1
        P_b_power[0:10, day] = P_battery * SOC_upper
        P_b[10:13, day] = 0
        P_b_power[11, day] = 61.04
        P_b_power[12, day] = 48.7
        P_b_power[13, day] = 22.57

        # Charging the battery
        for hour in range(14, 24):
            if P_b_power[hour - 1, day] + P_charger < P_battery:
                P_b_power[hour, day] = P_b_power[hour - 1, day] + P_charger
            else:
                P_b_power[hour, day] = P_battery * SOC_upper

        P_b[14:24, day] = 1

    for day in range(a, a + 14):  # Start at day `a`, end at day `a+14`
        if day < 365:  # Ensure day does not exceed bounds
            if day == a:  # For the first day (day `a`)
                P_b[0:10, day] = 1  # Set the first 10 hours to 1
                P_b[10:24, day] = 0  # Set the rest of the hours to 0
            else:  # For the remaining days (day `a+1` to `a+13`)
                P_b[:, day] = 0  # Set all hours to 0
            P_b_power[:, day] = 0  # Reset the power for all hours

            if day == a + 13:
                P_b_power[13, day] = 22.57
                # Charging the battery
                for hour in range(14, 24):
                    if P_b_power[hour - 1, day] + P_charger < P_battery:
                        P_b_power[hour, day] = P_b_power[hour - 1, day] + P_charger
                    else:
                        P_b_power[hour, day] = P_battery * SOC_upper
                        P_b[hour, day] = 1

    return P_b, P_b_power

def boat_load(availability, SOC_leaving, SOC_arriving):
    boat_load = zeros((24, 365))
    for d in range(365):
        for h in range(24):
            if h == 0 and d == 0:
                boat_load[h, d] = 0  # Use assignment operator
            elif h == 0:
                if availability[23, d-1] == 1 and availability[h, d] == 0:
                    boat_load[23, d-1] = SOC_leaving  # Use assignment operator
                elif availability[23, d-1] == 0 and availability[h, d] == 1:
                    boat_load[23, d-1] = -SOC_arriving
                else:
                    boat_load[23, d-1] = 0
            else:
                if availability[h-1, d] == 1 and availability[h, d] == 0:
                    boat_load[h-1, d] = SOC_leaving  # Use assignment operator
                elif availability[h-1, d] == 0 and availability[h, d] == 1:
                    boat_load[h-1, d] = -SOC_arriving
                else:
                    boat_load[h-1, d] = 0
    return boat_load

# #region Calling on function

P_b, P_b_power=usage_pattern(205, 100, 0.9, 60)

a=163
# Flatten the P_b_power array to 1x8760
P_b_power_flat = P_b_power.flatten(order='F')
P_b_flat=P_b.flatten(order='F')
P_b_power_day=P_b_power_flat[3024:3049]
P_b_power_week=P_b_power_flat[a*24:a*24+24*14]

#endregion

#region Plotting
# # Plotting the battery power usage pattern as a line plot
# plt.figure(figsize=(8, 5))
# plt.plot(P_b_power_day, label='Battery Power')
# plt.xlabel('Hours')
# plt.ylabel('Battery Power (kWh)')
# plt.title('Boat battery availability')
# plt.xticks(ticks=range(25), labels=range(25))
# plt.xlim(0, 24)
# plt.grid(True)
# plt.legend()
# plt.show()

# #Create a continuous colormap
# cmap = LinearSegmentedColormap.from_list('custom_cmap', ['white', 'blue', 'lightblue'])

# # Plotting the usage pattern for verification
# plt.figure(figsize=(10, 5))
# plt.imshow(P_b, aspect='auto', cmap=cmap, interpolation='none')
# plt.colorbar(label='Usage Pattern')
# plt.xlabel('Days of the Year')
# plt.ylabel('Hours of the Day')
# plt.title('Usage Pattern of Leisure Boat')
# plt.gca().invert_yaxis()
# plt.show()
#endregion
#_____________________________________________________________________________________________
# # Convert the NumPy array to a DataFrame
# P_b_power_df = pd.DataFrame(P_b_power)

# # Save the frequency data to a CSV file for further analysis
# P_b_power_df.to_csv('usage_pattern.csv', index=False)

# Boat_load = boat_load(P_b, 0.8)

# Boat_load_df = pd.DataFrame(Boat_load)
# Boat_load_df.to_csv('boat_load.csv', index=False)

# Charge_req_df = pd.DataFrame(charge_required1)
# Charge_req_df.to_csv('charge_requirements.csv', index=False)

# # Convert the NumPy array to a DataFrame
# P_b_df = pd.DataFrame(P_b)

# # Save the frequency data to a CSV file for further analysis
# P_b_df.to_csv('usage_pattern_01.csv', index=False)


#________________Anteckningar_______________________________________________________________________________
#Oktober - april båten står still 
#0, båten står alltid i hamnen
#Maj - september båten används en gång varannan vecka
#Används varje dag i två veckor någon gång melan maj och september 
#1, båten borta

#FRÅGA! Ska jag simulera tillgänglig energi i batteriet också?
#FRÅGA! Under helgerna på sommaren när båtarna är i hamnen tänkte 
#jag att den kommer vara 0 vissa timmar och 1 vissa (under natten)
#Hur åker de iväg en vanlig dag?

