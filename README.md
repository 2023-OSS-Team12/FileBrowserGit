# FileBrowserGit

FileBrowserGit is a Python application that combines the power of PyQt5's QFileDialog with some of Git's most used features, such as initialize a repository, add files to staging, commit changes, restore files, remove files, and rename files. 

The original project is here: [FileManager](https://github.com/Tristan296/FileManager)

*****

## Download
⚠ **Requirements**
- OS : Windows
- Storage : at least 40MB

📎**Download Link**

```v1.0``` https://github.com/2023-OSS-Team12/FileBrowserGit/releases/tag/v1.x

✔️ **If you want to run this program in other OS (Linux, MacOS, ...), you must install these packages. Then run OSSProjFM.py.**

 ``` pip install PyQt5 ```
 
 ``` pip install GitPython ```
 
 ``` pip install git-status ```


## Features

### 1. File Browser
> This is a standard file dialog that lets you navigate through your file system and select files or folders. 
>
> You can **Rename, Delete, Create Folders** and **Rename, Delete Files** using right click.
>
> You can **Move Folders and Files** using clicking and dragging.
>
> You can **Select or Open Directory(Folder)** using double-clicking.
> 
> The selected files or folders can then be processed with Git operations. 
> 
> The file browsing starts from the most recently visited directory
> 

### 2. Git Features : This section provides buttons for several Git operations such as:
#### ✅(Important!) All files must be selected before use these buttons!

>   **Git Init** : Button for `git init` command. This button initializes a Git repository in the current directory of the selected file.
>   
>   **Git Add** : Button for `git add` command. This button stages the selected file.
>   
>   **Git Commit** : Button for `git commit` command and shows staged files. 
>   
>   >   **Show Staged Changes** : This button shows the staeged changes(files on staged).
>   >   
>   >   **Commit Staged Changes** : This button commits the staged changes with a user-specified commit message.
>      
>   **Git Restore** : Button for `git restore` command. This button unstages the selected file.
>   
>   **Git rm** : Button for `git rm` command. This button removes the selected file from the working tree and stages the deletion.
>   
>   **Git rm --cached** : Button for `git rm --cached` command. This button unstages the selected file and keeps it on your working tree.
>   
>   **Git mv** : Button for `git mv` command. This button renames the selected file and stages the change.
>   
>   **Create File** : This button creates a new file in the directory of the selected file.
>   
>   **Git Status** : Button for `git status` command. This button shows the output of the 'git status' command on the directory of the selected file.
>   
>   >   **?? : untracked**
>   >   
>   >   **M : modified**
>   >   
>   >   **A : added**
>   >   
>   >   **D : removed**
>   >   
>   >   **R : moved**

## Usage

Simply run the script, and a dialog will open. Navigate to the desired directory, select the file or files you want to perform Git operations on, and click on the corresponding button for the Git operation you want to perform.

This application assumes that you have Git installed on your system and that it can be called using the command `git`.

This tool can be especially useful for those who are new to Git and want a more visual way of performing common Git operations, or for those who prefer using a GUI over the command line.

## Examples

### ex1) In case you press the button before selecting any files.

![Animation1](https://github.com/2023-OSS-Team12/FileBrowserGit/assets/58902513/bd2a1f55-90da-42f7-97f0-5cda6d7e23ab)

### ex2-1) Git init current working directory, Git add new.txt(staging), and Display git status.

![Animation2](https://github.com/2023-OSS-Team12/FileBrowserGit/assets/58902513/32a5e399-7fec-4f32-95f4-cfc9f33e4d4c)

### ex2-2) After 2-1, Git commit and Remove new.txt

![Animation3](https://github.com/2023-OSS-Team12/FileBrowserGit/assets/58902513/2fe68a62-94b9-4e6b-a0f4-8b89e57fd323)





## License

This project is licensed under [GNU General Public License v3.0](./LICENSE).

