from __future__ import annotations

import tkinter as tk
from tkinter import ttk

from .core import StateStore
from .firebase_sync import FirebaseSync
from .router import AIRouter


class InfinityApp:
    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title("Infinity OS V7 — Nexus")
        self.root.geometry("1180x760")
        self.root.minsize(980, 650)
        self.store = StateStore()
        self.state = self.store.load()
        self.router = AIRouter()
        self.firebase = FirebaseSync()
        self.workspace_var = tk.StringVar(value=self.state.active_workspace)
        self.provider_var = tk.StringVar(value=self.state.preferred_provider)
        self.status_var = tk.StringVar(value="Infinity Core ready")
        self._build()

    def run(self) -> None:
        self.root.mainloop()

    def _build(self) -> None:
        style = ttk.Style(self.root)
        if "clam" in style.theme_names():
            style.theme_use("clam")
        shell = ttk.Frame(self.root, padding=18)
        shell.pack(fill="both", expand=True)
        header = ttk.Frame(shell)
        header.pack(fill="x")
        ttk.Label(header, text="INFINITY OS", font=("Segoe UI", 24, "bold")).pack(side="left")
        ttk.Label(header, text="V7 · NEXUS", font=("Segoe UI", 12)).pack(side="left", padx=(12, 0), pady=(10, 0))
        ttk.Label(header, textvariable=self.status_var).pack(side="right", pady=(8, 0))
        command = ttk.Entry(shell, font=("Segoe UI", 13))
        command.pack(fill="x", pady=(18, 14), ipady=8)
        command.insert(0, "Ask AEGIS or search Infinity OS…")
        command.bind("<Return>", lambda _: self._route_command(command.get()))
        body = ttk.Panedwindow(shell, orient="horizontal")
        body.pack(fill="both", expand=True)
        nav = ttk.Frame(body, padding=12)
        content = ttk.Frame(body, padding=12)
        body.add(nav, weight=1)
        body.add(content, weight=4)
        ttk.Label(nav, text="NEXUS", font=("Segoe UI", 11, "bold")).pack(anchor="w", pady=(0, 8))
        for name in ["Command Center", "AEGIS", "Workspaces", "AI Router", "Memory", "Permissions", "Mesh", "Forge", "Settings"]:
            ttk.Button(nav, text=name, command=lambda n=name: self.status_var.set(f"{n} selected")).pack(fill="x", pady=3)
        hero = ttk.LabelFrame(content, text="Infinity Core", padding=18)
        hero.pack(fill="x")
        ttk.Label(hero, text="One intelligence layer across your devices", font=("Segoe UI", 18, "bold")).pack(anchor="w")
        ttk.Label(hero, text="AI routing · memory · permissions · sync · AEGIS agents", font=("Segoe UI", 11)).pack(anchor="w", pady=(4, 12))
        firebase_ok, firebase_text = self.firebase.status()
        ttk.Label(hero, text=("● " if firebase_ok else "○ ") + firebase_text).pack(anchor="w")
        grid = ttk.Frame(content)
        grid.pack(fill="both", expand=True, pady=(14, 0))
        grid.columnconfigure(0, weight=1); grid.columnconfigure(1, weight=1); grid.rowconfigure(0, weight=1); grid.rowconfigure(1, weight=1)
        self._workspace_card(grid).grid(row=0, column=0, sticky="nsew", padx=(0, 7), pady=(0, 7))
        self._router_card(grid).grid(row=0, column=1, sticky="nsew", padx=(7, 0), pady=(0, 7))
        self._permissions_card(grid).grid(row=1, column=0, sticky="nsew", padx=(0, 7), pady=(7, 0))
        self._mesh_card(grid).grid(row=1, column=1, sticky="nsew", padx=(7, 0), pady=(7, 0))

    def _workspace_card(self, parent: ttk.Frame) -> ttk.LabelFrame:
        box = ttk.LabelFrame(parent, text="Project Memory", padding=14)
        ttk.Label(box, text="Separate memory spaces keep contexts clean.").pack(anchor="w")
        combo = ttk.Combobox(box, textvariable=self.workspace_var, state="readonly", values=["Personal", "School", "Cyber Pulse", "Coding", "StudyLock", "Infinity OS"])
        combo.pack(fill="x", pady=10)
        ttk.Button(box, text="Switch workspace", command=self._save_workspace).pack(anchor="w")
        return box

    def _router_card(self, parent: ttk.Frame) -> ttk.LabelFrame:
        box = ttk.LabelFrame(parent, text="AI Router", padding=14)
        ttk.Label(box, text="Choose a provider or let Infinity decide.").pack(anchor="w")
        combo = ttk.Combobox(box, textvariable=self.provider_var, state="readonly", values=self.router.providers)
        combo.pack(fill="x", pady=10)
        ttk.Button(box, text="Save route", command=self._save_provider).pack(anchor="w")
        return box

    def _permissions_card(self, parent: ttk.Frame) -> ttk.LabelFrame:
        box = ttk.LabelFrame(parent, text="Permission Engine", padding=14)
        for name, value in self.state.permissions.__dict__.items():
            ttk.Label(box, text=f"{name.title()}: {value.upper()}").pack(anchor="w", pady=2)
        ttk.Label(box, text="Sensitive actions remain confirmation-gated in this foundation.").pack(anchor="w", pady=(10, 0))
        return box

    def _mesh_card(self, parent: ttk.Frame) -> ttk.LabelFrame:
        box = ttk.LabelFrame(parent, text="Infinity Mesh", padding=14)
        ttk.Label(box, text="Desktop device identity").pack(anchor="w")
        ttk.Label(box, text=self.state.device_id, font=("Consolas", 9)).pack(anchor="w", pady=(6, 10))
        ttk.Label(box, text="Firebase sync activates after configuration.").pack(anchor="w")
        ttk.Button(box, text="Sync device", command=self._sync_device).pack(anchor="w", pady=(10, 0))
        return box

    def _route_command(self, text: str) -> None:
        decision = self.router.choose(self.provider_var.get(), self.state.permissions.internet == "allow")
        self.status_var.set(f"{decision.provider}: {text[:55]}")

    def _save_workspace(self) -> None:
        self.state.active_workspace = self.workspace_var.get()
        self.store.save(self.state)
        self.status_var.set(f"Workspace: {self.state.active_workspace}")

    def _sync_device(self) -> None:
        try:
            uid = self.firebase.sync_device(self.state.device_id, self.workspace_var.get())
            self.status_var.set(f"Firebase sync complete: {uid[:10]}…")
        except Exception as exc:
            self.status_var.set(f"Firebase sync failed: {str(exc)[:65]}")

    def _save_provider(self) -> None:
        self.state.preferred_provider = self.provider_var.get()
        self.store.save(self.state)
        self.status_var.set(f"AI provider: {self.state.preferred_provider}")
