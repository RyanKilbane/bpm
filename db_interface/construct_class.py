from sqlalchemy import Column, String

class ClassBuild:
    def __init__(self, class_name, values, column_def, *inherits):
        self.name = class_name
        self.values = values
        self.inherits = inherits
        self.cols = column_def
    
    def build_inheritance(self):
        inherit_values = ()
        for inherit in self.inherits:
            inherit_values += (inherit,)
        return inherit_values

    def build_orm_cols(self):
        built_orm_cols = {"__tablename__": self.name}
        for col in self.cols:
            if col["primary_key"] == 1:
                built_orm_cols[col["name"]] = Column(String, primary_key=True)
            else:
                built_orm_cols[col["name"]] = Column(String)
        print(built_orm_cols)
        return built_orm_cols

    def build_class(self):
        return type(self.name, self.build_inheritance(), self.build_orm_cols())
