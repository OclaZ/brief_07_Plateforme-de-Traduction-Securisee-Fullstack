import sys
from pathlib import Path

# Ajouter le dossier backend au PYTHONPATH
backend_path = Path(__file__).parent.parent
sys.path.insert(0, str(backend_path))