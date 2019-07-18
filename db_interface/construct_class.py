class ClassBuild:
    def __init__(self, class_name, values, *inherits):
        self.name = class_name
        self.values = values
        self.inherits = inherits
    
    def build_inheritance(self):
        inherit_values = ()
        for inherit in self.inherits:
            inherit_values += (inherit,)
        return inherit_values

    def build_class(self):
        self.values["__tablename__"] = self.name
        print(self.values)
        return type(self.name, self.build_inheritance(), self.values)
