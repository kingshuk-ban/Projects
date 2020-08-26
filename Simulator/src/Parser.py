# this is the module Parser
class Parser:
	def __init__(self, filename):
		self.filename = filename
		self.filehandle = open(filename, "r")
		self.card_iter = 0
		self.cards = []
		self.nodes = set()
		
	def parse(self):
		print("Parsing the file %s" % (self.filename))
		contents = self.filehandle.readlines()
		for l in contents:
			print(l)
			tokens = l.split()
			if (tokens[0] == "#"):
				continue;
			device = tokens[0]
			nodes = list()
			if (tokens[1] == "("):
				i = 2
				while (tokens[i] != ")"):
					nodes.append(tokens[i])
					self.nodes.add(tokens[i])
					i = i + 1
				value = tokens[i+1]
			else: 
				nodes = [tokens[1], tokens[2]]
				self.nodes.add(tokens[1])
				self.nodes.add(tokens[2])
				value = tokens[3]
			d = {'D':device, 'N':nodes, 'V':value}
			self.cards.append(d)
		return True
		
	def rewind(self):
		self.card_iter = 0
		
	def getCard(self):
		card = self.cards[self.card_iter]
		self.card_iter = self.card_iter + 1
		return card
		
	def print(self):
		self.rewind()
		for card in self.cards:
			card = self.getCard()
			print("Card: %d - Device=%s Nodes=%s Value=%s" % (self.card_iter, card['D'], card['N'], card['V']))
		print("Nodes in circuit: (%s)" % (self.nodes))
def test():
	filename = input('Enter the filename: ')
	p = Parser(filename)
	p.parse();
	p.print();
	p.print();

# test()
		