class Argtab:
    def __init__(self, mode="w"):
        self.num_args=0
        self.curr_st = 0
        self.argtab = open("Intermediate_Files/argtab.txt",mode)

    def Insert(self, args):
        for ele in args:
            self.argtab.write(str(self.num_args) + ' '+ ele+'\n')
            self.num_args+=1
    
    def Search(self, key):
        self.argtab.close()
        with open("Intermediate_Files/argtab.txt","r") as argtab:
            while True:
                line = argtab.readline().strip()
                if len(line) <=0:
                    break
                id, arg = line.split(' ')
                id = int(id)
                if id==key:
                    self.argtab = open("Intermediate_Files/argtab.txt","a")
                    return arg
        self.argtab = open("Intermediate_Files/argtab.txt","a")
        return ''

    
    def Retrieve(self):
        self.argtab.close()
        with open("Intermediate_Files/argtab.txt","r") as argtab:
            for i in range(self.curr_st):
                line = argtab.readline().strip()
            
            line = argtab.readline().strip()
            #print(line)
            id, arg = line.split(' ')
            
            self.curr_st+=1
            self.argtab = open("Intermediate_Files/argtab.txt","a")
            return arg
        self.argtab = open("Intermediate_Files/argtab.txt","a")
        return ''