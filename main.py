# main.py
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QFileDialog, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget, QTableWidgetItem,
    QProgressBar, QMessageBox, QWidget, QLineEdit, QHeaderView
)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QIcon
import os


class FileManager(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Big File Eraser")
        self.resize(800, 60)

        # Central Widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Main Layout
        self.main_layout = QVBoxLayout(central_widget)

        # Header Buttons
        self.header_layout = QHBoxLayout()
        self.select_button = QPushButton("Select Folder")
        self.header_layout.addWidget(self.select_button)
        self.main_layout.addLayout(self.header_layout)

        # Search Bar
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Search files...")
        self.search_bar.setVisible(False)  # Initially hidden
        self.search_bar.textChanged.connect(self.filter_files)
        self.main_layout.addWidget(self.search_bar)

        # File Table
        self.file_table = QTableWidget()
        self.file_table.setColumnCount(3)
        self.file_table.setHorizontalHeaderLabels(["File Name", "Size", "Actions"])
        self.file_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)  # File Name column stretches
        self.file_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)  # Size column auto-resizes
        self.file_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)  # Actions column auto-resizes
        self.file_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.file_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.file_table.setSelectionMode(QTableWidget.SingleSelection)
        self.file_table.setVisible(False)  # Initially hidden
        self.main_layout.addWidget(self.file_table)

        # Progress Bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        self.progress_bar.setVisible(False)  # Initially hidden
        self.main_layout.addWidget(self.progress_bar)

        # Status Variables
        self.current_folder = None
        self.progress_timer = QTimer(self)  # Timer to hide the progress bar after 30 seconds
        self.progress_timer.setSingleShot(True)
        self.progress_timer.timeout.connect(self.hide_progress_bar)

        # Signal Connections
        self.select_button.clicked.connect(self.select_folder)

    def select_folder(self):
        """Open a dialog to select a folder and scan its contents."""
        folder = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder:
            self.current_folder = folder
            self.select_button.setVisible(False)  # Hide the select folder button
            self.file_table.setVisible(True)  # Show the file table
            self.search_bar.setVisible(True)  # Show the search bar
            self.scan_folder(folder)

    def scan_folder(self, folder):
        """Scan the selected folder for files and display them in the table."""
        self.file_table.setRowCount(0)
        self.progress_bar.setValue(0)
        self.progress_bar.setVisible(True)  # Show the progress bar
        self.progress_timer.stop()  # Stop any existing timer

        try:
            files = []
            total_files = sum(len(files) for _, _, files in os.walk(folder))
            processed_files = 0

            for root, _, filenames in os.walk(folder):
                for filename in filenames:
                    file_path = os.path.join(root, filename)
                    try:
                        size = os.path.getsize(file_path)
                        files.append((filename, size, file_path))
                    except Exception as e:
                        print(f"Error reading file {file_path}: {e}")

                    # Update progress
                    processed_files += 1
                    progress = int((processed_files / total_files) * 100)
                    self.progress_bar.setValue(progress)

            # Sort files by size (descending)
            files.sort(key=lambda x: x[1], reverse=True)

            # Populate the table
            for file_name, size, file_path in files:
                self.add_file_to_table(file_name, size, file_path)

            self.progress_bar.setValue(100)
            self.progress_timer.start(30000)  # Start the timer to hide the progress bar after 30 seconds
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to scan folder: {e}")
            self.progress_bar.setVisible(False)  # Hide the progress bar on error

    def add_file_to_table(self, file_name, size, file_path):
        """Add a file to the table."""
        row_position = self.file_table.rowCount()
        self.file_table.insertRow(row_position)

        # File Name
        name_item = QTableWidgetItem(file_name)
        name_item.setToolTip(file_path)
        name_item.setIcon(QIcon.fromTheme("text-x-generic"))  # Add file icon
        self.file_table.setItem(row_position, 0, name_item)

        # File Size
        size_item = QTableWidgetItem(self.human_readable_size(size))
        size_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.file_table.setItem(row_position, 1, size_item)

        # Actions
        delete_button = QPushButton("Delete")
        delete_button.setFixedWidth(100)  # Set button width to 100px
        delete_button.clicked.connect(lambda: self.delete_file(file_path, row_position))
        self.file_table.setCellWidget(row_position, 2, delete_button)

    def delete_file(self, file_path, row):
        """Delete the selected file after confirmation."""
        reply = QMessageBox.question(
            self, "Delete File", f"Are you sure you want to delete:\n{file_path}?",
            QMessageBox.Yes | QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            try:
                os.remove(file_path)
                self.file_table.removeRow(row)
                QMessageBox.information(self, "Success", f"File deleted: {file_path}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to delete file: {e}")

    def filter_files(self, text):
        """Filter files in the table based on the search text."""
        for row in range(self.file_table.rowCount()):
            item = self.file_table.item(row, 0)  # File Name column
            self.file_table.setRowHidden(row, text.lower() not in item.text().lower())

    def hide_progress_bar(self):
        """Hide the progress bar."""
        self.progress_bar.setVisible(False)

    @staticmethod
    def human_readable_size(size):
        """Convert file size to a human-readable format."""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size < 1024:
                return f"{size:.2f} {unit}"
            size /= 1024
        return f"{size:.2f} PB"


if __name__ == "__main__":
    app = QApplication([])
    window = FileManager()
    window.show()
    app.exec()
