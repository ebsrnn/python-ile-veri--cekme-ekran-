import sys
import requests
import os

from PyQt5.QtWidgets import QWidget, QApplication, QTextEdit, QLabel, QPushButton, QVBoxLayout, QFileDialog, QHBoxLayout, QLineEdit
from bs4 import BeautifulSoup

class Pencere(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.yazi_alani = QTextEdit()
        self.veri_cek = QPushButton("Verileri Çek")
        self.kaydet = QPushButton("Kaydet")
        self.temizle = QPushButton("Temizle")

        h_box = QHBoxLayout()
        h_box.addWidget(self.temizle)
        h_box.addWidget(self.veri_cek)
        h_box.addWidget(self.kaydet)

        v_box = QVBoxLayout()
        v_box.addWidget(self.yazi_alani)
        v_box.addLayout(h_box)

        self.setLayout(v_box)
        self.setWindowTitle("IMDb")

        self.temizle.clicked.connect(self.yazi_temizle)
        self.veri_cek.clicked.connect(self.dosya_verilerini_cek)
        self.kaydet.clicked.connect(self.dosya_kaydet)

    def yazi_temizle(self):
        self.yazi_alani.clear()

    def dosya_verilerini_cek(self):
        url = "https://www.imdb.com/chart/top/"
        response = requests.get(url)
        html_icerigi = response.content
        soup = BeautifulSoup(html_icerigi, "html.parser")

        for i in soup.find_all("td", {"class": "titleColumn"}):
            self.yazi_alani.append(i.text)

    def dosya_kaydet(self):
        dosya_ismi, _ = QFileDialog.getSaveFileName(self, "Dosya Kaydet", os.getenv("HOME"))

        with open(dosya_ismi, "w") as file:
            file.write(self.yazi_alani.toPlainText())


app = QApplication(sys.argv)
pencere = Pencere()
pencere.show()
sys.exit(app.exec_())