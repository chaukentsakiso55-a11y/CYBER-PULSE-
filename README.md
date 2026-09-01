# Cyber Pulse Website

Official source for the Cyber Pulse public website.

## Production source

The public landing page is `index.html`. It is a self-contained HTML/CSS/JavaScript build so it can run on GitHub Pages or Firebase Hosting from the same repository.

## GitHub Pages

Repository: `chaukentsakiso55-a11y/CYBER-PULSE-`

Expected project-site URL when GitHub Pages is enabled from `main` / repository root:

`https://chaukentsakiso55-a11y.github.io/CYBER-PULSE-/`

## Firebase Hosting

Firebase project alias: `studylock-family`

Deployment files:
- `.firebaserc`
- `firebase.json`

After the Firebase project has a registered Web App, deploy from an authenticated Firebase CLI session with:

```bash
firebase deploy --only hosting
```

The website checks Firebase Hosting's reserved `/__/firebase/init.json` endpoint first, so a Firebase-hosted deployment can load the project's Web App configuration automatically.

## Authentication

The Cyber Pulse Identity Portal supports:
- Email/password
- Google
- Facebook
- Password reset
- Persistent or session authentication

Before production sign-in works, register a Firebase Web App in the `studylock-family` project and enable the required Authentication providers. Facebook also requires its provider credentials to be configured in Firebase Authentication.

Never commit Firebase Admin SDK service-account credentials or private OAuth secrets to this repository.

## Custom domain

A custom domain can be connected through Firebase Hosting. After DNS verification, add the final domain to Firebase Authentication's authorized domains and configure OAuth redirects as required for Google/Facebook sign-in.

## Search discovery

The repository includes `robots.txt` and `sitemap.xml`. Update the sitemap URLs when the final custom domain becomes the canonical site.
