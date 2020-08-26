from matplotlib.backends.backend_pdf import PdfPages
import datetime
import os
import streamlit as st
from PIL import Image
import graphviz as graphviz

class StreamLitOutput:
    def __init__(self, program):
        st.write("")
        self.graph = graphviz.Digraph()
        self.lastnode = 'start'

    def print_header(self, program):
        now = datetime.datetime.today().strftime("%Y/%m/%d at %H-%M-%S")
        st.title("Analysis prepared by %s on %s" % (program, now))

    def close(self):
        st.header("Analysis done. Here are your action items in order!")
        st.graphviz_chart(self.graph)
        self.lastnode = 'start'
        self.graph = graphviz.Digraph()

    def print(self, text, htmltagstart="""<body>""", htmltagend="""</body>"""):
        st.write(text)

    def image(self, filename):
        image = Image.open(filename)
        st.image(image)

    def tag(self, tag):
        st.write("")

    def tabprint(self, text, htmltagstart="""<body>""", htmltagend="""</body>"""):
        st.write(text)

    def tabstart(self, name):
        st.write(name)

    def tabend(self):
        st.write("")

    def rowitems(self, items):
        #st.write("Table")
        out = ""
        for i in items:
            out += i + " "
        st.write(out)
        #st.write("Table end")

    def error(self, s):
        st.error(s)

    def info(self, s):
        st.info(s)

    def warn(self, s):
        st.warning(s)

    def action(self, s):
        st.success('**_Action_**: %s' % (s))
        self.graph.edge(self.lastnode, s)
        self.lastnode = s

    def quit(self):
        st.write("")

    def section_start(self, text):
        st.subheader(text)

    def section_end(self):
        st.subheader("")


