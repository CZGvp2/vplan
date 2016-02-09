$(document).on(
    'dragover',
    function(e) {
        e.preventDefault();
        e.stopPropagation();
        console.log('dragOver');
    }
)
$(document).on(
    'dragenter',
    function(e) {
        e.preventDefault();
        e.stopPropagation();
        console.log('dragEnter');
    }
)

/* Eigentliches Dropevent fangen */
$(document).on(
    'drop',
    function(e){
        console.log('drop');
            if (e.originalEvent.dataTransfer.files.length) {
                e.preventDefault();
                e.stopPropagation();
                upload(e.originalEvent.dataTransfer.files);
            }   
        }
    }
);

function handleServerResponse(response) {
    if (response.success) alert("Ja dat funktioniert");
    else alert("Computer says no.");
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