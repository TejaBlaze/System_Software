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

def Pad(n, ele):
    for i in range(n-len(ele)):
        ele += '0'
    return ele

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
        smt.load()
        with open('Intermediate_Files/assembled_reloc.obj','wb') as fp3:
            #Copy to reloc file
            fp3.write('H^'+padding(6,self.src)+'^'+hexa(6, self.start)+'^'+hexa(6, self.length)+'\n')
            M=[0]*12            
            q=0
            ovr_flag = 0
            check_next = 0

            #Text records
            curr_line = fp.readline().strip()
            fp_1.readline()
            st=int(self.start,16)
            rec_opcodes = ''
            rop = []
            #Copy to reloc
            fp3.write('T^'+hexa(6,hex(st)[2:]))
            curr_lim = st+rec_lim
            i1 = 0
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

                    if len(curr_opcode)!=6 and curr_opcode!='0000' and opcode not in assembler_directives:
                        flag=1
                    
                    if check_next == 1:
                        if opcode not in assembler_directives:
                            ovr_flag=1
                            check_next=0

                    if len(curr_opcode) != 6:
                        check_next = 1
                    else:
                        i1+=1

                    if(curr_opcode!='0000'): 

                        if i1>0 and (len(rec_opcodes+curr_opcode)>rec_lim or lc>curr_lim or ovr_flag==1):
                            length = hex(int(len(rec_opcodes)/2))[2:]
                            sta1 = (curr_line.split(' ')[0])
                            next_st = hexa(6,sta1)
                            
                            #Write to reloc file with bit mask
                            a1 = ''.join([str(ele) for ele in M])
                            b1 = int(a1, 2)
                            c1 = Pad(3,hex(b1)[2:])
                            if int(length,16)!=0:
                                fp3.write('^'+hexa(2,length)+'^'+c1+'^'+'^'.join(rop)+'\nT^'+next_st)
                            M=[0]*12            
                            q=0

                            rec_opcodes = curr_opcode
                            rop =[]
                            if(curr_opcode!=''):
                                rop.append(curr_opcode)
                            st=lc
                            curr_lim = st+rec_lim
                            if ovr_flag==1:
                                ovr_flag=0
                        
                        else:
                            rec_opcodes += curr_opcode
                            if(curr_opcode!=''):
                                rop.append(curr_opcode)
                    if(opcode.upper() != 'RSUB') and opcode.upper() != 'START' and curr_opcode!='' and curr_opcode!='0000':
                        if opcode not in assembler_directives:
                            M[q]=1
                    if curr_opcode!='' and curr_opcode!='0000':
                        q+=1
                    

                curr_line = fp.readline().strip()
                
                #print("{} : {} => {}, {}".format(q,M, opcode, curr_opcode))
                
            length = hex(int(len(rec_opcodes)/2))[2:]
            #Write to reloc file with bit mask
            a1 = ''.join([str(ele) for ele in M])
            b1 = int(a1, 2)
            c1 = Pad(3,hex(b1)[2:])
            fp3.write('^'+hexa(2,length)+'^'+c1+'^'+'^'.join(rop))
            
            #End record
            fp3.write('\nE^'+hexa(6,self.start))

asm = Assembler_2pass()
asm.Pass2()