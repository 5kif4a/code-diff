import sys

from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget

from config import (
    MAIN_WINDOW_MIN_HEIGHT,
    MAIN_WINDOW_MIN_WIDTH,
    MODIFIED_CODE_FILE_PATH,
    ORIGINAL_CODE_FILE_PATH,
)
from widget import CodeDiffWidget


def read_file(file_path: str) -> str:
    with open(file_path, "r", encoding="utf8") as file:
        return file.read()


def main():
    # sys.argv += ['-platform', 'windows:darkmode=1']
    app = QApplication(sys.argv)
    window = QMainWindow()
    window.setWindowTitle("Code Diff")
    window.setMinimumSize(MAIN_WINDOW_MIN_WIDTH, MAIN_WINDOW_MIN_HEIGHT)

    main_widget = QWidget()
    main_layout = QVBoxLayout()
    main_layout.setContentsMargins(0, 0, 0, 0)
    main_layout.setSpacing(0)
    main_widget.setLayout(main_layout)

    original_code = read_file(ORIGINAL_CODE_FILE_PATH)
    latest_code = read_file(MODIFIED_CODE_FILE_PATH)

    code_diff_widget = CodeDiffWidget(original_code, latest_code)
    main_layout.addWidget(code_diff_widget)

    window.setCentralWidget(main_widget)
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
