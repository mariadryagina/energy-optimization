# Requires pip install pyomo
import numpy as np
import pandas as pd
from pyomo.environ import *
from pyomo.opt import SolverStatus, TerminationCondition
import matplotlib as plt

# Define the optimization model
def optimize_microgrid(solar_data, wind_data, load_data, spot_price_data, grid_limit, bess_capacity, bess_charge_rate, bess_discharge_rate, boat_capacity, boat_charge_rate, boat_discharge_rate, number_boats1, number_boats2, number_boats3, boat_availability1, boat_availability2, boat_availability3, boat_load1, boat_load2, boat_load3, user, energy_tax, transmission_fee, peak_cost, bids_effekthandelväst_data, activated_bids_effekthandelväst_data):
    model = ConcreteModel()

    # ---Define sets---
    model.HOURS = RangeSet(0, 23)  # 24 hours
    model.DAYS = RangeSet(0, 364)   # 365 days
    model.MONTHS = Set(initialize=['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']) # Months of the year
    
    month_day_ranges = {'jan': (0,30), 'feb': (31,58), 'mar': (59,89), 'apr': (90,119), 'may': (120,150), 'jun': (151,180), 'jul': (181,211), 'aug': (212,242), 'sep': (243,272), 'oct': (273,303), 'nov': (304,333), 'dec': (334, 364)}

    # ---Parameters---
    model.solar_param = Param(model.HOURS, model.DAYS, initialize=lambda m, h, d: solar_data[h, d])
    model.wind_param = Param(model.HOURS, model.DAYS, initialize=lambda m, h, d: wind_data[h, d])
    model.self_production = Param(model.HOURS, model.DAYS, initialize=lambda m, h, d: solar_data[h, d] + wind_data[h, d])
    model.load_param = Param(model.HOURS, model.DAYS, initialize=lambda m, h, d: load_data[h, d])
    model.spot_price = Param(model.HOURS, model.DAYS, initialize=lambda m, h, d: spot_price_data[h, d])
    

    model.boat_usage1 = Param(model.HOURS, model.DAYS, initialize=lambda m, h, d: boat_availability1[h, d])
    model.boat_usage2 = Param(model.HOURS, model.DAYS, initialize=lambda m, h, d: boat_availability2[h, d])
    model.boat_usage3 = Param(model.HOURS, model.DAYS, initialize=lambda m, h, d: boat_availability3[h, d])

    model.boat_load1 = Param(model.HOURS, model.DAYS, initialize=lambda m, h, d: (boat_load1[h, d] * boat_capacity * number_boats1))
    model.boat_load2 = Param(model.HOURS, model.DAYS, initialize=lambda m, h, d: (boat_load2[h, d] * boat_capacity * number_boats2))
    model.boat_load3 = Param(model.HOURS, model.DAYS, initialize=lambda m, h, d: (boat_load3[h, d] * boat_capacity * number_boats3))

    model.bids_effekthandelväst = Param(model.HOURS, model.DAYS, initialize=lambda m, h, d: bids_effekthandelväst_data[h, d])
    model.activated_bids_effekthandelväst = Param(model.HOURS, model.DAYS, initialize=lambda m, h, d: activated_bids_effekthandelväst_data[h, d])

    # ---Constants---
    bess_initial_soc = bess_capacity/2
    boat_initial_soc = boat_capacity/2
    bess_availability = np.ones((24, 365))  # Assuming the battery is always available
    zeros = np.zeros((24, 365)) 

    # ---Variables---
    model.self_sufficiency = Var(model.HOURS, model.DAYS, within=NonNegativeReals)
    model.grid_used = Var(model.HOURS, model.DAYS, bounds=(0, grid_limit))
    model.grid_sold = Var(model.HOURS, model.DAYS, within=NonNegativeReals)
    model.peak_month = Var(model.MONTHS, bounds=(0, grid_limit))
    
    model.bess_soc = Var(model.HOURS, model.DAYS, bounds=(0, bess_capacity))
    model.bess_charge = Var(model.HOURS, model.DAYS, bounds=(0, bess_charge_rate))
    model.bess_discharge = Var(model.HOURS, model.DAYS, bounds=(0, bess_discharge_rate))
    
    model.boat_soc1 = Var(model.HOURS, model.DAYS, bounds=(0, boat_capacity*number_boats1))
    model.boat_soc2 = Var(model.HOURS, model.DAYS, bounds=(0, boat_capacity*number_boats2))
    model.boat_soc3 = Var(model.HOURS, model.DAYS, bounds=(0, boat_capacity*number_boats3))

    model.boat_charge1 = Var(model.HOURS, model.DAYS, bounds=(0, boat_charge_rate*number_boats1))
    model.boat_charge2 = Var(model.HOURS, model.DAYS, bounds=(0, boat_charge_rate*number_boats2))
    model.boat_charge3 = Var(model.HOURS, model.DAYS, bounds=(0, boat_charge_rate*number_boats3))
    
    model.boat_discharge1 = Var(model.HOURS, model.DAYS, bounds=(0, boat_discharge_rate*number_boats1))
    model.boat_discharge2 = Var(model.HOURS, model.DAYS, bounds=(0, boat_discharge_rate*number_boats2))
    model.boat_discharge3 = Var(model.HOURS, model.DAYS, bounds=(0, boat_discharge_rate*number_boats3))
    
    # ---Objective---
    # Minimize cost of grid electricity
    def total_grid_cost(model):
        electricity_cost = sum(
            (energy_tax + transmission_fee + model.spot_price[h, d]) * model.grid_used[h, d] #Cost of electricity
            for h in model.HOURS for d in model.DAYS)
        
        peak_total_cost = sum(
            peak_cost * model.peak_month[m] 
            for m in model.MONTHS)

        electricity_revenue = sum(
            model.spot_price[h, d] * model.grid_sold[h, d] #Revenue from selling electricity
            for h in model.HOURS for d in model.DAYS)
        
        # power_revenue = sum()
    
        return (electricity_cost + peak_total_cost - electricity_revenue) #+ cycling_cost
    model.objective = Objective(rule=total_grid_cost, sense=minimize)

    # Returns the maximum grid load for each month, makes the objective function work
    def peak_month_rule(model, h, d):
        for month, (start, end) in month_day_ranges.items():
            if start <= d <= end:
                return model.grid_used[h, d] <= model.peak_month[month]
        return Constraint.Skip 
    model.peak_month_constraint = Constraint(model.HOURS, model.DAYS, rule=peak_month_rule)

    # ---Constraints---
    # Load must be exactly met
    def load_balance_rule(model, h, d):
        return model.self_sufficiency[h, d] + model.bess_discharge[h, d] + model.boat_discharge1[h, d] + model.boat_discharge2[h, d]+ model.boat_discharge3[h, d] + model.grid_used[h, d] == model.load_param[h, d] + model.grid_sold[h, d]
    model.load_balance_constraint = Constraint(model.HOURS, model.DAYS, rule=load_balance_rule)

    # Sold electricity constraint
    def grid_sold_limit(model, h, d):
        return model.grid_sold[h, d] <= grid_limit/2
    model.grid_sold_constraint = Constraint(model.HOURS, model.DAYS, rule=grid_sold_limit)

    # Sold electricity only from batteries
    def grid_sold_from_batteries(model, h, d):
        return model.grid_sold[h, d] <= model.bess_discharge[h, d] + model.boat_discharge1[h, d] + model.boat_discharge2[h, d] + model.boat_discharge3[h, d]
    model.grid_sold_from_batteries_constraint = Constraint(model.HOURS, model.DAYS, rule=grid_sold_from_batteries)

    # Self-sufficiency cannot exceed self-production or demand
    def self_sufficiency_limit(model, h, d):
        return model.self_sufficiency[h, d] + model.bess_charge[h, d] + model.boat_charge1[h, d] + model.boat_charge2[h, d] + model.boat_charge3[h, d] <= model.self_production[h, d]
    model.self_sufficiency_constraint = Constraint(model.HOURS, model.DAYS, rule=self_sufficiency_limit)

    # Battery SOC limits: limits the charging to the available storage in the battery
    def soc_charge_limit(CHR, CAP, SOC):
        def rule(model, h, d):
            return CHR[h, d] <= CAP - SOC[h, d]
        return rule
    model.bess_soc_charge_constraint = Constraint(model.HOURS, model.DAYS, rule=soc_charge_limit(model.bess_charge, bess_capacity, model.bess_soc))
    model.boat1_soc_charge_constraint = Constraint(model.HOURS, model.DAYS, rule=soc_charge_limit(model.boat_charge1, boat_capacity*number_boats1, model.boat_soc1))
    model.boat2_soc_charge_constraint = Constraint(model.HOURS, model.DAYS, rule=soc_charge_limit(model.boat_charge2, boat_capacity*number_boats2, model.boat_soc2))
    model.boat3_soc_charge_constraint = Constraint(model.HOURS, model.DAYS, rule=soc_charge_limit(model.boat_charge3, boat_capacity*number_boats3, model.boat_soc3))

    # Battery SOC limit: limits the discharge to the electricity in the battery
    def soc_discharge_limit(DIS, SOC):
        def rule(model, h, d):
            return DIS[h, d] <= SOC[h, d]
        return rule
    model.bess_soc_discharge_constraint = Constraint(model.HOURS, model.DAYS, rule=soc_discharge_limit(model.bess_discharge, model.bess_soc))
    model.boat1_soc_discharge_constraint = Constraint(model.HOURS, model.DAYS, rule=soc_discharge_limit(model.boat_discharge1, model.boat_soc1))
    model.boat2_soc_discharge_constraint = Constraint(model.HOURS, model.DAYS, rule=soc_discharge_limit(model.boat_discharge2, model.boat_soc2))
    model.boat3_soc_discharge_constraint = Constraint(model.HOURS, model.DAYS, rule=soc_discharge_limit(model.boat_discharge3, model.boat_soc3))

    # Battery SoC dynamics: rule of charging and discharging
    def soc_update(USE, SOC, CHR, DIS, INIT, BLOAD, ACT, BUD):
        def rule(model, h, d):
            if h == 0 and d == 0:
                return SOC[h, d] == INIT
            elif h == 0:
                if USE[h, d] == 0:
                    return SOC[h, d] == SOC[23, d-1] - BLOAD[23, d-1]
                elif USE[h, d] == 1 and USE[23, d-1] == 0:
                    return SOC[h, d] == SOC[23, d-1] - BLOAD[23, d-1]
                # elif ACT[h, d] == 1 and ACT[23, d-1] == 1:
                #     return SOC[h, d] == SOC[23, d-1] - BUD
                # elif ACT[h, d] == 0 and ACT[23, d-1] == 1:
                #     return SOC[h, d] == SOC[23, d-1] - BUD
                else:
                    return SOC[h, d] == SOC[23, d-1] + CHR[23, d-1] - DIS[23, d-1]
            else:
                if USE[h, d] == 0:
                    return SOC[h, d] == SOC[h-1, d] - BLOAD[h-1, d]
                elif USE[h, d] == 1 and USE[h-1, d] == 0:
                    return SOC[h, d] == SOC[h-1, d] - BLOAD[h-1, d]
                elif ACT[h, d] == 1 and ACT[h-1, d] == 1:
                    return SOC[h, d] == SOC[h-1, d] - ACT[h-1, d]*BUD
                # elif ACT[h, d] == 0 and ACT[h-1, d] == 1:
                #     return SOC[h, d] == SOC[h-1, d] - BUD
                else:
                    return SOC[h, d] == SOC[h-1, d] + CHR[h-1, d] - DIS[h-1, d]

            # if USE[h, d] == 0:
            #     if h == 0 and d == 0:
            #         return SOC[h, d] == INIT
            #     elif h == 0:
            #         return SOC[h, d] == SOC[23, d-1] - BLOAD[23, d-1]
            #     else:
            #         return SOC[h, d] == SOC[h-1, d] - BLOAD[h-1, d]
            # elif USE[h, d] == 1 and USE[h-1, d] == 0:
            #     if h == 0 and d == 0:
            #         return SOC[h, d] == INIT
            #     elif h == 0:
            #         return SOC[h, d] == SOC[23, d-1] - BLOAD[23, d-1]
            #     else:
            #         return SOC[h, d] == SOC[h-1, d] - BLOAD[h-1, d]
            # elif ACT[h, d] == 1 and ACT[h-1, d]==1:
            #     if h == 0 and d == 0:
            #         return SOC[h, d] == INIT
            #     elif h == 0:
            #         return SOC[h, d] == SOC[23, d-1] - BUD
            #     else:
            #         return SOC[h, d] == SOC[h-1, d] - BUD
            # elif ACT[h, d] == 0 and ACT[h-1, d]==1:
            #     if h == 0 and d == 0:
            #         return SOC[h, d] == INIT
            #     elif h == 0:
            #         return SOC[h, d] == SOC[23, d-1] - BUD
            #     else:
            #         return SOC[h, d] == SOC[h-1, d] - BUD
            # else:
            #     if h == 0 and d == 0:
            #         return SOC[h, d] == INIT
            #     elif h == 0:
            #         return SOC[h, d] == SOC[23, d-1] + CHR[23, d-1] - DIS[23, d-1]
            #     else:
            #         return SOC[h, d] == SOC[h-1, d] + CHR[h-1, d] - DIS[h-1, d]
        return rule  
    model.bess_soc_dynamics = Constraint(model.HOURS, model.DAYS, rule=soc_update(bess_availability, model.bess_soc, model.bess_charge, model.bess_discharge, bess_initial_soc, zeros, model.activated_bids_effekthandelväst, 0.2*bess_capacity))
    model.boat1_soc_dynamics = Constraint(model.HOURS, model.DAYS, rule=soc_update(boat_availability1, model.boat_soc1, model.boat_charge1, model.boat_discharge1, boat_initial_soc * number_boats1, boat_load1, model.activated_bids_effekthandelväst, 0.2*boat_capacity*number_boats1))
    model.boat2_soc_dynamics = Constraint(model.HOURS, model.DAYS, rule=soc_update(boat_availability2, model.boat_soc2, model.boat_charge2, model.boat_discharge2, boat_initial_soc * number_boats2, boat_load2, model.activated_bids_effekthandelväst, 0.2*boat_capacity*number_boats2))
    model.boat3_soc_dynamics = Constraint(model.HOURS, model.DAYS, rule=soc_update(boat_availability3, model.boat_soc3, model.boat_charge3, model.boat_discharge3, boat_initial_soc * number_boats3, boat_load3, model.activated_bids_effekthandelväst, 0.2*boat_capacity*number_boats3))

    # Boat available to charge
    def boat_charge_availability(CHR, RATE, USE):
        def rule(model, h, d):
            if h == 0 and d == 0:
                return CHR[h, d] <= RATE * USE[h, d]
            elif h == 0:
                if USE[h, d] == 1 and USE[23, d-1] == 0:
                    return CHR[23, d] <= RATE
                else:
                    return CHR[h, d] <= RATE * USE[h, d]
            else:
                if USE[h, d] == 1 and USE[h-1, d] == 0:
                    return CHR[h-1, d] <= RATE
                else:
                    return CHR[h, d] <= RATE * USE[h, d]
        return rule
    model.boat1_charge_availability_constraint = Constraint(model.HOURS, model.DAYS, rule=boat_charge_availability(model.boat_charge1, boat_charge_rate*number_boats1, model.boat_usage1))
    model.boat2_charge_availability_constraint = Constraint(model.HOURS, model.DAYS, rule=boat_charge_availability(model.boat_charge2, boat_charge_rate*number_boats2, model.boat_usage2))
    model.boat3_charge_availability_constraint = Constraint(model.HOURS, model.DAYS, rule=boat_charge_availability(model.boat_charge3, boat_charge_rate*number_boats3, model.boat_usage3))

    # Boat available to discharge
    def boat_discharge_availability(DIS, RATE, USE, SOC):
        def rule(model, h, d):
            if h == 23 and d == 364:
                return DIS[h, d] <= RATE * USE[h, d]
            elif h == 23:
                if USE[h, d] == 1 and USE[0, d+1] == 0:
                    return DIS[h, d] <= SOC[h, d]
                else:
                    return DIS[h, d] <= RATE * USE[h, d]
            else:
                if USE[h, d] == 1 and USE[h+1, d] == 0:
                    return DIS[h, d] <= SOC[h, d]
                else:
                    return DIS[h, d] <= RATE * USE[h, d]
        return rule
    model.boat1_discharge_availability_constraint = Constraint(model.HOURS, model.DAYS, rule=boat_discharge_availability(model.boat_discharge1, boat_discharge_rate*number_boats1, model.boat_usage1, model.boat_soc1))
    model.boat2_discharge_availability_constraint = Constraint(model.HOURS, model.DAYS, rule=boat_discharge_availability(model.boat_discharge2, boat_discharge_rate*number_boats2, model.boat_usage2, model.boat_soc2))
    model.boat3_discharge_availability_constraint = Constraint(model.HOURS, model.DAYS, rule=boat_discharge_availability(model.boat_discharge3, boat_discharge_rate*number_boats3, model.boat_usage3, model.boat_soc3))

    # Boat need to be charged before usage
    def boat_SOC_before_usage(USE, SOC, CAP):
        def rule(model, h, d):
            if h == 0 and d == 0:
                return Constraint.Skip
            elif h == 0:
                if USE[h, d] == 0 and USE[23, d-1] == 1:
                    return SOC[23, d-1] >= CAP
                else:
                    return Constraint.Skip
            else:
                if USE[h, d] == 0 and USE[h-1, d] == 1:
                    return SOC[h-1, d] >= CAP
                else:
                    return Constraint.Skip
        return rule
    model.boat1_SOC_before_usage_constraint = Constraint(model.HOURS, model.DAYS, rule=boat_SOC_before_usage(model.boat_usage1, model.boat_soc1, boat_capacity*number_boats1))
    model.boat2_SOC_before_usage_constraint = Constraint(model.HOURS, model.DAYS, rule=boat_SOC_before_usage(model.boat_usage2, model.boat_soc2, boat_capacity*number_boats2))
    model.boat3_SOC_before_usage_constraint = Constraint(model.HOURS, model.DAYS, rule=boat_SOC_before_usage(model.boat_usage3, model.boat_soc3, boat_capacity*number_boats3))

    # Boat needs to have a charge of zero during usage
    def boat_SOC_during_usage(USE, SOC, CAP):
        def rule(model, h, d):
            if h == 0 and d == 0:
                return Constraint.Skip
            elif h == 0:
                if USE[h, d] == 0 and USE[23, d-1] == 1:
                    return SOC[h, d] <= CAP
                else:
                    return Constraint.Skip
            else:
                if USE[h, d] == 0 and USE[h-1, d] == 1:
                    return SOC[h, d] <= CAP
                else:
                    return Constraint.Skip
        return rule
    model.boat1_SOC_during_usage_constraint = Constraint(model.HOURS, model.DAYS, rule=boat_SOC_during_usage(model.boat_usage1, model.boat_soc1, boat_capacity*number_boats1))
    model.boat2_SOC_during_usage_constraint = Constraint(model.HOURS, model.DAYS, rule=boat_SOC_during_usage(model.boat_usage2, model.boat_soc2, boat_capacity*number_boats2))
    model.boat3_SOC_during_usage_constraint = Constraint(model.HOURS, model.DAYS, rule=boat_SOC_during_usage(model.boat_usage3, model.boat_soc3, boat_capacity*number_boats3))

    # Sell electricity on the electricity market
    # Ladda batterier med el från nätet?

    # Sell electricity on the frequency market

        

    # Sell electricity on Effekthandel Väst
     
    def SOC_before_effekthandelväst(USE, SOC, CAP):
        def rule(model, h, d):
            if h == 23 and d == 364:
                return Constraint.Skip
            elif h == 23:
                if USE[h, d] == 1 and USE[0, d+1]==0:
                    return  SOC[h, d] >= 0.5 * CAP 
                elif USE[h,d] == 0 and USE[0,d+1] == 1:
                    return SOC[h,d] >= 0.5 * CAP
                else:
                    return Constraint.Skip
            else:
                if USE[h, d] == 1 and USE[h+1,d] == 1:
                    return  SOC[h, d] >= 0.5 * CAP 
                elif USE[h, d] == 1 and USE[h+1,d] == 0:
                    return SOC[h,d] >= 0.3 * CAP
                elif USE[h,d] == 0 and USE[h+1,d] == 1:
                    return SOC[h,d] >= 0.5 * CAP
                else:
                    return Constraint.Skip
        return rule
    model.BESS_SOC_before_effetkhandelväst_constraint = Constraint(model.HOURS, model.DAYS, rule=SOC_before_effekthandelväst(model.bids_effekthandelväst, model.bess_soc, bess_capacity))
    model.boat1_SOC_before_effetkhandelväst_constraint = Constraint(model.HOURS, model.DAYS, rule=SOC_before_effekthandelväst(model.bids_effekthandelväst, model.boat_soc1, boat_capacity*number_boats1))
    model.boat2_before_effetkhandelväst_constraint = Constraint(model.HOURS, model.DAYS, rule=SOC_before_effekthandelväst(model.bids_effekthandelväst, model.boat_soc2, boat_capacity*number_boats2))
    model.boat3_before_effetkhandelväst_constraint = Constraint(model.HOURS, model.DAYS, rule=SOC_before_effekthandelväst(model.bids_effekthandelväst, model.boat_soc3, boat_capacity*number_boats3))


    # Solve
    if user == 1:
        solver = SolverFactory('glpk', executable='C:\\Users\\a518244\\Python\\energy-optimization\\winglpk-4.65\\glpk-4.65\\w64\\glpsol.exe')
    elif user == 2:
        solver = SolverFactory('glpk', executable='C:\\Users\\a517469\\Python\\energy-optimization\\glpk-4.65\\w64\\glpsol.exe')
    results = solver.solve(model, tee=True)

    if (results.solver.status != SolverStatus.ok) or (results.solver.termination_condition != TerminationCondition.optimal):
        print("Solver failed!")
        print("Status:", results.solver.status)
        print("Termination:", results.solver.termination_condition)
    else:
        print("Solver succeeded!")

    return model
