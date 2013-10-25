import sys
import os
sys.path.insert(0, os.path.abspath(".."))
from cloud.serialization.cloudpickle import dumps
from pickle import load

class ObjectDumperAndLoader:
    """Dumps/loads the object to/from a file."""

    def __init__(self):
        pass
        
    def dump(self, Object, destinationPath, fileName):
        """Dumps the object at a specified location."""
        
        with open(destinationPath + fileName, 'wb') as outputFile:
            outputFile.write(dumps(Object))

    def load(self, srcPath, fileName):
        """Load and return the object from source file."""
        
        Obj = None
        with open(srcPath + fileName, 'rb') as inputFile:
            Obj = load(inputFile)
        return Obj