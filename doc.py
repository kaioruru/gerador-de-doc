import sys
import inspect
import importlib
import os
from typing import List
import types

class DocGenerator:

    def __init__(self, ignore_files: list, ignore_folders: list):
        ignore_files.append(os.path.basename(__file__))
        self.ignore_files = ignore_files
        self.ignore_folders = ignore_folders
        self.base_path = os.getcwd()
        self.documentation_file = "project documentation"

    def __browse_folder(self, base_folder: List[str]):
        list_folder = list()
        for dir in base_folder:
            if dir not in self.ignore_folders and dir not in self.ignore_files:
                if os.path.isfile(os.path.join(os.getcwd(), dir)):
                    if dir.endswith('.py'):
                        self.__get_doc_str(path=os.path.join(
                            os.getcwd(), dir), name=dir)
                    else:
                        self.__normal_file(path=os.path.join(
                            os.getcwd(), dir), name=dir)
                else:
                    list_folder.append(dir)
    def __normal_file(self,path:str, name:str):
        print("-="*4+name+"-="*4+"\n")
        with open(path,'r') as arq:
            print(arq.read())
    def __get_doc_str(self, path: str, name: str):

        sys.path.append(path)
        modulo = importlib.import_module(name.replace(".py", ""))
        print("-="*4+modulo.__name__+"-="*4+"\n")
        print(" "*4+"__dict__:\n" +
                    modulo.__doc__ if modulo.__doc__ else "")
        for mame, obj in inspect.getmembers(modulo, inspect.isfunction):
            if obj.__module__ == modulo.__name__:
                if isinstance(obj, types.FunctionType):
                    print(" "*4+f"função: {obj.__name__}")
                    print(" "*4+"__dict__:\n" +
                                obj.__doc__ if obj.__doc__ else "")

                else:
                    self.class_doc(obj)
        print("\n"*4)

    def class_doc(self, obj):
        print(f"classe: {obj.__name__}\n")
        print(" "*4+"__dict__:\n"+obj.__doc__)
        for method_mame, method_obj in inspect.getmembers(obj, inspect.isfunction):
            print(""*8 +
                  f"função: {method_obj.__name__}\n")
            print(" "*12+"__dict__:\n" +
                  obj.__doc__ if obj.__doc__ else "")

    def browse_folder(self):
        first_run = self.__browse_folder(os.listdir())
        if first_run:
            for _ in first_run:
                self.__browse_folder(os.listdir(os.path.join(os.getcwd(), _)))

    def __call__(self):
        self.browse_folder()


if __name__ == '__main__':
    doc_generator = DocGenerator(
        ignore_files=['test.py', '.env', 'power_bi.py', 'ver_email.py','log.log'], ignore_folders=['venv', '__pycache__', '.git'])
    doc_generator()
