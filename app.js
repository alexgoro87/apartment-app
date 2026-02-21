// Register Service Worker for PWA offline support
if ('serviceWorker' in navigator) {
    navigator.serviceWorker.register('./service-worker.js').catch(() => { });
}

document.addEventListener('DOMContentLoaded', () => {
    // State
    // Format apartmentsData keys since CSV had Hebrew headers. The parsed JS keys might be Hebrew.
    console.log("Raw Data Loaded:", apartmentsData.length, "items");

    // Safe localStorage wrapper for local files
    const safeGetItem = (key) => {
        try { return localStorage.getItem(key); }
        catch (e) { return null; }
    };
    const safeSetItem = (key, val) => {
        try { localStorage.setItem(key, val); }
        catch (e) { console.warn("Local storage blocked"); }
    };

    // Exact apartment type codes from the catalog table (4th column from right)
    // Key: "building-apartment" → catalog type code
    const APT_TYPE_MAP = {
        // === מגרש 103 ===
        // 7P
        '7P-1': 'A', '7P-2': 'C', '7P-3': 'A 1', '7P-4': 'C 4',
        '7P-5': 'A 5', '7P-6': 'C 6', '7P-7': 'D1',
        // 8R
        '8R-1': 'A+', '8R-2': 'C 1', '8R-3': 'A 2', '8R-4': 'C 5',
        '8R-5': 'A 5', '8R-6': 'C 7', '8R-7': 'D1',
        // 9R
        '9R-1': 'C-', '9R-2': 'B', '9R-3': 'A 3', '9R-4': 'B-',
        '9R-5': 'A 6', '9R-6': 'B- 1', '9R-7': 'D',
        // 10R
        '10R-1': 'B 1', '10R-2': 'A+ 1', '10R-3': 'B-', '10R-4': 'A 2',
        '10R-5': 'B- 1', '10R-6': 'A 5', '10R-7': 'D',
        // 11R
        '11R-1': 'A+ 1', '11R-2': 'B 1', '11R-3': 'A 2', '11R-4': 'B-',
        '11R-5': 'A 5', '11R-6': 'B- 1', '11R-7': 'D',
        // 12R
        '12R-1': 'B 2', '12R-2': 'C- 1', '12R-3': 'B-', '12R-4': 'A 3',
        '12R-5': 'B- 1', '12R-6': 'A 6', '12R-7': 'D2',
        // 13R
        '13R-1': 'C 2', '13R-2': 'A+ 2', '13R-3': 'C 5', '13R-4': 'A 2',
        '13R-5': 'C 7', '13R-6': 'A 5', '13R-7': 'D1',
        // 14R
        '14R-1': 'A+ 3', '14R-2': 'C 3', '14R-3': 'A 2', '14R-4': 'C 5',
        '14R-5': 'A 5', '14R-6': 'C 7', '14R-7': 'D1',
        // 15R
        '15R-1': 'C- 2', '15R-2': 'B 3', '15R-3': 'A 3', '15R-4': 'B-',
        '15R-5': 'A 6', '15R-6': 'B- 1', '15R-7': 'D',
        // 16R
        '16R-1': 'B 4', '16R-2': 'A+ 4', '16R-3': 'B-', '16R-4': 'A 2',
        '16R-5': 'B- 1', '16R-6': 'A 5', '16R-7': 'D',
        // === מגרש 102 (לפי נספח ג'4) ===
        // 1T
        '1T-1': 'C', '1T-2': 'E', '1T-3': 'C 1', '1T-4': 'E 1',
        '1T-5': 'C 2', '1T-6': 'E 2', '1T-7': 'C 1', '1T-8': 'E 1', '1T-9': 'D',
        // 2R
        '2R-1': 'A', '2R-2': 'B', '2R-3': 'A 1', '2R-4': 'B 1',
        '2R-5': 'A 2', '2R-6': 'B 2', '2R-7': 'A 4', '2R-8': 'B 3',
        '2R-9': 'A 2', '2R-10': 'B 2', '2R-11': 'D3',
        // 3T
        '3T-1': 'E 3', '3T-2': 'C 3', '3T-3': 'E 1', '3T-4': 'C 1',
        '3T-5': 'E 2', '3T-6': 'C 2', '3T-7': 'E 1', '3T-8': 'C 1', '3T-9': 'D',
        // 4R
        '4R-1': 'B 4', '4R-2': 'A 5', '4R-3': 'B 1', '4R-4': 'A 1',
        '4R-5': 'B 2', '4R-6': 'A 2', '4R-7': 'B 3', '4R-8': 'A 4', '4R-9': 'D3',
        // 5R (חלקי/מוערך - התחלה A 6)
        '5R-1': 'A 6', '5R-2': 'B 4', '5R-3': 'A 2', '5R-4': 'B 2',
        '5R-5': 'A 4', '5R-6': 'B 3', '5R-7': 'A 2', '5R-8': 'B 2', '5R-9': 'D3',
        // 6T (הערכה עד לקבלת העמוד הבא)
        '6T-1': 'E 3', '6T-2': 'C 3', '6T-3': 'E 1', '6T-4': 'C 1',
        '6T-5': 'E 2', '6T-6': 'C 2', '6T-7': 'D',
    };

    function getAptType(building, aptNum) {
        const key = `${building}-${aptNum}`;
        return APT_TYPE_MAP[key] || '?';
    }

    // Mapping between apartment catalog type and PDF page number (Populated by AI Vision Agent)
    const PDF_PAGE_MAP = {
        'A': 42, 'A+': 33, 'A 1': 42, 'A 2': 39, 'A 3': 45, 'A 5': 49, 'A 6': 56,
        'B': 23, 'B-': 54, 'B 1': 28, 'B 2': 29, 'B- 1': 53,
        'C': 13, 'C-': 18, 'C 1': 17, 'C 2': 20, 'C 4': 15, 'C 5': 51, 'C 6': 48, 'C 7': 52, 'C- 1': 19,
        'D': 12, 'D1': 12, 'D2': 12
    };

    function getPdfPageUrl(aptType) {
        // Base URL to the PDF
        const baseUrl = "../קטלוג-משתכן-רמת-רבין.pdf";
        const page = PDF_PAGE_MAP[aptType];

        // If we have a mapped page, append #page=X
        if (page) {
            return `${baseUrl}#page=${page}`;
        }
        return baseUrl;
    }

    // === BETA v2: FAVORITES SYSTEM ===
    let favorites = new Set(JSON.parse(safeGetItem('apt_favorites') || '[]'));
    const saveFavorites = () => safeSetItem('apt_favorites', JSON.stringify([...favorites]));
    window.toggleFavorite = function (id, e) {
        e.stopPropagation();
        if (favorites.has(id)) favorites.delete(id);
        else favorites.add(id);
        saveFavorites();

        // V6: Sync to Cloud
        if (window.syncFavorite && window.currentUser) {
            window.syncFavorite(id, window.currentUser, favorites.has(id));
        }

        renderData();
    };

    // === BETA v2: COMPARE SYSTEM ===
    let compareList = new Set();
    window.toggleCompare = function (id, e) {
        e.stopPropagation();
        if (compareList.has(id)) compareList.delete(id);
        else if (compareList.size < 3) compareList.add(id);
        renderData();
        updateCompareBar();
    };

    // === V3: Deal Score removed — using ₪/sqm as primary metric ===

    // === BETA v2: NOTES PER APARTMENT ===
    window.saveNote = function (id) {
        const noteEl = document.getElementById(`note_${id}`);
        if (noteEl) safeSetItem(`note_${id}`, noteEl.value);
    };
    window.getNote = (id) => safeGetItem(`note_${id}`) || '';

    let processedData = apartmentsData.map(item => {
        // Map Hebrew CSV headers to standard object keys
        return {
            id: String(item['דירה']).trim() + '-' + String(item['מבנה']).trim(),
            rank: parseInt(item['דירוג']) || 999,
            building: String(item['מבנה']).trim(),
            aptText: String(item['דירה']).trim(),
            floor: String(item['קומה']).trim(),
            rooms: String(item['חדרים']).trim(),
            area: parseFloat(item['שטח']) || 0,
            balcony: parseFloat(item['מרפסת']) || 0,
            storage: parseFloat(item['מחסן']) || 0,
            sun: String(item['חמה/קרירה']).trim(),
            distance: parseInt(item['מרחק חניה']) || 0,
            price: parseInt(item['מחיר']) || 0,
            isTopFloor: item['אחרונה?'] === 'כן',
            status: safeGetItem(`apt_${item['דירה']}_${item['מבנה']}`) || 'available',
            aptType: getAptType(String(item['מבנה']).trim(), String(item['דירה']).trim())
        };
    });

    // V3: Add pricePerSqm as primary metric
    processedData.forEach(apt => { apt.pricePerSqm = apt.area ? Math.round(apt.price / apt.area) : 0; });
    window.processedData = processedData;



    // Populate Filters
    const populateFilters = () => {
        const buildingFilter = document.getElementById('filter-building');
        const floorFilter = document.getElementById('filter-floor');

        const buildings = [...new Set(processedData.map(a => a.building))].sort();
        const floors = [...new Set(processedData.map(a => a.floor))].sort((a, b) => {
            if (a === 'קרקע') return -1;
            if (b === 'קרקע') return 1;
            return parseInt(a) - parseInt(b);
        });

        buildings.forEach(b => {
            const opt = document.createElement('option');
            opt.value = b;
            opt.textContent = `מבנה ${b}`;
            buildingFilter.appendChild(opt);
        });

        floors.forEach(f => {
            const opt = document.createElement('option');
            opt.value = f;
            opt.textContent = f === 'קרקע' ? 'קומה קרקע' : `קומה ${f}`;
            floorFilter.appendChild(opt);
        });
    };
    populateFilters();

    // Elements
    const grid = document.getElementById('apartments-grid');
    const filterRooms = document.getElementById('filter-rooms');
    const filterMinPrice = document.getElementById('filter-min-price');
    const filterMaxPrice = document.getElementById('filter-max-price');
    const sunRadios = document.querySelectorAll('input[name="sun"]');
    const filterAvailable = document.getElementById('filter-available');
    const sortSelect = document.getElementById('sort-select');
    const resetBtn = document.getElementById('reset-filters');
    const countDisplay = document.getElementById('count-display');
    const filterBuilding = document.getElementById('filter-building');
    const filterFloor = document.getElementById('filter-floor');
    const filterTopFloor = document.getElementById('filter-top-floor');

    // Format number to ILS
    const formatPrice = (num) => new Intl.NumberFormat('he-IL').format(num);

    // Search input — declared here so renderData() can access it
    const searchInput = document.getElementById('search-input');
    // ₪/sqm slider reference
    const sqmSlider = document.getElementById('filter-sqm-price');
    const sqmDisplay = document.getElementById('filter-sqm-display');
    if (sqmSlider) {
        sqmSlider.addEventListener('input', () => {
            const val = parseInt(sqmSlider.value);
            if (sqmDisplay) sqmDisplay.textContent = val >= 17000 ? 'הכל' : `עד ${formatPrice(val)} ₪`;
            renderData();
        });
    }

    // === ROUND 6: CLOUD SYNC & USER PROFILES ===
    window.currentUser = safeGetItem('selected_user') || null;

    window.setUser = function (userId) {
        safeSetItem('selected_user', userId);
        window.currentUser = userId;
        document.getElementById('user-selector-modal').style.display = 'none';
        showToast('פרופיל עודכן - הסנכרון פעיל', 'success');
        renderData(); // Refresh cards to show cloud favorites
    };

    function checkUser() {
        if (!window.currentUser) {
            document.getElementById('user-selector-modal').style.display = 'flex';
        }
    }
    setTimeout(checkUser, 1000);

    // Initial Render
    renderData();
    // === ROUND 2: GRID/LIST MODE ===
    let isListMode = false;
    window.toggleGridMode = function () {
        isListMode = !isListMode;
        const btn = document.getElementById('grid-toggle');
        if (btn) btn.innerHTML = isListMode ? '<i class="fa-solid fa-grip"></i>' : '<i class="fa-solid fa-list"></i>';
        const grid = document.getElementById('apartments-grid');
        grid.classList.toggle('list-mode', isListMode);
    };

    // === ROUND 2: MOBILE COLLAPSIBLE FILTERS ===
    let filtersOpen = true;
    window.toggleMobileFilters = function () {
        filtersOpen = !filtersOpen;
        const panel = document.getElementById('filters-panel');
        const btn = document.getElementById('mobile-filter-toggle');
        if (panel) panel.style.display = filtersOpen ? '' : 'none';
        if (btn) btn.innerHTML = filtersOpen
            ? '<i class="fa-solid fa-sliders"></i> הסתר סינון'
            : '<i class="fa-solid fa-sliders"></i> סינון דירות';
    };
    // Show toggle button on mobile
    function updateMobileUI() {
        const btn = document.getElementById('mobile-filter-toggle');
        if (btn) btn.style.display = window.innerWidth <= 768 ? 'flex' : 'none';
    }
    updateMobileUI();
    window.addEventListener('resize', updateMobileUI);

    // === ROUND 2: CSV EXPORT ===
    window.exportCSV = function () {
        const headers = ['דירוג', 'מבנה', 'דירה', 'קומה', 'חדרים', 'שטח', 'מרפסת', 'מחסן', 'כיוון', 'חניה', 'מחיר', 'ציון עסקה', 'סטטוס'];
        const rows = processedData.map(a => [
            a.rank, a.building, a.aptText, a.floor, a.rooms,
            a.area, a.balcony, a.storage, a.sun, a.distance,
            a.price, a.dealScore, a.status === 'available' ? 'פנויה' : 'נלקחה'
        ]);
        const csv = '\uFEFF' + [headers, ...rows].map(r => r.join(',')).join('\n');
        const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a'); a.href = url;
        a.download = 'ramat_rabin_apartments.csv'; a.click();
        URL.revokeObjectURL(url);
    };

    // === ROUND 2: ADD TO CALENDAR ===
    window.addToCalendar = function () {
        const ics = [
            'BEGIN:VCALENDAR', 'VERSION:2.0',
            'BEGIN:VEVENT',
            'DTSTART:20260310T070000Z',
            'DTEND:20260310T150000Z',
            'SUMMARY:יום בחירת דירה - פרויקט רבין כרמיאל',
            'DESCRIPTION:בחר את הדירה הטובה ביותר בפרויקט רבין כרמיאל',
            'END:VEVENT', 'END:VCALENDAR'
        ].join('\r\n');
        const blob = new Blob([ics], { type: 'text/calendar' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a'); a.href = url;
        a.download = 'selection_day.ics'; a.click();
        URL.revokeObjectURL(url);
    };
    filterRooms.addEventListener('change', renderData);
    if (filterMinPrice) filterMinPrice.addEventListener('input', renderData);
    if (filterMaxPrice) filterMaxPrice.addEventListener('input', renderData);
    sunRadios.forEach(r => r.addEventListener('change', renderData));
    filterAvailable.addEventListener('change', renderData);
    sortSelect.addEventListener('change', renderData);
    if (filterBuilding) filterBuilding.addEventListener('change', renderData);
    if (filterFloor) filterFloor.addEventListener('change', renderData);
    if (filterTopFloor) filterTopFloor.addEventListener('change', renderData);
    if (searchInput) searchInput.addEventListener('input', renderData);
    const showFavsEl = document.getElementById('show-favs-only');
    if (showFavsEl) showFavsEl.addEventListener('change', renderData);
    // Keyboard shortcut: Escape closes modals
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
            document.querySelectorAll('.modal.visible').forEach(m => m.classList.remove('visible'));
        }
    });

    resetBtn.addEventListener('click', () => {
        filterRooms.value = 'all';
        if (filterMinPrice) filterMinPrice.value = 900000;
        if (filterMaxPrice) filterMaxPrice.value = 2200000;
        sunRadios[0].checked = true;
        filterAvailable.checked = true;
        if (filterBuilding) filterBuilding.value = 'all';
        if (filterFloor) filterFloor.value = 'all';
        if (filterTopFloor) filterTopFloor.checked = false;
        renderData();
    });

    // Rendering Function
    function renderData() {
        // 1. Filter
        const rooms = filterRooms.value;
        const minPrice = filterMinPrice ? parseInt(filterMinPrice.value) || 0 : 0;
        const maxPrice = filterMaxPrice ? parseInt(filterMaxPrice.value) || Infinity : Infinity;
        const sun = document.querySelector('input[name="sun"]:checked').value;
        const onlyAvailable = filterAvailable.checked;
        const searchQ = (searchInput ? searchInput.value : '').trim().toLowerCase();

        let filtered = processedData.filter(apt => {
            if (rooms !== 'all' && apt.rooms.toString() !== rooms) return false;
            // Handle edge case like "4 גן" -> "4"
            if (rooms !== 'all' && !apt.rooms.toString().includes(rooms)) return false;

            if (apt.price < minPrice || apt.price > maxPrice) return false;
            if (sun !== 'all' && apt.sun !== sun) return false;
            if (onlyAvailable && apt.status === 'taken') return false;

            if (filterBuilding && filterBuilding.value !== 'all' && apt.building !== filterBuilding.value) return false;
            if (filterFloor && filterFloor.value !== 'all' && apt.floor !== filterFloor.value) return false;
            if (filterTopFloor && filterTopFloor.checked && !apt.isTopFloor) return false;

            // === V3: MIDDLE FLOOR FILTER ===
            const filterMiddle = document.getElementById('filter-middle-floor');
            if (filterMiddle && filterMiddle.checked) {
                const floorNum = apt.floor === 'קרקע' ? 0 : (parseInt(apt.floor) || 0);
                if (floorNum === 0 || apt.isTopFloor) return false;
            }

            // === ROUND 2: TEXT SEARCH ===
            if (searchQ) {
                const haystack = [
                    apt.building, apt.aptText, apt.floor, apt.aptType,
                    apt.rooms, apt.id, `מבנה ${apt.building}`, `דירה ${apt.aptText}`,
                    `קומה ${apt.floor}`, `טיפוס ${apt.aptType}`, `${apt.rooms} חדרים`
                ].join(' ').toLowerCase();
                if (!haystack.includes(searchQ)) return false;
            }

            // === ROUND 3: PRICE PER SQM FILTER ===
            if (sqmSlider) {
                const maxSqm = parseInt(sqmSlider.value);
                if (maxSqm < 17000 && apt.area > 0 && (apt.price / apt.area) > maxSqm) return false;
            }

            return true;
        });

        // 2. Sort — Beta v2 expanded sorts
        const sortMode = sortSelect.value;
        filtered.sort((a, b) => {
            switch (sortMode) {
                case 'rank-asc': return a.rank - b.rank;
                case 'price-asc': return a.price - b.price;
                case 'price-desc': return b.price - a.price;
                case 'size-desc': return b.area - a.area;
                case 'ppsqm-asc': return (a.pricePerSqm || 99999) - (b.pricePerSqm || 99999);
                case 'distance-asc': return a.distance - b.distance;
                case 'floor-desc': {
                    const fa = a.floor === 'קרקע' ? 0 : (parseInt(a.floor) || 0);
                    const fb = b.floor === 'קרקע' ? 0 : (parseInt(b.floor) || 0);
                    return fb - fa;
                }
                case 'balcony-desc': return b.balcony - a.balcony;
                default: return 0;
            }
        });

        // === BETA v2: Update Stats Bar ===
        const showFavsOnly = document.getElementById('show-favs-only')?.checked;
        const displayList = showFavsOnly ? filtered.filter(a => favorites.has(a.id)) : filtered;
        if (showFavsOnly) {
            filtered = displayList;
        }

        // Stats bar removed in V5

        countDisplay.textContent = filtered.length;

        // V3: Building Stats removed

        // === E2: PRICE CHART BY ROOM COUNT ===
        renderPriceChart(filtered);

        // === G2: FLOOR MAP UPDATE ===
        renderFloorMap();

        // 3. Render
        grid.innerHTML = '';
        filtered.forEach(apt => {
            const card = document.createElement('div');
            card.className = `apt-card ${apt.status === 'taken' ? 'taken' : ''}`;

            // Icon and Direction mapping based on original data
            const isHot = apt.sun === 'חמה';
            const sunIcon = isHot ? '<i class="fa-solid fa-sun" style="color:#fbbf24"></i>' : '<i class="fa-solid fa-snowflake" style="color:#60a5fa"></i>';
            const explicitDirection = isHot ? 'דרום/מערב (חמה)' : 'צפון/מזרח (קרירה)';

            const statusText = apt.status === 'taken' ? 'נלקחה' : 'פנויה (סמן כנלקחה)';
            const btnClass = apt.status === 'taken' ? 'btn-taken' : 'btn-available';

            const isFav = favorites.has(apt.id);
            const inCompare = compareList.has(apt.id);
            const pricePerSqm = apt.area ? Math.round(apt.price / apt.area) : 0;

            card.innerHTML = `
                <div class="card-header">
                    <div style="display:flex; align-items:center; gap:0.5rem;">
                        <div class="rank-badge" title="דירוג">#${apt.rank}</div>
                        <!-- V6: Cloud Sync Indicators -->
                        <div class="cloud-indicators" style="display:flex; gap:0.25rem;">
                            ${window.cloudFavs && window.cloudFavs[apt.id] ? Object.keys(window.cloudFavs[apt.id]).filter(uid => window.cloudFavs[apt.id][uid]).map(uid => {
                const config = {
                    me: { icon: 'fa-user-tie', color: 'var(--primary)', name: 'אלכס' },
                    wife: { icon: 'fa-user-nurse', color: '#ec4899', name: 'אנה' },
                    advisor: { icon: 'fa-user-graduate', color: '#10b981', name: 'יועץ' }
                };
                const c = config[uid] || { icon: 'fa-user', color: '#ccc', name: 'משתמש' };
                return `<i class="fa-solid ${c.icon}" style="font-size:0.75rem; color:${c.color}" title="נשמר ע״י ${c.name}"></i>`;
            }).join('') : ''}
                        </div>
                    </div>
                    <div style="display:flex; align-items:center; gap:0.4rem;">
                        <span style="font-size:0.75rem; color:var(--text-muted);">${formatPrice(pricePerSqm)} ₪/מ"ר</span>
                        <div class="price-tag">${formatPrice(apt.price)} ₪</div>
                    </div>
                </div>
                <div class="apt-details">
                    <div class="detail-item"><i class="fa-solid fa-map"></i> דגם: <span class="highlight">${apt.aptType}</span></div>
                    <div class="detail-item"><i class="fa-solid fa-building"></i> <span class="highlight">מבנה ${apt.building}</span></div>
                    <div class="detail-item"><i class="fa-solid fa-door-closed"></i> דירה ${apt.aptText}</div>
                    <div class="detail-item"><i class="fa-solid fa-layer-group"></i> קומה ${apt.floor}</div>
                    <div class="detail-item"><i class="fa-solid fa-bed"></i> ${apt.rooms} חדרים</div>
                    <div class="detail-item"><i class="fa-solid fa-ruler-combined"></i> ${apt.area} מ"ר</div>
                    <div class="detail-item"><i class="fa-solid fa-cloud-sun"></i> מרפסת: ${apt.balcony} מ"ר</div>
                    <div class="detail-item"><i class="fa-solid fa-box"></i> מחסן: ${apt.storage} מ"ר</div>
                    <div class="detail-item tooltip">${sunIcon} <span class="highlight">${explicitDirection}</span></div>
                    <div class="detail-item"><i class="fa-solid fa-car"></i> חניה: ${apt.distance}מ'</div>
                    ${apt.isTopFloor ? `<div class="detail-item" style="color:var(--accent)"><i class="fa-solid fa-arrow-up"></i> קומה אחרונה!</div>` : ''}
                </div>
                <div style="display: flex; gap: 0.4rem; margin-top: auto; padding-top: 1rem; flex-wrap: wrap;">
                    <button class="status-btn ${btnClass}" data-id="${apt.id}" style="flex:1; min-width:80px;">
                        ${statusText}
                    </button>
                    <button type="button" onclick="openImageViewer('${apt.aptType}'); event.stopPropagation();" class="btn-outline" style="padding: 0.65rem 0.75rem; font-family: inherit; font-size: 0.95rem; border-radius: 8px; cursor: pointer; background: transparent;" title="שרטוט">
                        <i class="fa-solid fa-map"></i>
                    </button>
                    <button type="button" onclick="toggleFavorite('${apt.id}', event)" class="btn-outline ${isFav ? 'fav-active' : ''}" style="padding: 0.65rem 0.75rem; font-family: inherit; font-size: 0.95rem; border-radius: 8px; cursor: pointer; background: transparent;" title="מועדפים">
                        <i class="fa-${isFav ? 'solid' : 'regular'} fa-heart" style="color:${isFav ? '#ef4444' : 'inherit'}"></i>
                    </button>
                    <button type="button" onclick="toggleCompare('${apt.id}', event)" class="btn-outline ${inCompare ? 'compare-active' : ''}" style="padding: 0.65rem 0.75rem; font-family: inherit; font-size: 0.95rem; border-radius: 8px; cursor: pointer; background: ${inCompare ? 'rgba(79,70,229,0.3)' : 'transparent'};" title="השוואה">
                        <i class="fa-solid fa-scale-balanced"></i>
                    </button>
                    <button type="button" onclick="shareWhatsApp('${apt.id}', event)" class="btn-outline" style="padding: 0.65rem 0.75rem; font-family: inherit; font-size: 0.95rem; border-radius: 8px; cursor: pointer; background: transparent;" title="שתף ב-WhatsApp">
                        <i class="fa-brands fa-whatsapp" style="color:#25d366;"></i>
                    </button>
                    <button type="button" onclick="copyAptLink('${apt.id}', event)" class="btn-outline" style="padding: 0.65rem 0.75rem; font-family: inherit; font-size: 0.95rem; border-radius: 8px; cursor: pointer; background: transparent;" title="עתק קישור">
                        <i class="fa-solid fa-link"></i>
                    </button>
                </div>
            `;

            // Add click listener to open detailed modal
            card.addEventListener('click', (e) => {
                // Ignore clicks on buttons/links
                if (e.target.closest('.status-btn') || e.target.closest('a') || e.target.closest('button')) return;
                openAptModal(apt);
            });

            // V3: Deal Score glow removed

            grid.appendChild(card);
        });

        // Add button listeners
        document.querySelectorAll('.status-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const id = e.target.getAttribute('data-id');
                toggleStatus(id);
            });
        });
    }

    function toggleStatus(id) {
        const apt = processedData.find(a => a.id === id);
        if (apt) {
            apt.status = apt.status === 'available' ? 'taken' : 'available';
            safeSetItem(`apt_${apt.aptText}_${apt.building}`, apt.status);
            renderData();
        }
    }

    // === BETA v2: WHATSAPP SHARE ===
    window.shareWhatsApp = function (id, e) {
        e.stopPropagation();
        const apt = processedData.find(a => a.id === id);
        if (!apt) return;
        const msg = `🏢 *רמת רבין — ${apt.aptType}*\n` +
            `מבנה ${apt.building} | דירה ${apt.aptText} | קומה ${apt.floor}\n` +
            `${apt.rooms} חד' | ${apt.area} מ"ר | ${apt.sun === 'חמה' ? '☀️ חמה' : '❄️ קרירה'}\n` +
            `💰 מחיר: *${formatPrice(apt.price)} ₪*\n` +
            `📊 ציון עסקה: ${apt.dealScore}/100`;
        window.open(`https://wa.me/?text=${encodeURIComponent(msg)}`, '_blank');
    };

    // === BETA v2: COMPARE BAR ===
    function updateCompareBar() {
        const bar = document.getElementById('compare-bar');
        if (!bar) return;
        if (compareList.size === 0) { bar.style.display = 'none'; return; }
        bar.style.display = 'flex';
        const apts = [...compareList].map(id => processedData.find(a => a.id === id)).filter(Boolean);
        bar.innerHTML = `
            <span style="font-weight:600;">⚖️ השוואה (${compareList.size}/3):</span>
            ${apts.map(a => `<span class="compare-tag">${a.aptType} מבנה ${a.building}/${a.aptText}</span>`).join('')}
            ${compareList.size >= 2 ? `<button onclick="openCompareModal()" style="background:var(--accent); color:white; border:none; border-radius:8px; padding:0.4rem 1rem; cursor:pointer; font-family:inherit;">השווה!</button>` : ''}
            <button onclick="clearCompare()" style="background:transparent; color:var(--text-muted); border:none; cursor:pointer; font-size:1.2rem;">✕</button>
        `;
    }
    window.clearCompare = () => { compareList.clear(); renderData(); updateCompareBar(); };

    // === BETA v2: COMPARE MODAL ===
    window.openCompareModal = function () {
        const modal = document.getElementById('compare-modal');
        if (!modal) return;
        const apts = [...compareList].map(id => processedData.find(a => a.id === id)).filter(Boolean);
        const fields = [
            ['מחיר', a => `${formatPrice(a.price)} ₪`],
            ['שטח', a => `${a.area} מ"ר`],
            ['₪/מ"ר', a => `${formatPrice(Math.round(a.price / a.area))} ₪`],
            ['חדרים', a => a.rooms],
            ['קומה', a => a.floor],
            ['מרפסת', a => `${a.balcony} מ"ר`],
            ['כיוון', a => a.sun === 'חמה' ? '☀️ חמה' : '❄️ קרירה'],
            ['מחסן', a => `${a.storage} מ"ר`],
            ['חניה', a => `${a.distance}מ'`],
            ['ציון עסקה', a => `${a.dealScore}/100`],
        ];
        const colWidth = `${Math.floor(80 / apts.length)}%`;
        let html = `<div class="modal-header"><h2><i class="fa-solid fa-scale-balanced"></i> השוואת דירות</h2><button class="close-btn" onclick="document.getElementById('compare-modal').classList.remove('visible')"><i class="fa-solid fa-xmark"></i></button></div>`;
        html += `<div style="overflow-x:auto;"><table class="compare-table"><thead><tr><th style="width:20%;">שדה</th>${apts.map(a => `<th style="width:${colWidth};text-align:center;">טיפוס ${a.aptType}<br><small>מבנה ${a.building}/ד' ${a.aptText}</small></th>`).join('')}</tr></thead><tbody>`;
        fields.forEach(([label, fn]) => {
            html += `<tr><td class="compare-label">${label}</td>${apts.map(a => `<td style="text-align:center;">${fn(a)}</td>`).join('')}</tr>`;
        });
        html += `</tbody></table></div>`;
        document.getElementById('compare-modal-content').innerHTML = html;
        modal.classList.add('visible');
    };

    window.openAptModal = function (apt) {
        const modal = document.getElementById('apt-modal');
        const content = document.getElementById('apt-modal-content');

        const price = apt.price;
        // V6: חלוקה מעודכנת להון עצמי 10% ומשכנתה 90%
        const equityTotal = Math.round(price * 0.10);
        const mortgageTotal = price - equityTotal;

        const paySelection = 2000;
        const payContract = Math.round(price * 0.07) - paySelection;
        // ה-13% הנותרים מורכבים מ-3% הון עצמי ו-10% משכנתה
        const pay13Equity = Math.round(price * 0.03);
        const pay13Mortgage = Math.round(price * 0.10);
        const pay13Total = pay13Equity + pay13Mortgage;

        const pay10 = Math.round(price * 0.10);

        content.innerHTML = `
            <div style="margin-bottom: 1.5rem; text-align: center;">
                <h2><i class="fa-solid fa-house"></i> טיפוס ${apt.aptType}</h2>
                <div style="color: var(--text-muted); font-size: 1.1rem; margin-top: 0.5rem;">
                    מבנה ${apt.building} | דירה ${apt.aptText} | קומה ${apt.floor} | ${apt.rooms} חדרים | ${apt.area} מ"ר
                </div>
                <div style="font-size: 1.8rem; font-weight: bold; color: var(--accent); margin-top: 0.75rem;">${formatPrice(price)} ₪</div>
            </div>
            
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin-bottom: 2rem;">
                <div class="glass-panel" style="padding: 1.5rem; text-align: center;">
                    <i class="fa-solid fa-piggy-bank" style="font-size: 2rem; color: var(--accent); margin-bottom: 0.5rem; display: block;"></i>
                    <h3 style="font-size: 1rem; color: var(--text-muted); margin-bottom: 0.5rem;">הון עצמי (10%)</h3>
                    <div style="font-size: 1.75rem; font-weight: bold; color: var(--text-main);">${formatPrice(equityTotal)} ₪</div>
                </div>
                <div class="glass-panel" style="padding: 1.5rem; text-align: center;">
                    <i class="fa-solid fa-hand-holding-dollar" style="font-size: 2rem; color: var(--primary); margin-bottom: 0.5rem; display: block;"></i>
                    <h3 style="font-size: 1rem; color: var(--text-muted); margin-bottom: 0.5rem;">מימון / משכנתא משוערת (90%)</h3>
                    <div style="font-size: 1.75rem; font-weight: bold; color: var(--text-main);">${formatPrice(mortgageTotal)} ₪</div>
                </div>
            </div>

            <div class="glass-panel" style="padding: 1.5rem; margin-bottom: 1.5rem;">
                <h3 style="margin-bottom: 1rem; border-bottom: 1px solid var(--panel-border); padding-bottom: 0.5rem;">
                    <i class="fa-regular fa-calendar-check"></i> לוח תשלומים רשמי (לפי חוזה)
                </h3>
                <ul style="list-style: none; padding: 0; font-size: 0.95rem;">
                    <!-- 7% -->
                    <li style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem; padding: 0.6rem; background: rgba(5, 150, 105, 0.1); border-radius: 6px;">
                        <div>
                            <div style="font-weight:600; color: var(--text-main);">מעמד בחירת דירה — דמי רצינות</div>
                            <div style="font-size: 0.8rem; color: var(--text-muted);">10.3.2026</div>
                        </div>
                        <strong style="color: var(--primary); font-size: 1.1rem;">${formatPrice(paySelection)} ₪</strong>
                    </li>
                    <li style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem; padding: 0.6rem; background: rgba(5, 150, 105, 0.1); border-radius: 6px;">
                        <div>
                            <div style="font-weight:600; color: var(--text-main);">חתימת חוזה — השלמה ל-7%</div>
                            <div style="font-size: 0.8rem; color: var(--text-muted);">24.3.2026 (השלמה בקיזוז 2,000₪)</div>
                        </div>
                        <strong style="color: var(--primary); font-size: 1.1rem;">${formatPrice(payContract)} ₪</strong>
                    </li>
                    <!-- 13% (split 3/10) -->
                    <li style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem; padding: 0.6rem; background: rgba(5, 150, 105, 0.05); border-radius: 6px;">
                        <div>
                            <div style="font-weight:600; color: var(--text-main);">יתרת תשלום שלישי (13%)</div>
                            <div style="font-size: 0.8rem; color: var(--text-muted);">7.5.2026 (3% הון + 10% משכנתה)</div>
                        </div>
                        <strong style="color: var(--primary); font-size: 1.1rem;">${formatPrice(pay13Total)} ₪</strong>
                    </li>
                    <!-- 8x 10% -->
                    <li style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem; padding: 0.5rem; border-bottom: 1px solid var(--panel-border);">
                        <div><div style="font-weight:500;">תשלום 10%</div><div style="font-size: 0.75rem; color: var(--text-muted);">עד 31.10.2026</div></div>
                        <strong style="color: var(--text-main);">${formatPrice(pay10)} ₪</strong>
                    </li>
                    <li style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem; padding: 0.5rem; border-bottom: 1px solid var(--panel-border);">
                        <div><div style="font-weight:500;">תשלום 10%</div><div style="font-size: 0.75rem; color: var(--text-muted);">עד 31.03.2027</div></div>
                        <strong style="color: var(--text-main);">${formatPrice(pay10)} ₪</strong>
                    </li>
                    <li style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem; padding: 0.5rem; border-bottom: 1px solid var(--panel-border);">
                        <div><div style="font-weight:500;">תשלום 10%</div><div style="font-size: 0.75rem; color: var(--text-muted);">עד 31.08.2027</div></div>
                        <strong style="color: var(--text-main);">${formatPrice(pay10)} ₪</strong>
                    </li>
                    <li style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem; padding: 0.5rem; border-bottom: 1px solid var(--panel-border);">
                        <div><div style="font-weight:500;">תשלום 10%</div><div style="font-size: 0.75rem; color: var(--text-muted);">עד 31.01.2028</div></div>
                        <strong style="color: var(--text-main);">${formatPrice(pay10)} ₪</strong>
                    </li>
                    <li style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem; padding: 0.5rem; border-bottom: 1px solid var(--panel-border);">
                        <div><div style="font-weight:500;">תשלום 10%</div><div style="font-size: 0.75rem; color: var(--text-muted);">עד 30.06.2028</div></div>
                        <strong style="color: var(--text-main);">${formatPrice(pay10)} ₪</strong>
                    </li>
                    <li style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem; padding: 0.5rem; border-bottom: 1px solid var(--panel-border);">
                        <div><div style="font-weight:500;">תשלום 10%</div><div style="font-size: 0.75rem; color: var(--text-muted);">עד 31.12.2028</div></div>
                        <strong style="color: var(--text-main);">${formatPrice(pay10)} ₪</strong>
                    </li>
                    <li style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem; padding: 0.5rem; border-bottom: 1px solid var(--panel-border);">
                        <div><div style="font-weight:500;">תשלום 10%</div><div style="font-size: 0.75rem; color: var(--text-muted);">עד 30.06.2029</div></div>
                        <strong style="color: var(--text-main);">${formatPrice(pay10)} ₪</strong>
                    </li>
                    <!-- Final 10% -->
                    <li style="display: flex; justify-content: space-between; align-items: center; padding: 0.6rem; background: rgba(59, 130, 246, 0.1); border-radius: 6px;">
                        <div>
                            <div style="font-weight:600; color: var(--text-main);">מסירה (10% אחרונים)</div>
                            <div style="font-size: 0.8rem; color: var(--text-muted);">מרץ 2030 (7 ימים לפני קבלת מפתח)</div>
                        </div>
                        <strong style="color: var(--primary); font-size: 1.1rem;">${formatPrice(pay10)} ₪</strong>
                    </li>
                </ul>
            </div>

            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 0.75rem; margin-bottom: 1.5rem;">
                <div class="glass-panel" style="padding: 1rem; font-size: 0.95rem;">
                    <div style="color: var(--text-muted); margin-bottom: 0.25rem;"><i class="fa-solid fa-cloud-sun"></i> מרפסת</div>
                    <div style="font-weight: 600;">${apt.balcony} מ"ר</div>
                </div>
                <div class="glass-panel" style="padding: 1rem; font-size: 0.95rem;">
                    <div style="color: var(--text-muted); margin-bottom: 0.25rem;"><i class="fa-solid fa-box"></i> מחסן</div>
                    <div style="font-weight: 600;">${apt.storage > 0 ? Number(apt.storage).toFixed(2) : 0} מ"ר</div>
                </div>
                <div class="glass-panel" style="padding: 1rem; font-size: 0.95rem;">
                    <div style="color: var(--text-muted); margin-bottom: 0.25rem;"><i class="fa-solid fa-compass"></i> כיוון</div>
                    <div style="font-weight: 600;">${apt.sun === 'חמה' ? '☀️ דרום/מערב (חמה)' : '❄️ צפון/מזרח (קרירה)'}</div>
                </div>
                <div class="glass-panel" style="padding: 1rem; font-size: 0.95rem;">
                    <div style="color: var(--text-muted); margin-bottom: 0.25rem;"><i class="fa-solid fa-car"></i> מרחק חניה</div>
                    <div style="font-weight: 600;">${apt.distance} מ'</div>
                </div>
            </div>

            <div class="glass-panel" style="padding: 1.5rem; margin-bottom: 1.5rem;">
                <h3 style="margin-bottom: 1rem; border-bottom: 1px solid var(--panel-border); padding-bottom: 0.5rem;">
                    <i class="fa-solid fa-calculator"></i> מחשבון משכנתא
                </h3>
                <div style="display:flex; gap:1rem; align-items:center; flex-wrap:wrap; margin-bottom:0.75rem;">
                    <div style="flex:1; min-width:140px;">
                        <label style="color:var(--text-muted); font-size:0.85rem;">ריבית שנתית (%)</label>
                        <input id="mort-rate" type="number" value="4.5" step="0.1" style="width:100%; margin-top:0.3rem; padding:0.5rem; border-radius:6px; background:rgba(15,23,42,0.8); color:white; border:1px solid var(--panel-border); font-family:inherit; text-align:center;" oninput="calcMort('${apt.id}',${apt.price})">
                    </div>
                    <div style="flex:1; min-width:140px;">
                        <label style="color:var(--text-muted); font-size:0.85rem;">שנות משכנתא</label>
                        <input id="mort-years" type="number" value="30" step="1" style="width:100%; margin-top:0.3rem; padding:0.5rem; border-radius:6px; background:rgba(15,23,42,0.8); color:white; border:1px solid var(--panel-border); font-family:inherit; text-align:center;" oninput="calcMort('${apt.id}',${apt.price})">
                    </div>
                    <div style="flex:1; min-width:140px; text-align:center;">
                        <div style="color:var(--text-muted); font-size:0.85rem;">תשלום חודשי</div>
                        <div id="mort-result" style="font-size:1.5rem; font-weight:bold; color:var(--accent); margin-top:0.3rem;">...</div>
                    </div>
                </div>
            </div>

            <div class="glass-panel" style="padding: 1.5rem; margin-bottom: 1.5rem;">
                <h3 style="margin-bottom:0.75rem; border-bottom:1px solid var(--panel-border); padding-bottom:0.5rem;">
                    <i class="fa-solid fa-note-sticky"></i> הערות שלי
                </h3>
                <textarea id="note_${apt.id}" rows="3" placeholder="כתוב הערות אישיות לדירה זו..." style="width:100%; padding:0.75rem; border-radius:8px; background:rgba(15,23,42,0.8); color:white; border:1px solid var(--panel-border); font-family:inherit; font-size:0.95rem; resize:vertical;" oninput="saveNote('${apt.id}')">${getNote(apt.id)}</textarea>
            </div>

            <div style="display: flex; gap: 1rem; justify-content: center; margin-top: 1.5rem;">
                <button onclick="openImageViewer('${apt.aptType}')" class="btn-outline" style="padding: 1rem 2rem; text-align: center; flex: 1; border: none; font-size: 1rem; cursor: pointer; background: rgba(59, 130, 246, 0.1); color: var(--text-main); font-family: inherit; border-radius: 8px;">
                    <i class="fa-solid fa-map"></i> שרטוט פלורפלן
                </button>
                <button onclick="shareWhatsApp('${apt.id}', {stopPropagation:()=>{}})" style="padding: 1rem 2rem; text-align: center; flex: 1; border: none; font-size: 1rem; cursor: pointer; background: rgba(37,211,102,0.1); color: var(--text-main); font-family: inherit; border-radius: 8px; cursor:pointer;">
                    <i class="fa-brands fa-whatsapp" style="color:#25d366;"></i> שתף ב-WhatsApp
                </button>
                <a href="../הגרלה-2279-מפרט-חתום.pdf" target="_blank" class="btn-outline" style="text-decoration:none; padding: 1rem 2rem; text-align: center; flex: 1; border-radius: 8px;">
                    <i class="fa-solid fa-clipboard-list"></i> מפרט טכני
                </a>
            </div>

            <!-- Similar Apartments Section -->
            <div style="margin-top: 2rem;">
                <h3 style="margin-bottom: 1rem; border-bottom: 1px solid var(--panel-border); padding-bottom: 0.5rem;">
                    <i class="fa-solid fa-clone"></i> דירות דומות
                </h3>
                <div style="display:grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap:0.75rem;">
                    ${processedData
                .filter(a => a.id !== apt.id && a.rooms === apt.rooms && Math.abs(a.price - apt.price) < 150000 && a.status !== 'taken')
                .sort((a, b) => b.dealScore - a.dealScore)
                .slice(0, 3)
                .map(a => `
                        <div onclick="window.openAptModal(processedData.find(x=>x.id==='${a.id}'))" style="cursor:pointer; background:var(--card-bg); border:1px solid var(--panel-border); border-radius:12px; padding:1rem; transition:all 0.2s;" onmouseover="this.style.borderColor='var(--primary)'" onmouseout="this.style.borderColor='var(--panel-border)'">
                            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.5rem;">
                                <span class="deal-score-badge score-${a.dealScore >= 70 ? 'high' : a.dealScore >= 45 ? 'mid' : 'low'}">${a.dealScore}</span>
                                <span style="font-size:0.8rem; color:var(--text-muted);">#${a.rank}</span>
                            </div>
                            <div style="font-weight:600; color:var(--accent); font-size:1.05rem;">${formatPrice(a.price)} ₪</div>
                            <div style="font-size:0.85rem; color:var(--text-muted); margin-top:0.4rem;">מבנה ${a.building} | ד׳ ${a.aptText} | ק׳ ${a.floor}</div>
                            <div style="font-size:0.8rem; color:var(--text-muted);">${a.area} מ"ר | ${a.sun === 'חמה' ? '☀️' : '❄️'}</div>
                        </div>`).join('')}
                </div>
            </div>

            <!-- Print Summary Button -->
        `;

        // Mortgage calc init
        setTimeout(() => calcMort(apt.id, apt.price), 50);

        modal.classList.add('visible');
    }

    // === V3 E2: AVAILABLE APARTMENTS COUNT BY ROOM ===
    function renderPriceChart(data) {
        const wrap = document.getElementById('price-chart-wrap');
        if (!wrap) return;
        const groups = {};
        data.filter(a => a.status !== 'taken').forEach(a => {
            const r = parseInt(a.rooms) || 0;
            if (r >= 2) {
                if (!groups[r]) groups[r] = 0;
                groups[r]++;
            }
        });
        const roomCounts = Object.keys(groups).map(Number).sort((a, b) => a - b);
        if (!roomCounts.length) { wrap.innerHTML = ''; return; }
        const maxCount = Math.max(...roomCounts.map(r => groups[r]));
        const colors = ['#1e40af', '#2563eb', '#3b82f6', '#60a5fa', '#93c5fd'];
        wrap.innerHTML = roomCounts.map((r, i) => {
            const count = groups[r];
            const h = Math.max(12, Math.round((count / maxCount) * 48));
            return `<div title="${r} חדרים: ${count} דירות פנויות" style="display:flex; flex-direction:column; align-items:center; gap:2px; cursor:default;">
                <span style="font-size:0.8rem; font-weight:700; color:var(--primary);">${count}</span>
                <div style="width:24px; height:${h}px; background:${colors[i % colors.length]}; border-radius:4px 4px 0 0; transition:height 0.4s;"></div>
                <span style="font-size:0.7rem; font-weight:600; color:var(--text-muted);">${r} חד'</span>
            </div>`;
        }).join('');
    }

    // === G2: FLOOR MAP ===
    function renderFloorMap() {
        const el = document.getElementById('floormap-content');
        if (!el) return;
        const buildings = [...new Set(processedData.map(a => a.building))].sort();
        const floorOrder = [...new Set(processedData.map(a => a.floor))].sort((a, b) => {
            if (a === 'קרקע') return 1;
            if (b === 'קרקע') return 1;
            return parseInt(b) - parseInt(a);
        });

        let html = `<table style="border-collapse:collapse; font-size:0.75rem; direction:rtl; min-width:max-content;">
            <thead><tr><th style="padding:4px 6px; color:var(--text-muted); font-size:0.7rem;">קומה \\ מבנה</th>`;
        buildings.forEach(b => { html += `<th style="padding:4px; color:var(--text-muted); font-size:0.7rem;">${b}</th>`; });
        html += `</tr></thead><tbody>`;

        floorOrder.forEach(floor => {
            html += `<tr><td style="padding:2px 6px; font-weight:600; color:var(--text-muted); font-size:0.7rem;">${floor === 'קרקע' ? 'קרקע' : 'ק׳' + floor}</td>`;
            buildings.forEach(b => {
                const floorApts = processedData.filter(a => a.building === b && a.floor === floor);
                if (!floorApts.length) {
                    html += `<td style="padding:2px;"><div style="width:100%; min-height:24px; border-radius:4px; background:rgba(255,255,255,0.04);"></div></td>`;
                } else {
                    html += `<td style="padding:2px; vertical-align:middle;">
                                <div style="display:flex; gap:2px; justify-content:center;">`;
                    floorApts.forEach(apt => {
                        const isFav = favorites && favorites.has(apt.id);
                        const bg = apt.status === 'taken' ? '#ef4444' : isFav ? '#3b82f6' : '#10b981';
                        const opacity = apt.status === 'taken' ? '0.4' : '0.85';
                        html += `
                            <div title="דירה ${apt.aptText} | ${apt.rooms} חדרים | ${formatPrice(apt.price)}₪" 
                                 onclick="window.openAptModal(processedData.find(x=>x.id==='${apt.id}'));document.getElementById('floormap-modal').classList.remove('visible');" 
                                 style="flex:1; min-width:24px; height:24px; border-radius:4px; background:${bg}; opacity:${opacity}; cursor:pointer; display:flex; align-items:center; justify-content:center; font-size:0.7rem; color:var(--text-main); font-weight:700; transition:all 0.15s;"
                                 onmouseover="this.style.transform='scale(1.15)'" onmouseout="this.style.transform='scale(1)'">
                                ${apt.rooms}
                            </div>`;
                    });
                    html += `</div></td>`;
                }
            });
            html += `</tr>`;
        });
        html += `</tbody></table>`;
        el.innerHTML = html;
    }
    window.openFloorMap = function () {
        renderFloorMap();
        document.getElementById('floormap-modal').classList.add('visible');
    };

    // === ROUND 6: PRINT APT ===
    window.printApt = function (aptId) {
        const apt = processedData.find(a => a.id === aptId);
        if (!apt) return;
        const note = safeGetItem(`note_${aptId}`) || '';
        const w = window.open('', '_blank', 'width=600,height=800');
        w.document.write(`<!DOCTYPE html><html dir="rtl"><head><meta charset="UTF-8">
        <title>דירה ${apt.aptText} - ${apt.building}</title>
        <style>body{font-family:'Segoe UI',sans-serif;padding:2rem;color:#111;direction:rtl;}h1{font-size:1.4rem;margin-bottom:0.5rem;}table{width:100%;border-collapse:collapse;margin-top:1rem;}td{padding:0.5rem 0.75rem;border-bottom:1px solid #eee;}td:first-child{color:#666;width:40%;}footer{margin-top:2rem;font-size:0.8rem;color:#888;text-align:center;}@media print{footer{display:none;}.print-btn{display:none;}}</style>
        </head><body>
        <h1>פרטי דירה — מבנה ${apt.building}, ד׳ ${apt.aptText}</h1>
        <div style="font-size:1.6rem;font-weight:bold;color:#2563eb;">${formatPrice(apt.price)} ₪</div>
        <table>
            <tr><td>ציון עסקה</td><td><strong>${apt.dealScore}/100</strong></td></tr>
            <tr><td>קומה</td><td>${apt.floor}</td></tr>
            <tr><td>חדרים</td><td>${apt.rooms}</td></tr>
            <tr><td>שטח</td><td>${apt.area} מ"ר</td></tr>
            <tr><td>מרפסת</td><td>${apt.balcony} מ"ר</td></tr>
            <tr><td>מחסן</td><td>${apt.storage > 0 ? Number(apt.storage).toFixed(2) : 0} מ"ר</td></tr>
            <tr><td>כיוון</td><td>${apt.sun === 'חמה' ? '☀️ דרום/מערב (חמה)' : '❄️ צפון/מזרח (קרירה)'}</td></tr>
            <tr><td>מרחק חניה</td><td>${apt.distance} מ'</td></tr>
            <tr><td>₪ למ"ר</td><td>${formatPrice(Math.round(apt.price / apt.area))} ₪</td></tr>
            ${note ? `<tr><td>הערות שלי</td><td>${note}</td></tr>` : ''}
        </table>
        <footer>הודפס מ-apartmentsrabin.netlify.app | פרויקט רבין כרמיאל ${new Date().toLocaleDateString('he-IL')}</footer>
        <button class="print-btn" onclick="window.print()" style="margin-top:1.5rem;padding:0.75rem 2rem;background:#2563eb;color:white;border:none;border-radius:8px;font-size:1rem;cursor:pointer;">הדפס / שמור PDF</button>
        </body></html>`);
        w.document.close();
    };

    // === BETA v2: MORTGAGE CALCULATOR ===
    window.calcMort = function (id, fullPrice) {
        const rateEl = document.getElementById('mort-rate');
        const yearsEl = document.getElementById('mort-years');
        const resultEl = document.getElementById('mort-result');
        if (!rateEl || !yearsEl || !resultEl) return;
        const loan = fullPrice * 0.9;
        const r = parseFloat(rateEl.value) / 100 / 12;
        const n = parseInt(yearsEl.value) * 12;
        if (r === 0 || n === 0) return;
        const monthly = Math.round(loan * (r * Math.pow(1 + r, n)) / (Math.pow(1 + r, n) - 1));
        resultEl.textContent = formatPrice(monthly) + ' ₪';
    };

    // Bind globally so the inline onclick can find it
    window.openImageViewer = function (aptType) {
        const viewerModal = document.getElementById('image-viewer-modal');
        const viewerImage = document.getElementById('viewer-image');

        // Sanitize string to match what we downloaded
        const safeName = aptType.replace(/[^a-zA-Z0-9\+\-]/g, '_');
        viewerImage.src = `floorplans/floorplan_${safeName}.png`;

        // Reset zoom state
        scale = 1;
        panX = 0;
        panY = 0;
        applyTransform();

        viewerModal.style.display = 'block';
    };



    // Modal Logic & Pinch Zoom handling
    let scale = 1;
    let panX = 0;
    let panY = 0;

    function applyTransform() {
        const viewerImage = document.getElementById('viewer-image');
        viewerImage.style.transform = `translate(${panX}px, ${panY}px) scale(${scale})`;
    }

    const initModals = () => {
        // Image Viewer specific logic
        const viewerModal = document.getElementById('image-viewer-modal');
        const closeViewerBtn = document.querySelector('.close-viewer');
        const viewerImage = document.getElementById('viewer-image');
        const viewerContainer = document.getElementById('image-viewer-container');

        closeViewerBtn.onclick = () => {
            viewerModal.style.display = 'none';
        };

        // --- iPhone Pinch to Zoom & Pan Logic ---
        let touchState = {
            startX: 0, startY: 0,
            initialDistance: 0, initialScale: 1,
            isPanning: false
        };

        viewerContainer.addEventListener('touchstart', (e) => {
            if (e.touches.length === 2) {
                // Pinch start
                touchState.initialDistance = Math.hypot(
                    e.touches[0].clientX - e.touches[1].clientX,
                    e.touches[0].clientY - e.touches[1].clientY
                );
                touchState.initialScale = scale;
            } else if (e.touches.length === 1) {
                // Pan start
                touchState.isPanning = true;
                touchState.startX = e.touches[0].clientX - panX;
                touchState.startY = e.touches[0].clientY - panY;
            }
        }, { passive: false });

        viewerContainer.addEventListener('touchmove', (e) => {
            e.preventDefault(); // Prevent standard scroll

            if (e.touches.length === 2) {
                // Pinch move
                const distance = Math.hypot(
                    e.touches[0].clientX - e.touches[1].clientX,
                    e.touches[0].clientY - e.touches[1].clientY
                );
                scale = touchState.initialScale * (distance / touchState.initialDistance);
                scale = Math.min(Math.max(1, scale), 4); // Clamp between 1x and 4x
                applyTransform();
            } else if (e.touches.length === 1 && touchState.isPanning) {
                // Pan move
                if (scale > 1) {
                    panX = e.touches[0].clientX - touchState.startX;
                    panY = e.touches[0].clientY - touchState.startY;
                    applyTransform();
                }
            }
        }, { passive: false });

        viewerContainer.addEventListener('touchend', () => {
            touchState.isPanning = false;
        });

        // Allow double tap to reset zoom on mobile
        let lastTap = 0;
        viewerImage.addEventListener('touchend', (e) => {
            const currentTime = new Date().getTime();
            const tapLength = currentTime - lastTap;
            if (tapLength < 500 && tapLength > 0) {
                e.preventDefault();
                scale = scale > 1 ? 1 : 2; // Toggle 1x and 2x
                panX = 0; panY = 0;
                applyTransform();
            }
            lastTap = currentTime;
        });

        // Desktop fallback zooming (Mouse Wheel)
        viewerContainer.addEventListener('wheel', (e) => {
            e.preventDefault();
            scale += e.deltaY * -0.005;
            scale = Math.min(Math.max(1, scale), 4);
            applyTransform();
        }, { passive: false });

        // Docs Modal
        const docsModal = document.getElementById('docs-modal');
        const docsBtn = document.getElementById('docs-btn');
        const docsCloseSpan = document.querySelector('.close-modal');

        docsBtn.onclick = () => docsModal.classList.add('visible');
        docsCloseSpan.onclick = () => docsModal.classList.remove('visible');

        // Specs Modal
        const specsModal = document.getElementById('specs-modal');
        const specsBtn = document.getElementById('specs-btn');
        const specsCloseSpan = document.querySelector('.close-specs-modal');

        specsBtn.onclick = () => specsModal.classList.add('visible');
        specsCloseSpan.onclick = () => specsModal.classList.remove('visible');

        // Apt Modal
        const aptModal = document.getElementById('apt-modal');
        const aptCloseSpan = aptModal.querySelector('.close-modal');
        if (aptCloseSpan) aptCloseSpan.onclick = () => aptModal.classList.remove('visible');

        window.onclick = (e) => {
            if (e.target == docsModal) docsModal.classList.remove('visible');
            if (e.target == specsModal) specsModal.classList.remove('visible');
            if (e.target == aptModal) aptModal.classList.remove('visible');
            if (e.target == viewerContainer) viewerModal.style.display = 'none';
            const compareModal = document.getElementById('compare-modal');
            if (compareModal && e.target == compareModal) compareModal.classList.remove('visible');
        };
    };
    initModals();

    // === BETA v2: COUNTDOWN TIMER ===
    function updateCountdown() {
        const target = new Date('2026-03-10T09:00:00+02:00');
        const now = new Date();
        const diff = target - now;
        const el = document.getElementById('countdown-timer');
        if (!el) return;
        if (diff <= 0) { el.textContent = '🎉 האירוע הגיע!'; return; }
        const d = Math.floor(diff / 86400000);
        const h = Math.floor((diff % 86400000) / 3600000);
        const m = Math.floor((diff % 3600000) / 60000);
        el.textContent = `${d} ימים, ${h} שעות, ${m} דק' עד לבחירת הדירה ⏱️`;
    }
    updateCountdown();
    setInterval(updateCountdown, 60000);

    // === V3: DARK/LIGHT MODE ===
    const savedTheme = safeGetItem('theme') || 'light';
    if (savedTheme === 'dark') {
        document.documentElement.setAttribute('data-theme', 'dark');
        document.body.classList.add('dark-mode');
    } else {
        document.body.classList.add('light-mode');
    }

    window.toggleTheme = function () {
        const isDark = document.documentElement.getAttribute('data-theme') === 'dark';
        if (isDark) {
            document.documentElement.removeAttribute('data-theme');
            document.body.classList.remove('dark-mode');
            document.body.classList.add('light-mode');
        } else {
            document.documentElement.setAttribute('data-theme', 'dark');
            document.body.classList.remove('light-mode');
            document.body.classList.add('dark-mode');
        }
        safeSetItem('theme', isDark ? 'light' : 'dark');
        const btn = document.getElementById('theme-toggle');
        if (btn) btn.innerHTML = isDark ? '<i class="fa-solid fa-moon"></i>' : '<i class="fa-solid fa-sun"></i>';
    };

    // === BETA v2: BACK TO TOP ===
    const backTop = document.getElementById('back-to-top');
    if (backTop) {
        document.addEventListener('scroll', () => {
            backTop.style.display = window.scrollY > 300 ? 'block' : 'none';
        }, { passive: true });
        backTop.addEventListener('click', () => window.scrollTo({ top: 0, behavior: 'smooth' }));
    }

    // === ROUND 4: TOAST NOTIFICATION SYSTEM ===
    window.showToast = function (msg, type = 'info', duration = 2800) {
        const colors = { info: '#3b82f6', success: '#10b981', warn: '#f59e0b', error: '#ef4444' };
        const t = document.createElement('div');
        t.textContent = msg;
        t.style.cssText = `position:fixed; bottom: calc(1rem + env(safe-area-inset-bottom)); left:50%; transform:translateX(-50%); background:${colors[type] || colors.info}; color:white; padding:0.65rem 1.25rem; border-radius:40px; font-family:inherit; font-size:0.9rem; font-weight:500; box-shadow:0 4px 20px rgba(0,0,0,0.3); z-index:99999; animation: toastIn 0.3s ease; pointer-events:none;`;
        document.body.appendChild(t);
        setTimeout(() => {
            t.style.animation = 'toastOut 0.3s ease forwards';
            setTimeout(() => t.remove(), 300);
        }, duration);
    };

    // === ROUND 4: COPY APT LINK ===
    window.copyAptLink = function (aptId, e) {
        if (e) e.stopPropagation();
        const url = `${location.origin}${location.pathname}?apt=${aptId}`;
        navigator.clipboard.writeText(url).then(() => {
            showToast('\u05e7\u05d9\u05e9\u05d5\u05e8 \u05d4\u05d3\u05d9\u05e8\u05d4 \u05d4\u05d5\u05e2\u05ea\u05e7 \u2714', 'success');
        }).catch(() => {
            showToast('\u05e2\u05ea\u05d9\u05e7\u05d4 \u05e0\u05db\u05e9\u05dc\u05d4 - \u05e0\u05e1\u05d4 \u05dc\u05d4\u05e2\u05ea\u05d9\u05e7 \u05d9\u05d3\u05e0\u05d9\u05ea', 'warn');
        });
    };

    // === ROUND 4: DEEP LINK SUPPORT ===
    const urlParams = new URLSearchParams(location.search);
    const deepApt = urlParams.get('apt');
    if (deepApt) {
        const found = processedData.find(a => a.id === deepApt);
        if (found) setTimeout(() => openAptModal(found), 400);
    }

    // === ROUND 4: MOBILE SWIPE FILTER TOGGLE ===
    let touchStartX = 0;
    document.addEventListener('touchstart', (e) => { touchStartX = e.touches[0].clientX; }, { passive: true });
    document.addEventListener('touchend', (e) => {
        const dx = e.changedTouches[0].clientX - touchStartX;
        if (window.innerWidth <= 768 && Math.abs(dx) > 60) {
            const panel = document.getElementById('filters-panel');
            if (dx > 0 && panel && panel.style.display === 'none') toggleMobileFilters();
            if (dx < 0 && panel && panel.style.display !== 'none') toggleMobileFilters();
        }
    }, { passive: true });

    // === V3: SMART RECOMMENDATION BANNER ===
    // Removed in V5

    // === ROUND 5: OFFLINE / ONLINE DETECTION ===
    function updateOnlineStatus() {
        const notice = document.getElementById('offline-notice');
        if (notice) notice.style.display = navigator.onLine ? 'none' : 'block';
    }
    window.addEventListener('online', updateOnlineStatus);
    window.addEventListener('offline', updateOnlineStatus);
    updateOnlineStatus();

    // === ROUND 5: PWA: INSTALL PROMPT CAPTURE ===
    let deferredInstallPrompt = null;
    window.addEventListener('beforeinstallprompt', (e) => {
        e.preventDefault();
        deferredInstallPrompt = e;
        // Show install hint toast after 3 seconds
        setTimeout(() => showToast('\u05d4\u05ea\u05e7\u05df \u05d0\u05ea \u05d4\u05d0\u05e4\u05dc\u05d9\u05e7\u05e6\u05d9\u05d4 \u05dc\u05de\u05e1\u05da \u05d4\u05d1\u05d9\u05ea \ud83d\udce2', 'info', 4000), 3000);
    });

    // === ROUND 5: FAVORITES SHORTLIST SUMMARY ===
    // Removed per user request in V5
});
