# -*- coding: utf-8 -*-
"""
Created on Sat Mar  9 00:46:28 2019

@author: caioc
"""

annual_salary = float(input("Enter your starting annual salary: "))
portion_saved = float(input("Enter the percent of your salary to save, as a decimal: "))
total_cost = float(input("Enter the cost of your dream home: "))
semi_annual_raise = float(input("Enter the semi­-annual raise, as a decimal: "))
portion_down_payment = 0.25*total_cost
current_savings = 0
r = 0.04

n_months = 0
while current_savings < portion_down_payment:
	current_savings += (current_savings*r/12)+(portion_saved*annual_salary/12)
	n_months += 1
	if n_months%6 == 0:
		annual_salary += annual_salary*semi_annual_raise
	#print(portion_down_payment)
	print(current_savings)
print(n_months)