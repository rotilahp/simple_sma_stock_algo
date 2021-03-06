from mystock import myStock
import time

stocksList = ['AMD','PCG','TEVA','SPXL','XRT','SLY',"JETS",'XLE']
#stocksList = ['AMD','PCG']
objectList=[]

#CREATE STOCK OBJECTS
for stock in stocksList:
    objectList.append(myStock(stock))

#set amount of stock to buy based on stock price
def setInventory():
    price = int(float(obj.currentPrice))
    obj.inventory = int(30000/(len(stocksList))/price) 
    print(obj.inventory)

def writeToFile():
    with open('history.txt','a+',newline='\n') as file:
        content = '{},{},{},{}\n'.format(obj.ticker,obj.buyState,obj.currentDate,obj.currentPrice)
        file.write(content)
        #file.write('\n')

flag = True
while flag:
    for obj in objectList:
        obj.getData()
        obj.loadData()
        print('now loading: {}'.format(obj.ticker))
        if obj.buyState == False and obj.previousBuyState == False:
            obj.smaDayTradeBuy()

        elif obj.buyState == False and obj.previousBuyState == True:
            #this means we sold shares of this stock
            writeToFile()
            obj.previousBuyState = False
            obj.smaDayTradeBuy()           

        elif obj.buyState == True and obj.previousBuyState ==False:
            #this means we bought shares of this stock
            writeToFile()
            setInventory()
            obj.previousBuyState = True
            obj.smaDayTradeSell() 

        time.sleep(15)        time.sleep(16)