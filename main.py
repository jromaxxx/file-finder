# main.py
from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog, QPushButton, QTextEdit, QVBoxLayout, QWidget
from finder.scanner import scan_directory, find_duplicates, find_large_files

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AntiRata File Scanner")
        self.resize(800, 600)

        self.text_area = QTextEdit()
        self.button = QPushButton("Seleccionar carpeta")

        layout = QVBoxLayout()
        layout.addWidget(self.button)
        layout.addWidget(self.text_area)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.button.clicked.connect(self.select_folder)

    def select_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Seleccionar Carpeta")
        if folder:
            df = scan_directory(folder)
            dups = find_duplicates(df)
            self.text_area.append(f"Archivos duplicados encontrados: {len(dups)}")
            self.text_area.append(dups[['path', 'size']].to_string(index=False))

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
