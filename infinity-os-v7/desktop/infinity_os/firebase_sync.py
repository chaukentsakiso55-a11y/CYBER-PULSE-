from pathlib import Path
import json

class FirebaseSync:
    def __init__(self) -> None:
        self.config_path = Path(__file__).resolve().parents[1] / "firebase_config.json"

    def status(self) -> tuple[bool, str]:
        if not self.config_path.exists():
            return False, "Firebase not configured"
        try:
            config = json.loads(self.config_path.read_text(encoding="utf-8"))
        except Exception:
            return False, "Firebase config is invalid JSON"
        required = {"apiKey", "authDomain", "projectId"}
        if not required.issubset(config):
            return False, "Firebase config is incomplete"
        return True, f"Firebase project: {config['projectId']}"
