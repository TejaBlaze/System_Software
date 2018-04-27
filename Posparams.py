class Posparams:
    def __init__(self):
        pass
    def Convert(self, mbody, mheader=''):
        self.pos_params = {}
        self.num_params = 0
        if mheader=='':
            mheader = mbody[:mbody.find('\n')]
        params = []
        curr_param = ''
        flag=0
        for ele in mheader:
            if flag==0 and ele =='&':
                curr_param+=ele
                flag=1
            elif flag==1 and ele==',' and ele!=' ':
                params.append(curr_param)
                curr_param=''
                flag=0
            elif flag==1:
                curr_param+=ele
        if flag==1:
            params.append(curr_param)
        for i,pm in enumerate(params):
            self.pos_params[pm] = self.num_params+ i
        curr_len = len(params)
        for i in range(len(params)):
            mbody = mbody.replace(params[i], '?'+str(self.pos_params[params[i]]))
        self.num_params += curr_len
        return mbody

    def Convert_new(self, mbody, mheader=''):
        if mheader!='':
            operands = mheader.strip().split(' ')[-1] 
            self.curr_params = operands.split(',')
        else:
            for i in range(len(self.curr_params)):
                mbody = mbody.replace(self.curr_params[i], '?'+str(i))    
        return mbody