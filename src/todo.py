#!/usr/local/bin/python3
import os
import argparse

todoDir="/Users/steinbeck/Dropbox/Documents/Projects"
exclDirs= list()
exclDirs.append("ZZ-COMPLETED")
exclDirs.append("ZZ-WAITINGFOR")
exclDirs.append("ZZ-SOMEDAYMAYBE")
exclDirs.append("Materials")

projects = {}
projectList = list()

class Project:
    
    def __init__(self, name):
        self.name = name
        self.tasks = list()

    def addTask(self, task):
        self.tasks.append(task)

    def getTasks(self):
        return self.tasks    


def scanProjectDirs(todoDir):

    for dirname, dirnames, filenames in os.walk(todoDir):
        # Advanced usage:
        # editing the 'dirnames' list will stop os.walk() from recursing into there.
        for exclDir in exclDirs:
            if exclDir in dirnames:
                # don't go into any of those directories.
                dirnames.remove(exclDir)
                
        # Put all directory names in todo_dir in a dictionary as hash keys
        # Add full pathes as values 
        for subdirname in dirnames:
            projects[subdirname] = os.path.join(dirname, subdirname)
    
def assembleProjectsTasks(projects):
    for key in projects:
        #print(key, projects[key])
        project = Project(key)
        for dirname, dirnames, filenames in os.walk(projects[key]):
            #print(len(filenames))
            for filename in filenames:            
                if filename == "TODO":
                    fqfilename=os.path.join(projects[key], filename)
                    with open(fqfilename, 'r') as fin:
                        line = fin.readline()
                        while line:
                            line = fin.readline()
                            line = line.strip()
                            if line != "":
                                project.addTask(line)
                        fin.close()
    
        projectList.append(project)
    
def printTaskList(projects, mailsubject):
    if mailsubject: print("subject: TODO for Chris")
    for project in projectList:
        tasks = project.getTasks()
        if len(tasks) > 0:
            print("*" + project.name + "*")
            for task in tasks:
                print(task)
            print()

def printProjectList(projects, mailsubject):
    if mailsubject: print("subject: Project list for Chris")
    for project in projectList:
        print("*" + project.name + "*")

def main():
    parser = argparse.ArgumentParser(description='Report various TODO list aspects')
    parser.add_argument('-t', '--tasks', action='store_true', help='list all tasks')
    parser.add_argument('-p', '--projects', action='store_true', help='list all projects, including empty ones')
    parser.add_argument('-m', '--mailsubject', action='store_true', help='Add a mail subject line')
    
    args = parser.parse_args()
    if args.mailsubject == 'none': 
            args.mailsubject == False
    
    scanProjectDirs(todoDir)
    assembleProjectsTasks(projects)
    if args.tasks:
        printTaskList(projects, args.mailsubject)
        
    if args.projects:
        printProjectList(projects, args.mailsubject)
    
main()



    



    