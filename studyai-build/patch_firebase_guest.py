from pathlib import Path

p = Path("build-src/StudyAI-Android/app/src/main/assets/study-app.html")
s = p.read_text(encoding="utf-8")

s = s.replace(
'''      <button class="social-btn" onclick="socialLogin('Apple')"><span>🍎</span> Continue with Apple</button>
      <div class="auth-divider"><span>or sign in with email</span></div>''',
'''      <button class="social-btn" onclick="socialLogin('Apple')"><span>🍎</span> Continue with Apple</button>
      <button class="social-btn" onclick="guestLogin()"><span>👤</span> Continue as Guest</button>
      <div class="auth-divider"><span>or sign in with email</span></div>''')

s = s.replace(
'''      <button class="social-btn" onclick="socialLogin('Apple')"><span>🍎</span> Sign up with Apple</button>
      <div class="auth-divider"><span>or create with email</span></div>''',
'''      <button class="social-btn" onclick="socialLogin('Apple')"><span>🍎</span> Sign up with Apple</button>
      <button class="social-btn" onclick="guestLogin()"><span>👤</span> Continue as Guest</button>
      <div class="auth-divider"><span>or create with email</span></div>''')

s = s.replace(
'''    <!-- AI Backend -->
    <div class="card">''',
'''    <!-- Firebase -->
    <div class="card">
      <div class="settings-section-title">Firebase</div>
      <div class="settings-row" style="flex-direction:column;align-items:stretch;gap:8px">
        <div class="settings-left">
          <div class="settings-label">Account Connection</div>
          <div class="settings-desc" id="firebase-status-text">Checking Firebase account status…</div>
        </div>
        <button class="start-btn" style="padding:11px 0" onclick="testFirebaseConnection()">Test Firebase Connection</button>
      </div>
    </div>

    <!-- AI Backend -->
    <div class="card">''')

s = s.replace(
'''onclick="showToast('Password reset link sent to your email!','success')"''',
'''onclick="sendPasswordReset()"''')

start = s.index("function doLogin() {")
end = s.index("function loginSuccess(user) {")

auth = r'''const FIREBASE_API_KEY = "AIzaSyAuQemi7gtaXjTyZFyKeYot9GabTLkjMFE";
const FIREBASE_PROJECT_ID = "study-ai-d5141";
const FIREBASE_AUTH_BASE = "https://identitytoolkit.googleapis.com/v1/accounts";

async function firebaseAuthRequest(action, payload) {
  const res = await fetch(`${FIREBASE_AUTH_BASE}:${action}?key=${encodeURIComponent(FIREBASE_API_KEY)}`, {
    method:"POST",
    headers:{"Content-Type":"application/json"},
    body:JSON.stringify(payload)
  });
  const data = await res.json().catch(()=>({}));
  if(!res.ok) throw new Error(data?.error?.message || `Firebase HTTP ${res.status}`);
  return data;
}

function firebaseMessage(code) {
  const map={
    EMAIL_EXISTS:"That email is already registered.",
    EMAIL_NOT_FOUND:"Account not found.",
    INVALID_PASSWORD:"Incorrect password.",
    INVALID_LOGIN_CREDENTIALS:"Incorrect email or password.",
    USER_DISABLED:"This account has been disabled.",
    OPERATION_NOT_ALLOWED:"Email/password sign-in is not enabled in Firebase Authentication.",
    TOO_MANY_ATTEMPTS_TRY_LATER:"Too many attempts. Try again later."
  };
  return map[code] || code.replaceAll("_"," ").toLowerCase().replace(/^./,c=>c.toUpperCase());
}

function cachedProfile(uid, fallback={}) {
  try {
    const v=JSON.parse(localStorage.getItem("sai_profile_"+uid)||"null");
    if(v) return {...fallback,...v};
  } catch(e) {}
  return fallback;
}

function cacheProfile(user) {
  if(user?.firebaseUid && !user.isGuest) {
    localStorage.setItem("sai_profile_"+user.firebaseUid, JSON.stringify({
      name:user.name,email:user.email,initials:user.initials,
      stats:user.stats||{sessions:0,quizzes:0,streak:0}
    }));
  }
}

async function doLogin() {
  clearErrors();
  const email=document.getElementById("login-email").value.trim();
  const pass=document.getElementById("login-pass").value;
  let ok=true;
  if(!email||!email.includes("@")){fieldErr("login-email","login-email-err");ok=false;}
  if(pass.length<6){fieldErr("login-pass","login-pass-err");ok=false;}
  if(!ok) return;
  showToast("Connecting to Firebase…","");
  try {
    const a=await firebaseAuthRequest("signInWithPassword",{email,password:pass,returnSecureToken:true});
    const cached=cachedProfile(a.localId,{});
    const name=cached.name||a.displayName||email.split("@")[0];
    const initials=cached.initials||name.split(" ").map(w=>w[0]).join("").slice(0,2).toUpperCase()||"ST";
    loginSuccess({
      name,email:a.email||email,initials,firebaseUid:a.localId,idToken:a.idToken,
      refreshToken:a.refreshToken,expiresAt:Date.now()+(Number(a.expiresIn||3600)*1000),
      isGuest:false,stats:cached.stats||{sessions:0,quizzes:0,streak:1}
    });
    showToast("Firebase connected ✓","success");
  } catch(err) {
    const msg=firebaseMessage(err.message);
    document.getElementById("login-pass-err").textContent=msg;
    fieldErr("login-pass","login-pass-err");
    showToast(msg,"err");
  }
}

async function doSignup() {
  clearErrors();
  const name=document.getElementById("signup-name").value.trim();
  const email=document.getElementById("signup-email").value.trim();
  const pass=document.getElementById("signup-pass").value;
  const pass2=document.getElementById("signup-pass2").value;
  let ok=true;
  if(!name){fieldErr("signup-name","signup-name-err");ok=false;}
  if(!email||!email.includes("@")){fieldErr("signup-email","signup-email-err");ok=false;}
  if(pass.length<6){fieldErr("signup-pass","signup-pass-err");ok=false;}
  if(pass!==pass2){fieldErr("signup-pass2","signup-pass2-err");ok=false;}
  if(!ok) return;
  showToast("Creating Firebase account…","");
  try {
    const a=await firebaseAuthRequest("signUp",{email,password:pass,returnSecureToken:true});
    let idToken=a.idToken;
    try {
      const u=await firebaseAuthRequest("update",{idToken,displayName:name,returnSecureToken:true});
      if(u.idToken) idToken=u.idToken;
    } catch(e) {}
    const user={
      name,email:a.email||email,initials:name.split(" ").map(w=>w[0]).join("").slice(0,2).toUpperCase(),
      firebaseUid:a.localId,idToken,refreshToken:a.refreshToken,
      expiresAt:Date.now()+(Number(a.expiresIn||3600)*1000),isGuest:false,
      stats:{sessions:0,quizzes:0,streak:0}
    };
    cacheProfile(user);
    loginSuccess(user);
    showToast("Firebase account created ✓","success");
  } catch(err) {
    const msg=firebaseMessage(err.message);
    document.getElementById("signup-email-err").textContent=msg;
    fieldErr("signup-email","signup-email-err");
    showToast(msg,"err");
  }
}

function guestLogin() {
  const saved=JSON.parse(localStorage.getItem("sai_guest")||"null");
  const user=saved||{name:"Guest Student",email:"Guest mode",initials:"GS",isGuest:true,stats:{sessions:0,quizzes:0,streak:0}};
  localStorage.setItem("sai_guest",JSON.stringify(user));
  loginSuccess(user);
  showToast("Guest mode active","success");
}

function socialLogin(provider) {
  showToast(provider+" sign-in needs its provider enabled in Firebase Authentication","err");
}

async function sendPasswordReset() {
  if(!currentUser||currentUser.isGuest||!currentUser.email||!currentUser.email.includes("@")) {
    showToast("Password reset is unavailable in Guest mode","err"); return;
  }
  try {
    await firebaseAuthRequest("sendOobCode",{requestType:"PASSWORD_RESET",email:currentUser.email});
    showToast("Password reset email sent ✓","success");
  } catch(err) { showToast(firebaseMessage(err.message),"err"); }
}

async function testFirebaseConnection() {
  if(!currentUser){showToast("Sign in first","err");return;}
  if(currentUser.isGuest){showToast("Guest mode works without Firebase","success");return;}
  if(!currentUser.idToken){showToast("Firebase session missing — sign in again","err");return;}
  try {
    const d=await firebaseAuthRequest("lookup",{idToken:currentUser.idToken});
    if(d?.users?.length) showToast("Firebase connected ✓","success");
    else throw new Error("ACCOUNT_NOT_FOUND");
  } catch(err) { showToast("Firebase test failed: "+firebaseMessage(err.message),"err"); }
}

'''

s = s[:start] + auth + s[end:]

s = s.replace(
'''function loginSuccess(user) {
  currentUser=user; saveUser();
  updateAvatars(); applyPrefsToUI();''',
'''function loginSuccess(user) {
  currentUser=user; saveUser(); cacheProfile(user);
  if(user.isGuest) localStorage.setItem("sai_guest",JSON.stringify(user));
  updateAvatars(); applyPrefsToUI();''')

s = s.replace(
'''    const accs=JSON.parse(localStorage.getItem("sai_accounts")||"{}");
    if(currentUser.email&&accs[currentUser.email]) accs[currentUser.email]=currentUser;
    localStorage.setItem("sai_accounts",JSON.stringify(accs));
    saveUser(); updateAvatars(); refreshSettings();''',
'''    if(currentUser.isGuest) localStorage.setItem("sai_guest",JSON.stringify(currentUser));
    else cacheProfile(currentUser);
    saveUser(); updateAvatars(); refreshSettings();''')

s = s.replace(
'''  document.getElementById("settings-email").textContent=currentUser.email||"—";''',
'''  document.getElementById("settings-email").textContent=currentUser.email||"—";
  const fstatus=document.getElementById("firebase-status-text");
  if(fstatus) fstatus.textContent=currentUser.isGuest
    ? "Guest mode — no Firebase account required. Your data stays on this device."
    : `Connected to Firebase project ${FIREBASE_PROJECT_ID} as ${currentUser.email||"account"}.`;''')

p.write_text(s, encoding="utf-8")

g = Path("build-src/StudyAI-Android/app/build.gradle")
gs = g.read_text(encoding="utf-8")
gs = gs.replace("versionCode 1", "versionCode 2").replace("versionName '1.0.0'", "versionName '1.0.1'")
g.write_text(gs, encoding="utf-8")

print("Firebase + Guest patch applied")
