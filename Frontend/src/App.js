import React, { useEffect, useRef, useState } from "react";
import L from "leaflet";
import "leaflet/dist/leaflet.css";
import "./App.css";
import Select from "react-select";
import { lineString, simplify } from '@turf/turf'; // Импортируем turf.js

// Красный маркер для текущего местоположения
const redIcon = new L.Icon({
  iconUrl: "https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-red.png",
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34],
  shadowUrl: "https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png",
  shadowSize: [41, 41],
});

const customIcon = new L.Icon({
  iconUrl: "https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon.png",
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34],
  shadowUrl: "https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png",
  shadowSize: [41, 41],
});

function App() {
    const mapRef = useRef(null);
    const [userLocation, setUserLocation] = useState(null);
    const [userMarker, setUserMarker] = useState(null);
    const [routeLayer, setRouteLayer] = useState(null);
    const [searchQuery, setSearchQuery] = useState("");
    const [darkMode, setDarkMode] = useState(false);

    useEffect(() => {
        if (!mapRef.current) {
            const map = L.map("map", {
                attributionControl: false, // Отключаем флаг и надпись
            }).setView([47.2357, 39.7015], 13); // Ростов-на-Дону
            mapRef.current = map;

            // Добавляем слой карты OpenStreetMap без атрибуции
            L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
                maxZoom: 19,
                attribution: '', // Убираем атрибуцию
            }).addTo(map);

            // Определяем текущее местоположение
            map.locate({ setView: true, maxZoom: 14 });

            // Обработчик события locationfound
            map.on("locationfound", (e) => {
                const { latlng } = e;

                // Удаляем старый маркер, если он существует
                if (userMarker) {
                    map.removeLayer(userMarker);
                }

                // Добавляем новый маркер для текущего местоположения
                const newUserMarker = L.marker(latlng, { icon: redIcon }).addTo(map).bindPopup("Вы здесь").openPopup();
                setUserMarker(newUserMarker);
                setUserLocation(latlng);
            });

            map.on("locationerror", () => {
                alert("Не удалось определить местоположение. Карта начнет с центра Ростова-на-Дону.");
            });
        }
    }, [userMarker]);

    const findPlaces = async () => {
        if (!searchQuery) {
            alert("Введите то, что вы хотите найти.");
            return;
        }

        const map = mapRef.current;
        const bbox = map.getBounds();
        const url = `https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(
            searchQuery
        )}&bounded=1&viewbox=${bbox.getWest()},${bbox.getNorth()},${bbox.getEast()},${bbox.getSouth()}&limit=15`;

        clearMap();

        try {
            const response = await fetch(url);
            const data = await response.json();

            if (data.length === 0) {
                alert("Места поблизости не найдены!");
                return;
            }

            data.forEach((place) => {
                const lat = parseFloat(place.lat);
                const lon = parseFloat(place.lon);
                const name = place.display_name;

                const placeMarker = L.marker([lat, lon], { icon: customIcon }).addTo(map);

                placeMarker.bindPopup(`
                    <div class="popup-card">
                        <img src="https://kartinki.pics/uploads/posts/2022-12/1670431829_3-kartinkin-net-p-serii-kvadrat-kartinka-oboi-3.jpg" alt="${name}">
                        <div class="info">
                            <h3>${name}</h3>
                            <p>Координаты: ${lat.toFixed(4)}, ${lon.toFixed(4)}</p>
                            <button onclick="window.navigateTo([${lat}, ${lon}])" class="navigate-btn">Отправиться</button>
                        </div>
                    </div>
                `);
            });
        } catch (error) {
            console.error("Ошибка поиска мест:", error);
            alert("Не удалось выполнить поиск. Попробуйте еще раз.");
        }
    };

    const navigateTo = async (destination) => {
        if (!userLocation) {
            alert("Местоположение пользователя не определено!");
            return;
        }

        const map = mapRef.current;
        const routingUrl = `https://router.project-osrm.org/route/v1/foot/${userLocation.lng},${userLocation.lat};${destination[1]},${destination[0]}?overview=simplified&steps=false&geometries=geojson`;

        try {
            const response = await fetch(routingUrl);
            const data = await response.json();

            if (!data.routes || data.routes.length === 0) {
                alert("Маршрут не найден!");
                return;
            }

            const route = data.routes[0].geometry;
            const distance = data.routes[0].distance; // Расстояние в метрах
            const duration = data.routes[0].duration; // Время в секундах

            // Проверка на реальное время в пути (5 км/ч = 83.3 м/мин)
            const realisticDuration = Math.max(duration, distance / 83.3 * 60);

            // Упрощаем маршрут с помощью turf.js
            const optimizedRoute = simplify(lineString(route.coordinates), { tolerance: 0.001, highQuality: true });

            // Удаляем предыдущий маршрут, если он есть
            if (routeLayer) {
                map.removeLayer(routeLayer);
            }

            // Отображаем маршрут на карте
            const newRouteLayer = L.geoJSON(optimizedRoute, {
                style: { color: "#42a5f5", weight: 4 },
            }).addTo(map);

            setRouteLayer(newRouteLayer);

            // Увеличиваем масштаб, чтобы показать весь маршрут
            const bounds = L.geoJSON(optimizedRoute).getBounds();
            map.fitBounds(bounds);

            // Отображаем расстояние и время в попапе
            const destinationMarker = L.marker(destination, { icon: customIcon }).addTo(map);
            destinationMarker.bindPopup(`
                <div class="popup-card">
                    <div class="info">
                        <h3>Расстояние: ${(distance / 1000).toFixed(2)} км</h3>
                        <p>Время в пути: ${Math.round(realisticDuration / 60)} мин</p>
                    </div>
                </div>
            `).openPopup();
        } catch (error) {
            console.error("Ошибка построения маршрута:", error);
            alert("Не удалось построить маршрут. Попробуйте позже.");
        }
    };

    const clearMap = () => {
        const map = mapRef.current;
        map.eachLayer((layer) => {
            // Исключаем маркер текущего местоположения из удаления
            if ((layer instanceof L.Marker || layer instanceof L.GeoJSON) && layer !== userMarker) {
                map.removeLayer(layer);
            }
        });

        if (routeLayer) {
            map.removeLayer(routeLayer);
        }
    };

    window.navigateTo = navigateTo;

    const toggleDarkMode = () => {
        setDarkMode(!darkMode);
        document.body.classList.toggle('dark-mode', !darkMode);
    };

    // Опции для react-select
    const options = [
        { value: "Кафе", label: "Кафе" },
        { value: "Музей", label: "Музей" },
        { value: "Парк", label: "Парк" },
        { value: "Ресторан", label: "Ресторан" },
    ];

    return (
        <div className="container">
            <div className="controls">
                <Select
                    options={options}
                    value={options.find((option) => option.value === searchQuery)}
                    onChange={(selectedOption) => setSearchQuery(selectedOption.value)}
                    placeholder="Что найти?"
                />
                <button onClick={findPlaces}>Поиск</button>
                <button onClick={toggleDarkMode}>
                    {darkMode ? "Светлый режим" : "Темный режим"}
                </button>
            </div>
            <div id="map" style={{ width: "100%", height: "700px" }}></div>
        </div>
    );
}

export default App;