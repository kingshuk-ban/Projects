class Output:
    def __init__(self, program):
        print("Base output class")

    def close(self):
        raise Exception('not implemented!') 

    def print(self, text, htmltagstart="""<body>""", htmltagend="""</body>"""):
        raise Exception('not implemented!') 

    def image(self, filename):
        raise Exception('not implemented!') 

    def tag(self, tag):
        raise Exception('not implemented!') 

    def tabprint(self, text, htmltagstart="""<body>""", htmltagend="""</body>"""):
        raise Exception('not implemented!') 

    def tabstart(self, name):
        raise Exception('not implemented!') 

    def tabend(self):
        raise Exception('not implemented!') 

    def rowitems(self, items):
        raise Exception('not implemented!') 

    def error(self, s):
        raise Exception('not implemented!') 

    def info(self, s):
        raise Exception('not implemented!') 

    def warn(self, s):
        raise Exception('not implemented!') 

    def action(self, s):
        raise Exception('not implemented!') 

    def quit(self):
        raise Exception('not implemented!') 

    def section_start(self, text):
        raise Exception('not implemented!') 

    def section_end(self):
        raise Exception('not implemented!') 


