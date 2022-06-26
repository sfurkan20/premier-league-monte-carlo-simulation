import plmc_framework.db.sqlite_orm

class Model:
    def __init__(self, **kwargs):
        """
            Constructor of the class.
            If id is given, allows the model to bind to a database entry with the corresponding primary key. Consequent load and save calls will use this, and must be specified to use.
        """
        self.__dict__.update(kwargs)  # Assigns given kwargs arguments to corresponding attributes

    @classmethod
    def getAll(cls):
        modelList = []
        id = 1
        while True:
            model = plmc_framework.db.sqlite_orm.SQLiteORM.selectModel(cls, id=id)
            id += 1

            if type(model) == NullModel:
                break

            modelList.append(model)
        
        return modelList

    def load(self):
        """
            Loads the database entry corresponding to the primary key into the attributes.
        """

        newTempModel = plmc_framework.db.sqlite_orm.SQLiteORM.selectModel(type(self), id=self.id)
        self.__dict__.update(newTempModel.__dict__)  # If newModel is an instance of 'NullModel' class (i.e. has no database entry representation), this instance will also be no longer usable, since '-1' will be copied as ID.

    def save(self):
        """
            Updates the database entry corresponding to the primary key, if primary key does not exist, makes an insertion instead.
        """

        modelExists = plmc_framework.db.sqlite_orm.SQLiteORM.modelExists(type(self), id=self.id)
        if modelExists:
            plmc_framework.db.sqlite_orm.SQLiteORM.updateModel(type(self), self.__dict__, id=self.id)
        else:
            self.__dict__.pop('id')
            insertedTempModel = plmc_framework.db.sqlite_orm.SQLiteORM.insertModel(type(self), self.__dict__)
            self.__dict__.update(insertedTempModel.__dict__)

class NullModel(Model):
    """
        Dummy class to handle models that are null, instead of traditional Python 'None' values.
    """

    def __init__(self):
        self.id = -1

    def load(self):
        pass

    def save(self):
        pass