# Infinity OS V7 — Nexus

Infinity OS V7 Nexus is a cross-device AI workspace by Cyber Pulse. This repository contains a Windows desktop app, a native Android app, Firebase integration templates, and shared architecture notes.

## Workspace

- `desktop/` — Python desktop application using Tkinter and the standard library.
- `android/` — Kotlin + Jetpack Compose Android application.
- `firebase/` — Firestore rules, indexes, and Firebase setup notes.

## Firebase

Copy your Android `google-services.json` to `android/app/google-services.json`. For desktop, copy `desktop/firebase_config.example.json` to `desktop/firebase_config.json` and fill in your Firebase Web App configuration. Never commit service-account credentials or AI-provider secrets.

## Desktop

```powershell
cd desktop
py -3 main.py
```

## Android

Open the `android` folder in Android Studio, use JDK 17, add your `google-services.json`, enable Anonymous Authentication and Cloud Firestore in Firebase, then sync and run.
