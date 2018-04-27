class Symtab:
    def __init__(self):
        pass

    def create(self):
        self.errflag=''
        self.symtab=[]

    def exit(self):
        del self.symtab

    def insert(self,label,address):
        if self.symtab:
            flag,c,dest=self.search(label)
            if(flag==1):
                self.errflag='insert'
                return
        self.symtab.append([label, address])

    def modify(self,old_label,new_label, new_address):
        if self.symtab:
            flag,c,dest = self.search(old_label)
            if(flag==0):
                self.errflag='modify'
            else:
                f2,c2,d2 = self.search(new_label)
                if(f2==1):
                    self.errflag='modify'
                    return
                self.symtab[c] = new_label, new_address
        else:
            self.errflag='modify'

    def search(self,label):
        if self.symtab:
            flag=0
            for i in range(len(self.symtab)):
                if(self.symtab[i][0] == label.strip()):
                    c=i
                    flag=1
                    dest = self.symtab[i][1]
                    break
            if(flag!=0):
                return [1, c, dest]
        return [0, -1, -1]
        self.errflag='search'

    def display(self):
        if self.symtab:
            print("\nSymbol Table Contents\n------------\n")
            print("Symbol\t\t\tAddress\n------\t\t\t--------")
            for sym,addr in self.symtab:
                print("%8s\t%16s"%(sym, addr))
            print("")
            return
        print("\nSymbol Table is empty\n")

    def delete(self,label):
        if self.symtab:
            flag,c,dest = self.search(label)
            if(flag==0):
                self.errflag='delete'
                return
            del self.symtab[c]
        else:
            self.errflag='delete'

    def save(self):
        with open('Intermediate_Files/symtab.txt','w') as f2:
            for lb,lc in self.symtab:
                s1=str(lb)+' '+str(lc)+'\n'
                f2.write(s1)
        
    def load(self):
        with open('Intermediate_Files/symtab.txt','r') as f2:
            self.symtab=[]
            fc = f2.read().splitlines()
            for line in fc:
                lb,lc = line.split(' ')
                self.symtab.append([lb,lc])

    