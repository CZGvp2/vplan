/* Browser machen sehr merkwürdige Sachen, 
wenn man keine Default-Events verhindert*/

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
        console.log('drop');
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

var global_buffer_debug;
function handleServerResponse(response) {
    global_buffer_debug = JSON.stringify(response);
    var b = $("#uploadList").get(0);
    $("#uploadList").css("display", "flex");

    for(var i = 0; i < response.results.length; i++){
        // hardcoded div-bastelschleife der Hölle

        var success = response.results[i].success;

        var filename = response.results[i].file;
        var msg = success ? "Erfolgeich!" : "Fehlgeschlagen: " + response.results[i].errorCode;
        var color = success ? "inherit" : "red";
        var image = success ? (response.results[i].action=="change" ? "upload_change.png" : "upload_new.png") : "upload_error.png";
        
        var el = "<div class=\"upload\"><img class=\"ulImg\" src=\"."+ statics + image +"\"></img>" +
            "<span> " + filename + "</span><span class=\"space\"></span>" + 
            "<span style=\"background-color:" + color + ";\">" + msg + "</span></div>";

        if(b.children.length > 6) b.children[0].remove();
        b.innerHTML+=el;  // vllt jQuery ind '"' statt "\"" ? // erstmal nicht, später vllt
        console.log("added " + el);
    }
}

function upload(files) {
    var formData = new FormData($('form')[0]); // besser?
    for (var i = 0; i < files.length; i++)
        formData.append('file', files[i]);

    return $.ajax({
        url: path,
        type: 'POST',
        data: formData,
        dataType: 'json',
        processData: false,
        contentType: false,
        success: handleServerResponse,
        failure: function () {alert('ups')}
    });
}