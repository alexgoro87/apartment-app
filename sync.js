// Firebase Synchronization Logic for Project Rabin Carmiel
// V26: Full real-time sync of favorites, notes, and apartment statuses

const firebaseConfig = {
    apiKey: "AIzaSyCmufyhGZJeSNXS6aRbyUweRCJ83LijeYY",
    authDomain: "rabin-apartment.firebaseapp.com",
    databaseURL: "https://rabin-apartment-default-rtdb.firebaseio.com",
    projectId: "rabin-apartment",
    storageBucket: "rabin-apartment.firebasestorage.app",
    messagingSenderId: "104278240998",
    appId: "1:104278240998:web:3cf37a570f6222ab02d527"
};

// Initialize Firebase
let firebaseReady = false;
if (typeof firebase !== 'undefined') {
    try {
        firebase.initializeApp(firebaseConfig);
        firebaseReady = true;
        console.log("✅ Firebase initialized successfully");
    } catch (e) {
        console.warn("Firebase init error:", e.message);
    }
}

// === SYNC FAVORITES ===
window.syncFavorite = function (aptId, userId, isFav) {
    if (!firebaseReady) return;
    const ref = firebase.database().ref(`favorites/${userId}/${aptId}`);
    if (isFav) {
        ref.set(true);
    } else {
        ref.remove();
    }
};

// === SYNC NOTES ===
window.syncNote = function (aptId, noteText) {
    if (!firebaseReady) return;
    const ref = firebase.database().ref(`notes/${aptId}`);
    if (noteText && noteText.trim()) {
        ref.set(noteText);
    } else {
        ref.remove();
    }
};

// === SYNC APARTMENT STATUS (taken/available) ===
window.syncAptStatus = function (aptKey, status) {
    if (!firebaseReady) return;
    const ref = firebase.database().ref(`statuses/${aptKey}`);
    if (status && status !== 'available') {
        ref.set(status);
    } else {
        ref.remove();
    }
};

// === LISTEN FOR REAL-TIME UPDATES ===
function startListening() {
    if (!firebaseReady) return;

    // Listen to favorites
    firebase.database().ref('favorites').on('value', (snapshot) => {
        const data = snapshot.val() || {};
        // Store cloud data for cross-user highlighting
        window.cloudFavs = data;

        // Merge into localStorage per user
        Object.keys(data).forEach(userId => {
            const userFavs = Object.keys(data[userId] || {});
            localStorage.setItem(`apt_favorites_${userId}`, JSON.stringify(userFavs));
        });

        console.log("☁️ Favorites synced from cloud");
        if (window.renderData) window.renderData();
    });

    // Listen to notes
    firebase.database().ref('notes').on('value', (snapshot) => {
        const data = snapshot.val() || {};
        Object.keys(data).forEach(aptId => {
            localStorage.setItem(`note_${aptId}`, data[aptId]);
        });
        console.log("☁️ Notes synced from cloud");
    });

    // Listen to statuses
    firebase.database().ref('statuses').on('value', (snapshot) => {
        const data = snapshot.val() || {};
        Object.keys(data).forEach(aptKey => {
            localStorage.setItem(aptKey, data[aptKey]);
        });
        console.log("☁️ Statuses synced from cloud");
        if (window.renderData) window.renderData();
    });
}

// === UPLOAD ALL LOCAL DATA TO CLOUD (one-time migration) ===
window.uploadAllToCloud = function () {
    if (!firebaseReady) return;

    // Upload favorites
    ['me', 'wife', 'advisor'].forEach(userId => {
        const favsJson = localStorage.getItem(`apt_favorites_${userId}`);
        if (favsJson) {
            try {
                const favs = JSON.parse(favsJson);
                favs.forEach(aptId => {
                    firebase.database().ref(`favorites/${userId}/${aptId}`).set(true);
                });
            } catch (e) { }
        }
    });

    // Upload notes
    for (let i = 0; i < localStorage.length; i++) {
        const key = localStorage.key(i);
        if (key.startsWith('note_')) {
            const aptId = key.replace('note_', '');
            const val = localStorage.getItem(key);
            if (val) firebase.database().ref(`notes/${aptId}`).set(val);
        }
    }

    // Upload statuses
    for (let i = 0; i < localStorage.length; i++) {
        const key = localStorage.key(i);
        if (key.startsWith('apt_') && !key.startsWith('apt_favorites')) {
            const val = localStorage.getItem(key);
            if (val && val !== 'available') {
                firebase.database().ref(`statuses/${key}`).set(val);
            }
        }
    }

    console.log("☁️ All local data uploaded to cloud");
};

// Start listening when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    setTimeout(() => {
        startListening();
        // One-time upload of existing local data to cloud
        if (firebaseReady && !localStorage.getItem('cloud_migrated')) {
            window.uploadAllToCloud();
            localStorage.setItem('cloud_migrated', 'true');
        }
    }, 1000);
});
