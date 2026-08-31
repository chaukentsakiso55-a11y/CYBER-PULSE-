# Firebase setup for Infinity OS V7

1. Add an Android app with package name `com.cyberpulse.infinityos`.
2. Download `google-services.json` into `android/app/google-services.json`.
3. Enable Anonymous Authentication for the foundation build.
4. Create Cloud Firestore.
5. Apply the included Firestore rules.
6. For desktop, create a Firebase Web App and fill `desktop/firebase_config.json` from the example template.

Do not commit service-account credentials or AI-provider secrets.
