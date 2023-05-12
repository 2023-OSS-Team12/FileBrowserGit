import sys
import os
import git
from git import Repo
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import subprocess
import platform
import shutil
import pathlib

from git import Repo


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
        set_layout = QHBoxLayout()  # set of layouts

        group_boxF = QGroupBox("File Browser")
        main_layout = self.layout()
        group_boxF.setLayout(main_layout)

        group_boxG = QGroupBox("Git Features")
        group_boxG.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        button_layout = QVBoxLayout()

        status_label = QLabel("Git Status : ", self)

        button_layout.addWidget(status_label)

        open_button = QPushButton("Git Init")
        open_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        open_button.clicked.connect(self.init_repository)
        button_layout.addWidget(open_button)

        add_button = QPushButton("Git Add")
        add_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        add_button.clicked.connect(self.git_add)
        button_layout.addWidget(add_button)

        commit_button = QToolButton()
        commit_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        commit_button.setText("Git Commit")
        commit_button.setMenu(self.create_commit_menu())
        commit_button.setPopupMode(QToolButton.InstantPopup)
        button_layout.addWidget(commit_button)

        restore_button = QPushButton("Git Restore")
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

        exit_button = QPushButton("Exit")
        exit_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        exit_button.clicked.connect(self.close)
        button_layout.addWidget(exit_button)

        group_boxG.setLayout(button_layout)

        sub1_layout = QHBoxLayout()
        sub1_layout.addWidget(group_boxF)
        sub2_layout = QHBoxLayout()
        sub2_layout.addWidget(group_boxG)

        set_layout.addLayout(sub1_layout)
        set_layout.addLayout(sub2_layout)

        self.setLayout(set_layout)

    def path(self, dir):
        FileDialog.selected_files = dir

    def init_repository(self, bare=False):
        index = FileDialog.selected_files[0].split('/')  # 파일 위치를 불러옴, /로 나눔
        filename = index[-1]  # 파일 이름만 저장
        index.remove(filename)
        filelocation = ""  # 파일 경로 파일이름빼고
        filelocation += "/".join(index)
        Repo.init(filelocation)  # 현재 작업 중인 디렉토리를 깃 저장소로 초기화
        print(f"Initialized empty Git repository in {filelocation}")

    def git_add(self, selected_files):  # git add누르면
        '''
        pathrepo = self.getExistingDirectory(self, 'search folder to git add', './')
        print("path repo",pathrepo)
        repo = git.Repo(pathrepo)
        repo.index.add('new.txt')
        '''
        index = FileDialog.selected_files[0].split('/')  # 파일 위치를 불러옴, /로 나눔
        filename = index[-1]  # 파일 이름만 저장
        index.remove(filename)
        filelocation = ""  # 파일 경로 파일이름빼고
        filelocation += "/".join(index)
        repo = Repo(filelocation)
        repo.index.add(filename)
        print(filename, "is on staged")



    def git_commit(self):
        if not FileDialog.selected_files:
            # [초안]
            # 파일 선택하지 않은 경우(폴더만 선택한 경우), 특정 폴더에서 바로 commit하고 싶은 경우
            # 대화형 폴더 선택 상자를 생성 -> commit 작업을 수행할 폴더 선택
            filelocation = QFileDialog.getExistingDirectory(self, "Select Directory")
        else:
            index = FileDialog.selected_files[0].split('/')
            filename = index[-1]
            index.remove(filename)
            filelocation = "/".join(index)

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

    def create_commit_menu(self):
        menu = QMenu()
        show_staged_changes = QAction("Show Staged Changes", self)
        show_staged_changes.triggered.connect(self.show_staged_changes)
        menu.addAction(show_staged_changes)
        commit_staged_changes = QAction("Commit Staged Changes", self)
        commit_staged_changes.triggered.connect(self.git_commit)
        menu.addAction(commit_staged_changes)
        self.show()
        return menu

    def show_staged_changes(self):
        if not FileDialog.selected_files:
            # [초안]
            # 파일 선택하지 않은 경우(폴더만 선택한 상태), 특정 폴더의 staged file을 보고 싶은 경우
            # 대화형 폴더 선택 상자를 생성 -> staged file을 보고 싶은 폴더 선택
            filelocation = QFileDialog.getExistingDirectory(self, "Select Directory")
        else:
            index = FileDialog.selected_files[0].split('/')
            filename = index[-1]
            index.remove(filename)
            filelocation = "/".join(index)

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

    def git_restore(self):  # restore 기능임
        index = FileDialog.selected_files[0].split('/')  # 파일 위치를 불러옴, /로 나눔
        filename = index[-1]  # 파일 이름만 저장
        index.remove(filename)
        filelocation = ""  # 파일 경로 파일이름빼고
        filelocation += "/".join(index)
        repo = Repo(filelocation)
        repo.git.reset(filename)
        print(filename, "is on untracked")
        
    def git_rm(self):  # git rm (committed -> staged)
        index = FileDialog.selected_files[0].split('/')  # 파일 위치를 불러옴, /로 나눔
        filename = index[-1]  # 파일 이름만 저장
        index.remove(filename)
        filelocation = ""  # 파일 경로 파일이름빼고
        filelocation += "/".join(index)
        repo = Repo(filelocation)
        repo.index.remove(filename, working_tree=True)
        print(filename, "is deleted")

    def git_rm_cached(self):  # git rm cached
        index = FileDialog.selected_files[0].split('/')  # 파일 위치를 불러옴, /로 나눔
        filename = index[-1]  # 파일 이름만 저장
        index.remove(filename)
        filelocation = ""  # 파일 경로 파일이름빼고
        filelocation += "/".join(index)
        repo = Repo(filelocation)
        repo.index.remove(filename)
        print(filename, "is untracked (committed -> untracked)")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    dialog = FileDialog()
    #dialog.exec_()

    while (dialog.exec_() == QFileDialog.Accepted):  # exit하기 전까지 무한 반복
        print(dialog.selectedFiles())  # 경로 나오는지 print
        # dialog.selectedFiles()
        dialog.selected_files = dialog.selectedFiles()  # 경로 선택해서 저장
        dialog.path(dialog.selectedFiles())

    sys.exit(app.exec_())
