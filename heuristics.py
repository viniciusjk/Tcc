# -*- coding: utf-8 -*-
"""
Created on Sat Mar 24 12:59:14 2018

@author: ViniciusJokubauskas
"""
import numpy as np
import pymprog as pp
import timeit
import csv



def initCsv(fileName):
    
    fieldName = ["Tamanho amostra", "Heuristica", "Tempo", "Fáctivel", "Resultado"]

    fileName = fileName + ".csv"
    with open(fileName,'a', newline='') as csvFile:

        writeFile = csv.DictWriter(csvFile, fieldnames=fieldName)
        writeFile.writeheader()
        
def appendCsv(fileName,sampleSize, HeuristicName, time, isFeasible, objctive):
     
    fileName = fileName + ".csv"
    with open(fileName,'a', newline='') as csvFile:

        writeFile = csv.writer(csvFile, delimiter=',')
        writeFile.writerow([sampleSize, HeuristicName, time, isFeasible, objctive])
    
def feasiabilityTest(rNumberClients,rNumberChannels, rNumberProducts, choice,
                       channelCap, maxOfferProduct, sumObj,cost, rurdleRate):
    foundLimitChannel=[]
    for j in rNumberChannels:
        foundLimitChannel.append( sum(choice[i][j][k] for i in rNumberClients\
                                      for k in rNumberProducts))
    
    foundOfferedProd = []
    for k in rNumberProducts:
        foundOfferedProd.append(sum(choice[i][j][k] for i in rNumberClients\
                                      for j in rNumberChannels))
        
    foundClientLimit = []
    for i in rNumberClients:
        foundClientLimit.append(sum(choice[i][j][k] for j in rNumberChannels\
                                  for k in rNumberProducts))
    
    costWithRurdle = (1+rurdleRate)*sum(choice[i][j][k]*cost[j] for i in\
                 rNumberClients for j in rNumberChannels for k\
                 in rNumberProducts)

    
    for i in rNumberChannels:
        if (foundLimitChannel[i]>channelCap[i]):
            feasibleChannel = False
            break
        else: feasibleChannel=True
        
    for k in rNumberProducts:
        if (foundOfferedProd[k]>maxOfferProduct[k]):
            feasibleProduct = False
            break
        else: feasibleProduct= True
    
    for i in rNumberClients:
        if (foundClientLimit[i]>1):
            feasibleClient=False
            break
        else: feasibleClient=True
    
    if (costWithRurdle>sumObj.sum()):
        feasibleRurdle = False
    else: feasibleRurdle = True
    
    
    print("Channels: ",foundLimitChannel, channelCap,feasibleChannel,
          "\nProducts:",foundOfferedProd, maxOfferProduct,feasibleProduct,
          "\nRurdle:",costWithRurdle,feasibleRurdle)
#          "\nClients:", foundClientLimit, feasibleClient)
#    print("Clients:", feasibleClient,"\nChannels: ", feasibleChannel,
#          "\nProducts: ", feasibleProduct, "\nRurdle: ", feasibleRurdle)
    feasiabilityTest = feasibleChannel and feasibleClient and feasibleProduct \
    and feasibleRurdle
#    print(feasiabilityTest)
    return feasiabilityTest
    
def ppSolver(expectedReturn, numberClients, numberChannels, 
                    numberProducts, cost, budget, channelCap, minOfferProduct,
                    maxOfferProduct, rurdleRate, fileName):

 
    startTime = timeit.default_timer()
    rNumberClients = range(numberClients)
    rNumberChannels = range(numberChannels)
    rNumberProducts = range(numberProducts)
    
    t = pp.iprod(rNumberClients,rNumberChannels,rNumberProducts)
    pp.begin('basic') # begin modelling
    pp.verbose(False)  # be verbose
    
    x = pp.var('choice', 
            t, bool)
            
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
    
#    for k in rNumberProducts:
#        sum(x[i,j,k] for i in rNumberClients for j in rNumberChannels)\
#        >=minOfferProduct[k]
        
    #budgetConstraint:
    
    pp.st(sum(x[i,j,k]*cost[j] for i in rNumberClients for j in\
        rNumberChannels for k in rNumberProducts)<=budget,"Budget Constr.")
        
    #clientLimitConstraint:
    
    for i in rNumberClients:
        pp.st(sum(x[i,j,k] for j in rNumberChannels for k in rNumberProducts)\
              <=1,"Client "+str(i)+" limit")
    
    #rurdleRateConstraint:
    
    pp.st(sum(x[i,j,k]*expectedReturn[i][j][k] for i in rNumberClients for j \
          in rNumberChannels for k in rNumberProducts)>= (1+rurdleRate)\
            *sum(x[i,j,k]*cost[j] for i in rNumberClients for j in\
                rNumberChannels for k in rNumberProducts),"Rurdle Rate Constr")
        
    pp.solve() # solve the model
    
#    pp.sensitivity() # sensitivity report
    endTime = timeit.default_timer()-startTime
    print("Objetivo encontrado: ", round(pp.vobj(),2)," em ", 
          round(endTime,3)," segundos")

    print("\n\n\n")
    appendCsv(fileName,numberClients,"Solver method",endTime, True,
             round(pp.vobj(),2) )
    pp.end() #Good habit: do away with the model

def nextProduct2Buy(expectedReturn, numberClients, numberChannels, 
                    numberProducts, cost, budget, choice,channelCap, 
                    minOfferProduct, maxOfferProduct, rurdleRate, fileName):
   
    print("\n===HEURISTIC 4===")
    print("-----------------------------------------")
    startTime = timeit.default_timer()
    iterations=numberClients*numberChannels*numberProducts  
    budgetAux = budget
    e = np.array(expectedReturn)
    sumCost=0
    rNumberClients = range(numberClients)
    rNumberChannels = range(numberChannels)
    rNumberProducts = range(numberProducts)
    
    for i in range(iterations):
        
        
        if (budgetAux<=cost.min()):
            
            break
    
    
        arg= e.argmax()
        cordClients =((arg//numberProducts)//numberChannels)%numberClients
        cordChannels = (arg//numberProducts)%numberChannels
        cordProducts = arg%numberProducts
    
        
        e[cordClients, cordChannels, cordProducts] = -.1
        
        if (budgetAux-cost[cordChannels] > 0):
            
            
         
            budgetAux = budgetAux-cost[cordChannels]
    
            sumCost = cost[cordChannels]+sumCost
            choice[cordClients, cordChannels, cordProducts] = 1
            
           
            
    sumObj = choice*expectedReturn
    
    
    feasibleSolution = feasiabilityTest(rNumberClients,rNumberChannels, rNumberProducts,
                        choice, channelCap, maxOfferProduct, sumObj, cost, rurdleRate)
    
    

    endTime = timeit.default_timer()-startTime
    

    appendCsv(fileName, numberClients,"Next Product2Buy",endTime, feasibleSolution,
             round(sumObj.sum(),2) )
    print ("Objective Found:", round(sumObj.sum(),2),"\nem",round(endTime,3),
           " segundos")   
    print("Sulution feasible? ", feasibleSolution)
#    print("Parou em: ", i, "iteraçoes\nEconomizou: ",iterations-i,
#          " iterações ou,",round(endTime*iterations/i,3)," segundos" )
    print("Budget ",budget,">=", sumCost, " Total cost") 
    print("-----------------------------------------\n\n")
    
def nextProduct2Buy_v2_1(expectedReturn, numberClients, numberChannels, 
                    numberProducts, cost, budget, choice,channelCap, 
                    minOfferProduct, maxOfferProduct, rurdleRate, fileName):
   
    print("\n===HEURISTIC 4 V2.1===")
    print("-----------------------------------------")
    startTime = timeit.default_timer()
    iterations=numberClients*numberChannels*numberProducts  
    budgetAux = budget
    e = np.array(expectedReturn)
    sumCost=0
    rNumberClients = range(numberClients)
    rNumberChannels = range(numberChannels)
    rNumberProducts = range(numberProducts)
    
    for i in range(iterations):
        
        

    
    
        arg= e.argmax()
        cordClients =((arg//numberProducts)//numberChannels)%numberClients
        cordChannels = (arg//numberProducts)%numberChannels
        cordProducts = arg%numberProducts
    
        
        e[cordClients, cordChannels, cordProducts] = -.1
        
        clientTest = choice.sum(1).sum(1)[cordClients]+1<=1
#        clientTest= (sum(choice[cordClients][j][k] for j in rNumberChannels\
#                         for k in rNumberProducts)+1<=1)
         
        
#        channelTest = (sum(choice[i][cordChannels][k] for i in rNumberClients\
#                           for k in rNumberProducts)+1<=channelCap[cordChannels])
        channelTest = choice.sum(0).sum(1)[cordChannels]+1\
                         <=channelCap[cordChannels]
        
#        productTest = (sum(choice[i][j][cordProducts] for i in rNumberClients\
#                           for j in rNumberChannels)+1<=maxOfferProduct[cordProducts])
        
        productTest = choice.sum(0).sum(0)[cordProducts]+1\
                                    <=maxOfferProduct[cordProducts]
        
        
        test = clientTest and channelTest and productTest
        if (budgetAux<=cost.min()):
            
            break
        if (budgetAux-cost[cordChannels] >= 0 and test):
            
            
         
            budgetAux = budgetAux-cost[cordChannels]
    
            sumCost = cost[cordChannels]+sumCost
            choice[cordClients, cordChannels, cordProducts] = 1
            
           
            
            
    sumObj = choice*expectedReturn        


    feasibleSolution = feasiabilityTest(rNumberClients,rNumberChannels, rNumberProducts,
                        choice,channelCap, maxOfferProduct, sumObj, cost, rurdleRate)
    
    endTime = timeit.default_timer()-startTime
    

    appendCsv(fileName, numberClients,"Next Product Improved V2.1",endTime, feasibleSolution,
             round(sumObj.sum(),2) )
   
    print ("Objective Found:", round(sumObj.sum(),2),"\nem",round(endTime,3),
           " segundos")   
    
    print("Sulution feasible? ", feasibleSolution)
   
    
#    print("Parou em: ", i, "iteraçoes\nEconomizou: ",iterations-i,
#          " iterações ou,",round(endTime*iterations/i,3)," segundos" )
    print("Budget ",budget,">=", sumCost, " Total cost") 
    print("-----------------------------------------\n\n")
    
def nextProduct2Buy_v2(expectedReturn, numberClients, numberChannels, 
                    numberProducts, cost, budget, choice,channelCap, 
                    minOfferProduct, maxOfferProduct, rurdleRate, fileName):
   
    print("\n===HEURISTIC 4 V2===")
    print("-----------------------------------------")
    startTime = timeit.default_timer()
    iterations=numberClients*numberChannels*numberProducts  
    budgetAux = budget
    e = np.array(expectedReturn)
    sumCost=0
    rNumberClients = range(numberClients)
    rNumberChannels = range(numberChannels)
    rNumberProducts = range(numberProducts)
    
    for i in range(iterations):
        
        

    
    
        arg= e.argmax()
        cordClients =((arg//numberProducts)//numberChannels)%numberClients
        cordChannels = (arg//numberProducts)%numberChannels
        cordProducts = arg%numberProducts
    
        
        e[cordClients, cordChannels, cordProducts] = -.1
        
#        clientTest = choice.sum(1).sum(1)[cordClients]+1<=1
        clientTest= (sum(choice[cordClients][j][k] for j in rNumberChannels\
                         for k in rNumberProducts)+1<=1)
         
        
        channelTest = (sum(choice[i][cordChannels][k] for i in rNumberClients\
                           for k in rNumberProducts)+1<=channelCap[cordChannels])
#        channelTest = choice.sum(0).sum(1)[cordChannels]+1\
#                         <=channelCap[cordChannels]
        
        productTest = (sum(choice[i][j][cordProducts] for i in rNumberClients\
                           for j in rNumberChannels)+1<=maxOfferProduct[cordProducts])
#        
#        productTest = choice.sum(0).sum(0)[cordProducts]+1\
#                                    <=maxOfferProduct[cordProducts]
        
        
        test = clientTest and channelTest and productTest
        if (budgetAux<=cost.min()):
            
            break
        if (budgetAux-cost[cordChannels] >= 0 and test):
            
            
         
            budgetAux = budgetAux-cost[cordChannels]
    
            sumCost = cost[cordChannels]+sumCost
            choice[cordClients, cordChannels, cordProducts] = 1
            
           
            
            
    sumObj = choice*expectedReturn        


    feasibleSolution = feasiabilityTest(rNumberClients,rNumberChannels, rNumberProducts,
                        choice,channelCap, maxOfferProduct, sumObj, cost, rurdleRate)
    
    endTime = timeit.default_timer()-startTime
    

    appendCsv(fileName, numberClients,"Next Product Improved",endTime, feasibleSolution,
             round(sumObj.sum(),2) )
   
    print ("Objective Found:", round(sumObj.sum(),2),"\nem",round(endTime,3),
           " segundos")   
    
    print("Sulution feasible? ", feasibleSolution)
   
    
#    print("Parou em: ", i, "iteraçoes\nEconomizou: ",iterations-i,
#          " iterações ou,",round(endTime*iterations/i,3)," segundos" )
    print("Budget ",budget,">=", sumCost, " Total cost") 
    print("-----------------------------------------\n\n")
    
    
