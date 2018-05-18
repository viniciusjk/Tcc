# -*- coding: utf-8 -*-
"""
Created on Thu Mar 29 23:09:54 2018

@author: ViniciusJokubauskas
"""


import numpy as np
import pymprog as pp
from variables import *

rNumberClients = range(numberClients)
rNumberChannels = range(numberChannels)
rNumberProducts = range(numberProducts)

t = pp.iprod(rNumberClients,rNumberChannels,rNumberProducts)
pp.begin('basic') # begin modelling
pp.verbose(True)  # be verbose

x = pp.var('choice', 
        t, bool) #create 3 variables
        
pp.maximize(sum(x[i,j,k]*expectedReturn[i][j][k] for i in rNumberClients\
             for j in rNumberChannels for k in rNumberProducts))

  
#channelLimitConstraint:
for j in rNumberChannels:
    sum(x[i,j,k] for i in rNumberClients for k in rNumberProducts)\
    <=channelCap[j]
    
#maxOfferProductConstraint:    
for k in rNumberProducts:
    sum(x[i,j,k] for i in rNumberClients for j in rNumberChannels)\
    <=maxOfferProduct[k]

#minOfferProductConstraint:  

#for k in rNumberProducts:
#    sum(x[i,j,k] for i in rNumberClients for j in rNumberChannels)\
#    >=minOfferProduct[k]
    
#budgetConstraint:

pp.st(sum(x[i,j,k]*cost[j] for i in rNumberClients for j in rNumberChannels\
    for k in rNumberProducts)<=budget, "Budget Constr")
    
#clientLimitConstraint:

for i in rNumberClients:
   pp.st( sum(x[i,j,k] for j in rNumberChannels for k in rNumberProducts)<=1,
         "client "+str(i)+" Limit")

#rurdleRateConstraint:

pp.st(sum(x[i,j,k]*expectedReturn[i][j][k] for i in rNumberClients for j in\
    rNumberChannels for k in rNumberProducts)>= (1+rurdleRate)*sum(x[i,j,k]\
    *cost[j] for i in rNumberClients for j in rNumberChannels\
    for k in rNumberProducts),"rurdleRate Cons")
    
pp.solve() # solve the model

pp.sensitivity() # sensitivity report
print(pp.KKT())
print("Objetivo encontrado: ", round(pp.vobj(),2))
#pp.end() #Good habit: do away with the model