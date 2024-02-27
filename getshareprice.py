import requests
import logging
from datetime import datetime

import os
import csv
import json

from pymodm.connection import connect
from Model.model import TodayShare
from Model.telegramU import Telegram
from datetime import datetime
import pytz


# from dotenv import dotenv_values
from dotenv import load_dotenv
load_dotenv()
# from bs4 import BeautifulSoup

logging.basicConfig(filename='sharedata.log', level=logging.INFO,
                    format='%(levelname)s:%(message)s')

class Shareprices:

    def __init__(self,stckSymbol):
        self.stckSymbol = stckSymbol

        self.timestamp = datetime.now(tz=pytz.timezone('Asia/Kathmandu')).timestamp() * 1000
        logging.info("Fetchin' for Timestamp "+ str(self.timestamp))
        header = {
            'Accept':'application/json',
            'Accept-Language':'en-US,en;q=0.9',
            'Cache-Control':'no-cache',
            'Content-Type': 'application/json; charset=UTF-8',
            'Origin':'https://nepalipaisa.com',
            'Host': 'nepalipaisa.com',
            'Pragma':'no-cache',
            'Referer':'https://nepalipaisa.com/live-market',
            'X-Requested-With':'XMLHttpRequest',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36 Edg/87.0.664.52'}
        
        params = {
            'stockSymbol': self.stckSymbol,
            '_': str(self.timestamp)
        }
        link = requests.get('https://nepalipaisa.com/api/GetStockLive',params=params,
                        headers=header)

        # response = link.text
        # print(link.content)
        # print(link.status_code)
        # raise Exception("data")
        self.data = link.json()['result']
        # print(self.data)
        if self.data["stocks"] != []:
            self.todayshareprice = self.data["stocks"][0]

            self.dt_obj = datetime.strptime(self.todayshareprice['asOfDate'],'%Y-%m-%dT%H:%M:%S')
            self.new_dt = self.dt_obj.strftime('%d %B, %Y')
        else:
            logging.error("No records of the symbol "+self.stckSymbol)
            raise Exception(f"The data of {self.stckSymbol} not found")
        # self.


    def shareinfo(self) -> str:
        """
        To get Share information

        :return: The text message consisting the information about the share prices
        """
        try:
            tosendText = f"""Share Symbol: **{self.todayshareprice['stockSymbol']}**
Name: __{self.todayshareprice['companyName']}__
************************************
Number of transaction : **{self.todayshareprice['noOfTransactions']}**
```
Max Price: Rs. {self.todayshareprice['maxPrice']}
Min Price: Rs. {self.todayshareprice['minPrice']}
```
****************
```
Closing Price: Rs. {self.todayshareprice['closingPrice']}
Difference: {self.todayshareprice['differenceRs']}
```
****************
```
Traded Shares: {self.todayshareprice['volume']}
Traded Amount: {self.todayshareprice['amount']}
Previous Closing: {self.todayshareprice['previousClosing']}
Percent Difference: {self.todayshareprice['percentChange']}```
.......................................
Date: {self.new_dt}"""
            return tosendText
        except Exception as e:
            print(e)



    def writetextfile(self,filepath:str):
        _todayShare = self.shareinfo()
        if not os.path.exists(filepath):
            with open(filepath,'w') as json_f:
                json_f.write(_todayShare)
                logging.info(f"Share file named '{filepath}' created successfully and valid latest data entered")
        else:
            _file = open(filepath,'r')
            _fileText = _file.read().splitlines()
            _lastline = _fileText[-1]

            if _lastline != _todayShare.splitlines()[-1]:
               with open(filepath,'a') as json_f:
                    json_f.write(_todayShare)
            _file.close()

    def writeCsv(self,filepath:str):
        fieldnames = ['Share Symbol',
                    'Name',
                    'Number of transaction',
                    'Max Price',
                    'Min Price',
                    'Closing Price',
                    'Difference',
                    'Traded Shares',
                    'Traded Amount',
                    'Previous Closing',
                    'Percent Difference',
                    'Date']


        row_data = {
                    'Share Symbol': str(self.todayshareprice['stockSymbol']),
                    'Name': str(self.todayshareprice['companyName']),
                    'Number of transaction' : str(self.todayshareprice['noOfTransactions']),
                    'Max Price': 'Rs. '+ str(self.todayshareprice['maxPrice']),
                    'Min Price': 'Rs. ' + str(self.todayshareprice['minPrice']),
                    'Closing Price': 'Rs. '+ str(self.todayshareprice['closingPrice']),
                    'Difference': str(self.todayshareprice['differenceRs']),
                    'Traded Shares': str(self.todayshareprice['volume']),
                    'Traded Amount': str(self.todayshareprice['amount']),
                    'Previous Closing': str(self.todayshareprice['previousClosing']),
                    'Percent Difference': str(self.todayshareprice['percentChange']),
                    'Date': self.new_dt
                }

        print(not os.path.exists(filepath))
        if not os.path.exists(filepath):
            with open(filepath,'w') as _csv:

                _w_csv = csv.DictWriter(_csv,fieldnames=fieldnames)
                _w_csv.writeheader()
                _w_csv.writerow(row_data)

        else:
            csv_read = open(filepath,'r')
            read_file = csv.DictReader(csv_read)
            last_updated = list(read_file)[-1]['Date']
            # print(last_updated)


            if last_updated != self.new_dt:
                with open(filepath,'a') as _csv:
                    _w_csv = csv.DictWriter(_csv,fieldnames=fieldnames)
                    _w_csv.writerow(row_data)

    def last_updatedDT(self):
        csv_read = open(str(self.stckSymbol).lower()+'_today.csv','r')
        read_file = csv.DictReader(csv_read)
        last_updated = list(read_file)[-1]['Date']
        return last_updated

    def send_to_telegram(self,creds:tuple):
        creds = creds
        telegram_ = Telegram()
        telegram_.newcreds = creds
        # print(self.telegram_.api_key)
        # print(self.shareinfo().splitlines()[-1])

        """To SEND TO TELEGRAM"""
        if self.last_updatedDT() != self.new_dt:
            telegram_.sendMessage(self.shareinfo()) #to send message in telegram
        else:
            logging.error("The data has already been updated")
            print("The data has already been sent")
        print(self.last_updatedDT())


        logging.info(f"The share data of Date:{self.new_dt} is updated")

    def insertToMongo(self):
        try:
            TodayShare(
                share_symbol = str(self.todayshareprice['stockSymbol']),
                name = str(self.todayshareprice['companyName']), 
                num_transactions = int(self.todayshareprice['noOfTransactions']),
                max_price = float(self.todayshareprice['maxPrice']),
                min_price = float(self.todayshareprice['minPrice']),
                closing_price = float(self.todayshareprice['closingPrice']),
                difference = float(self.todayshareprice['differenceRs']),
                traded_shares = float(self.todayshareprice['volume']),
                traded_amount = float(self.todayshareprice['amount']),
                previous_closing = float(self.todayshareprice['previousClosing']),
                percent_difference = float(self.todayshareprice['percentChange']),
                date = str(self.new_dt)
            ).save()
        except Exception as e:
            logging.error("Error discovered in Mongo is "+ str(e))



if __name__ == "__main__":

    #GETTING STORED DATA FROM CREDENTIALS
    # with open("..\\sharecreds.json","rb") as file:
    #     creds = json.loads(file.read())
    #     bot_api = creds['Nkd_bot']
    #     channel_id = '-100'+creds['channel_ID']

    ## ENABLE MONGODB CONNECTION
    mongo_url = os.environ['MONGOURL']
    connect(mongo_url,alias='my-app')
    
    my_shares = ['NABIL','NTC','HRL','USHEC','VLUCL','SONA','SGIC','NIFRA','SRLI','GVL','MBJC','ALBSL','USHEC','TAMOR','PPL',"ILI","GCIL","RNLI","SNLI","USHL"]

    for symbol in my_shares:
        logging.info("processing this page "+ symbol)
        try:
            obj = Shareprices(symbol)
            obj.writetextfile("ShareData/"+symbol.lower()+'_info.txt')
            obj.writeCsv("ShareData/"+symbol.lower()+'_today.csv')
            obj.insertToMongo()
        except Exception as error:
            logging.error(error)

    # obj = Shareprices("SGI")

    # obj.writetextfile('shareinfo.txt')
    # obj.writeCsv('sgitoday.csv')
    # # obj.send_to_telegram((bot_api,channel_id))


    # obj = Shareprices("NIFRA")
    # obj.writetextfile('nifrashare.txt')
    # obj.writeCsv('nifratoday.csv')
    # obj.send_to_telegram((bot_api,channel_id))
