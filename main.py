from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QPushButton,
    QProgressBar,
    QLabel,
    QLineEdit,
    QFileDialog,
    QRadioButton,
)
from PyQt5.QtCore import QThread, pyqtSignal
import sys
import cifrador
import os


class CifradoThread(QThread):
    progress_signal = pyqtSignal(int)

    def __init__(self, accion, clave, ruta):
        super().__init__()
        self.accion = accion
        self.clave = clave
        self.ruta = ruta

    def run(self):
        fernet = cifrador.obtener_fernet(self.clave)

        if os.path.isdir(self.ruta):
            archivos = list(os.walk(self.ruta))
            total_archivos = len(archivos)
            for i, (dirpath, dirnames, archivos) in enumerate(archivos):
                for nombre_archivo in archivos:
                    archivo = os.path.join(dirpath, nombre_archivo)
                    cifrador.transformar_archivo(self.accion, fernet, archivo)
                self.progress_signal.emit((i + 1) / total_archivos * 100)
        else:
            cifrador.transformar_archivo(self.accion, fernet, self.ruta)
            self.progress_signal.emit(100)


class AppDemo(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(300, 200)

        layout = QVBoxLayout()

        self.btn_file = QPushButton("Seleccionar archivo")
        self.btn_file.clicked.connect(self.abrir_archivo)
        layout.addWidget(self.btn_file)

        self.btn_dir = QPushButton("Seleccionar carpeta")
        self.btn_dir.clicked.connect(self.abrir_carpeta)
        layout.addWidget(self.btn_dir)

        self.label = QLabel("Ruta del archivo o carpeta")
        layout.addWidget(self.label)

        self.key_field = QLineEdit()
        self.key_field.setPlaceholderText("Introduce la clave para el cifrado")
        layout.addWidget(self.key_field)

        self.encrypt_option = QRadioButton("Cifrar")
        self.decrypt_option = QRadioButton("Descifrar")
        layout.addWidget(self.encrypt_option)
        layout.addWidget(self.decrypt_option)

        self.start_btn = QPushButton("Iniciar")
        self.start_btn.clicked.connect(self.cifrar_descifrar)
        layout.addWidget(self.start_btn)

        self.progress = QProgressBar()
        layout.addWidget(self.progress)

        self.close_btn = QPushButton("Cerrar")
        self.close_btn.clicked.connect(self.close)
        layout.addWidget(self.close_btn)

        self.setLayout(layout)

    def abrir_archivo(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getOpenFileName(
            self, "QFileDialog.getOpenFileName()", "", "All Files (*)", options=options
        )
        if file_name:
            self.label.setText(file_name)

    def abrir_carpeta(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        dir_name = QFileDialog.getExistingDirectory(self, "Seleccionar Directorio")
        if dir_name:
            self.label.setText(dir_name)

    def cifrar_descifrar(self):
        accion = "cifrar" if self.encrypt_option.isChecked() else "descifrar"
        ruta = self.label.text()
        clave = self.key_field.text()

        self.thread = CifradoThread(accion, clave, ruta)
        self.thread.progress_signal.connect(self.progress.setValue)
        self.thread.start()


app = QApplication(sys.argv)

demo = AppDemo()
demo.show()

sys.exit(app.exec_())
