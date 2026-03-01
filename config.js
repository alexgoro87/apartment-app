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

    // Architectural top floors (generated from full G4 / D4 dataset including free-market units)
    // Regenerate using: python calc_g4_floors.py
    architecturalTopFloors: {
        '10R': 3, '11R': 3, '12R': 3, '13R': 3, '14R': 3, '15R': 3, '16R': 3,
        '1T': 4, '2R': 5, '3T': 4, '4R': 4, '5R': 4, '6T': 3, '7P': 3, '8R': 3, '9R': 3
    }
};
