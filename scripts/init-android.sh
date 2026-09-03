#!/bin/bash
# ============================================================
# INICIALIZAR NUEVO PROYECTO ANDROID CON TODO CONFIGURADO
# ============================================================
set -e
if [ -z "$1" ]; then
  echo "Uso: ./init-android.sh nombre-del-proyecto"
  exit 1
fi
PROJECT_NAME="$1"
TOKEN_FILE="$HOME/.audit_token"
if [ ! -f "$TOKEN_FILE" ]; then
  echo "🔐 No hay token. Genera uno en https://github.com/settings/tokens"
  read -sp "Pega tu token: " TOKEN
  echo "$TOKEN" > "$TOKEN_FILE"
  chmod 600 "$TOKEN_FILE"
fi
TOKEN=$(cat "$TOKEN_FILE")

echo "📁 Creando proyecto $PROJECT_NAME..."
mkdir -p "$PROJECT_NAME"
cd "$PROJECT_NAME" || exit 1

# Crear estructura básica
mkdir -p app/src/main/java/com/example/$PROJECT_NAME app/src/main/res/layout
cat > app/build.gradle << 'EOF'
apply plugin: 'com.android.application'
android {
    compileSdk 34
    defaultConfig {
        applicationId "com.example.$PROJECT_NAME"
        minSdk 21
        targetSdk 34
        versionCode 1
        versionName "1.0"
    }
}
dependencies {
    implementation 'androidx.appcompat:appcompat:1.6.1'
}
✅ Estructura creada.
📤 Creando repositorio en GitHub...
Reinitialized existing Git repository in /data/data/com.termux/files/home/android-toolchain/.git/
[main 99c8b38] Initial commit
 25 files changed, 486 insertions(+), 15 deletions(-)
 create mode 100644 "\"$WORKDIR\"/repos.txt"
 create mode 100644 .github/workflows/audit.yml
 create mode 100644 .github/workflows/google-actions.yml
 create mode 100644 .github/workflows/google-scanner.yml
 create mode 100644 benchmarks/AllowBackup.xml
 create mode 100644 benchmarks/Debuggable.xml
 create mode 100644 benchmarks/ExportedComponent.xml
 create mode 100644 benchmarks/HardcodedSecret.kt
 create mode 100644 benchmarks/SQLInjection.kt
 create mode 100644 benchmarks/WorldReadable.kt
 create mode 100644 osv-scanner.toml
 create mode 100644 reporte_final.json
 create mode 100644 repos.txt
 create mode 100755 rules/auditor_completo.py
 create mode 100755 rules/auditor_completo_backup.py
 create mode 100755 rules/auto_fix.py
 create mode 100644 rules/semgrep/android-security.yml
 create mode 100644 settings.gradle
 create mode 100644 tests/__pycache__/test_auditor.cpython-314-pytest-9.1.1.pyc
 create mode 100644 tests/__pycache__/test_auto_fix.cpython-314-pytest-9.1.1.pyc
 create mode 100644 tests/__pycache__/test_integration.cpython-314-pytest-9.1.1.pyc
branch 'main' set up to track 'origin/main'.
✅ Proyecto  creado y subido a GitHub.
🔗 https://github.com/pitist/