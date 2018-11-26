var constants =
    {
        newTweetsEvt: 'new-tweets-evt',
        newRefCounts: 'new-ref-counts-evt'
    }

var globalData =
    {
        map: null,
        tweets: [],
        mapMarkers: {
            ninguno: [],
            positivo: [],
            negativo: [],
            neutral: []
        }
    };

function Tweet(tdata) {
    for (var key in tdata) {
        this[key] = tdata[key];
    }
    
    this.date_string = new Date(tdata.date.$date).toLocaleString();
    this.tc_string = tdata.tokenized_content.join(',');
}//end Tweet constructor

$(document).ready(function () {    
    let today = new Date();
    let tomorrow = new Date();
    tomorrow.setDate(tomorrow.getDate() + 1);
    $('#fechaDesde').val(today.toISOString().substring(0, 10));
    $('#fechaHasta').val(tomorrow.toISOString().substring(0, 10));

    $(document).on(constants.newTweetsEvt, function () { drawTweets(); gridSetup(); })
    $(document).on(constants.newRefCounts, function () { drawRefCounts(); })

    $(':checkbox').change(function(evt) {
        let elem = $(this);
        updateMarkers(elem.attr('name'), elem.is(':checked'));
    });

    $('#realTime').change(function(evt) {
        let checked = $(this).prop('checked')
        $('#searchBox').prop('disabled', !checked);
        $('input[type=date]').prop('disabled', checked);
    });
    
    $('#realTime').change();
});

function buscar() {
    let fechaDesde = $('#fechaDesde').val() + '-UTC';
    let fechaHasta = $('#fechaHasta').val() + '-UTC';

    var url = 'http://127.0.0.1:8000/tweets/' + fechaDesde + '/' + fechaHasta;

    $.getJSON(url, function (tweets) {        
        
        resetMapMarkers();
        globalData.tweets = [];
        //globalData.tweets = tweets;  

        $.each(tweets, function (i, tdata) {
            globalData.tweets.push(new Tweet(tdata));
        });

        //si real team, hago push, sino, reemplazo la coleccion.
        //En real time no se resetean las cuentas, sino que se actualizan
        /*
        $.each(tweets, function (i, tweet) {
            globalData.tweets.push(tweet);            
        });
        */

        $(document).trigger(constants.newTweetsEvt);
        $(document).trigger(constants.newRefCounts);
        $(':checkbox').change();
    });
}

function gridSetup() {
    $("#tweetsGrid").jsGrid({
        width: "100%",
        height: "400px",

        filtering: true,                
        sorting: true,
        paging: true,
        pageButtonCount: 11,
        pageSize: 50,
 
        data: globalData.tweets,
 
        fields: [
            { title: "Fecha", name: "date_string", type: "text", width: "15%" },
            { title: "En mapa", name: "with_marker", type: "checkbox", width: "5%" },
            { title: "Sentimiento", name: "polarity_str", type: "text", width: "10%" },
            { title: "Tweet", name: "content", type: "text", width: "35%" },
            { title: "Tokens", name: "tc_string", type: "text", width: "35%" }            
        ]
    });    
}

//Map related funcions

function mapsSetup() {
    var mapProp = {
        center: new google.maps.LatLng(-40, -67),
        zoom: 4,
        disableDefaultUI: true
    };

    globalData.map = new google.maps.Map(document.getElementById("mapArgentinaSVM"), mapProp);
}

//activa o desactiva los markers según el estado del respectivo checkbox.
//markerType: tipo del marker a actualizar, es decir, tipo de polaridad.
function updateMarkers(markerType, checked) {
    var markers = globalData.mapMarkers[markerType];

    if (checked) {
        for (var i in markers) {        
            markers[i].setMap(globalData.map);            
        }        
    } else {
        for (var i in markers) {        
            markers[i].setMap(null);
        }
    }
}//end updateMarkers

//elimina los markers sobre el mapa
function resetMapMarkers() {

    for (var prop in globalData.mapMarkers) {

        let markers = globalData.mapMarkers[prop];

        for (var i in markers) {
            markers[i].setMap(null);
        }
        
        markers.length = 0;
    }

}//end resetMapMarkers

//Dibuja los puntos en el mapa, actualiza la cuenta de referencias y realiza
//el trigger del evento que indica que hay nuevos valores de cuenta de referencias.
function drawTweets() {

    $.each(globalData.tweets, function (i, tweet) {

        if (tweet.geo != null && !tweet.with_marker) {

            var circle = new google.maps.Circle({
                strokeColor: fillColor(tweet.polarity_level),
                strokeOpacity: 1,
                strokeWeight: 2,
                fillColor: fillColor(tweet.polarity_level),
                fillOpacity: 1,
                map: null, //globalData.map,
                center:  { lat: tweet.geo.latitud, lng: tweet.geo.longitud },
                radius: 100
            });

            globalData.mapMarkers[tweet.polarity_str].push(circle);
            tweet.with_marker = true;
        }//end if

    });
}//end drawTweets

function drawRefCounts() {
    let ninguno = globalData.mapMarkers.ninguno.length;
    let positivo = globalData.mapMarkers.positivo.length;
    let negativo = globalData.mapMarkers.negativo.length;
    let neutral = globalData.mapMarkers.neutral.length;

    $('#polCounterNinguno').text(ninguno);
    $('#polCounterPositivo').text(positivo);
    $('#polCounterNegativo').text(negativo);
    $('#polCounterNeutral').text(neutral);
    
}//end drawRefCounts

//Establece el color para el círculo en el mapa que denota un tweet.
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

//End Map related funcions