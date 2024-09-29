import sys

from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget

from config import MAIN_WINDOW_MIN_HEIGHT, MAIN_WINDOW_MIN_WIDTH
from widget import CodeDiffWidget


def main():
    app = QApplication(sys.argv)
    window = QMainWindow()
    window.setWindowTitle("Code Diff")
    window.setMinimumSize(MAIN_WINDOW_MIN_WIDTH, MAIN_WINDOW_MIN_HEIGHT)

    main_widget = QWidget()
    main_layout = QVBoxLayout()
    main_widget.setLayout(main_layout)

    code_diff_widget = CodeDiffWidget()
    main_layout.addWidget(code_diff_widget)

    window.setCentralWidget(main_widget)
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
