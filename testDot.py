from dotenv import dotenv_values
from pymodm.connection import connect
from Model.model import TodayShare

config = dotenv_values('.env')
print(config['MONGOURL'])
print(type(config))
connect(config['MONGOURL'],alias='my-app')

data = TodayShare (
    share_symbol="SGIC",
    name = "Sanima General Insurance",
    num_transactions = 700,
    max_price = 450.02,
    min_price = 430.1,
    closing_price = 448.12,
    difference = -12.3,
    traded_shares = 9123123.0,
    traded_amount = 2312442.213,
    previous_closing = 420,
    percent_difference = -23,
    date = "12 dec 2022"
)
data.save()
print(data)
