import requests
import logging
from typing import Tuple

'''Telegram Portion to send different types of messages'''
logging.basicConfig(filename='telegram.log', level=logging.INFO,
                    format='%(levelname)s:%(message)s')


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
