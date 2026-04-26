// --------------------------------------------
// AgriCare - Nearby Agriculture Shops Map
// --------------------------------------------

let map;
let userMarker;
let directionsService;
let directionsRenderer;

// Initialize Map
function initMap() {
    directionsService = new google.maps.DirectionsService();
    directionsRenderer = new google.maps.DirectionsRenderer();

    // Default center (India)
    map = new google.maps.Map(document.getElementById("map"), {
        center: { lat: 20.5937, lng: 78.9629 },
        zoom: 6
    });

    directionsRenderer.setMap(map);

    // Get user location
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
            position => {
                const userLocation = {
                    lat: position.coords.latitude,
                    lng: position.coords.longitude
                };

                map.setCenter(userLocation);
                map.setZoom(14);

                userMarker = new google.maps.Marker({
                    position: userLocation,
                    map: map,
                    title: "Your Location",
                    icon: "https://maps.google.com/mapfiles/ms/icons/blue-dot.png"
                });

                findNearbyShops(userLocation);
            },
            () => {
                alert("Location access denied. Enable GPS to find nearby shops.");
            }
        );
    } else {
        alert("Geolocation is not supported by this browser.");
    }
}

// Find Nearby Agriculture Shops
function findNearbyShops(location) {
    const service = new google.maps.places.PlacesService(map);

    const request = {
        location: location,
        radius: 5000, // 5 KM radius
        keyword: ["fertilizer shop", "agriculture store", "pesticide shop"]
    };

    service.nearbySearch(request, (results, status) => {
        if (status === google.maps.places.PlacesServiceStatus.OK) {
            results.forEach(place => createShopMarker(place));
        } else {
            alert("No nearby agriculture shops found.");
        }
    });
}

// Create marker for shop
function createShopMarker(place) {
    const marker = new google.maps.Marker({
        position: place.geometry.location,
        map: map,
        title: place.name,
        icon: "https://maps.google.com/mapfiles/ms/icons/green-dot.png"
    });

    const infoWindow = new google.maps.InfoWindow({
        content: `
            <div style="font-size:14px">
                <b>${place.name}</b><br>
                ${place.vicinity || ""}<br>
                <button onclick="getRoute(${place.geometry.location.lat()}, ${place.geometry.location.lng()})"
                        style="margin-top:5px; padding:5px 10px; background:#2e7d32; color:white; border:none; border-radius:5px;">
                    Get Route
                </button>
            </div>
        `
    });

    marker.addListener("click", () => {
        infoWindow.open(map, marker);
    });
}

// Draw route from user to shop
function getRoute(destLat, destLng) {
    if (!userMarker) return;

    const request = {
        origin: userMarker.getPosition(),
        destination: { lat: destLat, lng: destLng },
        travelMode: google.maps.TravelMode.DRIVING
    };

    directionsService.route(request, (result, status) => {
        if (status === google.maps.DirectionsStatus.OK) {
            directionsRenderer.setDirections(result);
        } else {
            alert("Unable to calculate route.");
        }
    });
}
