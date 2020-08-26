from yattag import Doc
from webbrowser import open_new_tab
def error(s):
	with tag('br'):
		with tag('strong'):
			text(s)
def warn(s):
	with tag('br'):
		with tag('strong color=blue font-size=60px'):
			text(s)
def info(s):
	with tag('br'):
		with tag('b'):
			text(s)
def action(s):
	with tag('br'):
		with tag('mark'):
			text(s)

doc, tag, text = Doc().tagtext()
with tag('br'):
	with tag('h1'):
		text('Hello')
error("This is an error")
warn("This is a warning")
info("This is an info")
action("This is an action")

file = open("yt.html", 'w')
file.write(doc.getvalue())
file.close()
#print(doc.getvalue())
open_new_tab('file:///Users/kingshuk/Documents/TfChecker/yt.html')