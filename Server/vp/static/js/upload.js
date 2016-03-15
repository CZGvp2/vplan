/*
*   UPLOAD.JS
*
* This script will
* (1) Handle dropEvents
* (2) Use jQuery to post the dropped files and receive data from the server
*
*/

// Debug? Die Variable sollte evtl vom Server für localhost gesetzt werden
var debug = true;
var debugTag = "[DEBUG] ";

setColor = function(){
    $("body").css("background-color", "#3a7ab6");
}
resetColor = function(){
    $("body").css("background-color", "#0e0e0e");
}

// DragOver
$(document).on(
    'dragover',
    function(e) {
        e.preventDefault();
        e.stopPropagation();
    }
);

//DragEnter
$(document).on(
    'dragenter',
    function(e) {
        setColor();
        e.preventDefault();
        e.stopPropagation();
    }
);

//DragLeave
$(document).on(
    'dragleave',
    function(e) {
        resetColor();
        e.preventDefault();
        e.stopPropagation();
    }
);

/* Eigentliches Dropevent fangen */
$(document).on(
    'drop',
    function(e) {
        resetColor();
        if(debug) console.log(debugTag + 'dropEvent caught, pushing to server...');
        if(e.originalEvent.dataTransfer){
            if (e.originalEvent.dataTransfer.files.length) {
                e.preventDefault();
                e.stopPropagation();
                resetColor();
                upload(e.originalEvent.dataTransfer.files);
            }
        }
    }
);

var errorDict = {
  "ERR_PARSING_XML" : "Keine XML-Datei",
  "ERR_READING_XML" : "XML-Strukturfehler",
  "ERR_PARSING_DATE" : "Datumsformat fehlerhaft",
  "ERR_DECODING" : "Keine Textdatei (kein UTF-8 Format)"
}
/* Serverantwort abfangen und verarbeiten */
var global_debug_responseBuffer;
function handleServerResponse(response) {
    if(debug) { global_debug_responseBuffer = JSON.stringify(response);
                console.log(debugTag + 'Got AJAX response: ' + global_debug_responseBuffer); }

    var b = $("#uploadList").get(0);
    $("#uploadList").css("display", "flex");

    $("#content").html("Drag & Drop <br /> zum Hochladen");

    for(var i = 0; i < response.results.length; i++){
        // hardcoded div-bastelschleife der Hölle

        var success = response.results[i].success;

        var filename = response.results[i].file;

        var errorMsg = typeof errorDict[response.results[i].errorCode] == 'undefined'?response.results[i].errorCode:errorDict[response.results[i].errorCode];
        var msg = success ? "Erfolgeich!" : "Fehlgeschlagen: " + errorMsg;
        var color = success ? "inherit" : "#AA0000"; // Hier möchte nen schöner Fehlerfarbenhexwert hin!
        var image = success ? (response.results[i].replaced ? "upload_change.png" : "upload_new.png") : "upload_error.png";

        var el = "<div class=\"upload\"><img class=\"ulImg\" src=\"."+ statics + image +"\"></img>" +
            "<span> " + filename + "</span><span class=\"space\"></span>" +
            "<span style=\"background-color:" + color + ";\">" + msg + "</span></div>";

        if(b.children.length > 6) b.children[0].remove();
        b.innerHTML+=el;  // vllt jQuery ind '"' statt "\"" ? // erstmal nicht, später vllt... JavaScript Klassenorientierung ist Overkill, oder? Sonst würd ich das noch nen bisschen strukturieren
    }
}

// AJAX Upload
function upload(files) {

    $("#content").html("Hochladen...");

    var formData = new FormData($('form')[0]); // besser?
    for (var i = 0; i < files.length; i++)
        formData.append('file', files[i]);

    if(debug) console.log(debugTag + 'Posting data to ' + path + '.');

    return $.ajax({
        url: path,
        type: 'POST',
        data: formData,
        dataType: 'json',
        processData: false,
        contentType: false,
        success: handleServerResponse,
        failure: function () {
            var json = JSON.parse("results:[{success: false, filename: \"---\", errorCode: \"CONNECTION_ERROR\"}]");
            handleServerResponse(json);
        }
    });
}

// Löscht Datei
function delete_file(filename) {
    var formData = new FormData($('form')[0]); // besser?
    formData.append('delfile', filename);

    return $.ajax({
        url: path + '?delete',
        type: 'POST',
        data: formData,
        dataType: 'json',
        processData: false,
        contentType: false,
        success: function dosomething() {},
        failure: function dosomethingelse() {}
    });
}
