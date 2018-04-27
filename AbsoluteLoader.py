'''
Absolute loader program
-----------------
Structure of object program:
Header record: H^program name(8 bytes)^start address(8 bytes)^length(8 bytes)
Text record/s: T^start address(8 bytes)^length(2 bytes)^object code(x bytes)^ .. 
End record: E^start address(8 bytes)
Load into specified start address
'''
def Check_available(start_addr, length):
    for st,end in avail_mems:
        if(start_addr>=st and start_addr+length<=end):
            return True
    return False
avail_mems = [[1234, 2496],[4096, 8314],[7086, 15926]]                           #List of free memory blocks (start,end)
class Absloader:
    def __init__(self, ip_file):
        self.ip_file = ip_file
        self.op_file = 'absolute_load.txt'
        self.record_limit = 32
        self.field_limit = 8
    def TokenizeLine(self, curr_line):
        line_tokens = curr_line.strip().split('^')
        return line_tokens
    def Displayrecs(self, fpout, rec_addr, curr_record):
        fpout.write(hex(rec_addr)[2:]+'\t')
        for id in range(0, len(curr_record), self.field_limit):
            curr_field = curr_record[id:id+self.field_limit] 
            fpout.write(curr_field+' ')
        fpout.write('\n')
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
                        print("Error: Memory unavailable")
                        return
                    fpout = open(self.op_file, "w")
                    rec_addr = self.start_address
                else:
                    curr_address = int(tokens[1], 16)
                    if prev_address!=-1 and curr_address > (prev_address+self.record_limit) and overflow_flag==False:
                        overflow_flag = True
                        curr_record += ''.join(['X']*(self.record_limit-len(curr_record)))
                        self.Displayrecs(fpout, rec_addr, curr_record)
                        rec_addr = curr_address - curr_address%16
                        curr_record = ''.join(['X']*2*(curr_address%16)) 
                    curr_obcodes = ''.join(tokens[3:])
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
ab = Absloader('Intermediate_Files/assembled.obj')
ab.Driver()