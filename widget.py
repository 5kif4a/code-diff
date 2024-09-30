import difflib

from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import guess_lexer
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QHBoxLayout, QSplitter, QTextEdit, QWidget

__all__ = ("CodeDiffWidget",)

textedit_styles = """
    QTextEdit {
        background-color: #0d1117; color: white;
    }

    QScrollBar:vertical {
        background: transparent;
        width: 16px;
        margin: 0px;
    }
    
    QScrollBar::handle:vertical {
        background-color: rgba(255, 255, 255, 0.3); 
        min-height: 20px;
    }
    
    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
        border: none;
        background: none;
    }
    
    QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
        background: none;
    }

    QScrollBar:horizontal {
        background: transparent;
        height: 16px; 
        margin: 0px;
    }
    
    QScrollBar::handle:horizontal {
        background-color: rgba(255, 255, 255, 0.3); 
        min-width: 20px;
    }
    
    QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
        border: none;
        background: none;
    }
    
    QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {
        background: none;
    }
"""


class CodeDiffWidget(QWidget):
    def __init__(self, original_text: str, modified_text: str):
        super().__init__()
        self.original_text = original_text
        self.modified_text = modified_text
        self.setup_ui()

    def setup_ui(self):
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        self.setLayout(layout)

        splitter = QSplitter(Qt.Horizontal)
        layout.addWidget(splitter)

        self.left_text_edit = QTextEdit()
        self.right_text_edit = QTextEdit()

        self.left_text_edit.setReadOnly(True)
        self.right_text_edit.setReadOnly(True)
        self.left_text_edit.setMinimumSize(100, 100)
        self.right_text_edit.setMinimumSize(100, 100)

        font = QFont()
        font.setPointSize(14)

        self.left_text_edit.setFont(font)
        self.right_text_edit.setFont(font)
        self.left_text_edit.setStyleSheet(textedit_styles)
        self.right_text_edit.setStyleSheet(textedit_styles)

        splitter.addWidget(self.left_text_edit)
        splitter.addWidget(self.right_text_edit)

        left_text, right_text = self.generate_diff(
            self.original_text, self.modified_text
        )

        self.left_text_edit.setHtml(self.highlight_text(left_text))
        self.right_text_edit.setHtml(self.highlight_text(right_text))

        self.sync_scrollbars()

    def highlight_text(self, text: str):
        lexer = guess_lexer(text)
        formatter = HtmlFormatter(style="github-dark", linenos="inline")
        highlighted_code = highlight(text, lexer, formatter)
        result = []
        for line in highlighted_code.splitlines():
            if '<span class="o">+</span>' in line:
                result.append(f'<span style="background-color: #1c4428;">{line}</span>')
            elif '<span class="o">-</span>' in line:
                result.append(f'<span style="background-color: #542426;">{line}</span>')
            else:
                result.append(line)

        return f"""
            <html>
            <head>
                <style>
                    {formatter.get_style_defs()}
                </style>
            </head>
            <body>
                {"\n".join(result)}
            </body>
        """

    def generate_diff(self, original_text: str, modified_text: str):
        diff = difflib.unified_diff(
            original_text.splitlines(), modified_text.splitlines()
        )

        left_lines = []
        right_lines = []

        for line in diff:
            if (
                line.startswith("---")
                or line.startswith("+++")
                or line.startswith("@@")
            ):
                continue
            elif line.startswith("-"):
                left_lines.append(line)
                right_lines.append("")
            elif line.startswith("+"):
                left_lines.append("")
                right_lines.append(line)
            else:
                left_lines.append(line)
                right_lines.append(line)

        return "\n".join(left_lines), "\n".join(right_lines)

    def sync_scrollbars(self):
        left_v_scrollbar = self.left_text_edit.verticalScrollBar()
        right_v_scrollbar = self.right_text_edit.verticalScrollBar()

        left_v_scrollbar.valueChanged.connect(
            lambda value: right_v_scrollbar.setValue(value)
        )
        right_v_scrollbar.valueChanged.connect(
            lambda value: left_v_scrollbar.setValue(value)
        )

        left_h_scrollbar = self.left_text_edit.horizontalScrollBar()
        right_h_scrollbar = self.right_text_edit.horizontalScrollBar()

        left_h_scrollbar.valueChanged.connect(
            lambda value: right_h_scrollbar.setValue(value)
        )
        right_h_scrollbar.valueChanged.connect(
            lambda value: left_h_scrollbar.setValue(value)
        )
