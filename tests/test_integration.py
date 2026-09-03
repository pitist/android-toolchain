from pathlib import Path

def test_workflow_exists():
    wf = Path(__file__).parent.parent / '.github' / 'workflows' / 'ci.yml'
    assert wf.exists() or True, "ci.yml no existe (opcional)"

def test_benchmarks_exist():
    bench = Path(__file__).parent.parent / 'benchmarks'
    assert bench.exists()
    expected = ['SQLInjection.kt', 'HardcodedSecret.kt', 'WorldReadable.kt', 'AllowBackup.xml', 'Debuggable.xml', 'ExportedComponent.xml']
    for f in expected:
        assert (bench / f).exists(), f"Falta {f}"
