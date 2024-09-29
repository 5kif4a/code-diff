from PySide6.QtWidgets import QHBoxLayout, QPlainTextEdit, QWidget

__all__ = ("CodeDiffWidget",)


class CodeDiffWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        layout = QHBoxLayout()
        self.setLayout(layout)

        self.editable_text_edit = QPlainTextEdit()
        self.readonly_text_edit = QPlainTextEdit()
        layout.addWidget(self.editable_text_edit)
        layout.addWidget(self.readonly_text_edit)
