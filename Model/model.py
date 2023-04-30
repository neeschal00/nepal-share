from pymodm import MongoModel, fields
from pymongo.write_concern import WriteConcern

class TodayShare(MongoModel):
	share_symbol = fields.CharField(required=True)
	name = fields.CharField(required=True)
	num_transactions = fields.IntegerField()
	max_price = fields.FloatField()
	min_price = fields.FloatField()
	closing_price = fields.FloatField()
	difference = fields.FloatField()
	traded_shares = fields.FloatField()
	traded_amount = fields.FloatField()
	previous_closing = fields.FloatField()
	percent_difference = fields.FloatField()
	date = fields.CharField(required=True)
	
 
	class Meta:
		connection_alias = 'my-app'
		write_concern = WriteConcern(j=True)
        
        