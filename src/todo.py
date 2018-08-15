#!/usr/local/bin/python3
import os
import argparse
import sys

#
# Adjust these variables to fit your needs or preferences 
#
todoDir="/Users/steinbeck/Dropbox/Documents/Projects"   # the topmost directory where your projects reside
rootProjectName="Christoph's projects"  # The name of the entirety of your projects. Your topmost superproject, if you wish. Holds all other projects.
subjectLineTaskList = "Task list for Christoph" # If you mail this list to yourself, this will be the subject line. 
subjectLineProjectList = "Project list for Christoph" # If you mail this list to yourself, this will be the subject line. 
indentAtom = 4 # names of subproject are indented by multiples of indentAtom in the project list 


exclDirs= list()
exclDirs.append("ZZ-COMPLETED")
exclDirs.append("ZZ-WAITINGFOR")
exclDirs.append("ZZ-SOMEDAYMAYBE")
exclDirs.append("Materials")

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
    if mailsubject: print("subject: " +  subjectLineProjectList)
    for subproject in project.getProjects():
        printProject(subproject, 0, printTasks)
        
def printProject(project, indent, printTasks):
    indentString = ' ' * (indentAtom) * (indent)
    print(indentString + "*" + project.name + "*")
    if printTasks:
        tasks = project.getTasks()
        if len(tasks) > 0:  
            indentString = ' ' * (indentAtom) * (indent + 1 )
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



    



    