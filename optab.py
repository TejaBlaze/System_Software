class Optab:
    def __init__(self):
        pass
    
    def create(self):
        self.op_tab = []

    def read_op(self):
        with open('Intermediate_Files/sic_opcode.txt','r') as f:
            fc = f.read().splitlines()
            for entry in fc:
                self.op_tab.append(entry.split(' '))
            
    def search(self, instruction):
        flag,pos,address=0,-1,''
        for i in range(len(self.op_tab)):
            if(self.op_tab[i][0]==instruction):
                flag,pos,address=1,i,self.op_tab[i][1]
        return [flag,pos,address]