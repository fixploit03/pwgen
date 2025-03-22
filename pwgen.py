import sys
import random
import string
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QHBoxLayout, QCheckBox, QSpinBox, QPushButton, 
                            QLineEdit, QLabel, QMessageBox, QFileDialog, 
                            QTabWidget, QTextEdit)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
import secrets
import traceback
from datetime import datetime
import os
import webbrowser

class PasswordGenerator(QMainWindow):
    def __init__(self):
        """Initialize the PasswordGenerator instance."""
        super().__init__()
        try:
            self.init_ui()
            self.show_welcome_message()
            self.update_window_title()
        except Exception as e:
            self.handle_critical_error("Initialization Failed", "Failed to start PWGEN", e)

    def init_ui(self):
        """Set up the main user interface."""
        try:
            self.setFixedSize(725, 400)
            self.setWindowFlags(self.windowFlags() & ~Qt.WindowMaximizeButtonHint)
            self.setWindowIcon(QIcon(os.path.join("icon", "pwgen.ico")))
            main_widget = QWidget(self)
            self.setCentralWidget(main_widget)
            main_layout = QVBoxLayout(main_widget)
            self.tabs = QTabWidget()
            main_layout.addWidget(self.tabs)
            self.tab1 = QWidget()
            self.tabs.addTab(self.tab1, QIcon(os.path.join("icon", "password generator.ico")), "Password Generator")
            self.setup_tab1()
            self.tab2 = QWidget()
            self.tabs.addTab(self.tab2, QIcon(os.path.join("icon", "about.ico")), "About")
            self.setup_tab2()
            self.setStyleSheet("font-size: 16px;")
        except Exception as e:
            self.handle_critical_error("UI Initialization Error", "Failed to initialize UI", e)

    def setup_tab1(self):
        """Configure the Password Generator tab."""
        try:
            layout = QVBoxLayout(self.tab1)
            length_layout = QHBoxLayout()
            self.length_label = QLabel("Password Length:")
            self.length_spin = QSpinBox()
            self.length_spin.setRange(1, 999999)
            self.length_spin.setValue(16)
            self.length_spin.setStyleSheet("font-size: 18px;")
            length_layout.addWidget(self.length_label)
            length_layout.addWidget(self.length_spin)
            layout.addLayout(length_layout)
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
            self.password_display = QLineEdit()
            self.password_display.setReadOnly(True)
            self.password_display.setAlignment(Qt.AlignCenter)
            self.password_display.setStyleSheet("font-size: 20px; font-family: monospace;")
            layout.addWidget(self.password_display)
            top_button_layout = QHBoxLayout()
            self.generate_button = QPushButton("Generate Password")
            self.generate_button.setIcon(QIcon(os.path.join("icon", "generate.ico")))
            self.generate_button.setStyleSheet("font-size: 18px; padding: 5px;")
            self.generate_button.clicked.connect(self.generate_password)
            self.copy_button = QPushButton("Copy to Clipboard")
            self.copy_button.setIcon(QIcon(os.path.join("icon", "copy.ico")))
            self.copy_button.setStyleSheet("font-size: 18px; padding: 5px;")
            self.copy_button.clicked.connect(self.copy_to_clipboard)
            top_button_layout.addWidget(self.generate_button)
            top_button_layout.addWidget(self.copy_button)
            layout.addLayout(top_button_layout)
            bottom_button_layout = QHBoxLayout()
            self.clear_button = QPushButton("Clear")
            self.clear_button.setIcon(QIcon(os.path.join("icon", "clear.ico")))
            self.clear_button.setStyleSheet("font-size: 18px; padding: 5px;")
            self.clear_button.clicked.connect(self.clear_password)
            self.save_button = QPushButton("Save to File")
            self.save_button.setIcon(QIcon(os.path.join("icon", "save.ico")))
            self.save_button.setStyleSheet("font-size: 18px; padding: 5px;")
            self.save_button.clicked.connect(self.save_to_file)
            bottom_button_layout.addWidget(self.clear_button)
            bottom_button_layout.addWidget(self.save_button)
            layout.addLayout(bottom_button_layout)
            self.strength_label = QLabel("Password Strength: Not Generated")
            self.strength_label.setAlignment(Qt.AlignCenter)
            self.strength_label.setStyleSheet("font-size: 18px;")
            layout.addWidget(self.strength_label)
            powered_layout = QHBoxLayout()
            powered_layout.addStretch()
            powered_label = QLabel("Powered by Python")
            powered_label.setStyleSheet("font-size: 14px;")
            powered_layout.addWidget(powered_label)
            python_icon_label = QLabel()
            python_icon_label.setPixmap(QIcon(os.path.join("icon", "python.ico")).pixmap(24, 24))
            powered_layout.addWidget(python_icon_label)
            powered_layout.addStretch()
            layout.addLayout(powered_layout)
        except Exception as e:
            self.handle_critical_error("Tab 1 Setup Error", "Failed to setup Password Generator tab", e)

    def setup_tab2(self):
        """Configure the About tab."""
        try:
            layout = QVBoxLayout(self.tab2)
            about_text = QTextEdit()
            about_text.setReadOnly(True)
            about_text.setStyleSheet("font-size: 16px;")
            about_content = """
            <h2>PWGEN</h2>
            <p><b>Program Description:</b> PWGEN is a secure and user-friendly password generator program designed to assist users in creating strong and unique passwords. This program allows users to specify password length without practical limitations and select the character types to be included, such as uppercase letters, lowercase letters, digits, and special characters. PWGEN is equipped with features including a password strength indicator, copy-to-clipboard functionality, and the option to save passwords to text files. Built using Python and PyQt5, PWGEN utilizes the secrets module to ensure cryptographically secure password generation.</p>
            <p><b>Version:</b> 1.0</p>
            <p><b>Author:</b> Rofi (Fixploit03)</p>
            <p><b>GitHub Link:</b> <a href="https://github.com/fixploit03/pwgen">https://github.com/fixploit03/pwgen</a></p>
            """
            about_text.setHtml(about_content)
            layout.addWidget(about_text)
        except Exception as e:
            self.handle_critical_error("Tab 2 Setup Error", "Failed to setup About tab", e)

    def show_welcome_message(self):
        """Display welcome message with options to support developer or run the program."""
        try:
            msg = QMessageBox(self)
            msg.setWindowTitle("Welcome to PWGEN")
            msg.setText("Thank you for using PWGEN!\nWould you like to support the developer or start using the program?")
            msg.setStandardButtons(QMessageBox.NoButton)
            support_button = msg.addButton("Support Developer", QMessageBox.ActionRole)
            run_button = msg.addButton("Run", QMessageBox.AcceptRole)
            msg.exec_()
            if msg.clickedButton() == support_button:
                webbrowser.open("https://github.com/fixploit03/pwgen")
                self.show_welcome_message()
        except Exception as e:
            print(f"Failed to show welcome message: {str(e)}\n{traceback.format_exc()}")

    def update_window_title(self):
        """Set the window title with fixed size information."""
        try:
            self.setWindowTitle("PWGEN - 725x400")
        except Exception as e:
            print(f"Failed to update window title: {str(e)}\n{traceback.format_exc()}")
            self.setWindowTitle("PWGEN - Size Unknown")

    def generate_password(self):
        """Generate a secure password using string module character sets."""
        try:
            length = self.length_spin.value()
            if length <= 0:
                raise ValueError("Password length must be positive")
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
                characters += string.punctuation
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
                password[random.randint(0, length-1)] = secrets.choice(string.punctuation)
            password = ''.join(password)
            self.password_display.setText(password)
            self.update_strength_indicator(password)
        except ValueError as ve:
            self.show_error("Invalid Input", str(ve))
        except Exception as e:
            self.show_error("Generation Error", "Failed to generate password")
            print(f"Password generation failed: {str(e)}\n{traceback.format_exc()}")

    def clear_password(self):
        """Clear the displayed password and reset strength indicator."""
        try:
            self.password_display.clear()
            self.strength_label.setText("Password Strength: Not Generated")
            self.strength_label.setStyleSheet("font-size: 18px; color: black")
        except Exception as e:
            self.show_error("Clear Error", "Failed to clear password")
            print(f"Failed to clear password: {str(e)}\n{traceback.format_exc()}")

    def save_to_file(self):
        """Save the generated password to a file."""
        try:
            password = self.password_display.text()
            if not password:
                self.show_warning("Save Error", "No password to save!")
                return
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            default_filename = f"password_{timestamp}.txt"
            file_path, _ = QFileDialog.getSaveFileName(
                self, 
                "Save Password", 
                default_filename, 
                "Text Files (*.txt);;All Files (*)"
            )
            if not file_path:
                return
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, "w", encoding='utf-8') as f:
                f.write(f"Generated Password ({datetime.now().strftime('%Y-%m-%d %H:%M:%S')}):\n")
                f.write(password)
            self.show_info("Success", f"Password saved to {file_path}")
        except PermissionError as pe:
            self.show_error("Save Error", "Permission denied. Try a different location.")
            print(f"Permission denied while saving file: {str(pe)}\n{traceback.format_exc()}")
        except IOError as ioe:
            self.show_error("Save Error", f"Failed to write to file: {str(ioe)}")
            print(f"IO error while saving file: {str(ioe)}\n{traceback.format_exc()}")
        except Exception as e:
            self.show_error("Save Error", f"Failed to save password: {str(e)}")
            print(f"Failed to save password to file: {str(e)}\n{traceback.format_exc()}")

    def update_strength_indicator(self, password: str):
        """Update the password strength indicator based on the generated password."""
        try:
            if not password:
                self.strength_label.setText("Password Strength: Not Generated")
                self.strength_label.setStyleSheet("font-size: 18px; color: black")
                return
            score = 0
            length = len(password)
            if length >= 12: score += 2
            elif length >= 8: score += 1
            if self.upper_check.isChecked() and any(c.isupper() for c in password): score += 1
            if self.lower_check.isChecked() and any(c.islower() for c in password): score += 1
            if self.digits_check.isChecked() and any(c.isdigit() for c in password): score += 1
            if self.special_check.isChecked() and any(c in string.punctuation for c in password): score += 1
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
            self.strength_label.setText("Password Strength: Error")
            self.strength_label.setStyleSheet("font-size: 18px; color: red")
            print(f"Failed to update strength indicator: {str(e)}\n{traceback.format_exc()}")

    def copy_to_clipboard(self):
        """Copy the generated password to the clipboard."""
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
        except RuntimeError as re:
            self.show_error("Clipboard Error", str(re))
            print(f"Clipboard runtime error: {str(re)}\n{traceback.format_exc()}")
        except Exception as e:
            self.show_error("Clipboard Error", "Failed to copy to clipboard")
            print(f"Failed to copy to clipboard: {str(e)}\n{traceback.format_exc()}")

    def show_error(self, title: str, message: str):
        """Display an error message dialog."""
        try:
            QMessageBox.critical(self, title, message)
        except Exception as e:
            print(f"Failed to show error dialog: {str(e)}\n{traceback.format_exc()}")

    def show_warning(self, title: str, message: str):
        """Display a warning message dialog."""
        try:
            QMessageBox.warning(self, title, message)
        except Exception as e:
            print(f"Failed to show warning dialog: {str(e)}\n{traceback.format_exc()}")

    def show_info(self, title: str, message: str):
        """Display an information message dialog."""
        try:
            QMessageBox.information(self, title, message)
        except Exception as e:
            print(f"Failed to show info dialog: {str(e)}\n{traceback.format_exc()}")

    def handle_critical_error(self, title: str, message: str, exception: Exception):
        """Handle critical errors with detailed notification and program exit."""
        error_details = f"{str(exception)}\n{traceback.format_exc()}"
        try:
            QMessageBox.critical(self, title, f"{message}\n\nDetails: {str(exception)}")
        except Exception:
            print(f"Critical error: {title} - {message}\n{error_details}")
        sys.exit(1)

    @staticmethod
    def current_date_time() -> str:
        """Return the current date and time as a formatted string."""
        try:
            return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        except Exception as e:
            print(f"Failed to get current date time: {str(e)}\n{traceback.format_exc()}")
            return "Unknown Time"

def main():
    """Entry point for the PWGEN program."""
    try:
        app = QApplication(sys.argv)
        app.setStyleSheet("QWidget { font-size: 16px; }")
        window = PasswordGenerator()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        error_details = f"Fatal error: {str(e)}\n{traceback.format_exc()}"
        print(error_details)
        sys.exit(1)

if __name__ == '__main__':
    main()
