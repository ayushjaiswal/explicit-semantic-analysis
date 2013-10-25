import config
from ESAModel.objectDumperAndLoader import ObjectDumperAndLoader
import ESA_util

class Runner:
    """Creates a platform for running an ESA-based application program, and then runs it."""

    def __init__(self, ESADumpPath, ESADumpFileName, ApplicationRunner):
        loader = ObjectDumperAndLoader()
        self.__ESADump = loader.load(ESADumpPath, ESADumpFileName)
        self.__app = ApplicationRunner(self.__ESADump)

    def run(self):
        """Runs the application."""

        print "Application started!"
        shouldExit = 'n'
        while shouldExit != 'y':
            self.__app.run()
            shouldExit = raw_input("Exit? <y/n>: ")
        print "Bye!"

def main():
    runnerObj = Runner(config.ESADumpPath, config.ESADumpFileName, config.ApplicationRunner)
    runnerObj.run()

if __name__ == '__main__':
    main()