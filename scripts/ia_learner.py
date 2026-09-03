#!/usr/bin/env python3
"""
Módulo de IA para android-toolchain.
Analiza reportes históricos y genera nuevas reglas automáticamente.
"""
import os, json, re
from pathlib import Path
from collections import Counter

REPORTES_DIR = Path(os.environ.get('REPORTES_DIR', './reportes'))
RULES_FILE = Path(__file__).parent.parent / 'rules' / 'auditor_completo.py'

def cargar_reportes():
    """Carga todos los reportes_final.json disponibles."""
    reportes = []
    for f in REPORTES_DIR.rglob('reporte_final.json'):
        with open(f) as fp:
            reportes.append(json.load(fp))
    return reportes

def detectar_patrones(reportes):
    """Analiza violaciones recurrentes y sugiere nuevas reglas."""
    patrones = Counter()
    for r in reportes:
        for file in r.get('files', []):
            msg = file.get('msg', '')
            # Buscar mensajes de violaciones que no tienen una regla específica
            if 'px' in msg.lower():
                patrones['USO DE PX'] += 1
            elif 'sql' in msg.lower():
                patrones['SQL INJECTION'] += 1
            elif 'secret' in msg.lower():
                patrones['HARDCODED SECRET'] += 1
            elif 'world_readable' in msg.lower():
                patrones['WORLD_READABLE'] += 1
            elif 'allowbackup' in msg.lower():
                patrones['ALLOWBACKUP'] += 1
            elif 'exported' in msg.lower():
                patrones['EXPORTED COMPONENT'] += 1
    return patrones

def generar_nuevas_reglas(patrones, umbral=5):
    """Genera código Python para nuevas reglas si superan el umbral."""
    nuevas = []
    for patron, count in patrones.items():
        if count > umbral:
            # Crear una nueva regla dinámica (ejemplo)
            rule_id = f'S{len(nuevas)+200}'
            pattern_regex = {
                'USO DE PX': r'\d+px',
                'SQL INJECTION': r'execSQL.*\+',
                'HARDCODED SECRET': r'= "[A-Za-z0-9+/=_-]{20,}"',
                'WORLD_READABLE': r'MODE_WORLD_READABLE',
                'ALLOWBACKUP': r'allowBackup="true"',
                'EXPORTED COMPONENT': r'exported="true"',
            }.get(patron, r'.*')
            nuevas.append(f"    '{rule_id}': (r'{pattern_regex}', '{patron} detectado (auto-generado)', 'error'),")
    return nuevas

def main():
    reportes = cargar_reportes()
    if not reportes:
        print("⚠️  No se encontraron reportes. Ejecuta primero auditorías.")
        return
    patrones = detectar_patrones(reportes)
    nuevas_reglas = generar_nuevas_reglas(patrones)
    if nuevas_reglas:
        # Añadir al auditor_completo.py
        with open(RULES_FILE, 'r') as f:
            contenido = f.read()
        # Insertar antes del último '}'
        indice = contenido.rfind('}')
        nuevo_contenido = contenido[:indice] + '\n    # Reglas auto-generadas por IA\n' + '\n'.join(nuevas_reglas) + '\n' + contenido[indice:]
        with open(RULES_FILE, 'w') as f:
            f.write(nuevo_contenido)
        print(f"✅ {len(nuevas_reglas)} nuevas reglas añadidas al auditor.")
    else:
        print("✅ No se detectaron patrones nuevos.")

if __name__ == "__main__":
    main()