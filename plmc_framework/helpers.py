import os

from plmc_framework.settings import settings

def get_attribute_names(Class: type) -> list:
    """
        Returns the names of the attributes of the given class (excluding special attributes).
    """

    return [key for key in Class.__dict__ if key[0:2] != "__"]

def merge_dictionary_into_string_list(dictionary: dict) -> list:
    """
        Merges given dictionary keys and values, such that for each key and value, string "key=value" exists in the list
    """
    return [f"{key}={dictionary[key]}" for key in dictionary]

def get_absolute_path_of_frontend_file(relativePath: str):
    """
        Returns the absolute path of given path relative to public_html directory. 
    """

    return os.path.join(settings.PUBLIC_HTML_ABSOLUTE_PATH, relativePath)