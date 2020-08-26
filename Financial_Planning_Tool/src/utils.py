# This is the utils package
import numpy as np
import matplotlib.pyplot as pyplot
from HtmlOutput import HtmlOutput
from StreamLitOutput import StreamLitOutput

STOCK_GROWTH_RATE=8.0
BOND_GROWTH_RATE=3.0
CASH_GROWTH_RATE=1.0

#currency_symbol = ""

output = HtmlOutput("tfchecker")
#output = StreamLitOutput("The Tortoise Finance")

currency_symbol = "$"
def set_currency(curr):
	global currency_symbol
	currency_symbol = curr
	output.info("Currency set to %s" % (currency_symbol))

def get_currency():
	return currency_symbol

def report(name, data, total, pre="none", post=""):
	if (pre == "none"):
		pre = currency_symbol
	output.print("")
	output.tabstart("%s" % (name))
	rowitems = list()
	#rowitems.append("Name")
	#rowitems.append("Value")
	#output.rowitems(rowitems)
	#rowitems.clear()
	for n,v in data.items():
		rowitems.append("%s" % (n))
		rowitems.append("%s%.2f%s" % (pre, v, post))
		output.rowitems(rowitems)
		rowitems.clear()
	rowitems.clear()
	rowitems.append("Total")
	rowitems.append("%s%.2f%s" % (pre, total, post))
	output.rowitems(rowitems)
	output.tabend()
	
def report_personal(data):
	output.print("")

	output.tabstart("Personal Information")
	rowitems = list()
	rowitems.append("Name")
	rowitems.append("%s" % (data['name']))
	output.rowitems(rowitems)
	rowitems.clear()

	for n,v in data.items():
		if (n == 'name'):
			continue
		rowitems.append("%s" % (n))
		rowitems.append("%d" % (v))
		output.rowitems(rowitems)
		rowitems.clear()

	output.tabend()
	
	
def project(d, r, y):
	t = 0.0
	for n,v in d.items():
		d[n] = v * (1 + r/100)**y
		t += d[n]
	return t
	
def fv(d, pmt, y):
	t = 0.0
	for n,val in d.items():
		(pv, r) = val
		r = r/100
		#print("Debug-fv: r=%f pv=%f y=%d pmt=%f" % (r, pv, y, pmt))
		d[n] = np.fv(r/12, y*12, -pmt, -pv)
		#print("Debug-fv: fv=%f" % (d[n]))
		t += d[n]
	t = round(t, 2)
	return t

def fv_allocation(d, alloc, y):
	t = 0.0
	for n, val in d.items():
		(pv, r) = val
		pmt = alloc[n]
		r = r/100
		d[n] = (-1.0) * np.fv(r/12, y*12, pmt, pv)
		t += d[n]
	t = round(t, 2)
	return t
	
def sum(d):
	t = 0.0
	for n,v in d.items():
		t += v
	return t
	
def payment(v, r, y):
	r = r/100
	r = r/12
	if (y == -1):
		return float(r*v)
	else:
		return float(v * ((r*((1+r)**(y*12))) / ((1+r)**(y*12) - 1)))

def mortgage_payment(total, installs_paid, rate, years):
	output.info("Mortgage: Total=%.2f Paid months=%d rate=%.2f term=%d" % (total, installs_paid, rate, years))
	rate = rate/100
	pmt = -1 * np.pmt(rate/12, 12*years, total)
	ipmt = 0.0
	ppmt = 0.0
	for i in range(installs_paid):
		ipmt_t = -1 * np.ipmt(rate/12, i, 12*years, total)
		ppmt_t = -1 * np.ppmt(rate/12, i, 12*years, total)
		#info("Month: %d Interest: %.2f Principal: %.2f" % (i, ipmt_t, ppmt_t))
		ipmt += ipmt_t
		ppmt += ppmt_t
	output.info("Regular mortgage payment: %s%.2f" % (get_currency(), pmt))
	output.info("Interest paid in %d months: %s%.2f" % (installs_paid, get_currency(), ipmt))
	output.info("Principal paid in %d months: %s%.2f" % (installs_paid, get_currency(), ppmt))
	output.info("Balance at the end of %d months: %s%.2f" % (installs_paid, get_currency(), total - ppmt))
	return (ppmt, total - ppmt)
		
def func(pct, allvals):
	absolute = int(pct/100.*np.sum(allvals))
	return "{:.1f}%\n({:s}{:d})".format(pct, currency_symbol, absolute)
	
def piechart(filename, title, labels, values):
	final_l = list()
	final_v = list()
	i = 0
	for l in labels:
		v = values[i]
		i = i + 1
		if (v == 0):
			continue
		final_l.append(l)
		final_v.append(v)
	if (len(final_l) <= 1):
		return
	fig, axe = pyplot.subplots()
	fig.suptitle(title)
	axe.pie(final_v, labels=final_l, autopct=lambda pct: func(pct, final_v), startangle=90)
	axe.axis('equal')
	fig.savefig("%s.png" % (filename))
	output.image("%s.png" % (filename))
	pyplot.clf()
	pyplot.cla()
	pyplot.close()
