# HamsterWheel
## Introduction
HamsterWheel is a python script to help me manage my todo lists. 
I loosly follow the Getting Things Done (GTD) approach as laid out in great detail in the [seminal book by David Allen](https://en.wikipedia.org/wiki/Getting_Things_Done).
Having tried many, also commercial GDT apps, I wasn't satisfied with any of them, mostly because of a disjunction of projects and project material. 
The HamsterWheel approach uses the computer file system to organise projects. A folder under your $PROJECTS folder constitutes a project.
A subfolder therein is a subproject. A project folder holds at least one folder named 'Materials' which can have an abitrary collection of stuff, as
well as a file named 'TODO' which holds a list of tasks. 

The script todo.py, HamsterWheel's only file :), walks through the directory tree under $PROJECTS and accepts the directory name as a project name, 
unless the folder is called "Materials". If it finds a TODO file, it parses its lines into a list of tasks for this folder. 

## Usage

usage: todo.py [-h] [-t] [-p] [-m]

Report various TODO list aspects

optional arguments:
  -h, --help         show this help message and exit
  -t, --tasks        list all tasks
  -p, --projects     list all projects, including empty ones
  -m, --mailsubject  Add a mail subject line
  
 ## Trivia
 If you are interested in helping to develop HamsterWheel further, please contact me or just get going and push your improvements. 
 For GTD, many things are missing, such as Context.

