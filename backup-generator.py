#backup-generator.py

import sys
import shutil
from ConfigParser import RawConfigParser
from os.path import expanduser, join, exists, isdir
from os import listdir, mkdir
import time
import tempfile
import logging

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M',
                    filename='.myapp.log',
                    filemode='w')

console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
console.setFormatter(formatter)

logger = logging.getLogger("backup-generator")


SOURCE_DIRs = "SOURCE DIRECTORIES"
SOURCE_FILEs = "SOURCE FILES"
TARGET_DIRs = "TARGET DIRECTORY"
BACKUP_DATE = time.strftime("%d-%m-%y-%H-%M-%S")
TEMP_FOLDER_PATH = join(tempfile.gettempdir(), "backup-" + BACKUP_DATE)

#Vladimir Ignatyev's solution for dynamic prompt
def printProgress (iteration, total, prefix = '', suffix = '', decimals = 2, barLength = 100):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : number of decimals in percent complete (Int)
        barLength   - Optional  : character length of bar (Int)
    """
    filledLength    = int(round(barLength * iteration / float(total)))
    percents        = round(100.00 * (iteration / float(total)), decimals)
    bar             = '#' * filledLength + '-' * (barLength - filledLength)
    sys.stdout.write('\r%s |%s| %s%s %s' % (prefix, bar, percents, '%', suffix)),
    sys.stdout.flush()
    if iteration == total:
        sys.stdout.write('\n')
        sys.stdout.flush()


class ParseConfigure:

    def __init__(self):
        self.configFile = open("config.ini", "r")
        self.config = RawConfigParser()
        self.config.read("config.ini")
        logger.debug('<config.ini> readed successfully.')

    def setDefault(self):
        #TODO:
        #   Set default if there's no default target directories in config.ini
        pass

    def parseSourceDirs(self):
        for item in self.config.items(SOURCE_DIRs):
            yield (item[0], item[1])

    def parseSourceFiles(self):
        for item in self.config.items(SOURCE_FILEs):
            yield (item[0],item[1])

    def parseTargetDir(self):
        for item in self.config.items(TARGET_DIRs):
            return item[1]



class FileOperations:

    config = ParseConfigure()

    def __init__(self):
        if exists(self.config.parseTargetDir()) is True and isdir(self.config.parseTargetDir()) is True:
            pass
        else: mkdir(self.config.parseTargetDir())

    def copyFiles2Temp(self):
        i = 0
        if exists(TEMP_FOLDER_PATH) is True and isdir(TEMP_FOLDER_PATH) is True:
            pass

        else:
            mkdir(TEMP_FOLDER_PATH)
            logger.debug("TEMP folder created at %s"%TEMP_FOLDER_PATH)

        for tag, path in self.config.parseSourceDirs():
            if not exists( join(TEMP_FOLDER_PATH, tag) ):
                mkdir( join(TEMP_FOLDER_PATH, tag) )


            for source in listdir(path):
                progressLength = len(listdir(path))
                if isdir(join(path,source)):
                    shutil.copytree(join(path,source), join(TEMP_FOLDER_PATH, tag, source) )
                    i = i + 1
                    printProgress(i, progressLength)
                else:
                    shutil.copyfile(join(path,source), join(TEMP_FOLDER_PATH, tag, source) )
                    i = i + 1
                    printProgress(i, progressLength)


        for tag, source in self.config.parseSourceFiles():
            shutil.copyfile(source, join(TEMP_FOLDER_PATH, tag) )

    def compressBackupDir(self):
        shutil.make_archive(TEMP_FOLDER_PATH, "zip", TEMP_FOLDER_PATH)

    def copyZip2Target(self):
        shutil.copy(TEMP_FOLDER_PATH + ".zip", self.config.parseTargetDir() )

    def removeBackupInTemp(self):
        shutil.rmtree(TEMP_FOLDER_PATH)


class BackupGenerator:

    @staticmethod
    def execute():
        fileOP = FileOperations()
        fileOP.copyFiles2Temp()
        fileOP.compressBackupDir()
        fileOP.copyZip2Target()
        fileOP.removeBackupInTemp()


if __name__ == "__main__":
    BackupGenerator.execute()
