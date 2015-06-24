#backup-generator.py

import sys
import shutil
from ConfigParser import RawConfigParser
from os.path import expanduser, join, exists, isdir
from os import listdir, mkdir
import time
import tempfile


SOURCE_DIRs = "SOURCE DIRECTORIES"
SOURCE_FILEs = "SOURCE FILES"
TARGET_DIRs = "TARGET DIRECTORY"
BACKUP_DATE = time.strftime("%d-%m-%y-%H-%M-%S")
TEMP_FOLDER_PATH = join(tempfile.gettempdir(), "backup-" + BACKUP_DATE)

class ParseConfigure:
    
    def __init__(self):
        self.configFile = open("config.ini", "r")
        self.config = RawConfigParser()
        self.config.read("config.ini")
        
    def setDefault(self):
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
        
        if exists(TEMP_FOLDER_PATH) is True and isdir(TEMP_FOLDER_PATH) is True:
            pass
        
        else: 
            mkdir(TEMP_FOLDER_PATH)
        
        for tag, path in self.config.parseSourceDirs():
            print tag
            
            if not exists( join(TEMP_FOLDER_PATH, tag) ):
                mkdir( join(TEMP_FOLDER_PATH, tag) )
    
    
            for source in listdir(path):
                print tag, source
                if isdir(join(path,source)):
                    shutil.copytree(join(path,source), join(TEMP_FOLDER_PATH, tag,source) )
                else:
                    shutil.copyfile(join(path,source), join(TEMP_FOLDER_PATH, tag, source) )
            
        for tag, source in self.config.parseSourceFiles():
            shutil.copyfile(source, join(TEMP_FOLDER_PATH, tag) )
            
    def compressBackupDir(self):
        shutil.make_archive(TEMP_FOLDER_PATH, "zip", TEMP_FOLDER_PATH)
        
    def copyZip2Target(self):
        shutil.copy(TEMP_FOLDER_PATH + ".zip", self.config.parseTargetDir() )
        
    def removeBackupInTemp(self):
        shutil.rmtree(TEMP_FOLDER_PATH)
        
        
class Main:
    def __init__(self):
        self.fileOP = FileOperations()
        
    def execute(self):
        self.fileOP.copyFiles2Temp()
        self.fileOP.compressBackupDir()
        self.fileOP.copyZip2Target()
        self.fileOP.removeBackupInTemp()
        
        
if __name__ == "__main__":
    BackupGenerator = Main()
    BackupGenerator.execute()