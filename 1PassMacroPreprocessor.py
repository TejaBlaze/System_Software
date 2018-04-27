from Deftab import Deftab
from Namtab import Namtab
from Posparams import Posparams
from optab import Optab
from symtab import Symtab
from Argtab import Argtab

assembler_directives = ['START', 'END', 'BYTE', 'WORD', 'RESB', 'RESW', 'BASE', 'NOBASE', 'MACRO', 'MEND']

#Load opcode table
ot = Optab()
ot.create()
ot.read_op()

d1 = Deftab()
n1 = Namtab()
p1 = Posparams()
ar1 = Argtab()


class MacroProcessor:
    def __init__(self):
        pass


    def Tokenize(self,line):
        line = line.replace('\t',' ')
        self.ef1,self.ef2,self.ef3='','',''
        toks = [ele.replace('\n','') for ele in line.split(' ') if ele!='']
        if(len(toks) == 1):             #Only mnemonic
            if(toks[0].upper() not in assembler_directives):
                f,p,a = ot.search(toks[0].upper())
                if(f==0):
                    self.ef2='Invalid mnemonic'
            return ['',toks[0],'']
        
        elif(len(toks) == 2):             
            #Case 1: opcode operand
            f,p,a = ot.search(toks[0])
            if(toks[0].upper() in assembler_directives or f==1):
                f,p,a = ot.search(toks[1].upper())
                if(toks[1].upper() in assembler_directives or f==1):
                    self.ef3='Invalid operand'
                return ['',toks[0],toks[1]]

            #Case 2: label opcode
            else:
                f,p,a = ot.search(toks[0].upper())
                if(f==1):
                    self.ef1='Invalid label'    
                f,p,a = ot.search(toks[1].upper())
                if(toks[1].upper() not in assembler_directives and f==0):
                    self.ef2='Invalid mnemonic'
                return [toks[0],toks[1],'']
            
        elif(len(toks) >= 3):             
            #label opcode operand
            f,p,a = ot.search(toks[1].upper())
            if(toks[1].upper() in assembler_directives or f==1):
                f,p,a = ot.search(toks[0].upper())
                if(toks[0].upper() in assembler_directives or f==1):
                    self.ef1='Invalid label'
                f,p,a = ot.search(toks[0].upper())
                if(toks[2].upper() in assembler_directives or f==1):
                    self.ef3='Invalid operand'
            else:
                self.ef2='Invalid mnemonic'
            if(len==3):
                return toks
            opr=''
            for ele in toks[2:]:
                opr+=ele+' '
            return [toks[0],toks[1],opr.rstrip()]


    def Start(self, fn):
        self.expanding = False
        self.lno = 0
        self.args_num = 0
        self.fpin = open(fn,"r")
        self.fpout = open('Source_Codes/expanded.asm',"w")
        self.label, self.opcode, self.operands = '','',''
        while self.opcode.upper()!='END':
            #print("Getting line...")
            self.Getline()
            #print("{};{};{}".format(self.label, self.opcode,self.operands))
            #print("Processing line...")
            self.Processline()

    def Getline(self):
        if self.expanding:
            #print("Expanding")
            self.line = d1.RetrieveLine(self.mstart)
            if self.args_li==[]:
                for i in range(len(self.opcode.split(','))):
                    self.args_li.append(ar1.Retrieve())
            #print(self.args_li)
            for opr_no in range(len(self.args_li)):
                #self.line = self.line.replace('?'+str(opr_no), ar1.Search(opr_no+self.args_num))
                self.line = self.line.replace('?'+str(opr_no), self.args_li[opr_no])
            self.mstart += 1
        else:
            #print("Reading from file")
            self.line = self.fpin.readline()
            if len(self.line) == 0:
                exit(0)
        #print("Current line => {}".format(self.line))
        self.label, self.opcode, self.operands = self.Tokenize(self.line) 
        

    def Processline(self):
        l1 = n1.Search(self.label)
        if l1!='':
            #print("Macro invokation")
            self.args_li=[]
            self.mname, self.mstart, self.mstop = l1.split(' ')
            self.mstart, self.mstop = int(self.mstart), int(self.mstop)
            self.Expand()
        elif self.opcode.upper() == 'MACRO':
            #print("Macro definition")
            self.Define()
        else:
            #print("Normal line")
            self.fpout.write(self.line[:self.line.find('\n')]+'\n')

    def Define(self):
        #print("Inside definition")
        self.mname = self.label
        #print("Macro name => {}".format(self.mname))
        #n1.Insert(self.mname) - at last
        #d1.Insert(p1.Convert(self.line))
        d1.Insert(p1.Convert_new(self.line, self.line))
        mheader = self.line
        level = 1
        curr_lno = 0
        while level > 0:
            self.Getline()
            #print("{};{};{}".format(self.label, self.opcode,self.operands))
            
            if self.line[0] != '.':
                #ln = p1.Convert(self.line, mheader)
                ln = p1.Convert_new(self.line)
                if self.opcode.upper() == 'MACRO':
                    ln  =ln
                if ln.find('\n')==-1:
                    ln+='\n'
                #print("Converted line: {}".format(ln))
                d1.Insert(ln)
                #d1.Insert(ln)
            
            if self.opcode.upper() == 'MACRO':
                level +=1
            elif self.opcode.upper() == 'MEND':
                level -=1
            curr_lno +=1
        #print("Maco end")
        #print("{} {} {}".format(self.mname, self.lno, self.lno+curr_lno+1))
        n1.Insert(self.mname, self.lno, self.lno+curr_lno+1)
        self.lno += curr_lno+1

    def Expand(self):
        self.expanding = True
        #print("Line: {}".format(self.mstart))
        #print(self.line)
        #print("{};{};{}".format(self.label, self.opcode,self.operands))
            
        args = self.opcode.split(',')
        #print(args)
        num_args = len(args)
        ar1.Insert(args)
        self.fpout.write('.'+self.line)
        
        self.Getline()
        while self.mstart < self.mstop-1:
            self.Getline()
            self.Processline()
        self.expanding = False

fn = 'Source_Codes/'+ raw_input("Enter file name:")
m1 = MacroProcessor()
m1.Start(fn)