from PySide6.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QPushButton, QFrame
from PySide6.QtCore import Qt


class HelpWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Help")
        self.setWindowModality(Qt.ApplicationModal)
        self.setFixedSize(500, 300)
        
        container = QFrame()
        container.setFrameShape(QFrame.Box)
        container.setLineWidth(2)
        container.setStyleSheet("background: rgba(0,0,0,210);")

        layout = QVBoxLayout(container)
        self.setLayout(QVBoxLayout())
        self.layout().addWidget(container)
        
        help_text = QTextEdit()
        help_text.setReadOnly(True)
        help_text.setHtml("""
            <h2>Welcome to ChatGUI! </h2>
            <h4>曾为帅 2200012931  宣典村 2100017415  冯子桐 2400017788</h4>
        
            <h3> What is this? </h3>
            <p style="line-height: 1.5;">A light-weighted desktop software with unified and user-friendly interface to seamlessly interact with multiple large language models</p>
                          
            <h3> How to use? </h3>
            <ol style="list-style-position: inside; padding-left: 0;">
                <li style="margin-bottom: 10px;">Choose a model you would like to interact with</li>
                <li style="margin-bottom: 10px;">(Optional)Set the relevant configs by clipping the setting button</li>
                <li style="margin-bottom: 10px;">Type anything you would like to know in the input bar</li>
                <li style="margin-bottom: 10px;">Enjoy your chat with the prevailing LLMs</li>
            </ol>
                          
            <h3> Meet Trouble? </h3>
            Please do not hesitate to contact with us:
            <ul style="list-style-position: inside; padding-left: 0;">
                <li style="margin-bottom: 10px;">2200012931@stu.pku.edu.cn</li>
                <li style="margin-bottom: 10px;">2100017415@stu.pku.edu.cn</li>
                <li style="margin-bottom: 10px;">2400017788@stu.pku.edu.cn</li>
            </ul>             
            
            <h3> Some words in the end </h3>
            <p style="line-height: 1.5;">Due to the time constraint, we are sorry to present more brilliant features of our idea - ChatGUI, a powerful desktop application which may have the potential to be a real application. Still, we expect this demo to display the fun LLMs may bring you. </p>
        """)
        
        close_button = QPushButton("Close")
        close_button.clicked.connect(self.close)
        
        layout.addWidget(help_text)
        layout.addWidget(close_button)
