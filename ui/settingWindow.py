from PySide6.QtWidgets import (QWidget, QVBoxLayout, QPushButton, 
                              QFormLayout, QHBoxLayout, QLineEdit, QLabel, 
                              QDoubleSpinBox, QSpinBox, QFrame, QSizePolicy)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QIcon
import cfg.config as config

class SettingWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Settings")
        self.setWindowModality(Qt.ApplicationModal)
        self.setFixedSize(400, 400)

        container = QFrame()
        container.setFrameShape(QFrame.Box)
        container.setLineWidth(2)
        container.setStyleSheet("background: rgba(0,0,0,210);")
        
        main_layout = QVBoxLayout(container)
        self.setLayout(QVBoxLayout())
        self.layout().addWidget(container)

        general_header = QLabel("General Settings")
        general_header.setFont(QFont('Arial', 30, QFont.Bold))
        general_header.setStyleSheet("background: transparent;")
        main_layout.addWidget(general_header)
        
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        line.setLineWidth(1)
        main_layout.addWidget(line)

        form_layout = QFormLayout()
        form_layout.setVerticalSpacing(12)
        form_layout.setHorizontalSpacing(15)
        form_layout.setContentsMargins(5, 5, 5, 5)
        form_layout.setLabelAlignment(Qt.AlignRight)  # Align labels to right

        self.models = config.models
        self.current_model = self.parent().apiModels.currentText()
        self.current_model_idx = self.parent().apiModels.currentIndex()

        self.api_key_fields = {}
        model_list = set([m.split('-')[0] for m in self.models])
        for model in model_list:
            row_layout = QHBoxLayout()
            api_key_edit = QLineEdit()
            
            saved_key = getattr(config, f"{model}_API_KEY", "")
            api_key_edit.setText(saved_key)
            api_key_edit.setPlaceholderText(f"Enter {model} API key")
            
            row_layout.addWidget(api_key_edit)
            row_layout.setSpacing(5)
            self.api_key_fields[model] = api_key_edit
            
            label = QLabel(f"{model} API Key:")
            label.setStyleSheet("background: transparent;")
            label.setMinimumWidth(120)  # Ensures consistent label width
            label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            form_layout.addRow(label, row_layout)
        
        main_layout.addLayout(form_layout)

        if self.current_model:
            main_layout.addSpacing(10)
            
            model_header = QLabel(f"{self.current_model.split('-')[0]} Options")
            model_header.setFont(QFont('Arial', 30, QFont.Bold))
            model_header.setStyleSheet("background: transparent;")
            main_layout.addWidget(model_header)
            
            line = QFrame()
            line.setFrameShape(QFrame.HLine)
            line.setFrameShadow(QFrame.Sunken)
            line.setLineWidth(1)
            main_layout.addWidget(line)

            options_layout = QFormLayout()
            options_layout.setVerticalSpacing(12)
            options_layout.setHorizontalSpacing(15)
            options_layout.setContentsMargins(5, 5, 5, 5)
            options_layout.setLabelAlignment(Qt.AlignRight)

            self.temperature = QDoubleSpinBox()
            self.temperature.setRange(0.0, 2.0)
            self.temperature.setSingleStep(0.1)
            self.temperature.setValue(getattr(config, f"{self.current_model.split('-')[0]}_TEMPERATURE", 0.7))
            options_layout.addRow("Temperature:", self.temperature)

            self.max_tokens = QSpinBox()
            self.max_tokens.setRange(1, 3000)
            self.max_tokens.setValue(getattr(config, f"{self.current_model.split('-')[0]}_MAX_TOKENS", 2048))
            options_layout.addRow("Max Tokens:", self.max_tokens)

            main_layout.addLayout(options_layout)

        main_layout.addStretch()

        button_layout = QHBoxLayout()
        button_layout.setContentsMargins(0, 15, 0, 0)
        
        save_button = QPushButton("Save")
        save_button.setFixedWidth(100)
        save_button.clicked.connect(self.save_settings)
        
        cancel_button = QPushButton("Close")
        cancel_button.setFixedWidth(100)
        cancel_button.clicked.connect(self.close)
        
        button_layout.addStretch()
        button_layout.addWidget(save_button)
        button_layout.addWidget(cancel_button)
        button_layout.addStretch()

        main_layout.addLayout(button_layout)
    
    
    def save_settings(self):
        for model, field in self.api_key_fields.items():
            key = field.text()
            if key:
                setattr(config, f"{model}_API_KEY", key)
        
        if self.current_model:
            setattr(config, f"{self.current_model.split('-')[0]}_TEMPERATURE", self.temperature.value())
            setattr(config, f"{self.current_model.split('-')[0]}_MAX_TOKENS", self.max_tokens.value())
        
        print("Settings saved!")