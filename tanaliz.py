import sys
import re
from datetime import date

import matplotlib
matplotlib.use('QtAgg') 
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt

from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QLineEdit, QComboBox, 
                             QPushButton, QTextEdit, QFrame, QRadioButton, QButtonGroup)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

class MplCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=3, dpi=100):
        self.fig, self.ax = plt.subplots(figsize=(width, height), dpi=dpi, layout="constrained")
        super(MplCanvas, self).__init__(self.fig)

class TurkaProApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Turka Kişi Analiz")
        self.setMinimumSize(1250, 950)
        self.is_dark_mode = False
        
        self.init_ui()
        self.apply_theme()
        self.center_window()

    def center_window(self):
        qr = self.frameGeometry()
        cp = self.screen().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def apply_theme(self):
        if not self.is_dark_mode:
            # --- GÜNDÜZ MODU: SILVER & MINT ---
            self.setStyleSheet("""
                QMainWindow { background-color: #f0f2f5; }
                QFrame#LeftBar { background-color: #e8ecef; border-right: 2px solid #cbd5e0; }
                QLabel { color: #4a5568; font-family: 'Inter', 'Segoe UI'; }
                QLabel#Header { color: #2d6a4f; font-size: 26px; font-weight: 900; }
                QLineEdit, QComboBox { 
                    background-color: #ffffff; border: 1px solid #cbd5e0; 
                    border-radius: 8px; padding: 10px; color: #2d3748; 
                }
                QPushButton#ActionBtn { 
                    background-color: #52b788; color: white; border-radius: 8px; 
                    padding: 15px; font-weight: bold; font-size: 15px; 
                }
                QPushButton#ActionBtn:hover { background-color: #40916c; }
                QTextEdit { 
                    background-color: #ffffff; border: 1px solid #cbd5e0; 
                    border-radius: 12px; padding: 20px; color: #1a202c; font-size: 15px; line-height: 1.6;
                }
            """)
            self.canvas.fig.patch.set_facecolor('#f0f2f5')
            self.canvas.ax.set_facecolor('#ffffff')
        else:
            # --- GECE MODU: ANTHRACITE MINT ---
            self.setStyleSheet("""
                QMainWindow { background-color: #1a1b1e; }
                QFrame#LeftBar { background-color: #25262b; border-right: 2px solid #373a40; }
                QLabel { color: #c1c2c5; font-family: 'Inter', 'Segoe UI'; }
                QLabel#Header { color: #63e6be; font-size: 26px; font-weight: 900; }
                QLineEdit, QComboBox { 
                    background-color: #2c2e33; border: 1px solid #373a40; 
                    border-radius: 8px; padding: 10px; color: #f8f9fa; 
                }
                QPushButton#ActionBtn { 
                    background-color: #63e6be; color: #1a1b1e; border-radius: 8px; 
                    padding: 15px; font-weight: bold; font-size: 15px; 
                }
                QTextEdit { 
                    background-color: #25262b; border: 1px solid #373a40; 
                    border-radius: 12px; padding: 20px; color: #e9ecef; font-size: 15px;
                }
            """)
            self.canvas.fig.patch.set_facecolor('#1a1b1e')
            self.canvas.ax.set_facecolor('#25262b')
        self.canvas.draw()

    def init_ui(self):
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QHBoxLayout(main_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        left_bar = QFrame()
        left_bar.setObjectName("LeftBar")
        left_bar.setFixedWidth(380)
        s_layout = QVBoxLayout(left_bar)
        s_layout.setContentsMargins(35, 40, 35, 40)

        header = QLabel("TURKA ANALİZ")
        header.setObjectName("Header")
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        s_layout.addWidget(header)

        # Tema Seçimi
        theme_box = QHBoxLayout()
        self.light_radio = QRadioButton("Gündüz (Silver)")
        self.dark_radio = QRadioButton("Gece (Mint)")
        self.light_radio.setChecked(True)
        self.light_radio.toggled.connect(self.toggle_theme)
        theme_box.addWidget(self.light_radio)
        theme_box.addWidget(self.dark_radio)
        s_layout.addLayout(theme_box)
        s_layout.addSpacing(20)

        self.gender_cb = QComboBox()
        self.gender_cb.addItems(["Erkek", "Kadın"])
        self.birth_input = QLineEdit()
        self.birth_input.setPlaceholderText("Örn: 15.05.1990")
        self.height_input = QLineEdit()
        self.height_input.setPlaceholderText("Boy (cm)")
        self.weight_input = QLineEdit()
        self.weight_input.setPlaceholderText("Kilo (kg)")

        for label, widget in [("Cinsiyet", self.gender_cb), ("Doğum Tarihi", self.birth_input), 
                              ("Boy (cm)", self.height_input), ("Kilo (kg)", self.weight_input)]:
            lbl = QLabel(label)
            lbl.setStyleSheet("font-weight: bold; margin-top: 5px;")
            s_layout.addWidget(lbl)
            s_layout.addWidget(widget)

        self.btn = QPushButton("DERİN ANALİZİ ÇIKART")
        self.btn.setObjectName("ActionBtn")
        self.btn.clicked.connect(self.start_analysis)
        s_layout.addWidget(self.btn)
        s_layout.addStretch()

        content = QWidget()
        c_layout = QVBoxLayout(content)
        self.canvas = MplCanvas(self)
        c_layout.addWidget(self.canvas)
        self.result = QTextEdit()
        self.result.setReadOnly(True)
        c_layout.addWidget(self.result)

        layout.addWidget(left_bar)
        layout.addWidget(content)

    def toggle_theme(self):
        self.is_dark_mode = self.dark_radio.isChecked()
        self.apply_theme()

    def get_deep_zodiac_info(self, d, m):
        z_map = {1:(20,"Oğlak","Kova"), 2:(19,"Kova","Balık"), 3:(20,"Balık","Koç"), 4:(20,"Koç","Boğa"),
                 5:(21,"Boğa","İkizler"), 6:(21,"İkizler","Yengeç"), 7:(22,"Yengeç","Aslan"), 8:(23,"Aslan","Başak"),
                 9:(23,"Başak","Terazi"), 10:(23,"Terazi","Akrep"), 11:(22,"Akrep","Yay"), 12:(21,"Yay","Oğlak")}
        
        limit, curr, nxt = z_map[m]
        name = curr if d <= limit else nxt
        
        # --- Detaylı Karakteristik Veritabanı ---
        details = {
            "Koç": {
                "ozellik": "Atılgan, enerjik, dürüst ama sabırsız.",
                "sosyal": "Ortamlarda doğal bir liderdir. Dobralığıyla bilinir, kısıtlanmaya gelemez.",
                "saglik": "Kafa bölgesi, gözler ve adrenal sistem hassastır. Migrene dikkat!",
                "motto": "Ben varım ve başlatıyorum!"
            },
            "Boğa": {
                "ozellik": "Güvenilir, estetik tutkunu, sabırlı ama inatçı.",
                "sosyal": "Sadık bir dosttur. Konforuna düşkündür, değişimden pek hoşlanmaz.",
                "saglik": "Boğaz, boyun ve tiroit bezleri ön plandadır. Şeker tüketimine dikkat!",
                "motto": "Sahip olduğum her şey benim gücümdür."
            },
            "İkizler": {
                "ozellik": "Entelektüel, meraklı, hızlı ama değişken ruhlu.",
                "sosyal": "İletişim ustasıdır. Bilgi toplamayı sever, sıkıcılıktan hızla uzaklaşır.",
                "saglik": "Akciğerler, eller ve sinir sistemi hassastır. Zihinsel yorgunluk görülebilir.",
                "motto": "Düşünüyorum, o halde paylaşıyorum."
            },
            "Yengeç": {
                "ozellik": "Şefkatli, korumacı, sezgisel ama alıngan.",
                "sosyal": "Ailesine ve geçmişine bağlıdır. Güvende hissetmediği yerden uzaklaşır.",
                "saglik": "Mide, göğüs kafesi ve sindirim sistemi. Duygusal açlığa dikkat!",
                "motto": "Hissediyorum, koruyorum ve besliyorum."
            },
            "Aslan": {
                "ozellik": "Cömert, yaratıcı, karizmatik ama bazen kibirli.",
                "sosyal": "Girdiği her yerde parlamak ister. Sevdiklerini bir aslan gibi korur.",
                "saglik": "Kalp, omurga ve sırt bölgesi. Tansiyon kontrolü önemlidir.",
                "motto": "Yönetiyorum ve sahnedeyim."
            },
            "Başak": {
                "ozellik": "Analitik, titiz, yardımsever ama aşırı eleştirel.",
                "sosyal": "Mükemmeliyetçidir. Detayları kimsenin göremediği şekilde yakalar.",
                "saglik": "Bağırsaklar ve sinir sistemi. Takıntılı kaygı (anksiyete) riski.",
                "motto": "Analiz ediyorum ve faydalı hale getiriyorum."
            },
            "Terazi": {
                "ozellik": "Adil, estetik, uyumlu ama kararsız.",
                "sosyal": "Yalnız kalmayı sevmez. Diplomasi ve nezaket onun en güçlü silahıdır.",
                "saglik": "Böbrekler, bel bölgesi ve cilt. Su tüketimi kritik önemdedir.",
                "motto": "Dengede kalıyorum ve güzelleştiriyorum."
            },
            "Akrep": {
                "ozellik": "Tutkulu, stratejik, dayanıklı ama kıskanç.",
                "sosyal": "Gizemli bir havası vardır. Güveni kazanmak zordur ama kazanınca vazgeçmez.",
                "saglik": "Üreme sistemi ve boşaltım. Dönüşüm kapasitesi yüksektir.",
                "motto": "Arzuluyorum ve derinleşiyorum."
            },
            "Yay": {
                "ozellik": "Maceracı, iyimser, bilge ama patavatsız.",
                "sosyal": "Özgürlük onun nefesidir. Yeni kültürler ve felsefeler keşfetmeye bayılır.",
                "saglik": "Kalçalar, uyluklar ve karaciğer. Spor yaralanmalarına açıktır.",
                "motto": "Anlıyorum ve uzaklara bakıyorum."
            },
            "Oğlak": {
                "ozellik": "Disiplinli, hırslı, ciddi ama mesafeli.",
                "sosyal": "Başarı odaklıdır. Statü ve saygınlık onun için çok önemlidir.",
                "saglik": "Kemikler, eklemler, dişler ve deri. Kalsiyum dengesi önemlidir.",
                "motto": "Kullanıyorum ve zirveye tırmanıyorum."
            },
            "Kova": {
                "ozellik": "Yenilikçi, hümanist, zeki ama aykırı.",
                "sosyal": "Toplumsal tabuları yıkmayı sever. Dost canlısı ama duygusal olarak mesafelidir.",
                "saglik": "Dolaşım sistemi, alt bacaklar ve bilekler. Varis riski.",
                "motto": "Biliyorum ve değiştiriyorum."
            },
            "Balık": {
                "ozellik": "Merhametli, sanatsal, hayalperest ama kurban psikolojisine yatkın.",
                "sosyal": "Empati yeteneği çok yüksektir. Dünyanın sertliğinden hayallerine kaçar.",
                "saglik": "Ayaklar, lenf sistemi ve bağışıklık. Hassas bünye.",
                "motto": "İnanıyorum ve birleşiyorum."
            }
        }
        return name, details[name]

    def start_analysis(self):
        try:
            parts = re.split(r'[./-]', self.birth_input.text())
            d, m, y = int(parts[0]), int(parts[1]), int(parts[2])
            h, w = float(self.height_input.text()), float(self.weight_input.text())
            gender = self.gender_cb.currentText()

            # Hesaplamalar
            age = date.today().year - y - ((date.today().month, date.today().day) < (m, d))
            bmi = w / ((h/100)**2)
            ideal_w = 22 * ((h/100)**2)
            water = w * 0.033
            
            z_name, z_info = self.get_deep_zodiac_info(d, m)

            # Grafik Güncelleme
            self.canvas.ax.clear()
            self.canvas.ax.bar(['Mevcut', 'İdeal'], [w, ideal_w], color=['#52b788', '#ced4da'])
            self.canvas.ax.set_title(f"{z_name} Analiz Grafiği", color='#2d6a4f' if not self.is_dark_mode else '#63e6be')
            self.canvas.draw()

            # Rapor Hazırlama
            report = f"""
{'-'*55}
🛡️ TURKA DERİN KARAKTER VE FİZİKSEL ANALİZ
{'-'*55}
👤 KİŞİSEL PROFİL:
• Kimlik: {gender} | Yaş: {age}
• Vücut Kitle Endeksi: {bmi:.2f} ({"Normal" if 18.5<bmi<25 else "Kontrol Gerekli"})
• Günlük Su İhtiyacı: {water:.1f} Litre
• İdeal Kilo Hedefi: {ideal_w:.1f} kg

✨ {z_name.upper()} BURCU DETAYLI KARAKTER PORTRESİ:
• Temel Karakter: {z_info['ozellik']}
• Sosyal Maske: {z_info['sosyal']}
• Yaşam Mottosu: "{z_info['motto']}"

🩺 MEDİKAL ASTROLOJİ & SAĞLIK:
• Hassas Bölgeler: {z_info['saglik']}
• Tavsiye: {age} yaşında bir {z_name} olarak, fiziksel direncinizi 
  artırmak için özellikle {z_info['saglik'].split('.')[0]} sağlığınıza 
  odaklanmalısınız.

💡 ANALİZ SONUCU:
{z_name} burcunun baskın enerjisiyle {gender} doğanız birleştiğinde, 
yaşamda genellikle "{z_info['ozellik'].split(',')[0]}" tavrınızla dikkat çekersiniz. 
Fiziksel olarak {w} kg ağırlığındasınız; bu durum burcunuzun getirdiği 
"{z_info['ozellik'].split()[-1]}" eğilimiyle birleşince beslenme disiplini 
sizin için hayati önem taşır.

{'-'*55}
"""
            self.result.setText(report)
        except Exception as e:
            self.result.setText(f"HATA: Giriş formatını kontrol edin!\n{e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TurkaProApp()
    window.show()
    sys.exit(app.exec())