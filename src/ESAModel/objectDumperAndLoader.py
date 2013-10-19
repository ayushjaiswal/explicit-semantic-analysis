import pickle

class ObjectDumperAndLoader:
    """Dumps/loads the object to/from a file"""
    def __init__(self):
        pass
        
    def dump(self, Object, destinationPath, fileName):

        with open(destinationPath + fileName, 'wb') as outputFile:
            pickle.dump(Object, outputFile)

    def load(self, srcPath, fileName):
        
        with open(srcPath + fileName, 'rb') as inputFile:
            Obj = pickle.load(inputFile)
        return Obj
