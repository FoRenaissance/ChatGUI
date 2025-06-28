# system
import os
import sys
import platform
import ctypes
import pprint
import joblib

# UI
import qdarktheme
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication
from ui.mainWindow import MainWindow

# Config
if not os.path.isfile('cfg/config.py'):
    open("cfg/config.py", "a", encoding="utf-8").close()
import cfg.config as config

def AboutQuit():
    joblib.dump(config._hist_cache, config.hist_cache_path)
    with open("cfg/config.py","w",encoding="utf-8") as configObj:
        for name in dir(config):
            if not name.startswith("_"):
                try:
                    value = eval(f"config.{name}")
                    configObj.write(f"{name} = {pprint.pformat(value)}\n")
                except:
                    pass

if __name__ == '__main__':
    appName = "ChatGUI"

    # Windows speical handler
    oper_sys = platform.platform()
    if oper_sys == 'Windows':
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(appName)
    
    qdarktheme.enable_hi_dpi()
    app = QApplication(sys.argv)
    iconPath = os.path.abspath(os.path.join(sys.path[0], 'icons', f"{appName}.png"))
    appIcon = QIcon(iconPath)
    app.setWindowIcon(appIcon)
    if not hasattr(config, "mainWindow") or config._mainWindow is None:
        config._mainWindow = MainWindow()
        qdarktheme.setup_theme('dark')
    else:
        config._mainWindow.bringToForeground(config._mainWindow)
    app.aboutToQuit.connect(AboutQuit)
    
    sys.exit(app.exec())