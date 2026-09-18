from pathlib import Path
import re

root = Path('build-src/StudyAI-Android')
htmlp = root / 'app/src/main/assets/study-app.html'
manifestp = root / 'app/src/main/AndroidManifest.xml'
buildp = root / 'app/build.gradle'
javap = root / 'app/src/main/java/com/cyberpulse/studyai/MainActivity.java'

html = htmlp.read_text(encoding='utf-8')
html = html.replace("\n      <button class=\"social-btn\" onclick=\"socialLogin('Google')\"><span>🌐</span> Continue with Google</button>", '')
html = html.replace("\n      <button class=\"social-btn\" onclick=\"socialLogin('Google')\"><span>🌐</span> Sign up with Google</button>", '')
html = html.replace("\n      <button class=\"social-btn\" onclick=\"socialLogin('Apple')\"><span>🍎</span> Continue with Apple</button>", '')
html = html.replace("\n      <button class=\"social-btn\" onclick=\"socialLogin('Apple')\"><span>🍎</span> Sign up with Apple</button>", '')
html = html.replace('or sign in with email', 'Sign in with email').replace('or create with email', 'Create account with email')
html = html.replace('StudyAI ✦', 'StudyAI').replace('Install Study AI', 'Install StudyAI').replace('Install StudyAI', 'Install StudyAI')
html = html.replace('📲 Install Study AI on your iPhone', '📲 Install StudyAI on your iPhone').replace('📲 Install StudyAI on your iPhone', '📲 Install StudyAI on your iPhone')
html = html.replace('Study AI connected', 'StudyAI connected')
html = html.replace('Study AI installed successfully! 🎉', 'StudyAI installed successfully! 🎉')
html = html.replace('Installing Study AI… 🚀', 'Installing StudyAI… 🚀')
html = html.replace('content="Study AI"', 'content="StudyAI"').replace('<title>Study AI</title>', '<title>StudyAI</title>').replace('<title>StudyAI ✦</title>', '<title>StudyAI</title>')

about = '''
    <!-- About App -->
    <div class="card">
      <div class="settings-section-title">About App</div>
      <div class="settings-row" style="display:block">
        <div class="settings-label" style="margin-bottom:8px">StudyAI</div>
        <div class="settings-desc" style="line-height:1.6;margin-bottom:10px">
          StudyAI is a Cyber Pulse educational app designed to help learners study smarter with AI support, subject hubs, quizzes, and guided learning content.
        </div>
        <div class="settings-desc" style="line-height:1.6;margin-bottom:10px">
          <strong>Owner:</strong> Cyber Pulse<br>
          <strong>Built by:</strong> Ntsakiso Chauke (Darthwolf), Founder, CEO and Lead Developer of Cyber Pulse<br>
          <strong>App purpose:</strong> AI-powered learning, subject study support, revision, and quiz practice for students.
        </div>
        <div class="settings-desc" style="line-height:1.6;margin-bottom:10px">
          <strong>Data & privacy:</strong> Email/password accounts use Firebase Authentication. Study questions and quiz-generation requests sent while online are processed by Google Gemini. Guest mode does not require a Firebase account, and local preferences/progress are stored on the device.
        </div>
        <div class="settings-desc" style="line-height:1.6;margin-bottom:10px">
          <strong>Cyber Pulse contacts:</strong><br>
          Email: Cyberpulse546@gmail.com<br>
          Email: Chaukentsakiso55@gmail.com<br>
          Phone: +27 72 427 1860<br>
          Phone: 078 826 5274
        </div>
        <div class="settings-desc" style="line-height:1.6">
          <strong>Developer contact:</strong><br>
          Ntsakiso Chauke (Darthwolf)<br>
          Email: Chaukentsakiso55@gmail.com<br>
          Phone: 078 826 5274
        </div>
      </div>
    </div>
'''

if 'settings-section-title">About App<' not in html:
    pattern = r'\n\s*<div style="text-align:center;color:var\(--dim\);font-size:12px;margin-bottom:24px">.*?</div>\n\s*</div>\n</div>\n\n<!-- ════════════════ SCRIPT'
    repl = '\n' + about + '''
    <div style="text-align:center;color:var(--dim);font-size:12px;margin-bottom:24px">
      StudyAI &nbsp;·&nbsp; v1.2.0 &nbsp;·&nbsp; A Cyber Pulse app built by Ntsakiso Chauke (Darthwolf)
    </div>
  </div>
</div>

<!-- ════════════════ SCRIPT'''
    html = re.sub(pattern, repl, html, flags=re.S)
else:
    html = re.sub(r'Study AI\s*&nbsp;·&nbsp;\s*v[^<]+', 'Study AI &nbsp;·&nbsp; v1.2.0 &nbsp;·&nbsp; A Cyber Pulse app built by Ntsakiso Chauke (Darthwolf)', html)

html = re.sub(r"\nfunction socialLogin\(provider\) \{.*?\n\}\n", "\n", html, flags=re.S)

if 'Content-Security-Policy' not in html:
    csp = '<meta http-equiv="Content-Security-Policy" content="default-src \'self\' data: blob:; style-src \'self\' \'unsafe-inline\'; script-src \'self\' \'unsafe-inline\'; img-src \'self\' data: blob:; connect-src https://generativelanguage.googleapis.com https://identitytoolkit.googleapis.com https://securetoken.googleapis.com; font-src \'self\' data:;">\n'
    html = html.replace('<meta name="viewport"', csp + '<meta name="viewport"', 1)

htmlp.write_text(html, encoding='utf-8')

manifest = manifestp.read_text(encoding='utf-8')
manifest = manifest.replace('android:label="Study AI"', 'android:label="StudyAI"')
manifest = manifest.replace('android:allowBackup="true"', 'android:allowBackup="false"')
manifest = manifest.replace('android:usesCleartextTraffic="true"', 'android:usesCleartextTraffic="false"')
manifestp.write_text(manifest, encoding='utf-8')

bg = buildp.read_text(encoding='utf-8')
bg = re.sub(r'versionCode\s+\d+', 'versionCode 4', bg)
bg = re.sub(r"versionName\s+'[^']+'", "versionName '1.2.0'", bg)
bg = bg.replace('minifyEnabled false', 'minifyEnabled true')
buildp.write_text(bg, encoding='utf-8')

java = javap.read_text(encoding='utf-8')
java = java.replace('StudyAIAndroid/1.0', 'StudyAIAndroid/1.2')
java = java.replace('settings.setAllowContentAccess(true);', 'settings.setAllowContentAccess(false);')
java = java.replace('settings.setMediaPlaybackRequiresUserGesture(false);', 'settings.setMediaPlaybackRequiresUserGesture(true);')
java = java.replace('CookieManager.getInstance().setAcceptThirdPartyCookies(webView, true);', 'CookieManager.getInstance().setAcceptThirdPartyCookies(webView, false);')
if 'settings.setMixedContentMode' not in java:
    java = java.replace('settings.setCacheMode(WebSettings.LOAD_DEFAULT);', 'settings.setCacheMode(WebSettings.LOAD_DEFAULT);\n        settings.setGeolocationEnabled(false);\n        settings.setMixedContentMode(WebSettings.MIXED_CONTENT_NEVER_ALLOW);')
if 'setFilterTouchesWhenObscured' not in java:
    java = java.replace('webView.setBackgroundColor(Color.rgb(15, 23, 42));', 'webView.setBackgroundColor(Color.rgb(15, 23, 42));\n        webView.setFilterTouchesWhenObscured(true);')
if 'WebResourceRequest' not in java:
    java = java.replace('import android.webkit.WebViewClient;', 'import android.webkit.WebViewClient;\nimport android.webkit.WebResourceRequest;')
if 'shouldOverrideUrlLoading' not in java:
    replacement = '''webView.setWebViewClient(new WebViewClient() {
            @Override
            public boolean shouldOverrideUrlLoading(WebView view, WebResourceRequest request) {
                String url = request.getUrl().toString();
                return !url.startsWith("file:///android_asset/");
            }

            @Override
            public boolean shouldOverrideUrlLoading(WebView view, String url) {
                return url == null || !url.startsWith("file:///android_asset/");
            }
        });'''
    java = java.replace('webView.setWebViewClient(new WebViewClient());', replacement)
javap.write_text(java, encoding='utf-8')

print('production patch applied')
