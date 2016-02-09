/* Wenn der Browser JS nicht versteht, wird der Code nicht angezeigt sondern als Kommentar betrachtet. JS ignoriert den Kommentaranfang einfach. */

/* Versuch, Drag and Drop mit jQuery/CSS ohne weitere Bibliotheken hinzubekommen */


/* Browser machen sehr merkwürdige Sachen, 
wenn man keine Default-Events verhindert

evtl. highlighting der Box
*/
$(document).on(
    'dragover',
    function(e) {
        e.stopPropagation();
        e.preventDefault();
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
        if(e.originalEvent.dataTransfer){
            /* .files sind alle gedroppten Dateien */

            /* Überprüfen ob >= eine Datei im Array ist*/
            if (e.originalEvent.dataTransfer.files.length) {
                /* Defaultzeug*/
                e.preventDefault();
                e.stopPropagation();
                /* Das hier sollte alles hochladen, ich hab kine Ahnung ob das funktioniert */
                upload(e.originalEvent.dataTransfer.files);
            }   
        }
    }
);
function upload(files) {
    var formData = new FormData($('form')[0]);
    
    /* Tadaa, die Lösung des Problems: ganz viele einzelne 'file'-POST-vars (unglaublich, ich weiß) */
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
            // und es muss $('form')[0] sein sonst liesst der ne liste und es wirft nen TypeError
            else alert("Computer says no.");
        }

    });
}