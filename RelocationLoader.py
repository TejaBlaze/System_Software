'''
Relocation loader program
-----------------
Structure of object program:
Header record: H^program name(8 bytes)^start address(8 bytes)^length(8 bytes)
Text record/s: T^start address(8 bytes)^length(2 bytes)^mask(3 bytes)^object code(x bytes)^ .. 
End record: E^start address(8 bytes)

Load into specified start address or system specific address
'''
import sys
def Check_available(start_addr, length):
    for st,end in avail_mems:
        if(start_addr>=st and start_addr+length<=end):
            return True
    return False
avail_mems = [[1234, 2996],[4096, 4314],[7086, 15926]]                           #List of free memory blocks (start,end)
class RelocationLoader:
    def __init__(self, ip_file, prog_addr = 0):
        self.ip_file = ip_file
        self.op_file = 'relocation_load.txt'
        self.record_limit = 32
        self.field_limit = 8
        self.prog_addr = prog_addr
    def Padding(self, n, ele):
        for j in range(n-len(ele)):
            ele = '0'+ele
        return ele
    def Findfit(self):
        i = 0 
        for st,end in avail_mems:
            if self.total_len <= (end-st):
                return i
            i+=1
        return -1
    def TokenizeLine(self, curr_line):
        line_tokens = curr_line.strip().split('^')
        return line_tokens
    def Displayrecs(self, fpout, rec_addr, curr_record):
        fpout.write(self.Padding(4,hex(rec_addr)[2:])+'\t')
        for id in range(0, len(curr_record), self.field_limit):
            curr_field = curr_record[id:id+self.field_limit] 
            fpout.write(curr_field+' ')
        fpout.write('\n')
    def Adjust(self, line):
        tokens = self.TokenizeLine(line)
        M = [int(ele) for ele in bin(int(tokens[3], 16))[2:]]
        for i in range(len(tokens)-4):
            curr_obcode = int(tokens[i+4], 16)
            if M[i] == 1:
                curr_obcode += self.prog_addr
            tokens[i+4] = hex(curr_obcode)[2:]
            tokens[i+4] = self.Padding(6, tokens[i+4])
        line = '^'.join(tokens)
        return line
    def Driver(self):
        prev_address = -1
        overflow_flag = False
        curr_record = ''
        with open(self.ip_file, "r") as fpin:
            line = fpin.readline()
            tokens = self.TokenizeLine(line)
            while len(line) > 0 and tokens[0]!='E':
                if tokens[0].upper() == 'H':
                    self.start_address = int(tokens[2],16)
                    self.total_len = int(tokens[3],16)
                    if not Check_available(self.start_address, self.total_len):
                        id = self.Findfit()
                        if id==-1:
                            print("Memory unavailable => Exiting")
                            return
                        self.prog_addr = avail_mems[id][0] - self.start_address
                        print("Memory unavailable => Relocating to : {}".format(avail_mems[id][0]))
                        
                    fpout = open(self.op_file, "w")
                    rec_addr = self.start_address + self.prog_addr
                else:
                    line = self.Adjust(line)
                    tokens = self.TokenizeLine(line)
                    #print(tokens)
                    curr_address = int(tokens[1], 16)
                    if prev_address!=-1 and curr_address > (prev_address+self.record_limit) and overflow_flag==False:
                        overflow_flag = True
                        curr_record += ''.join(['X']*(self.record_limit-len(curr_record)))
                        self.Displayrecs(fpout, rec_addr, curr_record)
                        rec_addr = curr_address - curr_address%16 + self.prog_addr
                        curr_record = ''.join(['X']*2*(curr_address%16)) 
                    curr_obcodes = ''.join(tokens[4:])
                    for id in range(0, len(curr_obcodes), 2):
                        curr_byte = curr_obcodes[id:id+2]
                        curr_record += curr_byte
                        if len(curr_record) == self.record_limit:
                            self.Displayrecs(fpout, rec_addr, curr_record)
                            rec_addr += self.record_limit/2
                            curr_record = ''
                    if overflow_flag:
                        overflow_flag = False    
                    prev_address = curr_address
                line = fpin.readline()
                tokens = self.TokenizeLine(line)
            while len(curr_record) < self.record_limit:
                curr_record += 'X'
            self.Displayrecs(fpout, rec_addr, curr_record)
#fn = raw_input("Enter file name: ")
st_add=0
if len(sys.argv) > 1:
    st_add = int(sys.argv[1])
rel = RelocationLoader('Intermediate_Files/assembled_reloc.obj', st_add)#, int('4000', 16))
rel.Driver()