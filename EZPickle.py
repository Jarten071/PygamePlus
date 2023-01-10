from pickle import dump as pkd
from pickle import load as pkl

for i in range(1):
    def save(value, file):
        try:    
            with open(file, "wb") as filename:
                pkd(value, filename)    
        except FileNotFoundError:
            file = open(file, "x")
            pkd(value, file)
    def load(file):
        try:
            with open(file, "rb") as filename:
                value = pkl(filename)
            return value
        except FileNotFoundError:
            print("Failed to load data: No file currently present. Creating a new one...")
            open(file, "x")
            with open(file, "wb") as filename:
                pkd(False, filename)
            return False
        except EOFError:
            print("File data error, resetting propereties to default...")
            open(file, "w")
            with open(file, "wb") as filename:
                pkd(False, filename)
            return False
    