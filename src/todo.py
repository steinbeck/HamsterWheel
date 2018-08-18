#!/usr/local/bin/python3
import os
import argparse
import sys


exclDirs= list()

#
# Adjust these variables to fit your needs or preferences 
#
todoDir="/Users/steinbeck/Dropbox/Documents/Projects"   # the topmost directory where your projects reside
rootProjectName="Christoph's projects"  # The name of the entirety of your projects. Your topmost superproject, if you wish. Holds all other projects.
subjectLineTaskList = "Task list for Christoph" # If you mail this list to yourself, this will be the subject line. 
subjectLineProjectList = "Project list for Christoph" # If you mail this list to yourself, this will be the subject line. 
indentAtom = "    " # names of subproject are indented by multiples of indentAtom in the project list 

exclDirs.append("ZZ-COMPLETED") # The directory where you move completed projects. Will not be traversed for active projects and tasks
exclDirs.append("ZZ-WAITINGFOR") # The directory where you move projects that you are waiting for. Will not be traversed for active projects and tasks
exclDirs.append("ZZ-SOMEDAYMAYBE") #  The directory where you move projects that you will not work on in the foreseeable future. Will not be traversed for active projects and tasks
exclDirs.append("Materials") # The directory in each project where you keep supporting materials (documents, etc) for a project.  # The directory where you move projects that you are waiting for. Will not be traversed for active projects and tasks

projects = {}
projectList = list()

class Project:
    
    def __init__(self, name, path):
        self.name = name
        self.path = path
        self.tasks = list()
        self.projects = list()

    def addTask(self, task):
        self.tasks.append(task)

    def getTasks(self):
        return self.tasks    

    def setPath(self, path):
        self.path = path

    def getPath(self):
        return self.path

    def addProject(self, project):
        self.projects.append(project)

    def getProjects(self):
        return self.projects    


def scanProjectDirs(project):
    projectDir = project.getPath()
    for root, dirs, files in os.walk(projectDir):
        #editing the 'dirnames' list will stop os.walk() from recursing into there.
        for exclDir in exclDirs:
            if exclDir in dirs:
                # don't go into any of those directories.
                dirs.remove(exclDir)
                
        level = root.replace(projectDir, '').count(os.sep)
        #print('listing ' + str(len(dirs)) + ' dirs')
        for dir in dirs:
            newproject = Project(dir, root + os.sep + dir)
            project.addProject(newproject)
            scanProjectDirs(newproject)            
        #print('done')
        break
   
    
def assembleProjectsTasks(project):
    for subproject in project.projects:
        for dirname, dirnames, filenames in os.walk(subproject.path):
            for filename in filenames:            
                if filename == "TODO":
                    fqfilename=os.path.join(subproject.path, filename)
                    #print(fqfilename)
                    with open(fqfilename, 'r') as fin:
                        line = fin.readline()
                        while line:
                            line = line.strip()
                            if line != "":
                                subproject.addTask(line)
                                #print("Adding task " + line)
                            line = fin.readline()
                        fin.close()
            break
        assembleProjectsTasks(subproject)


def printProjectList(project, mailsubject, printTasks):
    if mailsubject:
        if printTasks: print("subject: " +  subjectLineTaskList)
        else: print("subject: " +  subjectLineProjectList)
    
    for subproject in project.getProjects():
        printProject(subproject, 0, printTasks)
        
def printProject(project, indent, printTasks):
    indentString = indentAtom * indent
    tasks = project.getTasks()
    if (printTasks and len(tasks) > 0) or not printTasks:
        print(indentString + "*" + project.name + "*")
    else: 
        return
    if printTasks:
        if len(tasks) > 0:  
            indentString = indentAtom * (indent + 1 )
            for task in tasks:
                print(indentString + task)
    print()
    for subproject in project.projects:
        printProject(subproject, indent+1, printTasks)

def main():
    parser = argparse.ArgumentParser(description='Report various TODO list aspects')
    parser.add_argument('-t', '--tasks', action='store_true', help='list all tasks')
    parser.add_argument('-p', '--projects', action='store_true', help='list all projects, including empty ones')
    parser.add_argument('-m', '--mailsubject', action='store_true', help='Add a mail subject line')
    
    args = parser.parse_args()
    rootProject = Project(rootProjectName, todoDir)
    
    if len(sys.argv) < 2:
        parser.print_help()
        sys.exit(1)
    
    if args.mailsubject == 'none': 
            args.mailsubject == False
    
    #listFiles(todoDir)
    scanProjectDirs(rootProject)
    assembleProjectsTasks(rootProject)
    if args.tasks:
        printProjectList(rootProject, args.mailsubject, True)
        
    if args.projects:
        printProjectList(rootProject, args.mailsubject, False)
    
main()



    



    