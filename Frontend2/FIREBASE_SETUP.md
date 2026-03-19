# Firebase Setup Guide

Follow these steps exactly to get authentication working.

---

## Step 1 — Create a Firebase Project

1. Go to **[https://console.firebase.google.com](https://console.firebase.google.com)**
2. Click **"Add project"**
3. Name it (e.g. `finova-app`) → Continue → Create project

---

## Step 2 — Register a Web App

1. On the Project Overview page, click the **`</>`** (Web) icon
2. Name it (e.g. `finova-web`) → Click **"Register app"**
3. You'll see a `firebaseConfig` object — **copy it**, you'll need it next

It looks like this:
```js
const firebaseConfig = {
  apiKey: "AIzaSy...",
  authDomain: "finova-app.firebaseapp.com",
  projectId: "finova-app",
  storageBucket: "finova-app.appspot.com",
  messagingSenderId: "123456789",
  appId: "1:123456789:web:abc123"
};
```

---

## Step 3 — Enable Authentication

1. In the Firebase Console sidebar → **Authentication** → **Get started**
2. Click **Sign-in method** tab
3. Enable **Email/Password**:
   - Click it → Toggle **Enable** → Save
4. Enable **Google**:
   - Click it → Toggle **Enable**
   - Add a support email → Save

---

## Step 4 — Add Authorized Domain (if needed)

If you get an `auth/unauthorized-domain` error:

1. Firebase Console → Authentication → **Settings** tab
2. Scroll to **Authorized domains**
3. Click **Add domain** → type `localhost` (should already be there)
4. For production: add your deployed domain (e.g. `myapp.vercel.app`)

---

## Step 5 — Configure .env.local

In your project root, create `.env.local` (copy from `.env.local.example`):

```bash
cp .env.local.example .env.local
```

Fill in the values from your Firebase `firebaseConfig`:

```env
NEXT_PUBLIC_BACKEND_URL=http://localhost:8000

NEXT_PUBLIC_FIREBASE_API_KEY=AIzaSy...
NEXT_PUBLIC_FIREBASE_AUTH_DOMAIN=your-project.firebaseapp.com
NEXT_PUBLIC_FIREBASE_PROJECT_ID=your-project-id
NEXT_PUBLIC_FIREBASE_STORAGE_BUCKET=your-project.appspot.com
NEXT_PUBLIC_FIREBASE_MESSAGING_SENDER_ID=123456789
NEXT_PUBLIC_FIREBASE_APP_ID=1:123456789:web:abc123
```

> ⚠️ **Never commit `.env.local` to git!** It contains sensitive keys.

---

## Step 6 — Restart the Dev Server

After editing `.env.local`, you **must restart** Next.js:

```bash
# Stop the server (Ctrl+C), then:
npm run dev
```

---

## Common Errors & Fixes

| Error | Fix |
|-------|-----|
| `auth/invalid-api-key` | Wrong or missing `NEXT_PUBLIC_FIREBASE_API_KEY` in `.env.local` |
| `auth/configuration-not-found` | `.env.local` not created, or dev server not restarted |
| `auth/operation-not-allowed` | Email/Password or Google not enabled in Firebase Console → Authentication |
| `auth/unauthorized-domain` | Add `localhost` to Firebase Console → Authentication → Settings → Authorized domains |
| `auth/popup-blocked` | Allow popups for `localhost` in your browser settings |
| `auth/invalid-credential` | Wrong email or password |
| `auth/email-already-in-use` | Account exists — sign in instead of registering |
| `auth/too-many-requests` | Wait 5 minutes, you've been temporarily blocked |

---

## Verify It's Working

Open your browser console (F12). If Firebase is misconfigured you'll see:
```
⚠️ Firebase Auth will NOT work. Missing env vars: NEXT_PUBLIC_FIREBASE_API_KEY
```

If the config is correct and auth is enabled, sign-in should work immediately.
