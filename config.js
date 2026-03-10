/**
 * config.js — V18 Generic Project Configuration
 * Replace values below to adapt this app to any apartment project.
 * No changes needed in app.js or index.html.
 */
const PROJECT_CONFIG = {
    // Project Identity
    projectName: 'פרויקט רבין כרמיאל',
    projectSubtitle: 'בחירת דירה',
    lot: '103',

    // PWA / Title
    appTitle: 'פרויקט רבין כרמיאל - בחירת דירה',

    // Selection Day — default countdown target (ISO string)
    // Can be overridden by user via the date picker (saved in localStorage)
    selectionDayISO: '2026-03-12T09:00:00+02:00',

    // Payment schedule: each entry = { dayOffset, label, pct, highlight }
    // dayOffset is relative to selectionDay (day 0)
    paymentSchedule: [
        { dayOffset: 0, label: 'מעמד בחירת דירה — דמי רצינות', pct: '2,000₪', pctNum: null, highlight: 'green' },
        { dayOffset: 14, label: 'חתימת חוזה — השלמה ל-7%', pct: '7%', pctNum: 0.07, highlight: 'green', note: 'השלמה בקיזוז 2,000₪' },
        { dayOffset: 58, label: 'יתרת תשלום שלישי (13%)', pct: '13%', pctNum: 0.13, highlight: 'green-light', note: '3% הון + 10% משכנתה' },
        { dayOffset: 234, label: 'תשלום 10%', pct: '10%', pctNum: 0.10, highlight: 'none' },
        { dayOffset: 385, label: 'תשלום 10%', pct: '10%', pctNum: 0.10, highlight: 'none' },
        { dayOffset: 538, label: 'תשלום 10%', pct: '10%', pctNum: 0.10, highlight: 'none' },
        { dayOffset: 691, label: 'תשלום 10%', pct: '10%', pctNum: 0.10, highlight: 'none' },
        { dayOffset: 842, label: 'תשלום 10%', pct: '10%', pctNum: 0.10, highlight: 'none' },
        { dayOffset: 1026, label: 'תשלום 10%', pct: '10%', pctNum: 0.10, highlight: 'none' },
        { dayOffset: 1207, label: 'תשלום 10%', pct: '10%', pctNum: 0.10, highlight: 'none' },
        { dayOffset: 1451, label: 'מסירה (10% אחרונים)', pct: '10%', pctNum: 0.10, highlight: 'blue', note: '7 ימים לפני קבלת מפתח' },
    ],

    // Data file: relative path to the JS data file (must declare `const apartmentData = [...]`)
    dataFile: './data_v12.js',

    // Floor plan image directory (relative)
    floorplanDir: './floorplans/',

    // Documents
    specsPdf: './docs/הגרלה-2279-מפרט-חתום.pdf',

    // Colors (CSS custom properties override)
    themeColors: {
        '--primary': '#3b82f6',
        '--primary-dark': '#2563eb',
        '--accent': '#8b5cf6',
    },

    // "קומה אחרונה" — ONLY these buildings have ML apartments on their true last floor.
    // All other buildings: the top floor is a free-market penthouse (not in the 100-unit list).
    // Confirmed directly from the G4 document by the user on 2026-03-01.
    mlTopFloors: {
        '4R': 3,   // קומה 3 היא הקומה האחרונה עם דירות מחיר למשתכן
        '11R': 2   // קומה 2 היא הקומה האחרונה עם דירות מחיר למשתכן
    }
};
