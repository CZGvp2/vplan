/* 
*   UPLOAD.JS
*
* This script will
* (1) Handle dropEvents
* (2) Use jQuery to post the dropped files and receive data from the server
*
*/

// Debug?
var debug = true;
var debugTag = "[DEBUG] ";

setColor = function(){
    $("body").css("background-color", "#4db038");
}
resetColor = function(){
    $("body").css("background-color", "#282828");
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

/* Serverantwort abfangen und verarbeiten */
var global_debug_responseBuffer;
function handleServerResponse(response) {
    if(debug) { global_debug_responseBuffer = JSON.stringify(response); 
                console.log(debugTag + 'Got AJAX response: ' + global_debug_responseBuffer); }
    
    var b = $("#uploadList").get(0);
    $("#uploadList").css("display", "flex");

    for(var i = 0; i < response.results.length; i++){
        // hardcoded div-bastelschleife der Hölle

        var success = response.results[i].success;

        var filename = response.results[i].file;
        var msg = success ? "Erfolgeich!" : "Fehlgeschlagen: " + response.results[i].errorCode;
        var color = success ? "inherit" : "red"; // Hier möchte nen schöner Fehlerfarbenhexwert hin!
        var image = success ? (response.results[i].action=="replace" ? "upload_change.png" : "upload_new.png") : "upload_error.png";
        
        var el = "<div class=\"upload\"><img class=\"ulImg\" src=\"."+ statics + image +"\"></img>" +
            "<span> " + filename + "</span><span class=\"space\"></span>" + 
            "<span style=\"background-color:" + color + ";\">" + msg + "</span></div>";

        if(b.children.length > 6) b.children[0].remove();
        b.innerHTML+=el;  // vllt jQuery ind '"' statt "\"" ? // erstmal nicht, später vllt... JavaScript Klassenorientierung ist Overkill, oder? Sonst würd ich das noch nen bisschen strukturieren
    }
}

// AJAX Upload
function upload(files) {
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
        failure: function () {alert('AJAX: Connection Error')}
    });
}