#!/usr/bin/env python3
import sys, json, re
from pathlib import Path
from collections import defaultdict

RULES = {
    # SQL Injection (captura execSQL con concatenación)
    'S127': (
        r'execSQL\s*\([^;]*\+[^;]*\)',
        'SQL Injection detectada (concatenación en execSQL)',
        'error'
    ),
    # Hardcoded secrets (cadenas largas con caracteres alfanuméricos + / = + _)
    'S128': (
        r'=\s*"[A-Za-z0-9+/=_-]{20,}"',
        'Hardcoded secret detectado',
        'error'
    ),
    # World Readable
    'S129': (
        r'MODE_WORLD_READABLE|MODE_WORLD_WRITEABLE',
        'Almacenamiento WORLD_READABLE/WRITEABLE inseguro',
        'error'
    ),
    # AllowBackup
    'S130': (
        r'android:allowBackup="true"',
        'allowBackup activado',
        'warning'
    ),
    # Debuggable
    'S131': (
        r'android:debuggable="true"',
        'debuggable activado en release',
        'error'
    ),
    # Exported
    'S132': (
        r'android:exported="true"',
        'Componente exportado sin protección',
        'warning'
    ),
    # px a dp
    'R02': (
        r'\d+px',
        'Uso de px',
        'error'
    ),
    # Left/Right
    'R04': (
        r'(padding|margin)(Left|Right)',
        'Usar Start/End para RTL',
        'warning'
    ),
}

class Auditor:
    def __init__(self, root):
        self.root = Path(root)
        self.reports = []

    def run(self):
        # Extensions: aseguramos .kt y .xml
        for ext in ['*.xml', '*.kt', '*.java', '*.gradle', '*.yml', '*.yaml', '*.md']:
            for f in self.root.rglob(ext):
                try:
                    content = f.read_text(errors='ignore')
                    for rule_id, (pat, msg, sev) in RULES.items():
                        if re.search(pat, content, re.DOTALL | re.IGNORECASE):
                            self.reports.append({'file': str(f), 'rule': rule_id, 'severity': sev, 'msg': msg})
                except:
                    pass
        return self._summary()

    def _summary(self):
        errors = sum(1 for r in self.reports if r['severity'] == 'error')
        warnings = len(self.reports) - errors
        debt = errors * 0.5 + warnings * 0.2
        score = max(0, 100 - errors * 5 - debt * 0.5)
        return {
            'meta': {
                'total': len(self.reports),
                'errors': errors,
                'warnings': warnings,
                'debt': round(debt, 1),
                'score': round(score, 1),
                'savings': round(debt * 50, 2)
            },
            'files': self.reports[:50]
        }

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python3 auditor_completo.py /ruta/al/proyecto")
        sys.exit(1)
    data = Auditor(sys.argv[1]).run()
    with open('reporte_final.json', 'w') as f:
        json.dump(data, f, indent=2)
    print(f"\n📊 Score: {data['meta']['score']}% | Deuda: {data['meta']['debt']}h | Ahorro: ${data['meta']['savings']}")
