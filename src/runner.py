import sys
import csv
import config
from ESAModel.objectDumperAndLoader import ObjectDumperAndLoader
import ESA_util

class Runner:
    """Creates a platform for running an ESA-based application program, and then runs it."""

    def __init__(self, ESADumpPath, ESADumpFileName, ApplicationRunner, ApplicationName):
        loader = ObjectDumperAndLoader()
        self.__ESADump = loader.load(ESADumpPath, ESADumpFileName)
        self.__app = ApplicationRunner(self.__ESADump)
        self.__appName = ApplicationName

    def run(self):
        """Runs the application."""

        print self.__appName, "started!"
        shouldExit = 'n'
        while shouldExit != 'y':
            self.__app.run()
            shouldExit = raw_input("Exit? <y/n>: ")
        print "Bye!"

    def runBatch(self, pairs):
        """Runs the application in batch mode."""

        print self.__appName, "started!"
        print "Word pairs read."
        print "Calculating semantic relatedness scores..."
        scores = self.__app.runBatch(pairs)
        print "Calculation complete."
        return scores

def batch():
    runnerObj = Runner(config.ESADumpPath, config.ESADumpFileName, config.ApplicationRunner, config.ApplicationName)
    pairs = []
    with open(config.BatchDataFile) as fIn:
        contents = csv.reader(fIn)
        first = True
        for row in contents:
            if first:
                first = False
            else:
                pairs.append((row[config.Word1Index], row[config.Word2Index]))
    scores = runnerObj.runBatch(pairs)
    with open(config.BatchResultsDumpFile, 'w') as fOut:
        for score in scores:
            fOut.write(str(score) + '\n')
    print "Results saved to", config.BatchResultsDumpFile

if __name__ == '__main__':
    print "Loading..."
    runnerObj = Runner(config.ESADumpPath, config.ESADumpFileName, config.ApplicationRunner, config.ApplicationName)
    print "Done"
    if len(sys.argv) > 1 and sys.argv[1] == 'batch':
        batch()
    else:
        runnerObj.run()