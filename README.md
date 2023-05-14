# FileBrowserGit

FileBrowserGit is a Python application that combines the power of PyQt5's QFileDialog with some of Git's most used features, such as initialize a repository, add files to staging, commit changes, restore files, remove files, and rename files. 
The original project is here: https://github.com/Tristan296/FileManager

## Setup
GUI File Manager:
Before use, please install PyQt5 please run the following command in the python terminal.

MacOS: 
- ```pip3 install pyqt5```
- ```pip3 install gitpython```
- ```pip3 install git_status```

## Features

1. File Browser: This is a standard file dialog that lets you navigate through your file system and select files or folders. The selected files or folders can then be processed with Git operations.

2. Git Features: This section provides buttons for several Git operations such as:
   - Git Init: This button initializes a Git repository in the current directory of the selected file.
   - Git Add: This button stages the selected file.
   - Git Commit: This button commits the staged changes with a user-specified commit message.
   - Git Restore: This button unstages the selected file.
   - Git rm: This button removes the selected file from the working tree and stages the deletion.
   - Git rm --cached: This button unstages the selected file and keeps it on your working tree.
   - Git mv: This button renames the selected file and stages the change.
   - Create File: This button creates a new file in the directory of the selected file.

3. Git Status: This section shows the output of the `git status` command on the directory of the selected file.

## Usage

Simply run the script, and a dialog will open. Navigate to the desired directory, select the file or files you want to perform Git operations on, and click on the corresponding button for the Git operation you want to perform.

This application assumes that you have Git installed on your system and that it can be called using the command `git`.

This tool can be especially useful for those who are new to Git and want a more visual way of performing common Git operations, or for those who prefer using a GUI over the command line.
