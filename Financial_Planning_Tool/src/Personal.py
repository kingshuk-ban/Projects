# Personal information
import utils
from utils import report

class Personal:
	def __init__(self):
		self.data = dict()
		self.data['name'] = "Unknown"
		self.data['age'] = 40
		self.data['retirement age'] = 65
		self.data['risk aversion'] = 50
	
	def add(self, n, a, r, ri):
		self.data['name'] = n
		self.data['age'] = a
		self.data['retirement age'] = r
		self.data['risk aversion'] = ri
		
	def report(self):
		utils.report_personal(self.data)
		
	def getRetireAge(self):
		return self.data['retirement age']
		
	def getCurrentAge(self):
		return self.data['age']
	
	def getRiskNumber(self):
		return self.data['risk aversion']
		