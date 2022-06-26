import sqlite3

import plmc_framework.architecture.model
from plmc_framework.settings import settings
from plmc_framework.helpers import get_attribute_names, merge_dictionary_into_string_list

class SQLiteORM:
    """
        Performs CRUD operations by converting model-related inputs to SQL queries.
    """

    _SQLITE_CONNECTION = sqlite3.connect(settings.DB_ABSOLUTE_PATH)
    _SQLITE_CURSOR = _SQLITE_CONNECTION.cursor()

    def precheckORMMethod(function):
        """
            Decorator that checks whether invalid inputs are given to an ORM method.
        """

        def innerFunction(modelClass, **kwargs):
            if len(kwargs) == 0:
                raise Exception("No attribute is given to select according to.")

            if modelClass.__base__ is not plmc_framework.architecture.model.Model:
                raise Exception("Given type does not inherit from Model class.")

            return function(modelClass, **kwargs)
        
        return innerFunction

    @staticmethod
    @precheckORMMethod
    def modelExists(modelClass: type, **kwargs):
        """ 
            Checks if the model from given class and attributes exists in the database.
            modelClass: Class to determine the query's table.
            kwargs: Condition attributes of the model.

            Returns:
            True if exists, False if not.
        """

        mergedKwargs = merge_dictionary_into_string_list(kwargs)
        query = f"SELECT COUNT(*) FROM {modelClass.__name__} WHERE {' AND '.join(mergedKwargs)}"
        entryCount = SQLiteORM._SQLITE_CURSOR.execute(query).fetchone()
        return entryCount[0] >= 1

    @staticmethod
    @precheckORMMethod
    def selectModel(modelClass: type, **kwargs):
        """ 
            Selects and returns the model from given class and attributes.
            modelClass: Class to determine the query's table.
            kwargs: Condition attributes of the model.

            Returns:
            Selected 'Model' class instance.
        """

        mergedKwargs = merge_dictionary_into_string_list(kwargs)
        modelClassAttributes = get_attribute_names(modelClass)
        query = f"SELECT {','.join(modelClassAttributes)} FROM {modelClass.__name__} WHERE {' AND '.join(mergedKwargs)}"

        entryData = SQLiteORM._SQLITE_CURSOR.execute(query).fetchone()  # Tuple consisting of the data
        if entryData == None:
            return plmc_framework.architecture.model.NullModel()

        attributeDict = {key: entryData[index]    for index, key in enumerate(modelClassAttributes)}
        return modelClass(**attributeDict)

    @staticmethod
    @precheckORMMethod
    def insertModel(modelClass: type, **kwargs):
        """ 
            Inserts and returns a model into given modelClass (table) and using the attributes.
            modelClass: Class to determine the query's table.
            kwargs: Attributes of the entry.

            Returns:
            Inserted 'Model' class instance.
        """

        query = f"""INSERT INTO {modelClass.__name__} ({','.join(kwargs.keys())}) VALUES ({','.join(kwargs.values)});
                    SELECT SCOPE_IDENTITY();
                 """
        modelID = SQLiteORM._SQLITE_CURSOR.execute(query).fetchone()
        SQLiteORM._SQLITE_CONNECTION.commit()
        return modelClass(id=modelID, **kwargs)

    @staticmethod
    @precheckORMMethod
    def updateModel(modelClass: type, newValues: dict, **kwargs):
        """ 
            Updates and returns the model into given modelClass (table) and with the use of the attributes.
            modelClass: Class to determine the query's table.
            newValues: New attributes of the model.
            kwargs: Condition attributes of the model.

            Returns:
            Updated 'Model' class instance.
        """

        mergedNewValues = merge_dictionary_into_string_list(newValues)
        mergedKwargs = merge_dictionary_into_string_list(kwargs)
        query = f"""UPDATE {modelClass.__name__} SET {','.join(mergedNewValues)} WHERE {' AND '.join(mergedKwargs)};
                    SELECT changes();
                 """

        changesCount = SQLiteORM._SQLITE_CURSOR.execute(query).fetchone()
        if changesCount == 0:
            return plmc_framework.architecture.model.NullModel()

        SQLiteORM._SQLITE_CONNECTION.commit()
        return modelClass(**newValues)

    @staticmethod
    @precheckORMMethod
    def removeModel(modelClass: type, **kwargs):
        """ 
            Removes the model from given modelClass (table).
            modelClass: Class to determine the query's table.
            kwargs: Condition attributes of the model.
        """

        mergedKwargs = merge_dictionary_into_string_list(kwargs)
        query = f"DELETE FROM {modelClass.__name__} WHERE {' AND '.join(mergedKwargs)}"
        SQLiteORM._SQLITE_CURSOR.execute(query)
        SQLiteORM._SQLITE_CONNECTION.commit()