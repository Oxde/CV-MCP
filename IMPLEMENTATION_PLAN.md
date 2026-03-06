# CV Craft UX Overhaul

## Context
The current app has a boring landing page, a slow chat-based onboarding, and too many separate screens (5 pages behind a nav bar). The user wants a Cal.ai-inspired premium experience: immersive funnel onboarding, sidebar-driven main layout, and jobs as a right panel — not a separate page. Profile data should reliably fill from onboarding (structured inputs, not AI extraction).

## Files to Modify/Create

| Action | File | What |
|--------|------|------|
| REWRITE | `frontend/src/pages/Landing.jsx` | Dark premium hero, social proof, feature showcase |
| REWRITE | `frontend/src/pages/Onboarding.jsx` | 11-step funnel (not chat) |
| CREATE | `frontend/src/components/OnboardingStep.jsx` | Reusable step wrapper with progress bar |
| REWRITE | `frontend/src/components/Layout.jsx` | Sidebar + main + right jobs panel |
| CREATE | `frontend/src/components/Sidebar.jsx` | Left sidebar: CVs list, nav links |
| CREATE | `frontend/src/components/JobsPanel.jsx` | Right panel: job cards, add job modal |
| REWRITE | `frontend/src/pages/Dashboard.jsx` | CV preview center (iframe), toolbar |
| REWRITE | `frontend/src/lib/store.jsx` | Add selectedCvId, cvs list, sidebar state |
| UPDATE | `frontend/src/App.jsx` | Remove /vacancies route |
| UPDATE | `frontend/src/index.css` | Add keyframe animations |
| SIMPLIFY | `frontend/src/pages/Profile.jsx` | Keep fields, remove redundancy |
| DELETE | `frontend/src/pages/Vacancies.jsx` | Replaced by JobsPanel component |
| KEEP | `frontend/src/pages/Chat.jsx` | Full page via sidebar link |
| KEEP | `frontend/src/pages/Templates.jsx` | Full page via sidebar link |

## 1. Landing Page (Dark, Premium)

```
bg-gray-950 full page
├── Hero (h-screen centered)
│   ├── h1: "Your resume. Perfected by AI." (text-5xl md:text-7xl white)
│   ├── p: "Tailored to every job. Built in minutes." (text-gray-400)
│   ├── CTA: "Start Building — Free" (bg-white text-gray-950, large)
│   └── Social proof strip: "2,400+ CVs" | "8 templates" | "AI-powered"
├── Features (3 cards with glow icons, hover:translate-y-[-2px])
├── How it works (3 numbered steps)
└── Final CTA section
```

## 2. Onboarding Funnel (11 Steps)

Replace chat entirely. Each step = fullscreen card with one question. Data saves via `PATCH /api/users/{id}` after each step (no AI extraction needed).

| Step | Question | UI | Required |
|------|----------|-----|----------|
| 0 | "What's your name?" | Large text input | Yes |
| 1 | "What do you do?" | Text input + suggestion chips (SWE, PM, Designer...) | Yes |
| 2 | "Years of experience?" | 5 clickable cards (0-1, 1-3, 3-5, 5-10, 10+) | Yes |
| 3 | "Where are you based?" | Text input + chips (SF, NYC, London, Remote...) | Yes |
| 4 | "Your email?" | Email input | Yes |
| 5 | "Phone number?" | Phone input | Skip |
| 6 | "LinkedIn profile?" | Prefixed input (linkedin.com/in/...) | Skip |
| 7 | "Your key skills?" | Tag input + popular suggestions | Yes (min 1) |
| 8 | "Most recent job?" | Mini-form: title, company, dates, 3 bullets | Yes |
| 9 | "Education?" | Mini-form: degree, school, year | Skip |
| 10 | "What roles are you targeting?" | Tag input + suggestions | Skip |

**After step 10:** Loading screen → AI generates professional `summary` from profile data → save → redirect to dashboard.

**OnboardingStep wrapper:** Progress bar at top, back/skip buttons, centered content, large "Continue" button at bottom. Step transitions via CSS `animate-slide-right`.

## 3. Main App Layout (Sidebar + Main + Jobs)

```
┌──────────────┬─────────────────────────────┬──────────────┐
│  SIDEBAR     │      MAIN CONTENT           │  JOBS PANEL  │
│  (w-60)      │      (flex-1)               │  (w-80)      │
│              │                              │              │
│  Logo        │   CV Preview (iframe)        │  Job cards   │
│  ─────       │   or empty state             │  Add Job +   │
│  My CVs      │                              │  Status tags │
│   · CV 1     │   Toolbar: template picker,  │              │
│   · CV 2     │   download, delete           │              │
│   + New CV   │                              │              │
│  ─────       │                              │              │
│  Templates   │                              │              │
│  Profile     │                              │              │
│  AI Chat     │                              │              │
│  ─────       │                              │              │
│  User/Logout │                              │              │
└──────────────┴─────────────────────────────┴──────────────┘
```

**Mobile:** Sidebar = drawer from left (hamburger toggle). Jobs panel = bottom sheet (briefcase icon toggle). Main content always visible.

## 4. Dashboard = CV Preview Center

- Selected CV shows as full iframe preview with toolbar
- Toolbar: CV name, template dropdown, download PDF, edit with AI (→ /chat), delete
- No CV selected: empty state with "Create your first CV" prompt
- CV selection state shared via context (store.jsx)

## 5. JobsPanel Component

Extracted from current Vacancies.jsx. Compact vertical card list:
- Each card: title, company, status badge
- Click job → generate tailored CV for it
- "Add Job" button opens modal (URL/text/manual — same as current)

## 6. Animations (index.css)

4 keyframes added: `fade-up`, `fade-in`, `slide-in-right`, `slide-in-left`. Used for:
- Landing hero entrance
- Onboarding step transitions
- Sidebar/panel open/close

No new dependencies. Tailwind `transition-all duration-300` for hover states.

## Implementation Order

1. `index.css` — animations
2. `OnboardingStep.jsx` — new component
3. `Onboarding.jsx` — funnel rewrite
4. `Landing.jsx` — premium rewrite
5. `store.jsx` — add shared state
6. `Sidebar.jsx` — new component
7. `JobsPanel.jsx` — new component (from Vacancies)
8. `Layout.jsx` — sidebar layout rewrite
9. `Dashboard.jsx` — CV preview center
10. `App.jsx` — update routes
11. `Profile.jsx` — simplify
12. Delete `Vacancies.jsx`

## Verification

1. Run `npm run dev` in frontend, `uvicorn` in backend
2. Landing page: dark theme, CTA creates user → redirects to onboarding
3. Onboarding: step through all 11 steps, verify profile is filled (check `/api/users/{id}`)
4. Dashboard: sidebar shows CVs, clicking one shows preview, jobs panel on right
5. Create CV from sidebar, change template, download PDF
6. Add job via URL/text/manual in jobs panel
7. Mobile: sidebar drawer works, jobs panel bottom sheet works
8. Run `npm run build` to verify production build
