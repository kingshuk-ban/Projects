import datetime
import os
import time
import psutil
from PIL import Image
import graphviz as graphviz
from Output import Output

class StandardOutput(Output):
    def __init__(self, program):
        super().__init__(program)
        print("")
        self.graph = graphviz.Digraph()
        self.lastnode = 'start'

    def print_header(self, program):
        now = datetime.datetime.today().strftime("%Y/%m/%d at %H-%M-%S")
        print("Analysis prepared by %s on %s" % (program, now))

    def close(self):
        print("Analysis done. Here are your action items in order!")
        st.graphviz_chart(self.graph)
        self.lastnode = 'start'
        self.graph = graphviz.Digraph()

    def print(self, text, htmltagstart="""<body>""", htmltagend="""</body>"""):
        print(text)

    def image(self, filename):
        image = Image.open(filename)
        image.show()
        time.sleep(5)

    def tag(self, tag):
        print("")

    def tabprint(self, text, htmltagstart="""<body>""", htmltagend="""</body>"""):
        print(text)

    def tabstart(self, name):
        print(name)

    def tabend(self):
        print("")

    def rowitems(self, items):
        #print("Table")
        out = ""
        for i in items:
            out += i + " "
        print(out)
        #print("Table end")

    def error(self, s):
        print("Error: %s\n" % s)

    def info(self, s):
        print("Info: %s\n" % s)

    def warn(self, s):
        print("Warning: %s\n" % s)

    def action(self, s):
        print('**_Action_**: %s' % (s))
        self.graph.edge(self.lastnode, s)
        self.lastnode = s

    def quit(self):
        print("")

    def section_start(self, text):
        print(text)

    def section_end(self):
        print("")


