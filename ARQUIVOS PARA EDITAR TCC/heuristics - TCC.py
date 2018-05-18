# -*- coding: utf-8 -*-
"""
Created on Sat Mar 24 12:59:14 2018

@author: ViniciusJokubauskas
"""
import numpy as np
import pymprog as pp
import timeit
import csv



def initCsv():
    
    fieldName = ["Tamanho amostra", "Heuristica", "Tempo", "Fáctivel", "Resultado"]


    with open('Results.csv','w', newline='') as csvFile:

        writeFile = csv.DictWriter(csvFile, fieldnames=fieldName)
        writeFile.writeheader()
        
def appendCsv(sampleSize, HeuristicName, time, isFeasible, objctive):
     
    with open('Results.csv','a', newline='') as csvFile:

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
                    maxOfferProduct, rurdleRate):

 
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
    appendCsv(numberClients,"Solver method",endTime, True,
             round(pp.vobj(),2) )
    pp.end() #Good habit: do away with the model

def nextProduct2Buy(expectedReturn, numberClients, numberChannels, 
                    numberProducts, cost, budget, choice,channelCap, 
                    minOfferProduct, maxOfferProduct, rurdleRate):
   
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
    
    for i in range(numberClients*numberChannels*numberProducts):
	#loop do tamanho da nossa amostra, vamos ordenar a matriz 
	#de acordo com o descrito na seção acima
        
        
        if (budgetAux<=cost.min()): 
		#se o budget já se esgotou, podemos parar a função
            
            break
    
    
        arg= e.argmax() #recebemos o valor máximo da matriz 
		
        cordClients =((arg//numberProducts)//numberChannels)%numberClients
        cordChannels = (arg//numberProducts)%numberChannels
        cordProducts = arg%numberProducts
		#pegamos as coordenadas deste valor máximo na matriz original
        
        e[cordClients, cordChannels, cordProducts] = -.1
		
		#após copiado o valor original, colocamos o valor -.1
		#para garantir que este valor não será usado
		# novamente na próxima iteração
		
        
        if (budgetAux-cost[cordChannels] > 0):
            
            # teste lógico, que testa se temos budget suficiente para
			# utilizar essa oferta
         
            budgetAux = budgetAux-cost[cordChannels]
			#se escolhida a oferta, debitamos seu custo do nosso budget
			
    
            sumCost = cost[cordChannels]+sumCost
			#variável auxiliar para sabermos o custo para testarmos
			# a factibilidade da solução
            choice[cordClients, cordChannels, cordProducts] = 1
			#colocamos o valor da nossa variável de escolha
			#como 1 nesta posição, pois utilizamos essa oferta 
            
           
            
    sumObj = choice*expectedReturn
	#soma do lucro total de nossa solução
    
    
    feasibleSolution = feasiabilityTest(rNumberClients,rNumberChannels, rNumberProducts,
                        choice, channelCap, maxOfferProduct, sumObj, cost, rurdleRate)
    #função criada para testarmos a factibilidade da solução
	#testamos todas as restrições dadas com a solução encotrada
    

    endTime = timeit.default_timer()-startTime
    

    appendCsv(numberClients,"Next Product2Buy",endTime, feasibleSolution,
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
                    minOfferProduct, maxOfferProduct, rurdleRate):
   
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
    

    appendCsv(numberClients,"Next Product Improved V2.1",endTime, feasibleSolution,
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
                    minOfferProduct, maxOfferProduct, rurdleRate):
   
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
    
    for i in range(numberClients*numberChannels*numberProducts ):
    #loop do tamanho da nossa amostra, vamos ordenar a matriz 
	#de acordo com o descrito na seção acima  
        

    
    
        arg= e.argmax() #pegamos os maior valor da nossa matriz de retorno esperado
						#assim como na heurística NP2B
        cordClients =((arg//numberProducts)//numberChannels)%numberClients
        cordChannels = (arg//numberProducts)%numberChannels
        cordProducts = arg%numberProducts
		#pegamos as coordenadas deste item
        
        e[cordClients, cordChannels, cordProducts] = -.1
        #o este valor é passado para a coordenada do item porque 
		#não queremos mais utilizar esse item nas próximas iterações, ele já foi utilizado

        clientTest= (sum(choice[cordClients][j][k] for j in rNumberChannels\
                         for k in rNumberProducts)+1<=1)
		#testamos se, escolhendo este item da matriz, violamos a regra de oferecer
		#apenas um produto por cliente
         
        
        channelTest = (sum(choice[i][cordChannels][k] for i in rNumberClients\
                           for k in rNumberProducts)+1<=channelCap[cordChannels])
		#testamos se a escolha do item vai estourar o limite de produtos oferecidos por canal

        
        productTest = (sum(choice[i][j][cordProducts] for i in rNumberClients\
                           for j in rNumberChannels)+1<=maxOfferProduct[cordProducts])
		#é testado se a escolha do item viola a restrição do número máximo de produtos que 
		#podem ser oferecidos

        
        
        test = clientTest and channelTest and productTest #o teste será verdadeiro apenas se todas
														  # as restrições são respeitadas
        if (budgetAux<=cost.min()): #se o budget já é menor que o menor custo
									# o loop inteiro pode para, pois não é possível escolher mais nenhum
									#produto
            
            break
        if (budgetAux-cost[cordChannels] >= 0 and test): #se a escolha deste item não violou nenhuma
														 # das restrições acima e não viola o budget
														 #finalmente podemos escolher o item
            
            
         
            budgetAux = budgetAux-cost[cordChannels] #debitamos o custo do budget
    
            sumCost = cost[cordChannels]+sumCost #somamos o custo ao custo total
            choice[cordClients, cordChannels, cordProducts] = 1 #setamos como 1 a variavel de escolha
																#das coordenadas do item, pois utilizamos 
																#este produto
            
           
            
            
    sumObj = choice*expectedReturn  #no fim do loop, calculamos o retorno total


    feasibleSolution = feasiabilityTest(rNumberClients,rNumberChannels, rNumberProducts,
                        choice,channelCap, maxOfferProduct, sumObj, cost, rurdleRate)
						#testamos a factibilidade da solução
    
    endTime = timeit.default_timer()-startTime
    

    appendCsv(numberClients,"Next Product Improved",endTime, feasibleSolution,
             round(sumObj.sum(),2) )
   
    print ("Objective Found:", round(sumObj.sum(),2),"\nem",round(endTime,3),
           " segundos")   
    
    print("Sulution feasible? ", feasibleSolution)
   
    
#    print("Parou em: ", i, "iteraçoes\nEconomizou: ",iterations-i,
#          " iterações ou,",round(endTime*iterations/i,3)," segundos" )
    print("Budget ",budget,">=", sumCost, " Total cost") 
    print("-----------------------------------------\n\n")
    
    
