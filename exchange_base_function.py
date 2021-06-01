import time
import ccxt
from asciichartpy import plot

class CryptoExchange:
	def __init__(self, exchange_id: str, apiK: str, secK: str):  
		self.exchange_id = exchange_id
		exchange_class = getattr(ccxt, exchange_id)
		exchange = exchange_class({
			'apiKey': apiK,
			'secret': secK,
		})
		self.exchange = exchange  
		self.exchange.load_markets()  


# Robot to check the trend(CT -> Check Trend)
class AntCTRobot():
	def __init__(self, exchange: CryptoExchange, notice): 
		self.loop_interval = 10      # check data per 10 seconds
		self.exchange = exchange
		self.notice = notice

	def set_rule(self, rules):
		self.rules = rules
		for x in range(len(self.rules)):
			self.rules[x]['t'] = 0
			self.rules[x]['head_price'] = 0
			self.rules[x]['head_time'] = '0'
			self.rules[x]['tail_price'] = 0
			self.rules[x]['tail_time'] = '0'
			print(str(x))
			print("\tsymbol: " + self.rules[x]['symbol'])
			print("\ttimeframe: " + str(self.rules[x]['timeframe']))
			print("\tdiff: " + str(self.rules[x]['diff']))

	def action(self, x):

		# make the standard output clear
		print("\n\n")
		print("-----------------------------------------------")

		content = ''
		h_price = float(self.rules[x]['head_price'])
		t_price = float(self.rules[x]['tail_price'])

		content = content + str(self.rules[x]['head_price']) + " ===> " + str(self.rules[x]['tail_price']) + "\n\n"
		content = content + self.rules[x]['head_time'] + " ===> " + self.rules[x]['tail_time'] + "\n\n"

		sbj = ''
		if(h_price >= t_price):
			result = h_price - t_price
			if(result >= self.rules[x]['diff']):
				sbj = "Down"
				content = self.rules[x]['symbol'] + " was down !!" + "\n\ndiff: " + str(result) + "\n\n" + content
				self.notice.send(sbj, content)
			else:
				content = self.rules[x]['symbol'] + "\n\n" + content
		else:
			result = t_price - h_price
			if(result >= self.rules[x]['diff']):
				sbj = "Up"
				content = self.rules[x]['symbol'] + " was up !!" + "\n\ndiff: " + str(result) + "\n\n" + content
				self.notice.send(sbj, content)
			else:
				content = self.rules[x]['symbol'] + "\n\n" + content

		print(content)

	def get_localtime(self):
		localtime = time.localtime()
		result = time.strftime("%Y-%m-%d %I:%M:%S %p", localtime)
		return result

	def __check_update(self, data):
		for x in range(len(self.rules)):
			if(self.rules[x]['t'] == 0):
				self.rules[x]['head_price'] = data[self.rules[x]['symbol']]['info']['price']
				self.rules[x]['head_time'] = self.get_localtime()
				self.rules[x]['t'] = self.rules[x]['t'] + self.loop_interval
			elif(self.rules[x]['t'] >= self.rules[x]['timeframe']):
				self.rules[x]['tail_price'] = data[self.rules[x]['symbol']]['info']['price']
				self.rules[x]['tail_time'] = self.get_localtime()
				self.action(x)

				self.rules[x]['t'] = 0
				self.rules[x]['head_price'] = data[self.rules[x]['symbol']]['info']['price']
				self.rules[x]['head_time'] = self.get_localtime()
				self.rules[x]['t'] = self.rules[x]['t'] + self.loop_interval
			else:
				self.rules[x]['t'] = self.rules[x]['t'] + self.loop_interval
	

	def run(self):
		while 1:
			#data = self.exchange.fetch_ticker(self.rule_symbol)
			data = self.exchange.exchange.fetch_tickers()

			self.__check_update(data)

			time.sleep(self.loop_interval)
