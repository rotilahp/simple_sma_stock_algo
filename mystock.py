import requests
import json
import pandas as pd

twelveApi = '4138a26532c14163a10c81b40f323194'

class myStock:
    outputSize = 10
    timeBtnCrosses=3
    timeAlertMax=3
    smaTimePeriod=[3,21]
    
    def __init__(self,ticker,stockInt='5min'):
        self._ticker=ticker
        self.stockInterval = stockInt
        self.inventory=20
        self.technical='sma'
        self.mergeData={}
        self.smaList=[]
        self._buyState = False
        self._previousBuyState = False
        self._currentDate = ''
        self._currentPrice = 0

    def __dict__(self,item):
        self.item=item

    def getData(self):
        url = "https://api.twelvedata.com/time_series?symbol={}&interval={}&format=JSON&apikey={}".format(self._ticker,self.stockInterval,twelveApi)
        response = requests.get(url)
        price = json.loads(response.text)
        
        for timePeriod in self.smaTimePeriod:
            url = 'https://api.twelvedata.com/{}?symbol={}&interval={}&time_period={}&format=JSON&apikey={}'.format(self.technical,self._ticker,self.stockInterval,timePeriod,twelveApi)
            response = requests.get(url)
            smaData = json.loads(response.text)
            newDict = {'sma{}'.format(timePeriod):smaData}
            self.mergeData = {**self.mergeData,**newDict}
        
        self.mergeData = {**self.mergeData,**price}

        with open('{}_stockdata.json'.format(self._ticker), 'w') as json_file:
            json.dump(self.mergeData, json_file)

    def loadData(self):
        #Read stock data from file
        with open('{}_stockdata.json'.format(self._ticker)) as json_file:
            data = json.load(json_file)
        #All data 
        self.mergeData = data       
        #SMA data
        for timePeriod in self.smaTimePeriod:
            data = self.mergeData['sma{}'.format(timePeriod)]
            self.smaList.append(data)     

    def smaDayTradeBuy(self):
        sma3 = self.smaList[0]
        sma21 = self.smaList[1]

        df_sma3 = pd.DataFrame(sma3['values'])
        df_sma3_price = df_sma3['sma']

        df_sma21 = pd.DataFrame(sma21['values'])
        df_sma21_price = df_sma21['sma']

        if df_sma3_price[0] > df_sma21_price[0]:
            self._buyState = True

    def smaDayTradeSell(self):
        sma3 = self.smaList[0]
        sma21 = self.smaList[1]

        df_sma3 = pd.DataFrame(sma3['values'])
        df_sma3_price = df_sma3['sma']

        df_sma21 = pd.DataFrame(sma21['values'])
        df_sma21_price = df_sma21['sma']

        if df_sma3_price[0] < df_sma21_price[0]:
            self._buyState = False

    @property
    def buyState(self):
        return self._buyState

    @buyState.setter
    def buyState(self,value):
        if type(value) == bool:
            self._buyState=value
        else:
            print('need a bool fool')

    @property
    def previousBuyState(self):
        return self._previousBuyState

    @previousBuyState.setter
    def previousBuyState(self,value):
        if type(value) == bool:
            self._previousBuyState=value
        else:
            print('need a bool fool')

    @property
    def currentDate(self):
        _date = pd.DataFrame(self.mergeData['values'])['datetime'][0]
        self._currentDate = _date
        return self._currentDate

    @property
    def currentPrice(self):
        _price = pd.DataFrame(self.mergeData['values'])['open'][0]
        self._currentPrice = _price
        return self._currentPrice

    @property
    def ticker(self):
        return self._ticker
        


