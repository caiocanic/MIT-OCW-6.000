# -*- coding: utf-8 -*-
"""
Created on Sat Mar  9 00:32:21 2019

@author: caioc
"""

annual_salary = float(input("Enter your annual salary: "))
portion_saved = float(input("Enter the percent of your salary to save, as a decimal: "))
total_cost = float(input("Enter the cost of your dream home: "))
portion_down_payment = 0.25*total_cost
current_savings = 0
r = 0.04

n_months=0
while current_savings<portion_down_payment:
	current_savings+= (current_savings*r/12)+(portion_saved*annual_salary/12)
	n_months+=1
print(n_months)