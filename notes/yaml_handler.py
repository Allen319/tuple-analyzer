import os
import yaml
import numpy

class Handler:
    def __init__(self, fpath):
        if os.path.isfile(fpath) and os.path.getsize(fpath) > 0:
            tmpFile = open(fpath)
            self.node = yaml.load(tmpFile, Loader=yaml.FullLoader)
        else:
            self.node = None
        if self.node is not None:

            if "filename" in self.node:
                self.filename = self.node["filename"]
                print("loading config filename:" + self.filename)
            else:
                self.filename = None
                print("ATTENTION : No filename specified in config.")

            if "treename" in self.node:
                self.treename = self.node["treename"]
                print("loading config treename:" + self.treename)
            else:
                self.treename = None
                print("ATTENTION : No treename specified in config.")

            if "binning" in self.node:
                self.binning = self.node["binning"]
            else:
                self.binning = None
            
            if "category" in self.node:
                self.category = self.node["category"]
            else:
                self.category = None

            if "selection" in self.node:
                self.selection = self.node["selection"]
            else:
                self.selection = None

    def getNode(self):
        if self.node is not None:
            return self.node

    def getNodeList(self):
        if self.node is not None:
            return list(self.node.keys())

    def getObs(self):
        if self.node is not None and self.binning is not None:
            return list(self.binning.keys())
        else:
            return None

    def getBinning(self, obs):        
        if self.node is not None and self.binning is not None:
            return numpy.array(self.binning[obs], dtype = float)
        else:
            return None

    def getCategory(self):
        if self.node is not None and self.category is not None:
            return list(self.category.keys())
        else:
            return None

    def getSelection(self):
        if self.node is not None and self.selection is not None:
            return list(self.selection.keys())
        else:
            return None

    def getCut(self, cutname):
        if self.node is not None and self.selection is not None:
            return self.selection[cutname]
        else:
            return None
