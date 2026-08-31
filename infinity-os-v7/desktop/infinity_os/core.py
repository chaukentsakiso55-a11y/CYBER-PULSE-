from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
import json
import uuid

@dataclass
class PermissionState:
    files: str = "ask"
    internet: str = "allow"
    notifications: str = "ask"
    microphone: str = "ask"
    camera: str = "ask"
    commands: str = "ask"

@dataclass
class InfinityState:
    device_id: str
    active_workspace: str = "Personal"
    preferred_provider: str = "Auto"
    permissions: PermissionState = field(default_factory=PermissionState)

class StateStore:
    def __init__(self) -> None:
        self.root = Path(__file__).resolve().parents[1] / "user_data"
        self.root.mkdir(parents=True, exist_ok=True)
        self.path = self.root / "state.json"

    def load(self) -> InfinityState:
        if not self.path.exists():
            state = InfinityState(device_id=str(uuid.uuid4()))
            self.save(state)
            return state
        data = json.loads(self.path.read_text(encoding="utf-8"))
        permissions = PermissionState(**data.get("permissions", {}))
        return InfinityState(device_id=data.get("device_id", str(uuid.uuid4())), active_workspace=data.get("active_workspace", "Personal"), preferred_provider=data.get("preferred_provider", "Auto"), permissions=permissions)

    def save(self, state: InfinityState) -> None:
        payload = {"device_id": state.device_id, "active_workspace": state.active_workspace, "preferred_provider": state.preferred_provider, "permissions": state.permissions.__dict__, "updated_at": datetime.now(timezone.utc).isoformat()}
        self.path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
