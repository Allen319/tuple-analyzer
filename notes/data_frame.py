from ROOT import RDataFrame

class DataFrame(RDataFrame):
    def __init__(self, yaml_node):
        super(DataFrame, self).__init__(yaml_node.treename, yaml_node.filename)
        if yaml_node.filename is not None and yaml_node.treename is not None:
            self.node = yaml_node
        else:
            raise IOError
    #def __del__(self):
        #print("test")

    def getEventNumByNode(self, cutname):
        if not cutname in self.node.getSelection():
            raise NameError
        return self.Filter(self.node.getCut(cutname)).Count().GetValue()

    def getHistoByNode1D(self, cutname, obs, histoname = ""):
        if histoname == "" :
            histoname = obs + "_" + cutname
        if not obs in self.node.getObs():
            raise NameError
        return self.Filter(self.node.getCut(cutname)).Histo1D((histoname, histoname, len(self.node.getBinning(obs)) - 1, self.node.getBinning(obs)), obs)

    def getEventNumByCut(self, cutclass):
        cut_list = cutclass.name.split("__")
        for cut in cut_list:
            if not cut == "":
                if not cut in self.node.getSelection():
                    raise NameError
        return self.Filter(cutclass.cut).Count().GetValue()

    def getHistoByCut1D(self, cutclass, obs, histoname = ""):
        cut_list = cutclass.name.split("__")
        for cut in cut_list:
            if not cut == "":
                if not cut in self.node.getSelection():
                    raise NameError
        if histoname == "" :
            histoname = obs + "_" + cutclass.name
        if not obs in self.node.getObs():
            raise NameError
        return self.Filter(cutclass.cut).Histo1D((histoname, histoname, len(self.node.getBinning(obs)) - 1, self.node.getBinning(obs)), obs)
