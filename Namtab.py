class Namtab:
    def __init__(self, mode="w"):
        self.namtab = open('Intermediate_Files/namtab.txt',mode)

    def Insert(self, mname, def_start, def_end):
        self.namtab.write(mname+' '+str(def_start)+' '+str(def_end)+'\n')

    def Search(self, opcode):
        self.namtab.close()
        with open("Intermediate_Files/namtab.txt","r") as nmtb:
            ln = nmtb.readline()
            while len(ln)>0:
                mname = ln.split(' ')[0]
                if mname.upper() == opcode.upper():
                    self.namtab = open('Intermediate_Files/namtab.txt',"a")
                    return ln
                ln = nmtb.readline().strip()
        self.namtab = open('Intermediate_Files/namtab.txt',"a")
        return ''
'''
n1 = Namtab()
n1.Insert("m1",0,1)
n1.Insert("m2",1,2)
print(n1.Search("m2"))
'''