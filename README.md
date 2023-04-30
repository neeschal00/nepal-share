# nepal-share
Script to scrape data of particular share of last transaction price etc

## To Get the last updated share price of a company with symbol
```
from getshareprice import Shareprices
last_updated_price = Shareprices("SGI") #Enter the Symbol number which in this case is SGI
last_updated_price.writeCSV('sgiToday.csv') #Write the file path with the '.csv' extension
last_updated_price.writetextfile('sgiToday.txt')
last_updated_price.insertToMongo() #with preconfigured url in script
```
