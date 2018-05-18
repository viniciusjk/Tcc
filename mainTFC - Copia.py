# -*- coding: utf-8 -*-
"""
Created on Thu Mar 22 09:30:14 2018

@author: ViniciusJokubauskas
"""

import numpy as np
from heuristics2 import *
import datetime as dt


startTime = dt.datetime.now()

initCsv()

c = np.concatenate((np.arange(10,100,10),np.arange(100,500,50),
                    np.arange(500,1000,100), np.arange(1000,3200,200)))

#c = np.arange(2200,3200,200)
#c = np.arange(3500,5500,500)
#c = [1400,1600,1800,2500,3000,3500]
c = [1200,2200,2400,2200,2400]
for numberClients in c:
    
#    numberClients = 1200 #comenta isso
    numberChannels = 3
    numberProducts = 3
    expectedReturn = np.random.rand(numberClients,numberChannels,
                                    numberProducts)*1000/100
    cost = np.random.randint(1,10,numberChannels)
    cost = np.array([5,6,7])
    channelCap = np.random.rand(numberChannels)*numberClients
    channelCap = channelCap.round()
    minOfferProduct = np.random.randint(0,numberClients/3,numberProducts)
    maxOfferProduct = np.random.randint(numberClients/3,numberClients,
                                        numberProducts)
    budget = np.random.randint(min(cost)*numberClients,max(cost)*numberClients)
    rurdleRate = np.random.randint(1000,15000)/100000
    
    
    for i in range(minOfferProduct.size):
                if maxOfferProduct[i]<= minOfferProduct[i]:
                        maxOfferProduct[i] =  np.random.randint(minOfferProduct[i]
                        , numberClients)
                        
    
    choice = np.zeros([numberClients, numberChannels, numberProducts], dtype=int)
    
    
    """"
    Heuristic 4_picky for budget
    """
    
    print('-------\t',numberClients,'\t-------\n')
    ppSolver(expectedReturn,numberClients, numberChannels,numberProducts,
             cost,budget,channelCap, minOfferProduct,maxOfferProduct,
             rurdleRate)
    
    
             
    nextProduct2Buy(expectedReturn,numberClients, numberChannels,
                    numberProducts, cost,budget,choice,channelCap, 
                    minOfferProduct, maxOfferProduct, rurdleRate)
    
    choice = np.zeros([numberClients, numberChannels, numberProducts], 
                      dtype=int)   
            
    nextProduct2Buy_v2_1(expectedReturn,numberClients, numberChannels,
                    numberProducts, cost,budget,choice,channelCap,
                    minOfferProduct, maxOfferProduct, rurdleRate)
    
#    choice = np.zeros([numberClients, numberChannels, numberProducts], 
#                      dtype=int)   
#        
#    nextProduct2Buy_v2(expectedReturn,numberClients, numberChannels,
#                    numberProducts, cost,budget,choice,channelCap,
#                    minOfferProduct, maxOfferProduct, rurdleRate)
    #meanReturn = []
    #meanCost = np.array(cost)
    #for k in range(numberProducts):
    #   meanReturn.append(sum(expectedReturn[i][j][k] for i in range(numberClients) 
    #   for j in range(numberChannels) )/(numberClients*numberChannels))
    
    #print (expectedReturn)       
    #print(meanReturn)   
     

    
endTime = dt.datetime.now()
finalTime = endTime-startTime

print(finalTime)
appendCsv('--------', '--------', finalTime, '--------', '--------')
#input()
