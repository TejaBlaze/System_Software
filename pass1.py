from optab import Optab
from symtab import Symtab

assembler_directives = ['START', 'END', 'BYTE', 'WORD', 'RESB', 'RESW', 'BASE', 'NOBASE']

#Create a symbol table
smt = Symtab()
smt.create()

#Load opcode table
ot = Optab()
ot.create()
ot.read_op()

#Find length of byte strings
def sizeofop(x):
    p1 = x.find(chr(153))
    p2 = x.find(chr(226),p1+1)
    if(p1==-1 and p2==-1):
        return len(x)-3
    return len(x[p1+1:p2])

class Assembler_2pass:
    def Tokenize(self,line):
        line = line.replace('\t',' ')
        self.ef1,self.ef2,self.ef3='','',''
        toks = [ele.replace('\n','') for ele in line.split(' ') if ele!='']
        if(len(toks) == 1):             #Only mnemonic
            if(toks[0] not in assembler_directives):
                f,p,a = ot.search(toks[0])
                if(f==0):
                    self.ef2='Invalid mnemonic'
            return ['',toks[0],'']
        
        elif(len(toks) == 2):             
            #Case 1: opcode operand
            f,p,a = ot.search(toks[0])
            if(toks[0] in assembler_directives or f==1):
                f,p,a = ot.search(toks[1])
                if(toks[1] in assembler_directives or f==1):
                    self.ef3='Invalid operand'
                return ['',toks[0],toks[1]]

            #Case 2: label opcode
            else:
                f,p,a = ot.search(toks[0])
                if(f==1):
                    self.ef1='Invalid label'    
                f,p,a = ot.search(toks[1])
                if(toks[1] not in assembler_directives and f==0):
                    self.ef2='Invalid mnemonic'
                return [toks[0],toks[1],'']
            
        elif(len(toks) >= 3):             
            #label opcode operand
            f,p,a = ot.search(toks[1])
            if(toks[1] in assembler_directives or f==1):
                f,p,a = ot.search(toks[0])
                if(toks[0] in assembler_directives or f==1):
                    self.ef1='Invalid label'
                f,p,a = ot.search(toks[0])
                if(toks[2] in assembler_directives or f==1):
                    self.ef3='Invalid operand'
            else:
                self.ef2='Invalid mnemonic'
            if(len==3):
                return toks
            opr=''
            for ele in toks[2:]:
                opr+=ele+' '
            return [toks[0],toks[1],opr.rstrip()]

    def Pass1(self,src):
        fp = open(src, 'rb')
        fp2 = open('Intermediate_Files/intermediate.txt', 'wb')
        fc = fp.readline()       #1st line
        start,lc=0,0
        label, opcode, operand = self.Tokenize(fc)  
        #print("{};{};{}".format(label, opcode, operand))
        if(opcode.upper() == 'START'):
            if(operand!=''):
                lc=int(operand,16)
                start = lc
        fp2.write(hex(lc)[2:]+' '+fc)
            
        while(opcode.upper() != 'END'):
            
            self.ef4, self.ef5='',''
            if(fc[0]!='.'):             #not a comment line
                if(label != ''):
                    f,p,a = smt.search(label)
                    if(f==1):           #label already exists
                        self.ef4='Existing label'
                    else:
                        smt.insert(label, hex(lc)[2:])
                f,p,a = ot.search(opcode)
                if(f==1):
                    lc+=3
                elif(opcode.upper() == 'WORD'):
                    lc+=3
                elif(opcode.upper() == 'RESW'):
                    lc+=3*int(operand)
                elif(opcode.upper() == 'RESB'):
                    lc+=int(operand)
                elif(opcode.upper() == 'BYTE'):
                    if(operand[0].upper()=='C'):
                        lc += sizeofop(operand)
                    else:
                        lc+=1
                else:
                    self.ef5='Invalid opcode'
            fc = fp.readline()              #next line
            label, opcode, operand = self.Tokenize(fc) 
            label = label.strip()
            #print("{};{};{}".format(label, opcode, operand)) 
            fp2.write(hex(lc)[2:]+' '+fc)
        
        fp2.write('\n'+src[:src.find('.')]+' '+hex(start)[2:]+' '+hex(lc-start)[2:])
        smt.save()     

asm = Assembler_2pass()
src =  'Source_Codes/'+raw_input("Enter source:")
asm.Pass1(src)