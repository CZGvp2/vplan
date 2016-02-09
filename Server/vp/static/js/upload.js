/* Browser machen sehr merkwürdige Sachen, 
wenn man keine Default-Events verhindert*/

// DragOver
$(document).on(
    'dragover',
    function(e) {
        e.stopPropagation();
        e.preventDefault();
    }
)

//DragEnter
$(document).on(
    'dragenter',
    function(e) {
        e.preventDefault();
        e.stopPropagation();

        document.body.style.backgroundColor = "#CFF";
    }
)

//DragLeave
$(document).on(
    'dragleave',
    function(e) {
        e.preventDefault();
        e.stopPropagation();
        
        document.body.style.backgroundColor = "#FFF";
    }
)

/* Eigentliches Dropevent fangen */
$(document).on(
    'drop',
    function(e){
        console.log('Drop');
        if(e.originalEvent.dataTransfer){
            /* Überprüfen ob >= eine Datei im Array ist*/
            if (e.originalEvent.dataTransfer.files.length) {
                e.preventDefault();
                e.stopPropagation();
                upload(e.originalEvent.dataTransfer.files);
            }   
        }
    }
);
function upload(files) {
    var formData = new FormData($('form')[0]);
    
    /* Tadaa, die Lösung des Problems: ganz viele einzelne 'file'-POST-vars (unglaublich, ich weiß) // :c */
    for (var i = 0; i < files.length; i++)
        formData.append('file', files[i]);

    
    return $.ajax({
        url: path,
        type: 'POST',
        data: formData,
        processData: false,
        contentType: false,
        success: function(response) {
            // README
            /*
            nach 5h arbeit hab ich herausgefunden dasss der Server (richtig sick) JSON an die success-function übergeben kann.
            jetzt kann ajax also den Server-Response handeln. // nice
            */

            if (response.success) alert("Ja dat funktioniert");
            //  ^^^^^^^^^^^^^^^^
            //     die Flag          (kann auch genauere Info sein) // also kann man einfach ne jQuery("p") auf nen success.msg string setzen? Wär gut
            //                                                      //und es muss $('form')[0] sein sonst ließt der ne liste und es wirft nen TypeError
            else alert("Computer says no.");
        }

    });
}