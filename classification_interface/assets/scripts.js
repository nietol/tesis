function mapsSetup() {
    var mapProp = {
        center: new google.maps.LatLng(-40, -67),
        zoom: 4,
        disableDefaultUI: true
    };

    mapArgentinaSVM = new google.maps.Map(document.getElementById("mapArgentinaSVM"), mapProp);
    //var mapArgentinaNaive = new google.maps.Map(document.getElementById("mapArgentinaNaive"), mapProp);
}

function buscar() {
    var fechaDesde = 0;
    var fechaHasta = 0;

    //var url = 'http://127.0.0.1:8000/tweets/${fechaDesde}/${fechaHasta}'

    var url = 'http://127.0.0.1:8000/tweets/2018-10-29-UTC/2018-10-30-UTC';

    $.getJSON(url, function (tweets) {        
        for (var i in tweets) {
            // Add the circle for this city to the map.
            var cityCircle = new google.maps.Circle({
                strokeColor: fillColor(tweets[i].polarity_level),
                strokeOpacity: 1,
                strokeWeight: 2,
                fillColor: fillColor(tweets[i].polarity_level),
                fillOpacity: 1,
                map: mapArgentinaSVM,
                center: {lat: tweets[i].geo.latitud, lng: tweets[i].geo.longitud},
                radius: 100
            });
        }//end for
    });
}

function fillColor(polarity_level) {
    let color = '#FF0000';

    if (polarity_level == 0) { //ninguno
        color = 'Green';
    } else if (polarity_level == 1) {//positivo
        color = 'Blue';
    } else if (polarity_level == 2) {//negativo
        color = 'Red';
    } else if (polarity_level == 3) {//neutral
        color = 'Yellow';
    }

    return color;
}//end fillColor
