from __future__ import annotations

from pathlib import Path
import json
import urllib.error
import urllib.request


class FirebaseSync:
    def __init__(self) -> None:
        self.config_path = Path(__file__).resolve().parents[1] / "firebase_config.json"

    def _config(self) -> dict:
        if not self.config_path.exists():
            raise RuntimeError("Firebase not configured")
        config = json.loads(self.config_path.read_text(encoding="utf-8"))
        required = {"apiKey", "projectId"}
        if not required.issubset(config):
            raise RuntimeError("Firebase config is incomplete")
        return config

    def status(self) -> tuple[bool, str]:
        try:
            config = self._config()
            return True, f"Firebase project: {config['projectId']}"
        except Exception as exc:
            return False, str(exc)

    def _post_json(self, url: str, payload: dict, token: str | None = None) -> dict:
        data = json.dumps(payload).encode("utf-8")
        headers = {"Content-Type": "application/json"}
        if token:
            headers["Authorization"] = f"Bearer {token}"
        request = urllib.request.Request(url, data=data, headers=headers, method="POST")
        try:
            with urllib.request.urlopen(request, timeout=20) as response:
                return json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")
            raise RuntimeError(f"Firebase HTTP {exc.code}: {detail[:180]}") from exc

    def sign_in_anonymously(self) -> tuple[str, str]:
        config = self._config()
        url = f"https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={config['apiKey']}"
        result = self._post_json(url, {"returnSecureToken": True})
        return result["localId"], result["idToken"]

    def sync_device(self, device_id: str, workspace: str) -> str:
        config = self._config()
        uid, token = self.sign_in_anonymously()
        url = (
            f"https://firestore.googleapis.com/v1/projects/{config['projectId']}"
            f"/databases/(default)/documents/users/{uid}/devices?documentId={device_id}"
        )
        payload = {
            "fields": {
                "deviceId": {"stringValue": device_id},
                "workspace": {"stringValue": workspace},
                "platform": {"stringValue": "desktop"}
            }
        }
        self._post_json(url, payload, token)
        return uid
