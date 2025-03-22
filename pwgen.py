import sys
import random
import string
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QHBoxLayout, QCheckBox, QSpinBox, QPushButton, 
                            QLineEdit, QLabel, QMessageBox, QFileDialog)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
import secrets
import traceback
from datetime import datetime
import os

class PasswordGenerator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.update_window_title()

    def init_ui(self):
        """Initialize the user interface"""
        try:
            # Fix window size to 725x400 and disable maximize
            self.setFixedSize(725, 400)
            self.setWindowFlags(self.windowFlags() & ~Qt.WindowMaximizeButtonHint)

            # Set application icon
            icon_path = os.path.join("icon", "pwgen.ico")
            if os.path.exists(icon_path):
                self.setWindowIcon(QIcon(icon_path))
            else:
                print(f"Warning: Icon file not found at {icon_path}")

            # Main widget and layout
            main_widget = QWidget(self)
            self.setCentralWidget(main_widget)
            layout = QVBoxLayout(main_widget)

            # Set global font size
            self.setStyleSheet("font-size: 16px;")

            # Password length
            length_layout = QHBoxLayout()
            self.length_label = QLabel("Password Length:")
            self.length_spin = QSpinBox()
            self.length_spin.setRange(8, 128)
            self.length_spin.setValue(16)
            self.length_spin.setStyleSheet("font-size: 18px;")
            length_layout.addWidget(self.length_label)
            length_layout.addWidget(self.length_spin)
            layout.addLayout(length_layout)

            # Character type options
            self.upper_check = QCheckBox("Uppercase Letters (A-Z)")
            self.upper_check.setChecked(True)
            self.lower_check = QCheckBox("Lowercase Letters (a-z)")
            self.lower_check.setChecked(True)
            self.digits_check = QCheckBox("Digits (0-9)")
            self.digits_check.setChecked(True)
            self.special_check = QCheckBox("Special Characters (!@#$%^&*)")
            self.special_check.setChecked(True)
            layout.addWidget(self.upper_check)
            layout.addWidget(self.lower_check)
            layout.addWidget(self.digits_check)
            layout.addWidget(self.special_check)

            # Generated password display
            self.password_display = QLineEdit()
            self.password_display.setReadOnly(True)
            self.password_display.setAlignment(Qt.AlignCenter)
            self.password_display.setStyleSheet("font-size: 20px; font-family: monospace;")
            layout.addWidget(self.password_display)

            # Buttons - Top row (Generate and Copy)
            top_button_layout = QHBoxLayout()
            self.generate_button = QPushButton("Generate Password")
            self.generate_button.setStyleSheet("font-size: 18px; padding: 5px;")
            self.generate_button.clicked.connect(self.generate_password)
            
            self.copy_button = QPushButton("Copy to Clipboard")
            self.copy_button.setStyleSheet("font-size: 18px; padding: 5px;")
            self.copy_button.clicked.connect(self.copy_to_clipboard)
            
            top_button_layout.addWidget(self.generate_button)
            top_button_layout.addWidget(self.copy_button)
            layout.addLayout(top_button_layout)

            # Buttons - Bottom row (Clear and Save)
            bottom_button_layout = QHBoxLayout()
            self.clear_button = QPushButton("Clear")
            self.clear_button.setStyleSheet("font-size: 18px; padding: 5px;")
            self.clear_button.clicked.connect(self.clear_password)
            
            self.save_button = QPushButton("Save to File")
            self.save_button.setStyleSheet("font-size: 18px; padding: 5px;")
            self.save_button.clicked.connect(self.save_to_file)
            
            bottom_button_layout.addWidget(self.clear_button)
            bottom_button_layout.addWidget(self.save_button)
            layout.addLayout(bottom_button_layout)

            # Strength indicator
            self.strength_label = QLabel("Password Strength: Not Generated")
            self.strength_label.setAlignment(Qt.AlignCenter)
            self.strength_label.setStyleSheet("font-size: 18px;")
            layout.addWidget(self.strength_label)

            # Powered by Python with icon on the right
            powered_layout = QHBoxLayout()
            powered_layout.addStretch()
            
            powered_label = QLabel("Powered by Python")
            powered_label.setStyleSheet("font-size: 14px;")
            powered_layout.addWidget(powered_label)

            python_icon_path = os.path.join("icon", "python.ico")
            if os.path.exists(python_icon_path):
                python_icon_label = QLabel()
                python_icon_label.setPixmap(QIcon(python_icon_path).pixmap(24, 24))
                powered_layout.addWidget(python_icon_label)
            else:
                print(f"Warning: Python icon not found at {python_icon_path}")
            
            powered_layout.addStretch()
            layout.addLayout(powered_layout)

            # Connect resize event (though size is fixed, kept for consistency)
            self.resizeEvent = self.on_resize

        except Exception as e:
            self.show_error("UI Initialization Error", f"Failed to initialize UI: {str(e)}")
            self.log_error(e)

    def update_window_title(self):
        """Update window title with fixed size"""
        try:
            self.setWindowTitle("PWGEN - 725x400")
        except Exception as e:
            self.log_error(e)
            self.setWindowTitle("PWGEN - Size Unknown")

    def on_resize(self, event):
        """Handle window resize event (not applicable due to fixed size)"""
        self.update_window_title()
        super().resizeEvent(event)

    def generate_password(self):
        """Generate a secure password"""
        try:
            length = self.length_spin.value()
            
            if not any([self.upper_check.isChecked(), self.lower_check.isChecked(),
                       self.digits_check.isChecked(), self.special_check.isChecked()]):
                self.show_warning("Selection Error", "Please select at least one character type")
                return

            characters = ""
            if self.upper_check.isChecked():
                characters += string.ascii_uppercase
            if self.lower_check.isChecked():
                characters += string.ascii_lowercase
            if self.digits_check.isChecked():
                characters += string.digits
            if self.special_check.isChecked():
                characters += "!@#$%^&*()_+-=[]{}|;:,.<>?"

            if not characters:
                raise ValueError("No character set available")

            password = ''.join(secrets.choice(characters) for _ in range(length))
            password = list(password)
            if self.upper_check.isChecked():
                password[random.randint(0, length-1)] = secrets.choice(string.ascii_uppercase)
            if self.lower_check.isChecked():
                password[random.randint(0, length-1)] = secrets.choice(string.ascii_lowercase)
            if self.digits_check.isChecked():
                password[random.randint(0, length-1)] = secrets.choice(string.digits)
            if self.special_check.isChecked():
                password[random.randint(0, length-1)] = secrets.choice("!@#$%^&*()_+-=[]{}|;:,.<>?")
            password = ''.join(password)

            self.password_display.setText(password)
            self.update_strength_indicator(password)

        except Exception as e:
            self.show_error("Generation Error", "Failed to generate password")
            self.log_error(e)

    def clear_password(self):
        """Clear the generated password"""
        try:
            self.password_display.clear()
            self.strength_label.setText("Password Strength: Not Generated")
            self.strength_label.setStyleSheet("font-size: 18px; color: black")
        except Exception as e:
            self.show_error("Clear Error", "Failed to clear password")
            self.log_error(e)

    def save_to_file(self):
        """Save the generated password to a user-specified file"""
        try:
            password = self.password_display.text()
            if not password:
                self.show_warning("Save Error", "No password to save!")
                return

            # Open file dialog to choose location and filename
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            default_filename = f"password_{timestamp}.txt"
            file_path, _ = QFileDialog.getSaveFileName(
                self, 
                "Save Password", 
                default_filename, 
                "Text Files (*.txt);;All Files (*)"
            )

            # If user cancels the dialog, file_path will be empty
            if not file_path:
                return

            with open(file_path, "w") as f:
                f.write(f"Generated Password ({datetime.now().strftime('%Y-%m-%d %H:%M:%S')}):\n")
                f.write(password)
            
            self.show_info("Success", f"Password saved to {file_path}")
        except PermissionError:
            self.show_error("Save Error", "Permission denied. Try a different location or check file permissions.")
            self.log_error(PermissionError("Permission denied while saving file"))
        except Exception as e:
            self.show_error("Save Error", f"Failed to save password: {str(e)}")
            self.log_error(e)

    def update_strength_indicator(self, password: str):
        """Update password strength indicator"""
        try:
            score = 0
            length = len(password)

            if length >= 12: score += 2
            elif length >= 8: score += 1
            
            if self.upper_check.isChecked() and any(c.isupper() for c in password): score += 1
            if self.lower_check.isChecked() and any(c.islower() for c in password): score += 1
            if self.digits_check.isChecked() and any(c.isdigit() for c in password): score += 1
            if self.special_check.isChecked() and any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password): score += 1

            if score >= 5:
                strength = "Very Strong"
                color = "green"
            elif score >= 4:
                strength = "Strong"
                color = "blue"
            elif score >= 3:
                strength = "Moderate"
                color = "orange"
            else:
                strength = "Weak"
                color = "red"

            self.strength_label.setText(f"Password Strength: {strength}")
            self.strength_label.setStyleSheet(f"font-size: 18px; color: {color}")

        except Exception as e:
            self.log_error(e)
            self.strength_label.setText("Password Strength: Error")
            self.strength_label.setStyleSheet("font-size: 18px; color: red")

    def copy_to_clipboard(self):
        """Copy generated password to clipboard"""
        try:
            text = self.password_display.text()
            if not text:
                self.show_warning("Copy Error", "No password to copy!")
                return

            app = QApplication.instance()
            if app is None:
                raise RuntimeError("No QApplication instance found")
            app.clipboard().setText(text)
            self.show_info("Success", "Password copied to clipboard!")
        except Exception as e:
            self.show_error("Clipboard Error", "Failed to copy to clipboard")
            self.log_error(e)

    def show_error(self, title: str, message: str):
        """Show error message dialog"""
        QMessageBox.critical(self, title, message)

    def show_warning(self, title: str, message: str):
        """Show warning message dialog"""
        QMessageBox.warning(self, title, message)

    def show_info(self, title: str, message: str):
        """Show info message dialog"""
        QMessageBox.information(self, title, message)

    def log_error(self, exception: Exception):
        """Log error details for debugging"""
        with open("error_log.txt", "a") as f:
            f.write(f"Error occurred at {self.current_date_time()}:\n")
            f.write(f"{str(exception)}\n")
            f.write(f"{traceback.format_exc()}\n\n")

    @staticmethod
    def current_date_time() -> str:
        """Get current date and time"""
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def main():
    """Main application entry point"""
    try:
        app = QApplication(sys.argv)
        app.setStyleSheet("QWidget { font-size: 16px; }")
        window = PasswordGenerator()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        print(f"Fatal error: {str(e)}")
        print(traceback.format_exc())
        sys.exit(1)

if __name__ == '__main__':
    main()
