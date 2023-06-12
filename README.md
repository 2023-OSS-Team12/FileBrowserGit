# FileBrowserGit

FileBrowserGit is a Python application that combines the power of PyQt5's QFileDialog with some of Git's most used features, such as initialize a repository, add files to staging, commit changes, restore files, remove files, and rename files. Also displays a list of branches for the repository currently being managed by Git, as well as buttons for additional branch operations.

The original project is here: [FileManager](https://github.com/Tristan296/FileManager)

*****
## Updated in v2.0
- Git clone repository
- Show the git history
- Make a branch
- Delete the branch
- Rename the branch
- Checkout the other branch
## Download
⚠ **Requirements**
- OS : Windows
- Storage : at least 50MB

📎**Download Link**

[```v2.0```](https://github.com/2023-OSS-Team12/FileBrowserGit/releases/tag/v2.0) << Latest Version!

~~[```v1.0```](https://github.com/2023-OSS-Team12/FileBrowserGit/releases/tag/v1.0)~~

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
#### ✅(Important!) All files must be selected before use Git Features

### 2. Basic Git Features : This section provides buttons for several Git operations such as:

>   **Git Init** : Button for `git init` command. This button initializes a Git repository in the current directory of the selected file.
>   
>   **Git Clone** : A button for the `git clone` command. You can choose the public or private option. (The URL must end in '.git'.)
>
>   >   If public, it asks the user for the GitHub address.
>   >    
>   >   If private, it asks the user for the GitHub address, ID, and token.
>   >   
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

### 3. Git Features : Control Branch
>   **Show Branch list:** Shows a list of branches. If the selected file is managed by Git, it will show the name of the branch.
>   
>   **Make Branch** : A button for the `git branch <branch name>` command. It asks the user for a branch name and creates a new branch. At this time, the branch is created at the location of the branch currently being worked on.
>
>   **Delete branch** : A button for the `git branch -d <branch name>` command. It deletes the selected branch from the branch list.
>
>   **Rename branch** : A button for the `git branch -m old-branch new-branch` command. It modifies the name of the selected branch in the Git branch list.
>
>   **Checkout branch** : A button for the `git checkout` command. It performs a checkout to the branch selected from the branch list.
>
>   **Merge branch** : A button for the `git merge` command. It supports merging two branches. Select the branch you want to merge and try to merge. If a conflict occurs during this process, it provides unmerge paths and a simple abort option.
>
>   **Git History** : A button for the `git log` command. It shows git log with graph. If you want more information, select the one of the git log and click the Show detail commit button. Then it sequentially shows commit's 'checksum', 'author's name and email', 'commit time', 'commit message'
>

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

### ex3) Cloning a repository. (This process may take some time)

![Animation11](https://github.com/2023-OSS-Team12/FileBrowserGit/assets/58902513/51cdcfc4-71b7-4ccf-aa7e-96b6295e07af)

### ex4-1) Make branche 'new_branch'.

![Animation12](https://github.com/2023-OSS-Team12/FileBrowserGit/assets/58902513/711ce674-1325-451f-bc30-22706d74768b)

### ex4-2) Checkout to 'new_branch' and merge 'branch1'.

![Animation13](https://github.com/2023-OSS-Team12/FileBrowserGit/assets/58902513/63043a0e-deba-441e-88f5-c218df42c838)

### ex5) List out commit history and show detail of selected commit.

![Animation14](https://github.com/2023-OSS-Team12/FileBrowserGit/assets/58902513/487bb3f7-b956-4980-a8ce-5677ea34f100)

## License

This project is licensed under [GNU General Public License v3.0](./LICENSE).

