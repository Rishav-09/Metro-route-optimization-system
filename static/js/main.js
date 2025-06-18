document.addEventListener('DOMContentLoaded', function() {
    const sourceDropdown = document.getElementById('sourceDropdown');
    const destinationDropdown = document.getElementById('destinationDropdown');
    const searchBtn = document.getElementById('searchBtn');
    const routeDetails = document.getElementById('routeDetails');
    const routeSummary = document.getElementById('routeSummary');
    const noRoute = document.getElementById('noRoute');
    const sourceStation = document.getElementById('sourceStation');
    const destStation = document.getElementById('destStation');
    const totalDistance = document.getElementById('totalDistance');
    const totalStations = document.getElementById('totalStations');
    const estimatedFare = document.getElementById('estimatedFare');
    const stationList = document.getElementById('stationList');
    
    // Initialize map
    const metroMap = L.map('metroMap').setView([28.6139, 77.2090], 12);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(metroMap);
    
    let stationMarkers = {};
    let lineLayers = {};
    let currentRouteLayer = null;
    let visitedMarkers = [];
    
    // Create map legend
    const legend = L.control({position: 'bottomright'});
    legend.onAdd = function(map) {
        const div = L.DomUtil.create('div', 'map-legend');
        div.innerHTML = '<h3>Metro Lines</h3><div id="legendItems"></div>';
        return div;
    };
    legend.addTo(metroMap);
    
    // Fetch stations data
    fetch('/stations')
        .then(res => res.json())
        .then(stations => {
            // Populate dropdowns
            stations.forEach(station => {
                let opt1 = document.createElement('option');
                opt1.value = station;
                opt1.textContent = station;
                sourceDropdown.appendChild(opt1);

                let opt2 = document.createElement('option');
                opt2.value = station;
                opt2.textContent = station;
                destinationDropdown.appendChild(opt2);
            });
            
            // Draw basic map with stations
            fetch('/stations-data')
                .then(res => res.json())
                .then(stationsData => {
                    drawMetroMap(stationsData);
                })
                .catch(err => {
                    console.error('Error loading station data:', err);
                });
        })
        .catch(err => {
            console.error('Error loading stations:', err);
        });
    
    function drawMetroMap(stationsData) {
        // First get line colors
        fetch('/lines')
            .then(res => res.json())
            .then(lines => {
                // Update legend with line colors
                updateLegend(lines);
                
                // Group stations by line for better line drawing
                const stationsByLine = {};
                stationsData.forEach(station => {
                    if (!stationsByLine[station.line]) {
                        stationsByLine[station.line] = [];
                    }
                    stationsByLine[station.line].push(station);
                });

                // Draw lines first (so stations appear on top)
                Object.entries(stationsByLine).forEach(([lineName, stations]) => {
                    const lineColor = lines[lineName] || '#3498db';
                    
                    // Sort stations to draw line segments between neighbors
                    const lineCoords = stations.map(s => [s.coords[0], s.coords[1]]);
                    
                    // Add line to map
                    const lineLayer = L.polyline(lineCoords, {
                        color: lineColor,
                        weight: 4,
                        opacity: 0.7,
                        smoothFactor: 1
                    }).addTo(metroMap);
                    
                    lineLayers[lineName] = lineLayer;
                });

                // Draw stations with line-specific colors
                stationsData.forEach(station => {
                    const lineColor = lines[station.line] || '#3498db';
                    
                    const marker = L.circleMarker([station.coords[0], station.coords[1]], {
                        radius: 6,
                        fillColor: lineColor,
                        color: '#fff',
                        weight: 1.5,
                        opacity: 1,
                        fillOpacity: 0.9,
                        className: 'station-marker'
                    }).addTo(metroMap);
                    
                    marker.bindPopup(`<b>${station.name}</b><br>Line: ${station.line}`);
                    stationMarkers[station.name] = marker;
                });
            })
            .catch(err => {
                console.error('Error loading lines:', err);
            });
    }
    
    function updateLegend(lines) {
        const legendItems = document.getElementById('legendItems');
        legendItems.innerHTML = '';
        
        Object.entries(lines).forEach(([lineName, color]) => {
            const item = document.createElement('div');
            item.className = 'legend-item';
            
            const colorBox = document.createElement('div');
            colorBox.className = 'legend-color';
            colorBox.style.backgroundColor = color;
            
            const label = document.createElement('span');
            label.textContent = lineName.charAt(0).toUpperCase() + lineName.slice(1);
            
            item.appendChild(colorBox);
            item.appendChild(label);
            legendItems.appendChild(item);
        });
    }
    
    // Find route button
    searchBtn.addEventListener('click', function() {
        const source = sourceDropdown.value;
        const destination = destinationDropdown.value;
        
        if (!source || !destination) {
            alert('Please select both source and destination stations');
            return;
        }
        
        if (source === destination) {
            alert('Source and destination cannot be the same');
            return;
        }
        
        findRoute(source, destination);
    });
    
    function findRoute(source, destination) {
        // Clear previous route
        if (currentRouteLayer) {
            metroMap.removeLayer(currentRouteLayer);
            currentRouteLayer = null;
        }
        
        // Reset all markers to default style
        Object.values(stationMarkers).forEach(marker => {
            const lineColor = marker.options.fillColor;
            marker.setStyle({
                radius: 6,
                fillColor: lineColor,
                color: '#fff',
                weight: 1.5
            });
        });
        
        // Clear visited markers
        visitedMarkers.forEach(marker => metroMap.removeLayer(marker));
        visitedMarkers = [];
        
        fetch('/route', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ source, destination })
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            if (data.error) {
                routeDetails.classList.add('hidden');
                routeSummary.classList.add('hidden');
                noRoute.classList.remove('hidden');
                return;
            }
            
            // Show route details
            routeDetails.classList.remove('hidden');
            routeSummary.classList.remove('hidden');
            noRoute.classList.add('hidden');
            sourceStation.textContent = source;
            destStation.textContent = destination;
            totalDistance.textContent = data.distance + ' km';
            totalStations.textContent = data.stations_count;
            estimatedFare.textContent = '₹' + data.fare;
            
            // Display station list
            stationList.innerHTML = '';
            data.path.forEach(station => {
                const li = document.createElement('li');
                li.textContent = station.name;
                stationList.appendChild(li);
            });
            
            // Draw the route on the map
            const routeCoords = data.path.map(station => [
                station.coords[0], 
                station.coords[1]
            ]);
            
            currentRouteLayer = L.polyline(routeCoords, {
                color: '#FF4500',
                weight: 5,
                opacity: 0.9,
                className: 'path-highlight'
            }).addTo(metroMap);
            
            // Highlight source and destination
            if (stationMarkers[source]) {
                stationMarkers[source].setStyle({
                    radius: 8,
                    fillColor: '#FF0000',
                    color: '#000',
                    weight: 2
                });
            }
            
            if (stationMarkers[destination]) {
                stationMarkers[destination].setStyle({
                    radius: 8,
                    fillColor: '#00FF00',
                    color: '#000',
                    weight: 2
                });
            }
            
            // Fit map to route bounds
            metroMap.fitBounds(currentRouteLayer.getBounds(), { padding: [50, 50] });
        })
        .catch(error => {
            console.error('Error:', error);
            routeDetails.classList.add('hidden');
            routeSummary.classList.add('hidden');
            noRoute.classList.remove('hidden');
            noRoute.textContent = 'An error occurred while finding the route. Please try again.';
        });
    }
});
