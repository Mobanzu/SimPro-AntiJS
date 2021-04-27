class MySplit(object):
    data_array = []
    datalist = []
    def __init__(self, logic, datalist):
        self.datalist = datalist
        self.logic = logic
    def parse(self):
        logics = self.parse_coma(self.logic)
        theresult = []
        for logic in logics:
            if ">" in logic:
                res01 = self.do_logic(logic)
                self.util_append(res01, theresult)
            elif "<" in logic:
                res02 = self.do_logic(logic)
                self.util_append(res02, theresult)
            elif "-" in logic:
                res03 = self.do_range(logic)
                self.util_append(res03, theresult)
            else:
                res04 = self.do_append(logic)
                self.util_append(res04, theresult)
        last_step = self.util_filter_doubled(theresult)
        last_step.sort()
        return last_step
    def util_filter_doubled(self, nestlists):
        dmp = []
        for reslist in nestlists:
            for item in reslist:
                if item not in dmp:
                    dmp.append(item)
                else:
                    pass
        return dmp
    def util_append(self, data, thelist):
        if data != None:
            thelist.append(data)
    def do_append(self, logic):
        try:
            number = int(logic)
            if number in self.datalist:
                return [number]
            else: return None
        except:
            return None
    def do_logic(self, logic):
        dmp = []
        for d in self.datalist:
            state = eval("{0}{1}".format(d,logic))
            if state:
                dmp.append(d)
        return dmp
    def do_range(self, logic):
        rangedata = self.parse_minus(logic)
        if len(rangedata) == 1:
            return None
        elif len(rangedata) == 2:
            the_min = min( (int(rangedata[0])) , (int(rangedata[1])) )
            the_max = max( (int(rangedata[0])) , (int(rangedata[1])) )
            listrange = range(the_min, the_max+1)
            dmp = []
            for iter in self.datalist:
                if iter in set(listrange):
                    dmp.append(iter)
            return dmp
        elif len(rangedata) >= 3:
            return None
    def parse_minus(self,logic):
        logic = logic.split('-')
        return logic
    def parse_coma(self, logic):
        dat = logic.split(',')
        dmp = []
        for item in dat:
            if item != '':
                dmp.append(item)
        return dmp