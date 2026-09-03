import subprocess
import tempfile
from pathlib import Path
import sys

AUTO_FIX = Path(__file__).parent.parent / 'rules' / 'auto_fix.py'

def test_auto_fix_px():
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        f = tmp / 'test.xml'
        f.write_text('<TextView android:layout_width="100px" />')
        result = subprocess.run([sys.executable, str(AUTO_FIX), str(tmp)], capture_output=True, text=True)
        assert result.returncode == 0
        content = f.read_text()
        assert 'dp' in content
        assert 'px' not in content

def test_auto_fix_left_right():
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        f = tmp / 'test.xml'
        f.write_text('<TextView android:paddingLeft="16dp" />')
        result = subprocess.run([sys.executable, str(AUTO_FIX), str(tmp)], capture_output=True, text=True)
        assert result.returncode == 0
        content = f.read_text()
        assert 'paddingStart' in content
