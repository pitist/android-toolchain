import subprocess
import json
import sys
from pathlib import Path

AUDITOR = Path(__file__).parent.parent / 'rules' / 'auditor_completo.py'
BENCHMARKS = Path(__file__).parent.parent / 'benchmarks'
REPORTE = Path(__file__).parent.parent / 'reporte_final.json'

def test_auditor_sql():
    # Ejecutar auditor sobre benchmarks
    result = subprocess.run([sys.executable, str(AUDITOR), str(BENCHMARKS)], capture_output=True, text=True)
    assert result.returncode == 0, f"Auditor falló: {result.stderr}"
    # Verificar que el reporte existe
    assert REPORTE.exists(), f"No se encontró reporte en {REPORTE}"
    with open(REPORTE) as f:
        data = json.load(f)
    # La estructura real: files es una lista de objetos con 'rule' directamente
    found = any(
        item.get('rule') == 'S127'
        for item in data.get('files', [])
    )
    assert found, "No se detectó SQL Injection (regla S127)"

def test_auditor_secret():
    result = subprocess.run([sys.executable, str(AUDITOR), str(BENCHMARKS)], capture_output=True, text=True)
    assert result.returncode == 0
    assert REPORTE.exists()
    with open(REPORTE) as f:
        data = json.load(f)
    found = any(
        item.get('rule') == 'S128'
        for item in data.get('files', [])
    )
    assert found, "No se detectaron secretos hardcodeados (regla S128)"
