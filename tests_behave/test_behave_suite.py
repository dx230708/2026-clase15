import subprocess
import os
import pytest

@pytest.mark.bdd
def test_run_behave_smoke():
    """Ejecuta los escenarios críticos (@smoke) y genera el JSON de reporte."""
    os.makedirs("reports", exist_ok=True)
    
    # Invocamos Behave mediante subprocess con formato JSON y Pretty
    resultado = subprocess.run(
        ["behave", "--tags=@smoke", "-f", "json", "-o", "reports/behave_smoke.json", "-f", "pretty"],
        capture_output=False,
        text=True
    )
    assert resultado.returncode == 0, "La suite BDD de Smoke Tests tuvo fallos en sus escenarios"

@pytest.mark.bdd
def test_run_behave_regression():
    """Ejecuta la regresión total de comportamiento (@regression)."""
    os.makedirs("reports", exist_ok=True)
    
    resultado = subprocess.run(
        ["behave", "--tags=@regression", "-f", "json", "-o", "reports/behave_regression.json", "-f", "pretty"],
        capture_output=False,
        text=True
    )
    assert resultado.returncode == 0, "La suite BDD de Regresión tuvo fallos en sus escenarios"