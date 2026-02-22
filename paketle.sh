#!/bin/bash

# Değişkenler
APP_NAME="turka-analiz"
VERSION="1.0.0"
PACKAGE_DIR="${APP_NAME}_${VERSION}"
INSTALL_DIR="${PACKAGE_DIR}/opt/${APP_NAME}"
BIN_DIR="${PACKAGE_DIR}/usr/bin"
SHARE_DIR="${PACKAGE_DIR}/usr/share"

echo "📦 Paket yapısı oluşturuluyor..."
mkdir -p "$INSTALL_DIR"
mkdir -p "$BIN_DIR"
mkdir -p "${SHARE_DIR}/applications"
mkdir -p "${SHARE_DIR}/pixmaps"
mkdir -p "${PACKAGE_DIR}/DEBIAN"

# 1. Dosyaları kopyala
cp tanaliz.py "$INSTALL_DIR/"
cp icon.png "${SHARE_DIR}/pixmaps/${APP_NAME}.png"

# 2. Control dosyasını oluştur (Debian paket bilgisi)
cat <<EOT > "${PACKAGE_DIR}/DEBIAN/control"
Package: ${APP_NAME}
Version: ${VERSION}
Section: utils
Priority: optional
Architecture: all
Depends: python3, python3-pyqt6, python3-matplotlib, python3-numpy
Maintainer: mobilturka
Description: Turka Derin Karakter ve Fiziksel Analiz Aracı.
 PyQt6 ve Matplotlib kullanılarak geliştirilmiş analiz uygulaması.
EOT

# 3. Başlatıcı betiği oluştur (/usr/bin/turka-analiz)
cat <<EOT > "${BIN_DIR}/${APP_NAME}"
#!/bin/bash
python3 /opt/${APP_NAME}/tanaliz.py "\$@"
EOT
chmod +x "${BIN_DIR}/${APP_NAME}"

# 4. Masaüstü kısayolunu oluştur (Menu Entry)
cat <<EOT > "${SHARE_DIR}/applications/${APP_NAME}.desktop"
[Desktop Entry]
Name=Turka Analiz
Comment=Kişi ve Karakter Analiz Aracı
Exec=${APP_NAME}
Icon=${APP_NAME}
Terminal=false
Type=Application
Categories=Utility;
EOT

echo "🏗️ Paket derleniyor..."
dpkg-deb --build "$PACKAGE_DIR"

echo "✅ İşlem tamam! ${PACKAGE_DIR}.deb dosyası oluşturuldu."