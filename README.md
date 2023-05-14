# FileBrowserGit

FileBrowserGit is a Python application that combines the power of PyQt5's QFileDialog with some of Git's most used features, such as initialize a repository, add files to staging, commit changes, restore files, remove files, and rename files. 
The original project is here: [FileManager](https://github.com/Tristan296/FileManager) 

## Features

1. File Browser: This is a standard file dialog that lets you navigate through your file system and select files or folders. The selected files or folders(of selected files) can then be processed with Git operations.

2. Git Features: This section provides buttons for several Git operations such as:
   - **All files must be selected before use it’s button(Important!)!**
   - <button name="Git Init"]Git Init</button>: Button for `git init` command. This button initializes a Git repository in the current directory of the selected file.
   - Git Add: Button for `git add` command. This button stages the selected file.
   - Git Commit: Button for `git commit` command and shows staged files. 
      - Show Staged Changes: This button shows the staeged changes(files on staged).
      - Commit Staged Changes: This button commits the staged changes with a user-specified commit message.
   - Git Restore: Button for `git restore` command. This button unstages the selected file.
   - Git rm: Button for `git rm` command. This button removes the selected file from the working tree and stages the deletion.
   - Git rm --cached: Button for `git rm --cached` command. This button unstages the selected file and keeps it on your working tree.
   - Git mv: Button for `git mv` command. This button renames the selected file and stages the change.
   - Create File: This button creates a new file in the directory of the selected file.
   - Git Status: Button for `git status` command. This button shows the output of the 'git status' command on the directory of the selected file.

## Usage

Simply run OSSProjFM.exe, and a dialog will open. Navigate to the desired directory, select the file or files you want to perform Git operations on, and click on the corresponding button for the Git operation you want to perform.

This application assumes that you have Git installed on your system and that it can be called using the command `git`.

This tool can be especially useful for those who are new to Git and want a more visual way of performing common Git operations, or for those who prefer using a GUI over the command line.
