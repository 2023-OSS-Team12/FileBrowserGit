import sys
import os
import git
from git import Repo
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt
import subprocess
import platform
import shutil
import pathlib
import git_status
class FileSearcher:
    def __init__(self, root_path):
        self.root_path = root_path

    def search_file(self, name, filetype):
        for dirpath, dirname, filenames in os.walk(self.root_path):
            for filename in filenames:
                if filename == f"{name}":
                    return os.path.join(dirpath, filename)
        return None

    def list_files(self):
        return os.listdir(self.root_path)


def move_file(filePath, folder_path):
    shutil.move(filePath, folder_path)


def open_file(findPath):
    if platform.system() == 'Darwin':  # macOS
        subprocess.call(('open', findPath))
    elif platform.system() == 'Windows':  # Windows
        os.startfile(findPath)
    else:  # linux variants
        subprocess.call(('xdg-open', findPath))

class FileDialog(QFileDialog):
    selected_files = []

    def __init__(self):
        super().__init__()
        self.setOption(QFileDialog.DontUseNativeDialog, True)
        self.setFileMode(QFileDialog.ExistingFiles)
        self.searcher = FileSearcher("/")  # Create a FileSearcher object with root path '/'
        self.setup_UI()

    def setup_UI(self):  # initialize setup UI
        self.setWindowTitle("FileBrowserGit")

        self.resize(700, 500)  # setup window center and resizing
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

        set_layout = QHBoxLayout()  # set of layouts

        group_boxF = QGroupBox("File Browser")
        main_layout = self.layout()
        group_boxF.setLayout(main_layout)

        group_boxG = QGroupBox("Git Features")
        group_boxG.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        button_layout = QVBoxLayout()

        group_boxS = QGroupBox("Git Status")
        status_layout = QVBoxLayout()

        stat_button = QPushButton("Git status")
        stat_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        stat_button.clicked.connect(self.git_status)
        button_layout.addWidget(stat_button)


        git_clone_button = QPushButton("Git clone")
        git_clone_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        git_clone_button.clicked.connect(self.git_clone)
        button_layout.addWidget(git_clone_button)


        open_button = QPushButton("Git init")
        open_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        open_button.clicked.connect(self.init_repository)
        button_layout.addWidget(open_button)

        add_button = QPushButton("Git add")
        add_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        add_button.clicked.connect(self.git_add)
        button_layout.addWidget(add_button)

        commit_button = QToolButton()
        commit_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        commit_button.setText("Git commit")
        commit_button.setMenu(self.create_commit_menu())
        commit_button.setPopupMode(QToolButton.InstantPopup)
        button_layout.addWidget(commit_button)

        restore_button = QPushButton("Git restore")
        restore_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        restore_button.clicked.connect(self.git_restore)
        button_layout.addWidget(restore_button)

        rm_button = QPushButton("Git rm")
        rm_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        rm_button.clicked.connect(self.git_rm)
        button_layout.addWidget(rm_button)

        rmc_button = QPushButton("Git rm --cached")
        rmc_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        rmc_button.clicked.connect(self.git_rm_cached)
        button_layout.addWidget(rmc_button)

        mv_button = QPushButton("Git mv")
        mv_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        mv_button.clicked.connect(self.git_mv)
        button_layout.addWidget(mv_button)

        create_file_button = QPushButton("Create File")
        create_file_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        create_file_button.clicked.connect(self.create_new_file)
        button_layout.addWidget(create_file_button)

        BF_button = QPushButton("Branch Feature")
        BF_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        BF_button.clicked.connect(self.branch_open)
        button_layout.addWidget(BF_button)

        exit_button = QPushButton("Exit")
        exit_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        exit_button.clicked.connect(self.close)
        button_layout.addWidget(exit_button)

        group_boxG.setLayout(button_layout)

        global status_label
        status_label = QTextBrowser()
        status_label.setAcceptRichText(True)
        status_layout.addWidget(status_label)

        group_boxS.setLayout(status_layout)

        sub1_layout = QHBoxLayout()
        sub1_layout.addWidget(group_boxF)
        sub2_layout = QHBoxLayout()
        sub2_layout.addWidget(group_boxS)
        sub3_layout = QHBoxLayout()
        sub3_layout.addWidget(group_boxG)

        set_layout.addLayout(sub1_layout)
        set_layout.addLayout(sub2_layout)
        set_layout.addLayout(sub3_layout)

        self.setLayout(set_layout)

    def path(self, dir):
        FileDialog.selected_files = dir


    def call_file_repo(self):
        index = FileDialog.selected_files[0].split('/')
        filename = index[-1]
        index.remove(filename)
        filelocation = ""
        filelocation += "/".join(index)
        print(filelocation,'and',filename)
        return filelocation,filename

    def init_repository(self, bare=False):  # git init 기능
        try:
            filelocation, filename = self.call_file_repo()
            print("filelocation is ",filelocation)
            repo = Repo.init(filelocation)
            #Repo.init(filelocation)  # 현재 작업 중인 디렉토리를 깃 저장소로 초기화
            QMessageBox.information(self, "Git Init", f"Initialized empty Git repository in {filelocation}")
            print(f"Initialized empty Git repository in {filelocation}")
        except:
            QMessageBox.warning(self, "Error", "Empty File Directory.\nSelect File First")
    def git_add(self, selected_files):  # git add 기능
        try:
            filelocation,filename = self.call_file_repo()
            repo = Repo(filelocation)
            repo.index.add(filename)
            QMessageBox.information(self, "Git Add", f"{filename} is on staged")
            print(f"{filename} is on staged")
        except:
            QMessageBox.warning(self, "Error", "Empty File Directory.\nSelect File First")
    def git_commit(self):  # git commit 기능
        try:
            filelocation,filename = self.call_file_repo()
            repo = Repo(filelocation)
            # 사용자에게 커밋 메시지 입력창을 표시
            commit_message, ok = QInputDialog.getText(self, 'Commit Message', 'Enter commit message:')
            if ok:
                # 스테이징된 변경 사항이 있는지 확인하고, HEAD가 유효하지 않거나 첫 커밋인 경우에도 커밋을 수행
                if not repo.head.is_valid() or repo.index.diff("HEAD"):
                    repo.index.commit(commit_message)
                    QMessageBox.information(self, "Git Commit", f"Commit successful with message: {commit_message}")
                else:
                    QMessageBox.warning(self, "Git Commit", "No changes to commit.")
            else:
                QMessageBox.warning(self, "Git Commit", "Commit canceled by user.")
        except:
            QMessageBox.warning(self, "Error", "Empty File Directory.\nSelect File First")
    def create_commit_menu(self):
        try:
            menu = QMenu()
            show_staged_changes = QAction("Show Staged Changes", self)
            show_staged_changes.triggered.connect(self.show_staged_changes)
            menu.addAction(show_staged_changes)
            commit_staged_changes = QAction("Commit Staged Changes", self)
            commit_staged_changes.triggered.connect(self.git_commit)
            menu.addAction(commit_staged_changes)
            self.show()
            return menu
        except:
            QMessageBox.warning(self, "Error", "Empty File Directory.\nSelect File First")
    def show_staged_changes(self):  # show staged chages 기능
        try:
            filelocation,filename = self.call_file_repo()
            repo = Repo(filelocation)
            if repo.head.is_valid():
                staged_files = [item.a_path for item in repo.index.diff("HEAD")]
            else:
                # 아직 커밋이 입력되지 않은 경우
                # staged_files = [item.a_path for item in repo.index.diff(None)]
                staged_files = [e[0] for e in repo.index.entries.keys()]
                QMessageBox.information(self, "WARNING", f"No commits yet in this repository.")

            list_widget = QListWidget()
            list_widget.addItems(staged_files)

            staged_changes_dialog = QDialog(self)
            staged_changes_dialog.setWindowTitle("Staged Changes")
            layout = QVBoxLayout(staged_changes_dialog)
            layout.addWidget(list_widget)
            staged_changes_dialog.exec_()
        except:
            QMessageBox.warning(self, "Error", "Empty File Directory.\nSelect File First")
    def git_restore(self):  # git restore 기능
        try:
            filelocation,filename = self.call_file_repo()
            repo = Repo(filelocation)
            repo.git.reset(filename)
            QMessageBox.information(self, "Git Restore", f"{filename} is on untracked")
            print(f"{filename} is on untracked")
        except:
            QMessageBox.warning(self, "Error", "Empty File Directory.\nSelect File First")
    def git_rm(self):  # git rm 기능 (committed -> staged)
        try:
            filelocation,filename = self.call_file_repo()
            repo = Repo(filelocation)
            print(f"{filename} is deleted")
            repo.index.remove(filename,working_tree= True)
            QMessageBox.information(self, "Git Remove",f"{filename} is deleted" )
        except:
            QMessageBox.warning(self, "Error", "Empty File Directory.\nSelect File First")
    def git_rm_cached(self):  # git rm --cached 기능
        try:
            filelocation,filename = self.call_file_repo()
            repo = Repo(filelocation)
            repo.index.remove(filename)
            QMessageBox.information(self, "Git Remove Cached", f"{filename} is untracked (committed -> untracked)")
            print(f"{filename} is untracked (committed -> untracked)")
        except:
            QMessageBox.warning(self, "Error", "Empty File Directory.\nSelect File First")
    def git_mv(self):  # git mv
        try:
            filelocation,filename = self.call_file_repo()
            repo = Repo(filelocation)
            rename_text, ok = QInputDialog.getText(self, 'Rename', 'Rename file :')
            if ok:
                repo.index.move([filelocation + "/" + filename, filelocation + "/" + rename_text])
                QMessageBox.information(self, "Git Move", f"{filename} is renamed to {rename_text}")
                print(f"{filename} is renamed to {rename_text}")
            else:
                QMessageBox.warning(self, "Rename", "Rename canceled by user.")
        except:
            QMessageBox.warning(self, "Error", "Empty File Directory.\nSelect File First")
    def create_new_file(self):  # create file 기능
        try:
            # 생`성할 파일의 폴더를 지정하기 위해 폴더에 속한 파일을 반드시 선택
            # (미구현) 최초의 파일 경로 설정이 없으면 에러 - 디렉토리 경로 추출 가능시 구현 가능
            new_file_name, ok = QInputDialog.getText(self, 'New File', 'Enter name for new file:')  # 사용자에게 입력 받을 대화 상자 생성
            while ok and not new_file_name.strip():  # 파일 이름이 없는 경우를 처리
                QMessageBox.warning(self, "Invalid File Name", "File name cannot be empty. Please enter again.")
                new_file_name, ok = QInputDialog.getText(self, 'New File', 'Enter name for new file:')
            if ok:  # 'ok'가 True라면 (사용자가 'OK'를 눌렀다면), 새 파일 생성
                file_path = FileDialog.selected_files[0]
                file_location, file_name = os.path.split(file_path)

                new_file_path = os.path.join(file_location, new_file_name)  # 입력된 파일명으로 새 파일 경로 생성

                uniq = 1
                while os.path.exists(new_file_path):  # 새 파일에 대한 경로가 이미 존재하는 경우
                    new_file_path = os.path.join(file_location, new_file_name + "(" + str(uniq) + ")")  # 새 파일경로(1)..
                    uniq += 1
                if uniq > 1:
                    new_file_name += "(%d)" % (uniq - 1)  # 새 파일이름 (1)
                open(new_file_path, 'w').close()  # 파일 생성
                # 파일이 성공적으로 생성되었음을 알림
                QMessageBox.information(self, "Create New File", f"New file created: {new_file_name} in {new_file_path}")
        except:
            QMessageBox.warning(self, "Error", "Empty File Directory.\nSelect File First")
    def git_status(self):
        try:
            filelocation,filename = self.call_file_repo()
            stat = git_status.get(filelocation)
            status_label.setText(stat)
        except:
            QMessageBox.warning(self, "Error", "Empty File Directory.\nSelect File First")

    def branch_open(self):
        try:
            filelocation,filename = self.call_file_repo()
            repo = Repo(filelocation)
        except:
            QMessageBox.warning(self, "Error", "Empty File Directory.\nSelect File First")
            return

        bDialog = QDialog(self)
        bDialog.setWindowTitle("Branch Features")
        layout = QHBoxLayout(bDialog)

        self.list_widget = QListWidget()
        self.current_branches(repo,self.list_widget)

        layout.addWidget(self.list_widget)
        button_layout = QVBoxLayout()

        # branch button
        make_branch_button = QPushButton("Make branch")
        make_branch_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        make_branch_button.clicked.connect(self.make_branch)
        button_layout.addWidget(make_branch_button)

        delete_branch_button = QPushButton("Delete branch")
        delete_branch_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        delete_branch_button.clicked.connect(self.delete_branch)
        button_layout.addWidget(delete_branch_button)

        rename_branch_button = QPushButton("Rename branch")
        rename_branch_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        rename_branch_button.clicked.connect(self.rename_branch)
        button_layout.addWidget(rename_branch_button)

        checkout_branch_button = QPushButton("Checkout branch")
        checkout_branch_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        checkout_branch_button.clicked.connect(self.checkout_branch)
        button_layout.addWidget(checkout_branch_button)

        merge_branch_button = QPushButton("Merge branch")
        merge_branch_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        merge_branch_button.clicked.connect(self.git_merge)
        button_layout.addWidget(merge_branch_button)

        show_history_button = QPushButton("Show history")
        show_history_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        show_history_button.clicked.connect(self.show_git_history)
        button_layout.addWidget(show_history_button)
        layout.addLayout(button_layout)

        bDialog.exec_()

    def current_branches(self, repo, listwidget):
        res = []
        branches = repo.branches
        for b in branches:
            res.append(b.name)
        listwidget.clear()
        listwidget.addItems(res)

    def get_branch_name(self):
        try:
            branch_name, ok = QInputDialog.getText(self, 'Branch input', 'Enter name for Branch:')
            while ok and not branch_name.strip():  # 브랜치 이름 입력이 없는 경우를 처리
                QMessageBox.warning(self, "Invalid Branch Name", "Branch name cannot be empty. Please enter again.")
                branch_name, ok = QInputDialog.getText(self, 'Branch Name', 'Enter name for Branch:')
            if ok:  # 'ok'가 True라면 (사용자가 'OK'를 눌렀다면), 브랜치 이름 반환
                return branch_name
        except:
            QMessageBox.warning(self, "Error", "Error.\n")

    def show_branch(self):
        filelocation, filename = self.call_file_repo()
        repo = Repo(filelocation)
        branches = repo.branches
        for branch in branches:
            self.lbox_item = self.qtwid.QListWidget(self)
            self.lb_item = self.qtwid.QLabel("[선택 항목]", self)
            self.btn_remove = self.qtwid.QPushButton("삭제", self)
            print(branch.name)

    def make_branch(self):
        try:
            filelocation,filename = self.call_file_repo()
            repo = Repo(filelocation)
            branch_name = self.get_branch_name()
            if branch_name is not None:
                new_branch = repo.create_head(branch_name)
                QMessageBox.information(self,"Make branch",f"Created branch '{branch_name}' successfully.")
                self.current_branches(repo, self.list_widget) # update QListWidget
        except:
            QMessageBox.warning(self,"Error",f"An error occurred while creating branch '{branch_name}':")
    def delete_branch(self):
        try:
            filelocation,filename = self.call_file_repo()
            repo = Repo(filelocation)
            branch_name = self.list_widget.currentItem().text()
            repo.git.branch('-D', branch_name)
            QMessageBox.information(self,"Delete branch",f"Deleted branch '{branch_name}' successfully.")
            self.current_branches(repo, self.list_widget)  # update QListWidget
        except Exception as e:
            print(e)
            QMessageBox.warning(self,"Error",f"An error occurred while deleting branch '{branch_name}':")

    def rename_branch(self):
        try:
            filelocation, filename = self.call_file_repo()
            repo = Repo(filelocation)
            old_branch_name = self.list_widget.currentItem().text()
            new_branch_name = self.get_branch_name()
            repo.git.branch('-m', old_branch_name, new_branch_name)
            QMessageBox.information(self,"Rename branch",f"Renamed branch '{old_branch_name}' to '{new_branch_name}' successfully.")
            self.current_branches(repo, self.list_widget)  # update QListWidget
        except:
            QMessageBox.warning(self,"Error",f"An error occurred while renaming branch '{old_branch_name}':")
    def checkout_branch(self):
        try:
            filelocation, filename = self.call_file_repo()
            repo = Repo(filelocation)
            branch_name = self.list_widget.currentItem().text()
            repo.git.checkout(branch_name)
            print(f"Checked out branch '{branch_name}' successfully.")
            QMessageBox.information(self,"Checkout branch",f"Checked out branch '{branch_name}' successfully.")
        except:
            QMessageBox.warning(self,"Error",f"An error occurred while checking out branch '{branch_name}':")

    def git_merge(self):
        try:
            filelocation, filename = self.call_file_repo()
            repo = Repo(filelocation)
            branch_name = self.list_widget.currentItem().text()
            repo.git.merge(branch_name)
            QMessageBox.information(self,"Merge branch",f"Merged branch '{branch_name}' successfully.")
            self.current_branches(repo, self.list_widget)  # update QListWidget
        except:
            QMessageBox.warning(self,"Error",f"An error occurred while merging branch '{branch_name}':")
            if repo.is_dirty():
                repo.git.merge('--abort')
                QMessageBox.warning(self, "Error", "Merge aborted due to conflicts.")
                #print("Merge aborted due to conflicts.")

#히스토리랑 트리출력 메시지박스 해야됨
    def show_git_history(self):
        try:
            filelocation, filename = self.call_file_repo()
            repo = Repo(filelocation)

            commit_tree = []
            history_text = ""
            history_text += repo.git.log('--oneline', '--graph') #tree 출력
            commit_tree = history_text.split("\n")
            # Create a new window to display the Git history
            history_window = QDialog()
            history_window.setFixedSize(900,500)
            history_window.setWindowTitle("Git History")
            history_layout = QVBoxLayout()
            self.history_listbox = QListWidget()
            self.history_listbox.addItems(commit_tree)
            history_layout.addWidget(self.history_listbox)
            history_window.setLayout(history_layout)

            button_layout = QHBoxLayout()
            show_commit = QPushButton("Show detail commit")

            show_commit.clicked.connect(self.show_detail_commit)
            show_commit.setFixedSize(300,40)
            show_commit.setStyleSheet("	color: rgb(58, 134, 255);"
                                        "background-color: white;"
	                                    "border: 2px solid rgb(58, 134, 255);"
	                                    "border-radius: 5px;")

            button_layout.addWidget(show_commit)

            history_layout.addLayout(button_layout)
            history_window.exec_()

        except Exception as e:
            print("An error occurred while retrieving Git history:")
            print(e)


    def show_detail_commit(self):
        try:
            filelocation, filename = self.call_file_repo()
            repo = Repo(filelocation)
            commits = repo.iter_commits()
            commit_checksum = []
            commit_checksum = self.history_listbox.currentItem().text().split()
            i = 0
            for c in commit_checksum:
                if commit_checksum[i] != '*' and commit_checksum[i] != '/' and commit_checksum[i] != '|' and commit_checksum[i] != '\\':
                    break
                i += 1
            print(commit_checksum)
            print(i)
            commit_text = ""
            for c in commits:
                if c.hexsha[0:7] == commit_checksum[i]:
                    commit_text = ""
                    commit_text += f"Commit: {c.hexsha}\n"
                    commit_text += f"Author: {c.author.name} <{c.author.email}>\n"
                    commit_text += f"Date: {c.authored_datetime}\n"
                    commit_text += f"Message: {c.message}\n\n"


            detail_window = QDialog()
            detail_window.setFixedSize(400, 150)
            detail_layout = QVBoxLayout()
            detail_text = QTextEdit()
            detail_text.setText(commit_text)
            detail_text.setReadOnly(True)
            detail_layout.addWidget(detail_text)
            detail_window.setLayout(detail_layout)
            detail_window.exec_()

        except Exception as e:
            print(f"An error occurred while retrieving Git tree:")
            print(e)

    def git_clone(self,github_url, username=None, password=None):
        try:
            # Check if the repository is public or private
            filelocation, filename = self.call_file_repo()
            repository_visibility, ok = QInputDialog.getText(self, 'public or private',
                                          'Is the GitHub repository public or private? (public/private): ')

            print(repository_visibility)
            if repository_visibility.lower() == "public":
                # Prompt for the public repository URL
                repository_url = QInputDialog.getText(self, 'public',"Enter the GitHub repository URL: ")
                print(repository_url[0])
                print(filelocation)
                git.Git(filelocation).clone(repository_url[0])
                #git.Repo.clone_from(repository_url[0],filelocation)
                print("success")
            elif repository_visibility.lower() == "private":
                url = QInputDialog.getText(self, 'private',"Enter the GitHub repository URL: ")
                github_id = QInputDialog.getText(self, 'github id',"Enter your GitHub username or organization name: ")
                github_token = QInputDialog.getText(self, 'github id',"Enter your GitHub access token: ")
                # Set the GitHub credentials for cloning the private repository
                url = url[0][8:]
                private_url = 'https://'+github_token[0]+':x-oauth-basic@'+url

                git.Git(filelocation).clone(private_url)

        except:
            QMessageBox.warning(self, "Error","Invalid repository visibility.")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    dialog = FileDialog()

    while (dialog.exec_() == QFileDialog.Accepted):  # exit하기 전까지 무한 반복
        print(dialog.selectedFiles())  # 경로 나오는지 print
        dialog.selected_files = dialog.selectedFiles()  # 경로 선택해서 저장
        dialog.path(dialog.selectedFiles())
        dialog.show()

    sys.exit(app.exec_())



