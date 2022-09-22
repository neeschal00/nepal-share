import requests
import logging
import json
from datetime import datetime
from typing import Tuple
import os
import csv
import json

# from bs4 import BeautifulSoup

logging.basicConfig(filename='sharedata.log', level=logging.INFO,
                    format='%(levelname)s:%(message)s')

class Shareprices:

    def __init__(self,stckSymbol):
        self.stckSymbol = stckSymbol
        header = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36 Edg/87.0.664.52'}
        link = requests.post('https://www.nepalipaisa.com/Modules/GraphModule/webservices/MarketWatchService.asmx/GetTodaySharePrices',
                        data={"fromdate": "", "toDate": "", "stockSymbol": self.stckSymbol, "offset": "1", "limit": "50"},
                        headers=header)

        response = link.text



        
        self.data = link.json()
        if self.data != []:
            self.todayshareprice = self.data[0]

            self.dt_obj = datetime.strptime(self.todayshareprice['AsOfDate'],'%Y-%m-%dT%H:%M:%S')
            self.new_dt = self.dt_obj.strftime('%d %B, %Y')


        # self.


    def shareinfo(self) -> str:
        """
        To get Share information

        :return: The text message consisting the information about the share prices
        """

        tosendText = f"""Share Symbol: **{self.todayshareprice['stocksymbol']}**
Name: __{self.todayshareprice['stockname']}__
************************************
Number of transaction : **{self.todayshareprice['nooftransaction']}**
```
Max Price: Rs. {self.todayshareprice['maxprice']}
Min Price: Rs. {self.todayshareprice['minprice']}
```
****************
```
Closing Price: Rs. {self.todayshareprice['closingprice']}
Difference: {self.todayshareprice['difference']}
```
****************
```
Traded Shares: {self.todayshareprice['tradedshares']}
Traded Amount: {self.todayshareprice['tradedamount']}
Previous Closing: {self.todayshareprice['previousclosing']}
Percent Difference: {self.todayshareprice['percentdifference']}```
.......................................
Date: {self.new_dt}"""
        return tosendText

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
                    'Share Symbol': self.todayshareprice['stocksymbol'],
                    'Name': self.todayshareprice['stockname'],
                    'Number of transaction' : self.todayshareprice['nooftransaction'],
                    'Max Price': 'Rs. '+ self.todayshareprice['maxprice'],
                    'Min Price': 'Rs. ' + self.todayshareprice['minprice'],
                    'Closing Price': 'Rs. '+ self.todayshareprice['closingprice'],
                    'Difference': self.todayshareprice['difference'],
                    'Traded Shares': self.todayshareprice['tradedshares'],
                    'Traded Amount': self.todayshareprice['tradedamount'],
                    'Previous Closing': self.todayshareprice['previousclosing'],
                    'Percent Difference': self.todayshareprice['percentdifference'],
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
        csv_read = open(self.stckSymbol.lower()+'today.csv','r')
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


'''Telegram Portion to send different types of messages'''



class Telegram:
    def __init__(self):
        self.api_key = None
        self.chat_id = None

    def sendPicture(self,url:str,caption:str)->None:
        """
        Method to send picture

        :param url: The url of image to be sent
        :param caption: The caption along with the image
        """
        apiKey = self.api_key
        chatInfo = {'chat_id': self.chat_id,
                    'photo': url,
                    'caption': caption,
                    'parse_mode': 'Markdown'}
        try:

            r = requests.get(f'https://api.telegram.org/bot{apiKey}/sendPhoto', params=chatInfo)
            logging.debug('The picture successfully sent')

        except:

            logging.error('Connection Error')

    def sendVideo(self,url:str,caption:str)->None:
        """
        Method to send picture

        :param url: The url of video to be sent
        :param caption: The caption along with the video
        """
        apiKey = self.api_key
        chatInfo = {'chat_id': self.chat_id,
                    'video': url,
                    'caption': caption,
                    'parse_mode': 'Markdown'}

        try:
            r = requests.get(f'https://api.telegram.org/bot{apiKey}/sendVideo', params=chatInfo)
            logging.debug('The Video was successfully sent')
        except:
            logging.error('Connection error')

    def sendAnimation(self,url:str,caption:str)->None:
        """
        Method to send picture

        :param url: The url of animation to be sent
        :param caption: The caption along with the animation
        """
        apiKey = self.api_key
        chatInfo = {'chat_id': self.chat_id,
                    'animation': url,
                    'caption': caption,
                    'parse_mode': 'Markdown'}
        try:
            r = requests.get(f'https://api.telegram.org/bot{apiKey}/sendAnimation', params=chatInfo)
            logging.debug('The animation was sent successfully')
        except:
            logging.error('Connection error')

    def sendMessage(self,message:str)->None:
        """
        Method to send picture

        :param message: The text message to be sent
        """
        apiKey = self.api_key
        chatInfo = {'chat_id': self.chat_id,
                    'text': message,
                    'parse_mode': 'Markdown'}
        try:
            r = requests.get(f'https://api.telegram.org/bot{apiKey}/sendMessage', params=chatInfo)
            logging.debug('The message was sent successfully')

        except:
            logging.error('Connection error')

    @property
    def newcreds(self)->Tuple[str,str]:
        """
        The property decorator getter
        :return: The current apikey, chatid
        """
        return self.api_key, self.chat_id

    @newcreds.setter
    def newcreds(self,creds: tuple)->None:
        """
        The property setter to update the credentials that was intially given
        :param creds: A tuple of two values with api key and chat id
        :return:
        """
        api,chat = creds
        self.api_key = api
        self.chat_id = chat

if __name__ == "__main__":

    #GETTING STORED DATA FROM CREDENTIALS
    # with open("..\\sharecreds.json","rb") as file:
    #     creds = json.loads(file.read())
    #     bot_api = creds['Nkd_bot']
    #     channel_id = '-100'+creds['channel_ID']

    obj = Shareprices("SGI")

    obj.writetextfile('shareinfo.txt')
    obj.writeCsv('sgitoday.csv')
    # obj.send_to_telegram((bot_api,channel_id))

    obj = Shareprices("NIFRA")
    obj.writetextfile('nifrashare.txt')
    obj.writeCsv('nifratoday.csv')
    # obj.send_to_telegram((bot_api,channel_id))
