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
                console.log("dragOver");
            }
        )
        $(document).on(
            'dragenter',
            function(e) {
                e.preventDefault();
                e.stopPropagation();
                console.log("dragEnter");
            }
        )

        /* Eigentliches Dropevent fangen */
        $(document).on(
            'drop',
            function(e){
                console.log("drop");
                if(e.originalEvent.dataTransfer){
                    /* .files sind alle gedroppten Dateien */

                    /* Überprüfen ob >= eine Datei im Array ist*/
                    if(e.originalEvent.dataTransfer.files.length) {
                        /* Defaultzeug*/
                        e.preventDefault();
                        e.stopPropagation();
                        /* Das hier sollte alles hochladen, ich hab kine Ahnung ob das funktioniert */
                        upload(e.originalEvent.dataTransfer.files);
                    }   
                }
            }
        );

        /*upload = function(files){
            alert(files);
        }*/
        /* teilweise geklaut von http://stackoverflow.com/questions/15552112/add-input-of-type-file-to-a-form-dynamically */
        function upload(files) {

            console.log("Upload");
            /* Suche ersten formTag auf der Seite*/
            var formData = new FormData($("form")[0]);

            /* Dateien an POST anhängen 
            for( var i = 0; i < files.length; ++i ) {
                var file = files[i];
                i==0 ? formData.append("file", file) : formData.append("file" + (i), file);
            }
            */formData.append("file", files);

            /* Wie Klick auf den Submit-Button */
            return $.ajax({
                url: "http://localhost/edit",
                type: "POST",
                data: formData,
                processData: false,
                contentType: false,
                success: function() {
                    alert('Upload erfolgreich!');
                }

            });
        }