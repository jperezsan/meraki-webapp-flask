
var mx_devices = null;

$(document).ready(function() {
    FillMap();
});

$("#refresh-button").click(function () {
    location.reload();
});

function FillMap() {
    $.get({
        url: "/api/mx-devices", success: function (devices, status) {
            if (status === 'success') {
                map.removeObjects(map.getObjects());
                mx_devices = devices;

                // Request data that will be visualized on a map
                startClustering(map, ui, Object.values(devices));
                // Object.keys(devices).forEach(key => {
                //     device = devices[key]
                //     console.log(device);

                //     device_coords = { lat: device.lat, lng: device.lng }

                //     var svgMarkup = '<a href="https://www.google.com" target="_blank" onclick="displayTablita(\'' + device.serial + '\'); return false;"><svg  width="65" height="24" xmlns="http://www.w3.org/2000/svg">' +
                //         '<rect stroke="black" fill="${FILL}" x="1" y="1" width="65" height="22" />' +
                //         '<text x="30" y="18" font-size="12pt" font-family="Arial" font-weight="bold" ' +
                //         'text-anchor="middle" fill="${STROKE}">' +
                //         device.model +
                //         ' </text></svg></a>';

                //     var icon = new H.map.DomIcon(svgMarkup.replace('${FILL}', device.color).replace('${STROKE}', 'black'));

                //     var device_marker = new H.map.DomMarker(device_coords, { icon: icon });
                //     map.addObject(device_marker);
                // });
                
                map.getEngine().addEventListener('render', (evt) => {
                    if (map.getEngine() === evt.target) {                         
                        $("#loading-animation").addClass("d-none"); 
                        $("#loading-animation-text").addClass("d-none");                         
                    } 
                });
            }
        }
    });
};

/**
 * Make clustering of markers with a custom theme
 *
 * Note that the maps clustering module https://js.api.here.com/v3/3.1/mapsjs-clustering.js
 * must be loaded to use the Clustering
 *
 * @param {H.Map} map A HERE Map instance within the application
 * @param {H.ui.UI} ui Default ui component
 * @param {Object[]} data Raw data containing information about each device
 */
function startClustering(map, ui, data) {
    // First we need to create an array of DataPoint objects for the ClusterProvider
    var dataPoints = data.map(function (item) {
        // Note that we pass "null" as value for the "altitude"
        // Last argument is a reference to the original data to associate with our DataPoint
        // We will need it later on when handling events on the clusters/noise points for showing
        // details of that point
        return new H.clustering.DataPoint(item.lat, item.lng, null, item);
    });

    // Create a clustering provider with a custom theme
    var clusteredDataProvider = new H.clustering.Provider(dataPoints, {
        clusteringOptions: {
            // Maximum radius of the neighborhood
            eps: 32,
            // minimum weight of points required to form a cluster
            minWeight: 2
        },
        theme: CUSTOM_THEME
    });
    // Note that we attach the event listener to the cluster provider, and not to
    // the individual markers
    clusteredDataProvider.addEventListener('tap', onMarkerClick);

    // Create a layer that will consume objects from our clustering provider
    var layer = new H.map.layer.ObjectLayer(clusteredDataProvider);

    // To make objects from clustering provider visible,
    // we need to add our layer to the map
    map.addLayer(layer);
}

// Custom clustering theme description object.
// Object should implement H.clustering.ITheme interface
var CUSTOM_THEME = {
    getClusterPresentation: function (cluster) {
        var dataPoints = [];

        // Iterate through all points which fall into the cluster and store references to them
        cluster.forEachDataPoint(dataPoints.push.bind(dataPoints));
        
        var svgMarkup = `<svg xmlns="http://www.w3.org/2000/svg" width="50" height="50">                            
                            <circle stroke="black" cx="25" cy="25" r="20" fill="${getClusterColor(dataPoints)}"></circle>
                            <text x="25" y="30" font-size="12pt" font-family="Arial" font-weight="bold" text-anchor="middle">
                            ${dataPoints.length}
                            </text>
                         </svg>`;
        // Create a marker from a point in the cluster
        var clusterMarker = new H.map.Marker(cluster.getPosition(), {
            icon: new H.map.Icon(svgMarkup),

            // Set min/max zoom with values from the cluster,
            // otherwise clusters will be shown at all zoom levels:
            min: cluster.getMinZoom(),
            max: cluster.getMaxZoom()
        });

        // Link data from the random point from the cluster to the marker,
        // to make it accessible inside onMarkerClick
        clusterMarker.setData(dataPoints);

        return clusterMarker;
    },
    getNoisePresentation: function (noisePoint) {
        var svgMarkup = '<svg width="65" height="24" xmlns="http://www.w3.org/2000/svg">' +
                    '<rect stroke="black" fill="${FILL}" x="0" y="0" width="65" height="24" rx="5" />' +
                    '<text x="30" y="18" font-size="10pt" font-family="Arial, Helvetica, sans-serif" font-weight="bold" ' +
                    'text-anchor="middle" fill="${STROKE}">'+
                     '${NAME}'+
                    ' </text></svg>';
     
        //var icon = new H.map.DomIcon(svgMarkup.replace('${FILL}', 'white').replace('${STROKE}', 'black')); 
        // Get a reference to data object our noise points
        var data = noisePoint.getData(),
            // Create a marker for the noisePoint
            noiseMarker = new H.map.Marker(noisePoint.getPosition(), {
                // Use min zoom from a noise point
                // to show it correctly at certain zoom levels:
                min: noisePoint.getMinZoom(),
                icon: new H.map.Icon(svgMarkup.replace('${FILL}', getNoisePointColor(data.color))
                                              .replace('${STROKE}', '#fff')
                                              .replace('${NAME}','MX'))
            });

        // Link a data from the point to the marker
        // to make it accessible inside onMarkerClick
        noiseMarker.setData(data);

        return noiseMarker;
    }
};

/**
 * CLICK/TAP event handler for our markers. That marker can represent either a single device or
 * a cluster (group of devices)
 * @param {H.mapevents.Event} e The event object
 */
function onMarkerClick(e) {
    // Get position of the "clicked" marker
    var position = e.target.getGeometry(),
        // Get the data associated with that marker
        data = e.target.getData();

    if (data.length > 1) {
        map.setZoom(map.getZoom() + 1);
    }

    displayTablita(data);

    // Move map's center to a clicked marker
    map.setCenter(position, true);
}

function getStatusBadgeMarkup(color) {
    let colorMarkup = "";
    switch(color) {
        case "Green":
            colorMarkup = '<span class="badge badge-pill badge-meraki-green">Green</span>';
            break;
        case "Yellow":
            colorMarkup = '<span class="badge badge-pill badge-warning">Yellow</span>';
            break;
        case "Orange":
            colorMarkup = '<span class="badge badge-pill badge-orange">Orange</span>';
            break;
        case "Blue":
            colorMarkup = '<span class="badge badge-pill badge-primary">Blue</span>';
            break;
        case "Red":
            colorMarkup = '<span class="badge badge-pill badge-danger">Red</span>';
            break;
        default:
            colorMarkup = '<span class="badge badge-pill badge-info">Status Unknown</span>';                    
    }
    return colorMarkup;
}

function getClusterColor(devices) {
    for (var i=0; i<devices.length; i++) {
        let device = devices[i].getData();
        if (device.color !== "Green" ) {
            return "#dd0079";
        }
    }
    return "#6FB73A"
}

function getNoisePointColor(color) {
    switch(color) {
        case "Green":
            return "#6FB73A";
        case "Blue":
            return "#007bff";
        case "Yellow":
            return "#ffc107"; 
        case "Orange":
            return "#ff8b07";
        case "Red":
            return "#dc3545";            
    }
    return "White";
}

function displayTablita(devices) {
    if (Array.isArray(devices)) {
        var templateHTML = `                               
        <table class="table table-sm table-responsive">
            <thead>
                <tr>
                    <th>Name</th>
                    <th>Status</th>                                                       
                </tr>
            </thead>
            <tbody>
    `;

        for (var i = 0; i < devices.length; i++) {
            device = devices[i].getData();            
            templateHTML += `
            <tr>
                <td class="text-break">${device.name}</td>
                <td>${getStatusBadgeMarkup(device.color)}</td>
                <td>
                    <button onclick="displayTablita('${device.serial}')" class="btn btn-sm btn-primary">
                        Device Info
                    </button>
                </td>
                <td>
                    <a class="btn btn-sm btn-meraki-green" target="_blank" href="${device.url}" role="button">View in Dashboard</a>
                </td>             
            </tr>            
        `;
        }

        templateHTML += "</tbody></table><br />"
        $("#tablita").html(templateHTML);
    } else {
        var device = null;
        if (typeof devices === 'string') {
            device = mx_devices[devices];
        } else {
            device = devices;
        }
        
        var templateHTML = `        
        <h1>Device status ${getStatusBadgeMarkup(device.color)}</h1>
        <h2 class="text-break">${device.name}</h2>
        <h4><b>Serial:</b> ${device.serial}</h4>
        <h4><b>MAC address:</b> ${device.mac}</h4>
        <div class="card">
            <div class="card-body">
                <h5><b>Address:</b> ${device.address}</h5>
                <h5><b>Coordinates:</b> Lat: ${device.lat} Lng: ${device.lng}</h5>
            </div>        
        </div>   
        <br />     
        <h4>WAN uplinks health</h4>
        <ul>                        
    `;

        for (var i = 0; i < device.uplinks.length; i++) {
            templateHTML += `
            <li>${device.uplinks[i].uplink} ${getStatusBadgeMarkup(device.uplinks[i].color)}</li>
            <ul>
                <li>Test IP: ${device.uplinks[i].ip}</li>                
                <li>Packet loss Percent: ${device.uplinks[i].loss_average}%</li>
                <li>Latency: ${device.uplinks[i].latency_average} ms</li>
            </ul>
        `;
        }

        templateHTML += `</ul><a class="btn btn-block btn-meraki-green" target="_blank" href="${device.url}" role="button">View in Dashboard</a><br />`;

        $("#tablita").html(templateHTML);
        $('html, body').animate({
            scrollTop: $("#tablita").offset().top
        }, 2000);        
    }
}