import json
import os
from aqt.qt import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QTextBrowser,
    QSplitter, Qt, QDialogButtonBox, QWidget, QTextEdit
)
from aqt import mw
import markdown
from aqt.utils import showInfo
from .config_manager import ConfigManager

class ConfigDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent or mw)
        self.setWindowTitle("Confetti Add-on Configuration")
        self.setWindowFlags(Qt.Window)
        self.setWindowModality(Qt.ApplicationModal)
        self.setGeometry(100, 100, 800, 500)

        main_layout = QHBoxLayout()

        left_panel = QVBoxLayout()
        self.settings_label = QLabel("Configuration Settings")
        left_panel.addWidget(self.settings_label)

        self.config_manager = ConfigManager("confetti")

        self.config_editor = QTextEdit()
        self.config_editor.setPlainText(json.dumps(self.config_manager.config, indent=4))
        self.config_editor.setMinimumSize(200, 200)
        self.config_editor.setMaximumWidth(400)
        left_panel.addWidget(self.config_editor, stretch=6)

        button_layout = QHBoxLayout()
        self.restore_button = QPushButton("Restore Defaults")
        self.restore_button.clicked.connect(self.restore_defaults)
        button_layout.addWidget(self.restore_button)

        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.save_config)
        button_layout.addWidget(self.save_button)

        left_panel.addLayout(button_layout)

        self.help_text = QTextBrowser()
        self.help_text.setOpenExternalLinks(True)
        self.help_text.setHtml(self.load_guide())
        self.help_text.setMinimumSize(200, 200)

        self.help_text.setStyleSheet("""
            QTextBrowser {
                background: transparent;
                border: none;
                padding: 2px; 
                margin: 2px; 
            }
            QScrollBar:vertical {
                border: none;
                background: transparent;
                width: 6px;
                margin: 0px 2px 0px 0px;
            }
            QScrollBar::handle:vertical {
                background: rgba(100, 100, 100, 0.4);
                min-height: 20px;
                border-radius: 3px;
            }
            QScrollBar::handle:vertical:hover {
                background: rgba(100, 100, 100, 0.7);
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                border: none;
                background: none;
            }
        """)

        splitter = QSplitter(Qt.Horizontal)
        left_widget = QWidget()
        left_widget.setLayout(left_panel)

        splitter.addWidget(left_widget)
        splitter.addWidget(self.help_text)

        initial_config_width = min(400, int(self.width() * 0.6))
        initial_guide_width = self.width() - initial_config_width
        splitter.setSizes([initial_config_width, initial_guide_width])

        def adjust_splitter():
            total_width = self.width()
            available_extra_width = max(0, total_width - 800)

            guide_extra = available_extra_width * (2.5 / 3.5)
            config_extra = available_extra_width * (1 / 3.5)

            new_config_width = min(400, initial_config_width + config_extra)
            new_guide_width = max(200, initial_guide_width + guide_extra)

            splitter.setSizes([new_config_width, new_guide_width])

        self.resizeEvent = lambda event: adjust_splitter()

        main_layout.addWidget(splitter)
        self.setLayout(main_layout)

        self.raise_()
        self.activateWindow()

    def load_guide(self):
        guide_path = os.path.join(mw.addonManager.addonsFolder(), "confetti", "config.md")
        try:
            with open(guide_path, "r", encoding="utf-8") as file:
                return markdown.markdown(file.read())
        except FileNotFoundError:
            return "<b>Configuration Guide Not Found.</b>"

    def save_config(self):
        try:
            new_config = json.loads(self.config_editor.toPlainText())
            
            # ✅ Ensure every trigger inherits global opacity if not explicitly set
            global_opacity = new_config.get("global_opacity", 0.8)
            for trigger in new_config.get("triggers", []):
                trigger["pattern"]["opacity"] = trigger["pattern"].get("opacity", global_opacity)
            
            self.config_manager.save_config(new_config)
            self.config_editor.setPlainText(json.dumps(new_config, indent=4))
            showInfo("Configuration Saved!")
        except json.JSONDecodeError:
            showInfo("Error: Invalid JSON format. Please check your input.")

    def restore_defaults(self):
        """Restore the configuration from config.json file."""
        config_path = os.path.join(mw.addonManager.addonsFolder(), "confetti", "config.json")

        try:
            with open(config_path, "r", encoding="utf-8") as file:
                default_config = json.load(file)

            self.config_manager.save_config(default_config)  
            self.config_editor.setPlainText(json.dumps(default_config, indent=4))  
            showInfo("Configuration has been restored to default settings.")

        except FileNotFoundError:
            showInfo("Error: config.json file not found.")
        except json.JSONDecodeError:
            showInfo("Error: config.json is not a valid JSON.")
