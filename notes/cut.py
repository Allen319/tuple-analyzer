class Cut:
    def __init__(self, n = "", base_cut = ""):
        self.name = n
        self.cut = base_cut

    def __or__(self, other):
        cut = ""
        name = ""
        if other.cut == "":
            cut = self.cut
        elif self.cut == "":
            cut = other.cut
        else:
            cut = "( " + self.cut + " || " + other.cut + " )"
        if other.name == "":
            name = self.name
        elif self.name == "":
            name = other.name
        else:
            name = self.name + "__" + other.name
        return self.__class__(name, cut)

    def __mul__(self, other):
        cut = ""
        name = ""
        if other.cut == "":
            cut = self.cut
        elif self.cut == "":
            cut = other.cut
        else:
            cut = "( " + self.cut + " && " + other.cut + " )"
        if other.name == "":
            name = self.name
        elif self.name == "":
            name = other.name
        else:
            name = self.name + "__" + other.name
        return self.__class__(name, cut)

    def __repr__(self):
        if self.cut == "":
            return "<" + self.name + ">:None"
        else:
            return "<" + self.name + ">:" + self.cut
