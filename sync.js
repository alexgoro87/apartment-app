// Firebase Synchronization Logic for Project Rabin Carmiel
// Will be populated with actual config keys once established

const firebaseConfig = {
    // Keys will be injected or requested
    apiKey: "PLACEHOLDER",
    authDomain: "apartment-app-one-chi.firebaseapp.com",
    databaseURL: "https://apartment-app-one-chi-default-rtdb.firebaseio.com",
    projectId: "apartment-app-one-chi",
    storageBucket: "apartment-app-one-chi.appspot.com",
    messagingSenderId: "PLACEHOLDER",
    appId: "PLACEHOLDER"
};

// Initialize Firebase
if (typeof firebase !== 'undefined') {
    firebase.initializeApp(firebaseConfig);
    const db = firebase.database();
    console.log("Firebase initialized");
}

window.syncFavorite = function (aptId, userId, status) {
    if (typeof firebase === 'undefined' || !firebase.database) return;
    const ref = firebase.database().ref(`favorites/${aptId}/${userId}`);
    ref.set(status);
};

window.listenToFavorites = function (callback) {
    if (typeof firebase === 'undefined' || !firebase.database) return;
    const ref = firebase.database().ref('favorites');
    ref.on('value', (snapshot) => {
        const val = snapshot.val();
        if (val) callback(val);
    });
};

// Initial listener to merge cloud favorites into local favorites
document.addEventListener('DOMContentLoaded', () => {
    setTimeout(() => {
        if (window.listenToFavorites) {
            window.listenToFavorites((cloudData) => {
                // Here we store cloud data for cross-user highlighting in renderData
                window.cloudFavs = cloudData;
                if (window.renderData) window.renderData();
                console.log("Cloud sync update received");
            });
        }
    }, 1500);
});
