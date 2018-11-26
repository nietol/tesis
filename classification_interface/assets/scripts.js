var glb_polling = true;

var constants =
    {
        newTweetsEvt: 'new-tweets-evt',
        newRefCounts: 'new-ref-counts-evt',
        realTimeStartedEvt: 'rt-started-evt',
        realTimeStopedEvt: 'rt-stoped-evt',
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
        },
        notInMap: {
            ninguno: [],
            positivo: [],
            negativo: [],
            neutral: []            
        }
    };

var endpoints = {
    tweets: 'http://127.0.0.1:8000/tweets',
    classifications: 'http://127.0.0.1:8000/classifications',
    realtimetweets: 'http://127.0.0.1:8000/realtimetweets'
}

function Tweet(tdata) {
    for (var key in tdata) {
        this[key] = tdata[key];
    }
    
    this.date_string = new Date(tdata.date.$date).toLocaleString();
    this.tc_string = tdata.tokenized_content.join(',');
    this.en_mapa = tdata.geo != null ? 'Si' : 'No';
}//end Tweet constructor

$(document).ready(function () {    
    let today = new Date();    
    today.setTime(today.getTime() - (today.getTimezoneOffset() * 60 * 1000));
    
    let tomorrow = new Date();    
    tomorrow.setDate(tomorrow.getDate() + 1);
    tomorrow.setTime(tomorrow.getTime() - (tomorrow.getTimezoneOffset() * 60 * 1000));

    $('#fechaDesde').val(today.toISOString().slice(0, 16));
    $('#fechaHasta').val(tomorrow.toISOString().slice(0, 16));

    $(document).on(constants.newTweetsEvt, function () { onNewTweets(); })
    $(document).on(constants.newRefCounts, function () { onNewRefCounts(); })
    $(document).on(constants.realTimeStartedEvt, function (evt, started_at) { onRealTimeStarted(started_at); })
    $(document).on(constants.realTimeStopedEvt, function () { onRealTimeStoped(); })

    $('#ulReferencias :checkbox').change(function(evt) {
        let elem = $(this);
        updateMarkers(elem.attr('name'), elem.is(':checked'));
    });

    $('#realTime').change(function(evt) {
        let checked = $(this).prop('checked')
        $('#searchBox').prop('disabled', !checked);
        $('input[type=datetime-local]').prop('disabled', checked);
        $('#btnFind').val(checked ? 'Iniciar RT' : 'Buscar Histórico');
    });
    
    $('#realTime').change();

    $('#btnFind').click(function() { 
        findTweets();
    });
});

//Busqueda de histórico y lectura en tiemp real

function startPolling(started_at) {
    let url = endpoints.realtimetweets + '/' + started_at.toString();
    searchForTweets(url);

    if (glb_polling) {
        setTimeout(function() {
            startPolling(started_at);
        }, 10000);
    }
}

function stopPolling() {
    glb_polling = false;
}

function onRealTimeStarted(started_at) {
    $('#realTime').prop('disabled', true);
    $btnFind = $('#btnFind');
    
    $btnFind.val('Stop RT');
    $btnFind.off();
    $btnFind.click(function() { 
        stopRealTime();
    });

    $('#searchBox').prop('disabled', true);

    glb_polling = true;
    startPolling(started_at);
}

function onRealTimeStoped() {
    $('#realTime').prop('disabled', false);
    $btnFind = $('#btnFind');
    
    $btnFind.val('Start RT');
    $btnFind.off();
    $btnFind.click(function() { 
        findTweets();
    });

    $('#searchBox').prop('disabled', false);    
    stopPolling();
}

//Inicia la bùsqueda de tweets, ya sea histórico o en tiempo real.
function findTweets() {
    var isRT = $('#realTime').prop('checked');

    if (isRT) {
        startRealTime();        
    } else {
        buscarHistorico();
    }
}

//Inicia la lectura de tweets en tiempo real.
function startRealTime() {

    let started_at = 0;
    let url = endpoints.classifications;

    $.post(url, function(data) {
        started_at = data.started_at;
        $(document).trigger(constants.realTimeStartedEvt, started_at);
    });
}

//Detiene la lectura de tweets en tiempo real.
function stopRealTime() {

    $.ajax({
        url: endpoints.classifications,
        type: 'PUT'       
    });    

    $(document).trigger(constants.realTimeStopedEvt);
}

//Busca tweets almacenados en base de datos.
function buscarHistorico() {
    let fechaDesde = $('#fechaDesde').val() + "-UTC-0300";
    let fechaHasta = $('#fechaHasta').val() + "-UTC-0300";

    var url = endpoints.tweets + '/' + fechaDesde + '/' + fechaHasta;
    searchForTweets(url);
}

function searchForTweets(url) {
    $.getJSON(url, function (tweets) {    
        
        resetMapMarkers();
        globalData.tweets = [];

        $.each(tweets, function (i, tdata) {
            globalData.tweets.push(new Tweet(tdata));
        });

        $(document).trigger(constants.newTweetsEvt);
        $(document).trigger(constants.newRefCounts);        
    });
}

//FIN - Busqueda de histórico y lectura en tiemp real

function gridSetup() {
    $("#tweetsGrid").jsGrid({
        width: "100%",
        height: "100vh",
        
        selecting: false,
        sorting: true,
        paging: true,
        pageButtonCount: 11,
        pageSize: 50,        
 
        data: globalData.tweets,

        rowClick: function(args) {
            let $row = this.rowByItem(args.item);                         
            let tweet = args.item;

            if (tweet.map_marker) {
                if ( !$row.hasClass('highlight') ) {
                    let radio = tweet.map_marker.radius * 1000;
                    tweet.map_marker.setRadius(radio);
                    $row.toggleClass('highlight');
                } else {
                    let radio = tweet.map_marker.radius / 1000;
                    tweet.map_marker.setRadius(radio);
                    $row.toggleClass('highlight');
                }
            }
        },

        onRefreshing: function(grid) {
            let selectedRows = $('#tweetsGrid').find('table tr.highlight');
            if (selectedRows.length) {
                selectedRows.click();
            }
        },
 
        fields: [
            { title: "Fecha", name: "date_string", type: "text", width: "15%", align: "center" },
            { title: "En Mapa", name: "en_mapa", type: "text", width: "5%", align: "center" },
            { title: "Sentimiento", name: "polarity_str", type: "text", width: "10%", align: "center" },
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

    for (var prop in globalData.notInMap) {
        let tweets = globalData.mapMarkers[prop];
        tweets.length = 0;
    }

}//end resetMapMarkers

//Dibuja los puntos en el mapa, actualiza la cuenta de referencias y realiza
//el trigger del evento que indica que hay nuevos valores de cuenta de referencias.
function drawTweets() {

    $.each(globalData.tweets, function (i, tweet) {

        if (tweet.geo != null && !tweet.map_marker) {

            var circle = new google.maps.Circle({
                strokeColor: fillColor(tweet.polarity_level),
                strokeOpacity: 0.8,
                strokeWeight: 2,
                fillColor: fillColor(tweet.polarity_level),
                fillOpacity: 0.35,
                map: null, //globalData.map,
                center:  { lat: tweet.geo.latitud, lng: tweet.geo.longitud },
                radius: 100
            });

            globalData.mapMarkers[tweet.polarity_str].push(circle);
            tweet.map_marker = circle;
        }//end if

        if (tweet.geo == null) {
            globalData.notInMap[tweet.polarity_str].push(tweet);
        }
    });
}//end drawTweets

function onNewTweets() {
    drawTweets();
    gridSetup();
}

function onNewRefCounts() {
    
    let separador = ' de ';
    let ninguno = globalData.mapMarkers.ninguno.length.toString() + separador +  globalData.notInMap.ninguno.length.toString();
    let positivo = globalData.mapMarkers.positivo.length.toString() + separador +  globalData.notInMap.positivo.length.toString();
    let negativo = globalData.mapMarkers.negativo.length.toString() + separador +  globalData.notInMap.negativo.length.toString();
    let neutral = globalData.mapMarkers.neutral.length.toString() + separador +  globalData.notInMap.neutral.length.toString();

    $('#polCounterNinguno').text(ninguno);
    $('#polCounterPositivo').text(positivo);
    $('#polCounterNegativo').text(negativo);
    $('#polCounterNeutral').text(neutral);
    
    $('#ulReferencias :checkbox').change();
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