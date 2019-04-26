# -*- coding: utf-8 -*-
"""
Created on Tue Mar 12 20:19:59 2019

@author: caioc
"""
start_salary = float(input("Enter your starting annual salary: "))
semi_annual_raise = 0.07
total_cost = 1000000
portion_down_payment = 0.25*total_cost
current_savings = 0
r = 0.04
epsilon = 100
n_months = 36

n_guess = 0
low = 0
high = 10000
new_portion_saved = (high+low)//2
while abs(portion_down_payment-current_savings) > epsilon:
	k_months = 0;
	annual_salary = start_salary
	current_savings = 0
	best_portion_saved = new_portion_saved
	while k_months < n_months:
		current_savings += (current_savings*r/12)+(best_portion_saved*annual_salary/12/10000)	
		k_months += 1
		if k_months%6 == 0:
			annual_salary += annual_salary*semi_annual_raise
	if current_savings < portion_down_payment:
		low = best_portion_saved
	else:
		high = best_portion_saved
	new_portion_saved = (high+low)//2
	n_guess += 1
	if new_portion_saved == best_portion_saved:
		break
if abs(portion_down_payment-current_savings) < epsilon:
	print("Best savings rate:",best_portion_saved/10000)
	print("Steps in bisection search:",n_guess)
else:
	print("It is not possible to pay the down payment in three years.")