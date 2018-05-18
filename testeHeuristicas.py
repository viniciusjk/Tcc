# -*- coding: utf-8 -*-
"""
Created on Thu Mar 22 09:30:14 2018

@author: ViniciusJokubauskas
"""

import numpy as np
from heuristics import *
import datetime as dt


startTime = dt.datetime.now()
fileName = dt.datetime.now().strftime('%Y%m%d_%H%M%S_HEURISTICS_TEST')
initCsv(fileName)

c = np.concatenate((np.arange(10,100,10),np.arange(100,500,50),
                    np.arange(500,1000,100), np.arange(1000,2600,200),
                    np.arange(2500, 4000,500)))



for numberClients in c:
    
    numberChannels = 3
    numberProducts = 3
    expectedReturn = np.random.rand(numberClients,numberChannels,
                                    numberProducts)*1000/100
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
    
             
    nextProduct2Buy(expectedReturn,numberClients, numberChannels,
                    numberProducts, cost,budget,choice,channelCap, 
                    minOfferProduct, maxOfferProduct, rurdleRate,fileName)
    
    choice = np.zeros([numberClients, numberChannels, numberProducts], 
                      dtype=int)   
            
    nextProduct2Buy_v2_1(expectedReturn,numberClients, numberChannels,
                    numberProducts, cost,budget,choice,channelCap,
                    minOfferProduct, maxOfferProduct, rurdleRate,fileName)
    
    choice = np.zeros([numberClients, numberChannels, numberProducts], 
                      dtype=int)   

    nextProduct2Buy_v2(expectedReturn,numberClients, numberChannels,
                    numberProducts, cost,budget,choice,channelCap,
                    minOfferProduct, maxOfferProduct, rurdleRate,fileName)
    
endTime = dt.datetime.now()
finalTime = endTime-startTime

print(finalTime)
appendCsv('--------', '--------', finalTime, '--------', '--------')
input()
