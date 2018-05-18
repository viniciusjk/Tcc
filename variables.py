# -*- coding: utf-8 -*-
"""
Created on Fri Mar 30 11:44:59 2018

@author: ViniciusJokubauskas
"""
import numpy as np

numberClients = 10
numberChannels = 3
numberProducts = 3 
expectedReturn = np.random.rand(numberClients,numberChannels,
                                numberProducts)*1000/100
cost = np.random.randint(1,10,numberChannels)
cost = np.array([5,6,7])
channelCap = np.random.rand(numberChannels)*numberClients
channelCap = channelCap.round()
minOfferProduct = np.random.randint(0,numberClients,numberProducts)
maxOfferProduct = np.random.randint(0,numberClients,numberProducts)
budget = np.random.randint(min(cost)*numberClients,max(cost)*numberClients)
rurdleRate = np.random.randint(1000,15000)/100000


for i in range(minOfferProduct.size):
            if maxOfferProduct[i]<= minOfferProduct[i]:
                    maxOfferProduct[i] =  np.random.randint(minOfferProduct[i]
                    , numberClients)
                    

choice = np.zeros([numberClients, numberChannels, numberProducts], dtype=int)