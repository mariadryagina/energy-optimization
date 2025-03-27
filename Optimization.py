# Requires pip install pyomo
import numpy as np
import pandas as pd
from pyomo.environ import *
from pyomo.opt import SolverStatus, TerminationCondition
import load_björkö_bessekroken
import load_krossholmen_2023
#import load_björkö
import el_cost
import solarpower
import windpower
import el_price
import usage_pattern
import matplotlib as plt


# Load data 
# solar_data = solarpower.solar(100,0.20)                                             # 24x365
# wind_data = windpower.wind(1)                                                       # 24x365
# self_production = solar_data + wind_data                                            # 24x365
# load_data = load_björkö_bessekroken.load                                              # 24x365
# grid_cost_data =  el_cost.cost(None, None, load_data, 61.55, 0.439, 0.113, 1.25)    # 24x365
# spot_price_data = el_price.spotprice_2023                                           # 24x365
# boat_usage = usage_pattern.usage_pattern(163)

# Define the optimization model
def optimize_microgrid(solar_data, wind_data, load_data, spot_price_data, number_boats, boat_availability):
    model = ConcreteModel()

    # Define sets
    model.HOURS = RangeSet(0, 23)  # 24 hours
    model.DAYS = RangeSet(0, 364)   # 365 days
    
    # Parameters
    model.solar_param = Param(model.HOURS, model.DAYS, initialize=lambda m, h, d: solar_data[h, d])
    model.wind_param = Param(model.HOURS, model.DAYS, initialize=lambda m, h, d: wind_data[h, d])
    model.self_production = Param(model.HOURS, model.DAYS, initialize=lambda m, h, d: solar_data[h, d] + wind_data[h, d])
    model.load_param = Param(model.HOURS, model.DAYS, initialize=lambda m, h, d: load_data[h, d])
    #model.grid_cost = Param(model.HOURS, model.DAYS, initialize=lambda m, h, d: grid_cost_data[h, d])
    model.spot_price = Param(model.HOURS, model.DAYS, initialize=lambda m, h, d: spot_price_data[h, d])
    model.boat_usage = Param(model.HOURS, model.DAYS, initialize=lambda m, h, d: boat_availability[h, d])

    # Constants
    bess_capacity = 500
    bess_charge_rate = 350
    bess_discharge_rate = 350
    bess_initial_soc = bess_capacity/2
    boat_capacity = 100
    boat_charge_rate = 60
    boat_discharge_rate = 60
    boat_initial_soc = boat_capacity/2
    number_boats = number_boats

    # Variables
    model.self_sufficiency = Var(model.HOURS, model.DAYS, within=NonNegativeReals)
    model.grid_used = Var(model.HOURS, model.DAYS, within=NonNegativeReals)
    model.peak_grid_load = Var(within=NonNegativeReals)
    model.bess_charge = Var(model.HOURS, model.DAYS, within=NonNegativeReals)
    model.bess_discharge = Var(model.HOURS, model.DAYS, within=NonNegativeReals)
    model.bess_soc = Var(model.HOURS, model.DAYS, within=NonNegativeReals)
    model.boat_charge = Var(model.HOURS, model.DAYS, within=NonNegativeReals)
    model.boat_discharge = Var(model.HOURS, model.DAYS, within=NonNegativeReals)
    model.boat_soc = Var(model.HOURS, model.DAYS, within=NonNegativeReals)

    # Objective: Minimize cost of grid electricity
    def total_grid_cost(model):
        total_cost = sum((2*model.spot_price[h, d] * model.grid_used[h, d]) for h in model.HOURS for d in model.DAYS)
        peak_cost = 61.55
        return (total_cost + peak_cost * model.peak_grid_load)
    model.objective = Objective(rule=total_grid_cost, sense=minimize)

    # Constraints

    # Load must be exactly met
    def load_balance_rule(model, h, d):
        return model.self_sufficiency[h, d] + model.bess_discharge[h, d] + model.boat_discharge[h, d] + model.grid_used[h, d] == model.load_param[h, d]
    model.load_balance_constraint = Constraint(model.HOURS, model.DAYS, rule=load_balance_rule)

    def peak_grid_constraint(model, h, d):
        return model.grid_used[h, d] <= model.peak_grid_load
    model.peak_limit_constraint = Constraint(model.HOURS, model.DAYS, rule=peak_grid_constraint)

    # Self-sufficiency cannot exceed self-production or demand
    def self_sufficiency_limit(model, h, d):
        return model.self_sufficiency[h, d] + model.bess_charge[h, d] + model.boat_charge[h, d] <= model.self_production[h, d]
    model.self_sufficiency_constraint = Constraint(model.HOURS, model.DAYS, rule=self_sufficiency_limit)

    # Battery charging limits: limits the chargers rate of charging
    def bess_charge_rate_limit(model, h, d):
        return model.bess_charge[h, d] <= bess_charge_rate
    model.bess_charge_rate_constraint = Constraint(model.HOURS, model.DAYS, rule=bess_charge_rate_limit)

    def boat_charge_rate_limit(model, h, d):
        return model.boat_charge[h, d] <= (boat_charge_rate * number_boats)
    model.boat_charge_rate_constraint = Constraint(model.HOURS, model.DAYS, rule=boat_charge_rate_limit)

    # Battery SOC limits: limits the charging to the available storage in the battery
    def bess_soc_charge_limit(model, h, d):
        return model.bess_charge[h, d] <= bess_capacity - model.bess_soc[h, d]
    model.bess_soc_charge_constraint = Constraint(model.HOURS, model.DAYS, rule=bess_soc_charge_limit)

    def boat_soc_charge_limit(model, h, d):
        return model.boat_charge[h, d] <= (boat_capacity * number_boats) - model.boat_soc[h, d]
    model.boat_soc_charge_constraint = Constraint(model.HOURS, model.DAYS, rule=boat_soc_charge_limit)

    # Battery discharging limits: limits the chargers rate of discharge
    def bess_discharge_rate_limit(model, h, d):
        return model.bess_discharge[h, d] <= bess_discharge_rate
    model.bess_discharge_rate_constraint = Constraint(model.HOURS, model.DAYS, rule=bess_discharge_rate_limit)

    def boat_discharge_rate_limit(model, h, d):
        return model.boat_discharge[h, d] <= (boat_discharge_rate * number_boats)
    model.boat_discharge_rate_constraint = Constraint(model.HOURS, model.DAYS, rule=boat_discharge_rate_limit)

    # Battery SOC limit: limits the discharge to the electricity in the battery
    def bess_soc_discharge_limit(model, h, d):
        return model.bess_discharge[h, d] <= model.bess_soc[h, d]
    model.bess_soc_discharge_constraint = Constraint(model.HOURS, model.DAYS, rule=bess_soc_discharge_limit)

    def boat_soc_discharge_limit(model, h, d):
        return model.boat_discharge[h, d] <= model.boat_soc[h, d]
    model.bess_soc_discharge_constraint = Constraint(model.HOURS, model.DAYS, rule=boat_soc_discharge_limit)

    # Battery SoC dynamics: rule of charging and discharging
    def bess_soc_update(model, h, d):
        if h == 0 and d == 0:
            return model.bess_soc[h, d] == bess_initial_soc
        elif h == 0:
            return model.bess_soc[h, d] == model.bess_soc[23, d - 1] + model.bess_charge[23, d - 1] - model.bess_discharge[23, d - 1]
        else:
            return model.bess_soc[h, d] == model.bess_soc[h - 1, d] + model.bess_charge[h - 1, d] - model.bess_discharge[h - 1, d]
    model.bess_soc_dynamics = Constraint(model.HOURS, model.DAYS, rule=bess_soc_update)

    def boat_soc_update(model, h, d):
        if h == 0 and d == 0:
            return model.boat_soc[h, d] == boat_initial_soc * number_boats
        elif h == 0:
            return model.boat_soc[h, d] == model.boat_soc[23, d - 1] + model.boat_charge[23, d - 1] - model.boat_discharge[23, d - 1]
        else:
            return model.boat_soc[h, d] == model.boat_soc[h - 1, d] + model.boat_charge[h - 1, d] - model.boat_discharge[h - 1, d]
    model.boat_soc_dynamics = Constraint(model.HOURS, model.DAYS, rule=boat_soc_update)

    def boat_availiable_to_charge(model, h, d):
        return model.boat_charge[h, d] <= model.boat_usage[h, d] * boat_charge_rate * number_boats
    model.boat_availiable_to_charge_constraint = Constraint(model.HOURS, model.DAYS, rule=boat_availiable_to_charge)

    def boat_available_to_discharge(model, h, d):
        return model.boat_discharge[h, d] <= model.boat_usage[h, d] * boat_discharge_rate * number_boats
    model.boat_available_to_discharge_constraint = Constraint(model.HOURS, model.DAYS, rule=boat_available_to_discharge)

    def boat_charging_before_usage(model, h, d):
        if boat_availability[h-1, d] == 1 and boat_availability[h, d] == 0:
            return model.boat_soc[h, d] == boat_capacity
        else:
            return Constraint.Skip
    model.boat_charging_before_usage_constraint = Constraint(model.HOURS, model.DAYS, rule=boat_charging_before_usage)

    # Solve
    solver = SolverFactory('glpk', executable='C:\\Users\\a518244\\Python\\energy-optimization\\winglpk-4.65\\glpk-4.65\\w64\\glpsol.exe')
    results = solver.solve(model, tee=True)

    if (results.solver.status != SolverStatus.ok) or (results.solver.termination_condition != TerminationCondition.optimal):
        print("Solver failed!")
        print("Status:", results.solver.status)
        print("Termination:", results.solver.termination_condition)
    else:
        print("Solver succeeded!")

    return model


    # # Define parameters
    # model.solar_param = Param(model.HOURS, model.DAYS, initialize=lambda model, h, d: solar_data[h, d])
    # model.wind_param = Param(model.HOURS, model.DAYS, initialize=lambda model, h, d: wind_data[h, d])
    # model.self_production = Param(model.HOURS, model.DAYS, initialize=lambda model, h, d: self_production[h, d])
    # model.load_param = Param(model.HOURS, model.DAYS, initialize=lambda model, h, d: load_data[h, d])
    # model.grid_cost = Param(model.HOURS, model.DAYS, initialize=lambda model, h, d: grid_cost_data[h, d])
    # model.spot_price = Param(model.HOURS, model.DAYS, initialize=lambda model, h, d: spot_price_data[h, d])

    # # Define limits and costs
    # bess_capacity = 00  # Maximum capacity of BESS in kWh
    # #grid_delivery_limit = 1680  # Maximum electricity the grid can deliver in kW
    # #sell_limit = 800  # Maximum electricity that can be sold to the grid in kW
    # bess_charge_rate = 0  # Maximum charging rate of BESS in kW
    # bess_discharge_rate = 0  # Maximum discharging rate of BESS in kW
    # bess_initial_soc = 0
    # bess_cost = 0.8  # Cost of using electricity from BESS in SEK/kWh
    # zero_level = 0  # Zero level for the SoC of the BESS

    # # Define variables
    # model.self_sufficiency = Var(model.HOURS, model.DAYS, within=NonNegativeReals)
    # model.grid_used = Var(model.HOURS, model.DAYS, within=NonNegativeReals)
    # model.bess_charge = Var(model.HOURS, model.DAYS, within=NonNegativeReals)
    # model.bess_discharge = Var(model.HOURS, model.DAYS, within=NonNegativeReals)
    # model.bess_soc = Var(model.HOURS, model.DAYS, within=NonNegativeReals)

    # # Objective: Maximize revenue from selling electricity to the grid
    # def revenue_rule(model):
    #     return sum(model.spot_price[h, d] * (model.grid_used[h, d]) for h in model.HOURS for d in model.DAYS)
    # model.revenue = Objective(rule=revenue_rule, sense=minimize)

    # # Constraints

    # # 1. Load balance

    # # def load_balance_rule(model, h, d):
    # #     return model.load_param[h, d] <= model.self_production[h, d] + model.bess_discharge[h, d] + model.grid_used[h, d]
    # # model.load_balance_constraint = Constraint(model.HOURS, model.DAYS, rule=load_balance_rule)
    
    # def load_rule(model, h, d):
    #     return model.self_sufficiency[h, d] + model.bess_discharge[h, d] + model.grid_used[h, d] == model.load_param[h, d]
    # model.load_constraint = Constraint(model.HOURS, model.DAYS, rule=load_rule)

    # def self_sufficiency(model, h, d):
    #     return model.self_sufficiency[h, d] <= model.self_production[h, d]
    # model.self_sufficiency_constraint = Constraint(model.HOURS, model.DAYS, rule=self_sufficiency)

    # def self_sufficiency_limit(model, h, d):
    #     return model.self_sufficiency[h, d] <= model.load_param[h, d]
    # model.self_sufficiency_limit_constraint = Constraint(model.HOURS, model.DAYS, rule=self_sufficiency_limit)

    # def self_sufficiency_flow(model, h, d):
    #     return model.self_production[h, d] == model.self_sufficiency[h, d] + model.bess_charge[h, d]
    # model.self_sufficiency_flow_constraint = Constraint(model.HOURS, model.DAYS, rule=self_sufficiency_flow)

    #     # BESS inital SoC: sets the SoC for the first hour of the first day to 250 kWh
    # def bess_initial_soc_rule(model):
    #     return model.bess_soc[0, 0] == bess_initial_soc  # Use the initial SoC value directly
    # model.bess_initial_soc_constraint = Constraint(rule=bess_initial_soc_rule)

    # def grid_used_rule(model, h, d):
    #     #return model.grid_used[h, d] == model.load_param[h, d] - (model.self_production[h, d] + model.bess_discharge[h, d])
    #     return model.grid_used[h, d] >= model.load_param[h, d] - (model.self_production[h, d] + model.bess_discharge[h, d])
    # model.grid_used_constraint = Constraint(model.HOURS, model.DAYS, rule=grid_used_rule)     

    # # BESS charging rule: sets the parameters for when the BESS may charge
    # def bess_charge_rule(model, h, d):
    #     # if model.self_production[h, d] >= model.load_param[h, d]:
    #     #     return model.bess_charge[h, d] == model.self_production[h, d] - model.load_param[h, d]
    #     # else:
    #     #     return model.bess_charge[h, d] == 0
    #     return model.bess_charge[h, d] <= bess_charge_rate
    # model.bess_charge_constraint = Constraint(model.HOURS, model.DAYS, rule=bess_charge_rule)

    # def bess_charge_energy_rule(model, h, d):
    #     return model.bess_charge[h, d] <= model.self_production[h, d] - model.self_sufficiency[h, d]
    # model.bess_charge_energy_constraint = Constraint(model.HOURS, model.DAYS, rule=bess_charge_energy_rule)

    # # BESS discharging rule: sets the parameters for when the BESS may discharge
    # def bess_discharge_load_rule(model, h, d):
    #     # if model.load_param[h, d] <= model.self_production[h, d]:
    #     #     return model.bess_discharge[h, d] == 0
    #     # else:
    #     #     return model.bess_discharge[h, d] == model.bess_discharge[h, d]
    #     return model.bess_discharge[h, d] <= model.load_param[h, d] - model.self_production[h, d]
    # model.bess_discharge_load_constraint = Constraint(model.HOURS, model.DAYS, rule=bess_discharge_load_rule)

    # def bess_discharge_rate_rule(model, h, d):
    #     return model.bess_discharge[h, d] <= bess_discharge_rate
    # model.bess_discharge_rate_constraint = Constraint(model.HOURS, model.DAYS, rule=bess_discharge_rate_rule)

    # # def bess_discharge_price_rule(model, h, d):
    # #     if model.spot_price[h, d] < bess_cost:
    # #         return model.bess_discharge[h, d] == zero_level
    # #     else:
    # #         return Constraint.Skip
    # # model.bess_discharge_price_constraint = Constraint(model.HOURS, model.DAYS, rule=bess_discharge_price_rule)

    # # Battery SoC: sets rhe rule for how the SoC updates
    # # Set by the SoC the hour before + the charge or - the discharge
    # def bess_soc_update_rule(model, h, d):
    #     if h == 0 and d == 0:
    #         # First hour of the first day
    #         return model.bess_soc[h, d] == bess_initial_soc
    #     elif h == 0:
    #         # First hour of any day (not the first day)
    #         return model.bess_soc[h, d] == model.bess_soc[23, d-1] + model.bess_charge[23, d-1] - model.bess_discharge[23, d-1]
    #     else:
    #         # For all other hours
    #         return model.bess_soc[h, d] == model.bess_soc[h-1, d] + model.bess_charge[h-1, d] - model.bess_discharge[h-1, d]
    # model.bess_soc_update_constraint = Constraint(model.HOURS, model.DAYS, rule=bess_soc_update_rule)

    # # BESS charging limits, limits the BESS charging
    # def bess_charge_limit_rule(model, h, d):
    #     if h == 0 and d == 0:
    #         return model.bess_charge[0, 0] <= bess_capacity - bess_initial_soc
    #     # elif h == 0:
    #     #     return model.bess_charge[h, d] <= bess_capacity - model.bess_soc[23, d-1]
    #     else:
    #         return model.bess_charge[h, d] <= bess_capacity - model.bess_soc[h, d]
    # model.bess_charge_limit_constraint = Constraint(model.HOURS, model.DAYS, rule=bess_charge_limit_rule)

    # # BESS discharging limits
    # def bess_discharge_limit_rule(model, h, d):
    #     if (model.self_production[h, d] < model.load_param[h, d]):
    #         if h == 0 and d == 0:
    #             return model.bess_discharge[0, 0] <= bess_initial_soc
    #         # elif h == 0:
    #         #     return model.bess_discharge[h, d] <= model.bess_soc[23, d-1]
    #         else:
    #             return model.bess_discharge[h, d] <= model.bess_soc[h, d] 
    #     else:
    #         return model.bess_discharge[h, d] == zero_level
    # model.bess_discharge_limit_constraint = Constraint(model.HOURS, model.DAYS, rule=bess_discharge_limit_rule)

    # # BESS discharge limit
    # def bess_discharge_rate_rule(model, h, d):
    #     return model.bess_discharge[h, d] <= bess_discharge_rate
    # model.bess_discharge_rate_constraint = Constraint(model.HOURS, model.DAYS, rule=bess_discharge_rate_rule)

    # # BESS charge limit
    # def bess_charge_rate_rule(model, h, d):
    #     return model.bess_charge[h, d] <= bess_charge_rate
    # model.bess_charge_rate_constraint = Constraint(model.HOURS, model.DAYS, rule=bess_charge_rate_rule)


    # # Solve the model using GLPK with validation skipped
    # solver = SolverFactory('glpk', executable='C:\\Users\\a518244\\Python\\energy-optimization\\winglpk-4.65\\glpk-4.65\\w64\\glpsol.exe', validate=False)
    # #solver.solve(model) 
    # results = solver.solve(model, tee=True)
    # if (results.solver.status != SolverStatus.ok) or (results.solver.termination_condition != TerminationCondition.optimal):
    #     print("Solver failed!")
    #     print("Status:", results.solver.status)
    #     print("Termination:", results.solver.termination_condition)
    # else:
    #     print("Solver succeeded!")
    # return model