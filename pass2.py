from optab import Optab
from symtab import Symtab

#For formatting records in object code
def padding(lim, str):
    if(len(str)>lim):
        return str[:lim+1]
    for i in range(lim-len(str)):
        str+=' '
    return str

#Formatting address in text records
def hexa(lim,s1):
    for i in range(lim-len(s1)):
        s1='0'+s1
    return s1

#Find length of byte strings
def oper(x):
    p1 = x.find(chr(153))
    p2 = x.find(chr(226),p1+1)
    msg = x[p1+1:p2]
    if(p1==-1 and p2==-1):
        msg=x[2:-1]
    return msg

assembler_directives = ['START', 'END', 'BYTE', 'WORD', 'RESB', 'RESW', 'BASE', 'NOBASE']

#Create a symbol table
smt = Symtab()
smt.create()

#Load opcode table
ot = Optab()
ot.create()
ot.read_op()


class Assembler_2pass:
    def __init__(self):
        with open('Intermediate_Files/intermediate.txt','rb') as fp:
            fc = fp.read().splitlines()
            self.src, self.start, self.length = fc[-1:][0].split(' ')

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


    def Pass2(self):
        rec_lim = 60
        fp,fp_1 = open('Intermediate_Files/intermediate.txt','rb'),open('Intermediate_Files/intermediate.txt','rb')
        #fp3=open(self.src+'_reloc.obj','wb')
        smt.load()
        with open('Intermediate_Files/assembled.obj','wb') as fp2:
            #Head record
            fp2.write('H^'+padding(6,self.src)+'^'+hexa(6, self.start)+'^'+hexa(6, self.length)+'\n')
            
            #Copy to reloc file
            #fp3.write('H^'+padding(6,self.src)+'^'+hexa(6, self.start)+'^'+hexa(6, self.length)+'\n')
            #M=[0]*12            
            #q=0
            
            #Text records
            curr_line = fp.readline().strip()
            fp_1.readline()
            st=int(self.start,16)
            rec_opcodes = ''
            rop = []
            fp2.write('T^'+hexa(6,hex(st)[2:]))
            #Copy to reloc
            #fp3.write('T^'+hexa(6,hex(st)[2:]))
            curr_lim = st+rec_lim
            while(len(curr_line)>0):
                if curr_line.find('.')==-1:
                    fla=0
                    lc = int(curr_line.split(' ')[0],16)
                    ln = curr_line[curr_line.find(' ')+1:]
                    label, opcode, operand = self.Tokenize(ln)
                    if(opcode.upper() == 'END'):
                        break

                    f,c,opc = ot.search(opcode)   
                    if(operand != ''):
                        pos = operand.find(',')
                        if(pos==-1):
                            f2,c2,addr = smt.search(operand)
                        else:
                            for lab in operand.split(','):
                                f2,c2,addr = smt.search(lab.strip())
                                if(f2==1):
                                    break
                                
                        if(f2==1):
                            curr_opcode = str(opc+addr)
                        elif opcode in assembler_directives:
                            opco=''
                            if(opcode.upper()=='BYTE'):
                                if(operand[0]=='C'):
                                    for ch in oper(operand):
                                        opco+=hex(ord(ch))[2:]
                                else:
                                    opco=oper(operand)
                            elif(opcode.upper()=='WORD'):
                                opco=hexa(6,operand)
                            curr_opcode = str(opc+opco)
                    else:
                        curr_opcode = str(opc+hexa(4,'0'))
                        fla=1
                    print("{} => {}".format(curr_line, curr_opcode)) 
                    if(curr_opcode!='0000'):
                        if len(rec_opcodes+curr_opcode)>rec_lim or lc>curr_lim:
                            length = hex(int(len(rec_opcodes)/2))[2:]
                            sta1=(curr_line.split(' ')[0])
                            next_st = hexa(6,sta1)
                            fp2.write('^'+hexa(2,length)+'^'+'^'.join(rop)+'\nT^'+next_st)
                            
                            rec_opcodes = curr_opcode
                            rop =[]
                            if(curr_opcode!=''):
                                rop.append(curr_opcode)
                            st=lc
                            curr_lim = st+rec_lim        
                        else:
                            rec_opcodes += curr_opcode
                            if(curr_opcode!=''):
                                rop.append(curr_opcode)
                curr_line = fp.readline().strip()
            
            length = hex(int(len(rec_opcodes)/2))[2:]
            fp2.write('^'+hexa(2,length)+'^'+'^'.join(rop))
            
            #End record
            fp2.write('\nE^'+hexa(6,self.start))

asm = Assembler_2pass()
asm.Pass2()