# Requires pip install pyomo
import numpy as np
import pandas as pd
from pyomo.environ import *
from pyomo.opt import SolverStatus, TerminationCondition
import matplotlib as plt

# Define the optimization model
def optimize_microgrid(solar_data, wind_data, load_data, spot_price_data, grid_limit, bess_capacity, bess_charge_rate, bess_discharge_rate, bess_cycling_cost, boat_capacity, boat_charge_rate, boat_discharge_rate, boat_cycling_cost, number_boats1, number_boats2, number_boats3, boat_availability1, boat_availability2, boat_availability3, charge_required1, charge_required2, charge_required3, user, energy_tax, transmission_fee, peak_cost):
    model = ConcreteModel()

    # ---Define sets---
    model.HOURS = RangeSet(0, 23)  # 24 hours
    model.DAYS = RangeSet(0, 364)   # 365 days
    
    # ---Parameters---
    model.solar_param = Param(model.HOURS, model.DAYS, initialize=lambda m, h, d: solar_data[h, d])
    model.wind_param = Param(model.HOURS, model.DAYS, initialize=lambda m, h, d: wind_data[h, d])
    model.self_production = Param(model.HOURS, model.DAYS, initialize=lambda m, h, d: solar_data[h, d] + wind_data[h, d])
    model.load_param = Param(model.HOURS, model.DAYS, initialize=lambda m, h, d: load_data[h, d])
    model.spot_price = Param(model.HOURS, model.DAYS, initialize=lambda m, h, d: spot_price_data[h, d])
    

    model.boat_usage1 = Param(model.HOURS, model.DAYS, initialize=lambda m, h, d: boat_availability1[h, d])
    model.boat_usage2 = Param(model.HOURS, model.DAYS, initialize=lambda m, h, d: boat_availability2[h, d])
    model.boat_usage3 = Param(model.HOURS, model.DAYS, initialize=lambda m, h, d: boat_availability3[h, d])

    model.charge_required1 = Param(model.HOURS, model.DAYS, initialize=lambda m, h, d: charge_required1[h, d])
    model.charge_required2 = Param(model.HOURS, model.DAYS, initialize=lambda m, h, d: charge_required2[h, d])
    model.charge_required3 = Param(model.HOURS, model.DAYS, initialize=lambda m, h, d: charge_required3[h, d])

    # ---Constants---
    bess_initial_soc = bess_capacity/2
    boat_initial_soc = boat_capacity/2

    # ---Variables---
    model.self_sufficiency = Var(model.HOURS, model.DAYS, within=NonNegativeReals)
    model.grid_used = Var(model.HOURS, model.DAYS, bounds=(0, grid_limit))
    model.peak_grid_load = Var(bounds=(0, grid_limit))
    model.grid_sold = Var(model.HOURS, model.DAYS, within=NonNegativeReals)

    
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
        total_cost = sum(
            (energy_tax + transmission_fee + model.spot_price[h, d]) * model.grid_used[h, d] #Cost of electricity
            + peak_cost * model.peak_grid_load #Cost of power
            - model.spot_price[h, d] * model.grid_sold[h, d] #Revenue for selling electricity
            for h in model.HOURS for d in model.DAYS)
        # cycling_cost = sum(
        #     bess_cycling_cost * model.bess_charge[h, d] + 
        #     boat_cycling_cost * (model.boat_charge1[h, d] + model.boat_charge2[h, d] + model.boat_charge3[h, d])
        #     for h in model.HOURS for d in model.DAYS)
        return (total_cost)
    model.objective = Objective(rule=total_grid_cost, sense=minimize)

    # ---Constraints---
    # Load must be exactly met
    def load_balance_rule(model, h, d):
        return model.self_sufficiency[h, d] + model.bess_discharge[h, d] + model.boat_discharge1[h, d] + model.boat_discharge2[h, d]+ model.boat_discharge3[h, d] + model.grid_used[h, d] == model.load_param[h, d] + model.grid_sold[h, d]
    model.load_balance_constraint = Constraint(model.HOURS, model.DAYS, rule=load_balance_rule)

    # Grid peak can not be higher than the 
    def peak_grid_constraint(model, h, d):
        return model.grid_used[h, d] <= model.peak_grid_load
    model.peak_limit_constraint = Constraint(model.HOURS, model.DAYS, rule=peak_grid_constraint)

    # Sold electricity constraint
    def grid_sold_limit(model, h, d):
        return model.grid_sold[h, d] <= grid_limit/2
    model.grid_sold_constraint = Constraint(model.HOURS, model.DAYS, rule=grid_sold_limit)

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
    def soc_update(SOC, CHR, DIS, INIT):
        def rule(model, h, d):
            if h == 0 and d == 0:
                return SOC[h, d] == INIT
            elif h == 0:
                return SOC[h, d] == SOC[23, d-1] + CHR[23, d-1] - DIS[23, d-1]
            else:
                return SOC[h, d] == SOC[h-1, d] + CHR[h-1, d] - DIS[h-1, d]
        return rule  
    model.bess_soc_dynamics = Constraint(model.HOURS, model.DAYS, rule=soc_update(model.bess_soc, model.bess_charge, model.bess_discharge, bess_initial_soc))
    model.boat1_soc_dynamics = Constraint(model.HOURS, model.DAYS, rule=soc_update(model.boat_soc1, model.boat_charge1, model.boat_discharge1, boat_initial_soc * number_boats1))
    model.boat2_soc_dynamics = Constraint(model.HOURS, model.DAYS, rule=soc_update(model.boat_soc2, model.boat_charge2, model.boat_discharge2, boat_initial_soc * number_boats2))
    model.boat3_soc_dynamics = Constraint(model.HOURS, model.DAYS, rule=soc_update(model.boat_soc3, model.boat_charge3, model.boat_discharge3, boat_initial_soc * number_boats3))

    # Boat available to charge
    def boat_charge_availability(CHR, RATE, USE):
        def rule(model, h, d):
            return CHR[h, d] <= RATE * USE[h, d]
        return rule
    model.boat1_charge_availability_constraint = Constraint(model.HOURS, model.DAYS, rule=boat_charge_availability(model.boat_charge1, boat_charge_rate*number_boats1, model.boat_usage1))
    model.boat2_charge_availability_constraint = Constraint(model.HOURS, model.DAYS, rule=boat_charge_availability(model.boat_charge2, boat_charge_rate*number_boats2, model.boat_usage2))
    model.boat3_charge_availability_constraint = Constraint(model.HOURS, model.DAYS, rule=boat_charge_availability(model.boat_charge3, boat_charge_rate*number_boats3, model.boat_usage3))

    # Boat available to discharge
    def boat_discharge_availability(DIS, RATE, USE):
        def rule(model, h, d):
            if h == 0 and d == 0:
                return DIS[h, d] <= RATE * USE[h, d]
            elif h == 0:
                if USE[h, d] == 1 and USE[23, d-1] == 0:
                    return DIS[23, d] <= RATE
                else:
                    return DIS[h, d] <= RATE * USE[h, d]
            else:
                if USE[h, d] == 1 and USE[h-1, d] == 0:
                    return DIS[h-1, d] <= RATE
                else:
                    return DIS[h, d] <= RATE *USE[h, d]
        return rule
    model.boat1_discharge_availability_constraint = Constraint(model.HOURS, model.DAYS, rule=boat_discharge_availability(model.boat_discharge1, boat_discharge_rate*number_boats1, model.boat_usage1))
    model.boat2_discharge_availability_constraint = Constraint(model.HOURS, model.DAYS, rule=boat_discharge_availability(model.boat_discharge2, boat_discharge_rate*number_boats2, model.boat_usage2))
    model.boat3_discharge_availability_constraint = Constraint(model.HOURS, model.DAYS, rule=boat_discharge_availability(model.boat_discharge3, boat_discharge_rate*number_boats3, model.boat_usage3))

    # Boat need to be charged before usage
    def boat_charging_before_usage(USE, SOC, CAP):
        def rule(model, h, d):
            if h == 0 and d == 0:
                return Constraint.Skip
            elif h == 0:
                if USE[h, d] == 1 and USE[23, d-1] == 0:
                    return SOC[23, d-1] >= CAP
                else:
                    return Constraint.Skip
            else:
                if USE[h, d] == 1 and USE[h-1, d] == 0:
                    return SOC[h-1, d] >= CAP
                else:
                    return Constraint.Skip
        return rule
    model.boat1_charging_before_usage_constraint = Constraint(model.HOURS, model.DAYS, rule=boat_charging_before_usage(model.boat_usage1, model.boat_soc1, boat_capacity*number_boats1))
    model.boat2_charging_before_usage_constraint = Constraint(model.HOURS, model.DAYS, rule=boat_charging_before_usage(model.boat_usage2, model.boat_soc2, boat_capacity*number_boats2))
    model.boat3_charging_before_usage_constraint = Constraint(model.HOURS, model.DAYS, rule=boat_charging_before_usage(model.boat_usage3, model.boat_soc3, boat_capacity*number_boats3))

    # Boat need to be charged before usage
    # def boat_discharge_after_usage(USE, SOC, CAP):
    #     def rule(model, h, d):
    #         if h == 0 and d == 0:
    #             return Constraint.Skip
    #         elif h == 0:
    #             if USE[h, d] == 1 and USE[23, d-1] == 0:
    #                 return SOC[h, d] <= CAP*0.41
    #             else:
    #                 return Constraint.Skip
    #         else:
    #             if USE[h, d] == 1 and USE[h-1, d] == 0:
    #                 return SOC[h, d] <= CAP*0.41
    #             else:
    #                 return Constraint.Skip
    #     return rule
    # model.boat1_discharge_after_usage_constraint = Constraint(model.HOURS, model.DAYS, rule=boat_discharge_after_usage(model.boat_usage1, model.boat_soc1, boat_capacity*number_boats1))
    # model.boat2_discharge_after_usage_constraint = Constraint(model.HOURS, model.DAYS, rule=boat_discharge_after_usage(model.boat_usage2, model.boat_soc2, boat_capacity*number_boats2))
    # model.boat3_discharge_after_usage_constraint = Constraint(model.HOURS, model.DAYS, rule=boat_discharge_after_usage(model.boat_usage3, model.boat_soc3, boat_capacity*number_boats3))


    # def boat_charging_before_usage(REQ, SOC, CAP):
    #     def rule(model, h, d):
    #         if REQ[h, d] == None:
    #             return Constraint.Skip
    #         elif REQ[h, d] == 1.0:
    #             return SOC[h, d] >= CAP
    #         elif REQ[h, d] == 0.2:
    #             return SOC[h, d] <= 0.2*CAP
    #         else:
    #             return Constraint.Skip
    #     return rule
    # model.boat1_charging_before_usage_constraint = Constraint(model.HOURS, model.DAYS, rule=boat_charging_before_usage(model.charge_required1, model.boat_soc1, boat_capacity*number_boats1))
    # model.boat2_charging_before_usage_constraint = Constraint(model.HOURS, model.DAYS, rule=boat_charging_before_usage(model.charge_required2, model.boat_soc2, boat_capacity*number_boats2))
    # model.boat3_charging_before_usage_constraint = Constraint(model.HOURS, model.DAYS, rule=boat_charging_before_usage(model.charge_required3, model.boat_soc3, boat_capacity*number_boats3))


    # Sell electricity on the electricity market
    # Ladda batterier med el från nätet?

    # Sell electricity on the frequency market

        

    # Sell electricity on Effekthandel Väst

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
