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

    // Selection Day countdown target (ISO string)
    selectionDayISO: '2026-03-12T09:00:00+02:00',

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
