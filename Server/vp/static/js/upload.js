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
var glb;
function handleServerResponse(response) {
    glb = response;
    alert(JSON.stringify(response));
    var b = $("#list").get(0);

    for(var i = 0; i < response.results.length; i++){
        var success = response.results[0].success;

        var msg = success ? "Erfolgeich!" : "Fehlgeschlagen: " + response.results[0].errorCode;
        var color = success ? "green" : "red";
        var image = success ? (response.results[0].action=="change" ? "upload_change.png" : "upload_new.png") : "upload_error.png";
        
        var el = "<div class=\"list\" style=\"color:" + color + ";\"><img href=\""+ statics + image +"\"></img>" + msg + "</div>";
        b.innerHTML+=el;
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
        processData: false,
        contentType: false,
        success: handleServerResponse
    });
}