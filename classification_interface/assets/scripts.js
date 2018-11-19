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
                strokeColor: '#FF0000',
                strokeOpacity: 0.8,
                strokeWeight: 2,
                fillColor: '#FF0000',
                fillOpacity: 0.35,
                map: mapArgentinaSVM,
                center: {lat: tweets[i].geo.latitud, lng: tweets[i].geo.longitud},
                radius: 100
            });
        }//end for
    });
}