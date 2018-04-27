class Deftab:
    def __init__(self, mode="w"):
        self.deftab = open('Intermediate_Files/deftab.txt',mode)

    def Insert(self, mbody):
        self.deftab.write(mbody)

    def Retrieve(self, def_start, def_end):
        self.deftab.close()
        with open('Intermediate_Files/deftab.txt',"r") as dftb:
            for i in range(def_start+1):
                ln = dftb.readline()
            mbody = ''
            for i in range(def_end - def_start-2):
                ln = dftb.readline()
                mbody += ln
        self.deftab = open('Intermediate_Files/deftab.txt',"a")
        return mbody

    def RetrieveLine(self, lno):
        self.deftab.close()
        with open('Intermediate_Files/deftab.txt',"r") as dftb:
            for i in range(lno):
                ln = dftb.readline()
            ln = dftb.readline()
                
        self.deftab = open('Intermediate_Files/deftab.txt',"a")
        return ln