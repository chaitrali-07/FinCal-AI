# Finova — AI Financial Companion

A modern, production-ready fintech frontend built with Next.js 14, Tailwind CSS, shadcn/ui, and Firebase Authentication.

## 🚀 Quick Start

### 1. Install Dependencies
```bash
npm install
```

You may also need:
```bash
npm install tailwindcss-animate
```

### 2. Configure Environment Variables

Copy `.env.local.example` to `.env.local`:
```bash
cp .env.local.example .env.local
```

Fill in your values:
```env
NEXT_PUBLIC_BACKEND_URL=http://localhost:8000

NEXT_PUBLIC_FIREBASE_API_KEY=your_api_key
NEXT_PUBLIC_FIREBASE_AUTH_DOMAIN=your_project.firebaseapp.com
NEXT_PUBLIC_FIREBASE_PROJECT_ID=your_project_id
NEXT_PUBLIC_FIREBASE_STORAGE_BUCKET=your_project.appspot.com
NEXT_PUBLIC_FIREBASE_MESSAGING_SENDER_ID=your_sender_id
NEXT_PUBLIC_FIREBASE_APP_ID=your_app_id
```

### 3. Firebase Setup
1. Go to [Firebase Console](https://console.firebase.google.com)
2. Create a new project
3. Enable Authentication → Email/Password and Google providers
4. Copy config values to `.env.local`

### 4. Run Development Server
```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000)

## 📁 Project Structure

```
fintech-app/
├── app/
│   ├── layout.tsx          # Root layout with providers
│   ├── page.tsx            # Landing page
│   ├── globals.css         # Global styles + CSS vars
│   ├── login/page.tsx      # Sign in page
│   ├── register/page.tsx   # Sign up page
│   ├── calculators/
│   │   ├── page.tsx        # Calculator hub (grid)
│   │   └── [type]/page.tsx # Dynamic calculator detail
│   └── assistant/page.tsx  # AI chat interface
├── components/
│   ├── ui/                 # shadcn/ui components
│   ├── Navbar.tsx          # Sticky navbar with auth
│   ├── Footer.tsx          # Footer branding
│   ├── ThemeProvider.tsx   # Dark/light mode
│   ├── ThemeToggle.tsx     # Theme switch button
│   └── ProtectedRoute.tsx  # Auth guard HOC
├── context/
│   └── AuthContext.tsx     # Firebase auth context
└── lib/
    ├── firebase.ts         # Firebase initialization
    ├── api.ts              # Backend API calls
    ├── calculatorConfig.ts # Calculator metadata + fields
    └── utils.ts            # cn() utility
```

## ✨ Features

- **Firebase Auth**: Email/Password + Google Sign-In
- **6 Calculators**: EMI, SIP, FD, RD, Tax, ROI
- **AI Assistant**: Chat interface with streaming-like UX
- **Dark Mode**: Full system/manual dark mode support
- **Responsive**: Mobile-first design
- **Protected Routes**: Auth-guarded pages
- **Skeleton Loaders**: Loading states everywhere
- **Error Handling**: Graceful error UI

## 🎨 Design System

- **Font**: Sora (display/body)
- **Colors**: Emerald/Teal accent palette
- **Radius**: 12px rounded corners
- **Cards**: Glassmorphism with backdrop blur
- **Gradients**: Subtle mesh background
