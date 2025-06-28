import os
from datetime import datetime
import joblib
import markdown

# config
import cfg.config as config

# ui
from PySide6.QtWidgets import (QApplication, QWidget, QHBoxLayout, QVBoxLayout, 
                              QSplitter, QLineEdit, QListView, QPushButton, 
                              QComboBox, QPlainTextEdit, QProgressBar, QTabWidget, QTextEdit, QListWidget,QListWidgetItem, QFrame)
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QTimer
from PySide6.QtGui import QIcon, QPalette, QColor, QTextCharFormat, QFont, QTextCursor

from ui.helpWindow import HelpWindow
from ui.settingWindow import SettingWindow

# chat
from agent.agent_router import AgentRouter

class ChatWidget(QWidget):
    def __init__(self, parent):
        super().__init__()
        
        self.parent = parent
        self.parent.setWindowTitle("ChatGUI")

        self.setupUI()
        self.setupConnections()
        self.setupAgent()
        self.apply_minimal_theme()

        self.setupConfig()
        
    def setupUI(self):
        # Main layout
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        self.setLayout(main_layout)
        
        # left sidebar
        self.sidebar = QFrame()
        self.sidebar.setFrameShape(QFrame.NoFrame)
        sidebar_layout = QVBoxLayout()
        sidebar_layout.setContentsMargins(15, 15, 10, 15)
        sidebar_layout.setSpacing(15)
        self.sidebar.setLayout(sidebar_layout)
        
        # Search bar
        self.searchContent = QLineEdit()
        self.searchContent.setPlaceholderText("Search ...")
        self.searchContent.setClearButtonEnabled(True)
        
        # Conversation list
        self.conversationList = QListWidget()
        self.conversationList.setFrameShape(QFrame.NoFrame)
        
        # Settings button - minimal
        self.settingButton = QPushButton("Settings")
        self.settingButton.setIcon(QIcon.fromTheme("preferences-system"))
        self.settingButton.setFlat(True)

        self.helpButton = QPushButton("Help")
        self.helpButton.setIcon(QIcon.fromTheme("preferences-system"))
        self.helpButton.setFlat(True)

        button_container = QWidget()
        button_layout = QHBoxLayout()
        button_layout.setContentsMargins(0,0,0,0)
        button_layout.setSpacing(10)
        button_container.setLayout(button_layout)
        button_layout.addWidget(self.settingButton)
        button_layout.addWidget(self.helpButton)
        
        sidebar_layout.addWidget(self.searchContent)
        sidebar_layout.addWidget(self.conversationList, 1)
        sidebar_layout.addWidget(button_container,0,Qt.AlignBottom)
        
        # main
        self.contentArea = QFrame()
        self.contentArea.setFrameShape(QFrame.NoFrame)
        content_layout = QVBoxLayout()
        content_layout.setContentsMargins(15, 15, 15, 5)  # More bottom margin for input
        content_layout.setSpacing(15)
        self.contentArea.setLayout(content_layout)
        
        # Top bar
        top_bar = QWidget()
        # top_bar.setFixedHeight(40)
        top_bar.setObjectName("topBar")
        top_bar_layout = QHBoxLayout()
        # top_bar_layout.setContentsMargins(10, 10, 10, 10)
        top_bar.setLayout(top_bar_layout)
        
        self.apiModels = QComboBox()
        self.apiModels.addItems(config.models)
        self.apiModels.setEditable(False)
        self.current_model = self.apiModels.currentText()
        # self.current_model_idx = self.apiModels.currentIndex()
        
        self.newButton = QPushButton("New Chat")
        self.newButton.setFlat(True)
        
        top_bar_layout.addWidget(self.apiModels)
        top_bar_layout.addStretch()
        top_bar_layout.addWidget(self.newButton)
        
        # Content display
        self.contentView = QTextEdit()
        self.contentView.setFrameShape(QFrame.NoFrame)
        self.contentView.setReadOnly(True)
        self.contentView.setPlaceholderText("")
        self.contentView.setStyleSheet("""
            QTextEdit {
                background: transparent;
                border: none;
                padding: 10;
                margin: 0;
            }
        """)
      
        # Input area
        self.inputContainer = QWidget()
        self.inputContainer.setObjectName("inputContainer")
        input_layout = QVBoxLayout()
        self.inputContainer.setLayout(input_layout)
        
        self.userInput = QLineEdit()
        self.userInput.setPlaceholderText('Type your message...')
        self.userInput.setClearButtonEnabled(True)
        self.userInput.setMinimumHeight(40) 
        input_layout.addWidget(self.userInput)
        
        content_layout.addWidget(top_bar)
        content_layout.addWidget(self.contentView)
        content_layout.addWidget(self.inputContainer)
        
        # Create splitter with invisible handle
        self.splitter = QSplitter(Qt.Horizontal, self)
        self.splitter.setHandleWidth(1)
        self.splitter.addWidget(self.sidebar)
        self.splitter.addWidget(self.contentArea)
        self.splitter.setSizes([220, 680])
        main_layout.addWidget(self.splitter)
        
        # Animation for input focus
        self.inputAnimation = QPropertyAnimation(self.inputContainer, b"styleSheet")
        self.inputAnimation.setDuration(300)

        # Other windows
        self.help_window = None
        self.setting_window = None

    def setupConnections(self):
        self.conversationList.itemClicked.connect(self.on_chat_clicked)
        self.newButton.clicked.connect(self.start_new_chat)
        self.searchContent.textChanged.connect(self.filter_conversations)
        self.userInput.returnPressed.connect(self.send_message)
        self.helpButton.clicked.connect(self.show_help)
        self.settingButton.clicked.connect(self.show_setting)
        self.apiModels.currentIndexChanged.connect(self.on_model_changed)
        self.userInput.installEventFilter(self)

    def setupAgent(self):
        self.agent_router = AgentRouter(self, self.current_model)
    
    def setupConfig(self):
        
        if hasattr(config, "hist_cache_path"):
            config._hist_cache = joblib.load(config.hist_cache_path)
            self.load_cached_conversations()
            if len(config._hist_cache['chats']) == 0:
                self.is_first_input = True
            else:
                self.is_first_input = False
        else:
            config.hist_cache_path = "cache/hist.pkl"
            config._hist_cache = {
                "next_id": 1,
                "chats": {}
            }
            self.is_first_input = True
            self.current_chat_id = None

    def on_chat_clicked(self, item): 
        chat_id = item.data(Qt.UserRole)
        if chat_id in config._hist_cache['chats'] and self.current_chat_id!= chat_id:
            self.current_chat_id = chat_id
            self.display_conversation(chat_id)
    
    def display_conversation(self, id):
        chat_dict = config._hist_cache['chats'][id]
        self.contentView.clear()
        
        for message in chat_dict['messages']:
            if message['sender'] == 'user':
                self.add_user_message(message['content'], message['time'], display_only=True)
            else:
                self.add_bot_message(message['content'],message['time'], display_only=True)
            
        self.scroll_to_bottom()

    def start_new_chat(self):
        self.contentView.clear()
        self.current_chat_id = config._hist_cache['next_id']
        config._hist_cache['next_id'] +=1

        new_chat = {
            "title": "New Chat",
            "messages": [],
        }
        config._hist_cache['chats'][self.current_chat_id] = new_chat
        
        item = QListWidgetItem(new_chat['title'])
        item.setData(Qt.UserRole, self.current_chat_id)
        self.conversationList.insertItem(0, item)
        
        self.conversationList.setCurrentItem(item)
        self.conversationList.scrollToItem(item)

        self.is_first_input = False
    
    def filter_conversations(self, text):
        for i in range(self.conversationList.count()):
            item = self.conversationList.item(i)
            item.setHidden(text.lower() not in item.text().lower())
    
    def send_message(self):
        message = self.userInput.text()
        if message:
            if not self.agent_router.before_route():
                self.userInput.clear()
                return

            if self.is_first_input or self.current_chat_id is None:
                self.start_new_chat()

            user_time = datetime.now().strftime("%H:%M:%S")
            self.add_user_message(message, user_time)
            self.userInput.clear()

            bot_msg = self.agent_router.route_return(message)
            bot_time = datetime.now().strftime("%H:%M:%S")
            self.add_bot_message(bot_msg, bot_time)
            
    
    def apply_minimal_theme(self):
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(40, 40, 40))
        palette.setColor(QPalette.WindowText, QColor(220, 220, 220))
        palette.setColor(QPalette.Base, QColor(30, 30, 30))
        palette.setColor(QPalette.AlternateBase, QColor(45, 45, 45))
        palette.setColor(QPalette.Text, QColor(240, 240, 240))
        palette.setColor(QPalette.Button, QColor(60, 60, 60))
        palette.setColor(QPalette.ButtonText, QColor(240, 240, 240))
        palette.setColor(QPalette.Highlight, QColor(76, 175, 80))
        palette.setColor(QPalette.HighlightedText, Qt.black)
        self.setPalette(palette)
        
        # Custom stylesheet for subtle boundaries
        self.setStyleSheet("""
            /* Base styling */
            QWidget {
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 14px;
                border: none;
                outline: none;
            }
            
            /* Input fields */
            QLineEdit, QPlainTextEdit {
                background-color: rgba(50, 50, 50, 150);
                color: #f0f0f0;
                border-radius: 6px;
                padding: 12px;
                selection-background-color: #4CAF50;
                selection-color: white;
            }
            
            QLineEdit:focus, QPlainTextEdit:focus {
                background-color: rgba(55, 55, 55, 200);
            }
                           
            QTextEdit {
                background: transparent;
                color: #f0f0f0;
                border: none;
                padding: 5px;
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 14px;
            }
            
            /* Buttons */
            QPushButton {
                background-color: rgba(80, 80, 80, 100);
                color: #c0c0c0;
                padding: 6px 12px;
                border-radius: 6px;
            }
            
            QPushButton:hover {
                background-color: rgba(80, 80, 80, 100);
                color: white;
            }
            
            /* Combo box */
            QComboBox {
                background-color: rgba(50, 50, 50, 150);
                color: #f0f0f0;
                border-radius: 6px;
                padding: 6px;
                min-width: 120px;
            }
            
            QComboBox:hover {
                background-color: rgba(60, 60, 60, 200);
            }
            
            QComboBox::drop-down {
                border: none;
                width: 20px;
            }
            
            /* List widget */
            QListWidget {
                background-color: transparent;
                color: #e0e0e0;
                show-decoration-selected: 1;
            }
            
            QListWidget::item {
                padding: 10px;
                border-radius: 6px;
                background-color: rgba(60, 60, 60, 80);
                margin: 0;
            }
            
            QListWidget::item:hover {
                background-color: rgba(80, 80, 80, 120);
            }
            
            QListWidget::item:selected {
                background-color: rgba(76, 175, 80, 150);
                color: white;
            }
            
            /* Splitter */
            QSplitter::handle {
                background-color: rgba(60, 60, 60, 50);
                width: 1px;
            }
            
            /* Scrollbars */
            QScrollBar:vertical {
                border: none;
                background: transparent;
                width: 8px;
                margin: 0;
            }
            
            QScrollBar::handle:vertical {
                background: rgba(100, 100, 100, 100);
                min-height: 20px;
                border-radius: 4px;
            }
            
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0;
                background: none;
            }
                           
            QTextEdit {
                background: rgba(0, 0, 0, 0.2);
                border-radius: 8px;
            }
            
            #inputContainer {
                background: rgba(0, 0, 0, 0.1);
                border-radius: 8px;
                border: 1px solid rgba(255, 255, 255, 0.1);
            }
                           
            #topBar {
                background: rgba(0, 0, 0, 0.1);
                border-radius: 8px;
                border: 1px solid rgba(255, 255, 255, 0.1);
            }
        """)
        
    def add_user_message(self, message, time, display_only=False):
        if not display_only:
            self.store_message('user', message, time)

        cleaned_message = message.replace("\n", "<br>").replace("  ", "&nbsp;&nbsp;")
        bold_txt = f"""
        <br>
        <div>
            <b><font size='4'>USER   {time}</font></b><br>
            <div>
                {cleaned_message}
            </div>
        </div>
        <br>
        """
        self.contentView.insertHtml(bold_txt)

        if not display_only:
            self.scroll_to_bottom()


    def add_bot_message(self, message,time, display_only=False):
        if not display_only:
            self.store_message('bot', message, time)
        html_content = markdown.markdown(message)
        bold_txt = f"""
        <br>
        <div>
            <b><font size='4'>ASSISTANT   {time}</font></b><br>
            <div>
                {html_content}
            </div>
        </div>
        <br>
        """
        self.contentView.insertHtml(bold_txt)
        if not display_only:
            self.scroll_to_bottom()

    def store_message(self, sender, content, time):
        if self.current_chat_id in config._hist_cache['chats']:
            config._hist_cache['chats'][self.current_chat_id]['messages'].append({
                'sender': sender,
                'content': content,
                'time': time
            })
            
            if sender == 'user' and len(content) > 0:
                if len(config._hist_cache['chats'][self.current_chat_id]['messages']) == 1:
                    title = content[:30] + "..." if len(content) > 30 else content
                    config._hist_cache['chats'][self.current_chat_id]['title'] = title
                    
                    # Update the list item
                    for i in range(self.conversationList.count()):
                        item = self.conversationList.item(i)
                        if item.data(Qt.UserRole) == self.current_chat_id:
                            item.setText(title)
                            break

    def scroll_to_bottom(self):
        scrollbar = self.contentView.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())
        QTimer.singleShot(50, lambda: scrollbar.setValue(
            scrollbar.maximum()
        ))
    
    def show_help(self):
        if self.help_window is None:
            self.help_window = HelpWindow(self)
            self.help_window.move(
                self.geometry().center() - self.help_window.geometry().center()
            )
            self.help_window.show()
            self.help_window.raise_()
        else:
            self.help_window.close()
            self.help_window = None
    
    def show_setting(self):
        if self.setting_window is None:
            self.setting_window = SettingWindow(self)
            self.setting_window.move(
                self.geometry().center() - self.setting_window.geometry().center()
            )
            self.setting_window.show()
            self.setting_window.raise_()
        else:
            self.setting_window.close()
            self.setting_window = None

    def on_model_changed(self, index):
        selected_model = self.apiModels.currentText()
        self.current_model = selected_model
        self.agent_router.switch_model(self.current_model)
    
    def eventFilter(self, obj, event):
        if obj == self.userInput:
            if event.type() == event.Type.FocusIn:
                self.animate_input_focus(True)
            elif event.type() == event.Type.FocusOut:
                self.animate_input_focus(False)
        return super().eventFilter(obj, event)
    
    def animate_input_focus(self, has_focus):
        self.inputAnimation.stop()
        self.inputAnimation.setStartValue(self.inputContainer.styleSheet())
        
        if has_focus:
            self.inputAnimation.setEndValue("""
                #inputContainer {
                    border-radius: 8px;
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 rgba(60, 60, 60, 180), 
                        stop:1 rgba(45, 45, 45, 200));
                    padding: 2px;
                    border: 1px solid rgba(100, 100, 100, 80);
                }
            """)
        else:
            self.inputAnimation.setEndValue("""
                #inputContainer {
                    border-radius: 8px;
                    background: rgba(50, 50, 50, 150);
                    padding: 1px;
                    border: 1px solid rgba(80, 80, 80, 50);
                }
            """)
        self.inputAnimation.start()
    
    def load_cached_conversations(self):
        """Load and display cached conversations from history file"""
        if not config._hist_cache['chats']:
            return
        
        self.conversationList.clear()
        
        sorted_chats = sorted(
            config._hist_cache['chats'].items(),
            key=lambda x: x[0],
            reverse=True
        )
        
        for chat_id, chat_data in sorted_chats:
            item = QListWidgetItem(chat_data['title'])
            item.setData(Qt.UserRole, chat_id)
            self.conversationList.addItem(item)
        
        if sorted_chats:
            self.conversationList.setCurrentRow(0)
            self.current_chat_id = sorted_chats[0][0]
            self.display_conversation(self.current_chat_id)