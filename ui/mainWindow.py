from functools import partial

# config
import cfg.config as config

# chat window
from ui.chatWidget import ChatWidget

# ui
import qdarktheme
from PySide6.QtGui import QGuiApplication, QAction
from PySide6.QtWidgets import QMainWindow

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        # Center Widget
        self.chat_widget= ChatWidget(self)
        self.setCentralWidget(self.chat_widget)
        # Menu Bar
        # self.createMenubar()
        # Size
        self.resize(QGuiApplication.primaryScreen().availableSize() * 3 /4)
        # Display
        self.show()

    def createMenubar(self):
        menubar = self.menuBar()
        
        file_menu = menubar.addMenu(config.thisTranslation['chat'])
        
        new_action = QAction(config.thisTranslation["openDatabase"], self)
        new_action.setShortcut("Ctrl+Shift+O")
        new_action.triggered.connect(self.chat_widget.openDatabase)
        file_menu.addAction(new_action)

        new_action = QAction(config.thisTranslation["newDatabase"], self)
        new_action.setShortcut("Ctrl+Shift+N")
        new_action.triggered.connect(self.chat_widget.newDatabase)
        file_menu.addAction(new_action)

        new_action = QAction(config.thisTranslation["saveDatabaseAs"], self)
        new_action.setShortcut("Ctrl+Shift+S")
        new_action.triggered.connect(lambda: self.chat_widget.newDatabase(copyExistingDatabase=True))
        file_menu.addAction(new_action)

        file_menu.addSeparator()

        # new_action = QAction(config.thisTranslation["fileManager"], self)
        # new_action.triggered.connect(self.openDatabaseDirectory)
        # file_menu.addAction(new_action)

        # new_action = QAction(config.thisTranslation["pluginDirectory"], self)
        # new_action.triggered.connect(self.openPluginsDirectory)
        # file_menu.addAction(new_action)

        # file_menu.addSeparator()

        new_action = QAction(config.thisTranslation["newChat"], self)
        new_action.setShortcut("Ctrl+N")
        new_action.triggered.connect(self.chat_widget.newData)
        file_menu.addAction(new_action)

        new_action = QAction(config.thisTranslation["saveChat"], self)
        new_action.setShortcut("Ctrl+S")
        new_action.triggered.connect(self.chat_widget.saveData)
        file_menu.addAction(new_action)

        new_action = QAction(config.thisTranslation["exportChat"], self)
        new_action.triggered.connect(self.chat_widget.exportData)
        file_menu.addAction(new_action)

        new_action = QAction(config.thisTranslation["printChat"], self)
        new_action.setShortcut("Ctrl+P")
        new_action.triggered.connect(self.chat_widget.printData)
        file_menu.addAction(new_action)

        file_menu.addSeparator()

        new_action = QAction(config.thisTranslation["readTextFile"], self)
        new_action.triggered.connect(self.chat_widget.openTextFileDialog)
        file_menu.addAction(new_action)

        file_menu.addSeparator()

        new_action = QAction(config.thisTranslation["countPromptTokens"], self)
        new_action.triggered.connect(self.chat_widget.num_tokens_from_messages)
        file_menu.addAction(new_action)

        file_menu.addSeparator()

        # Create a Exit action and add it to the File menu
        exit_action = QAction(config.thisTranslation["exit"], self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.setStatusTip(config.thisTranslation["exitTheApplication"])
        exit_action.triggered.connect(QGuiApplication.instance().quit)
        file_menu.addAction(exit_action)

        # Create customize menu
        customise_menu = menubar.addMenu(config.thisTranslation["customize"])

        openSettings = QAction(config.thisTranslation["configure"], self)
        openSettings.triggered.connect(self.chat_widget.showApiDialog)
        customise_menu.addAction(openSettings)

        customise_menu.addSeparator()

        new_action = QAction(config.thisTranslation["toggleDarkTheme"], self)
        new_action.triggered.connect(self.toggleTheme)
        customise_menu.addAction(new_action)

        # new_action = QAction(config.thisTranslation["toggleSystemTray"], self)
        # new_action.triggered.connect(self.toggleSystemTray)
        # customise_menu.addAction(new_action)

        new_action = QAction(config.thisTranslation["toggleMultilineInput"], self)
        new_action.setShortcut("Ctrl+L")
        new_action.triggered.connect(self.chat_widget.multilineButtonClicked)
        customise_menu.addAction(new_action)

        # new_action = QAction(config.thisTranslation["toggleRegexp"], self)
        # new_action.setShortcut("Ctrl+E")
        # new_action.triggered.connect(self.toggleRegexp)
        # customise_menu.addAction(new_action)

        # Create predefined context menu
        context_menu = menubar.addMenu(config.thisTranslation["predefinedContext"])
        for index, context in enumerate(config.predefinedContexts):
            contextAction = QAction(context, self)
            if index < 10:
                contextAction.setShortcut(f"Ctrl+{index}")
            contextAction.triggered.connect(partial(self.chat_widget.bibleChatAction, context))
            context_menu.addAction(contextAction)

        # Create a plugin menu
        # plugin_menu = menubar.addMenu(config.thisTranslation["plugins"])

        # pluginFolder = os.path.join(os.getcwd(), "plugins")
        # for index, plugin in enumerate(self.fileNamesWithoutExtension(pluginFolder, "py")):
        #     new_action = QAction(plugin, self)
        #     new_action.setCheckable(True)
        #     new_action.setChecked(False if plugin in config.chatGPTPluginExcludeList else True)
        #     new_action.triggered.connect(partial(self.updateExcludePluginList, plugin))
        #     plugin_menu.addAction(new_action)

        # Create a text selection menu
        # text_selection_menu = menubar.addMenu(config.thisTranslation["textSelection"])

        # new_action = QAction(config.thisTranslation["webBrowser"], self)
        # new_action.triggered.connect(self.chatGPT.webBrowse)
        # text_selection_menu.addAction(new_action)

        # new_action = QAction(config.thisTranslation["runAsPythonCommand"], self)
        # new_action.triggered.connect(self.chatGPT.runPythonCommand)
        # text_selection_menu.addAction(new_action)

        # new_action = QAction(config.thisTranslation["runAsSystemCommand"], self)
        # new_action.triggered.connect(self.chatGPT.runSystemCommand)
        # text_selection_menu.addAction(new_action)

        # Create About menu
        # about_menu = menubar.addMenu(config.thisTranslation["about"])

        # openSettings = QAction(config.thisTranslation["repository"], self)
        # openSettings.triggered.connect(lambda: webbrowser.open("https://github.com/eliranwong/ChatGUI"))
        # about_menu.addAction(openSettings)

        # about_menu.addSeparator()

        # new_action = QAction(config.thisTranslation["help"], self)
        # new_action.triggered.connect(lambda: webbrowser.open("https://github.com/eliranwong/ChatGUI/wiki"))
        # about_menu.addAction(new_action)

        # about_menu.addSeparator()

        # new_action = QAction(config.thisTranslation["donate"], self)
        # new_action.triggered.connect(lambda: webbrowser.open("https://www.paypal.com/paypalme/MarvelBible"))
        # about_menu.addAction(new_action)

    def toggleTheme(self):
        config.darkTheme = not config.darkTheme
        qdarktheme.setup_theme() if config.darkTheme else qdarktheme.setup_theme('light')

    def bringToForeground(self,window):
        if window and not (window.visible() and window.isActiveWindow()):
            window.raise_()
            if window.isVisible() and not window.isActiveWindow():
                window.hide()
            window.show()