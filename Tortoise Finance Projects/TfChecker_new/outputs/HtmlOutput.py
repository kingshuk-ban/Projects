from matplotlib.backends.backend_pdf import PdfPages
import datetime
import os
from webbrowser import open_new_tab
from Output import Output
class HtmlOutput(Output):
    def __init__(self, program):
        super().__init__(program)
        now = datetime.datetime.today().strftime("%Y%m%d-%H%M%S")
        self.filename = program + '.html'
        self.file = open(self.filename, 'w')
        wrapper = """<html>
                <head>
                <title>%s output - %s</title>
                <style>
                table, th, td {
                    border: 1px solid black;
                }
                th, td {
                    padding: 10px;
                }
                </style>
                </head>
                """
        self.whole = wrapper % (program, now)
        self.file.write(self.whole)


    def close(self):
        print("CLOSED FILE")
        self.file.write("""<br></html>""")
        self.file.close()
        # Change the filepath variable below to match the location of your directory
        self.filename = 'file://' + os.getcwd() + '/' + self.filename
        print(self.filename)
        open_new_tab(self.filename)

    def print(self, text, htmltagstart="""<body>""", htmltagend="""</body>"""):
        print(text)
        wrapper = """
                %s%s<br>%s
                """
        self.whole = wrapper % (htmltagstart, text, htmltagend)
        self.file.write(self.whole)

    def image(self, filename):
        self.print("<img src=%s />" % (filename))

    def tag(self, tag):
        self.file.write(tag)

    def tabprint(self, text, htmltagstart="""<body>""", htmltagend="""</body>"""):
        print(text)
        wrapper = """
                %s%s%s
                """
        self.whole = wrapper % (htmltagstart, text, htmltagend)
        self.file.write(self.whole)

    def tabstart(self, name):
        #self.file.write("""<table class="center" style=float:right> <caption><strong>%s</strong></caption>""" % (name))
        self.file.write("""<table style=width:400px> <caption><strong>%s</strong></caption>""" % (name))

    def tabend(self):
        self.file.write("""</table>""")

    def rowitems(self, items):
        self.file.write("""<tr>""")
        for i in items:
            self.file.write("""<td>%s</td>""" % (i))
        self.file.write("""</tr>""")

    def error(self, s):
        self.print("")
        self.print("Error - %s" % (s), """<strong>""", """</strong>""")
        #self.quit()

    def info(self, s):
        self.print("")
        self.print("Info - %s" % (s), """<b>""", """</b>""")

    def warn(self, s):
        self.print("")
        self.tag("""<div class="alert">""")
        self.print("")
        self.print("Warning - %s" % (s), """<strong style=color:red font-size=60px>""", """</strong>""")
        self.tag("""</div>""")

    def action(self, s):
        self.print("")
        self.print("Act now - %s" % (s), """<mark>""", """</mark>""")

    def quit(self):
        self.info("Good luck and goodbye!!")
        self.close()
        #exit()

    def section_start(self, text):
        self.print("")
        self.tag("""<section>""")
        self.tag("""<h2>""")
        self.print(text, "", "")
        self.tag("""</h2>""")
        self.tag("""<p>""")

    def section_end(self):
        self.tag("""</p>""")
        self.print("")
        self.tag("""</section>""")


