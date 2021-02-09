tinymce.init({
    selector: 'textarea',
    branding: false,
    // directionality : 'rtl',
    // width : "200%",
    language: 'fa',
    menubar : 'format edit view',
    entity_encoding : "raw",
    elementpath: false,
    plugins: 'formattingcode  link image alignment directionality preview code table',
    toolbar: 'undo redo | bold italic | alignleft aligncenter alignright alignjustify | indent outdent | ltr rtl | code link image table | preview',
    image_title: true,
    automatic_uploads: true,
    images_upload_url: 'http://localhost',
    file_picker_types: 'image',

    file_picker_callback: function (cb, value, meta) {
        var input = document.createElement('input');
        input.setAttribute('type', 'file');
        input.setAttribute('accept', 'image/*');
        input.onchange = function () {
            var file = this.files[0];
            var reader = new FileReader();
            reader.onload = function () {
                var id = 'blobid' + (new Date()).getTime();
                var blobCache =  tinymce.activeEditor.editorUpload.blobCache;
                var base64 = reader.result.split(',')[1];
                var blobInfo = blobCache.create(id, file, base64);
                blobCache.add(blobInfo);
                cb(blobInfo.blobUri(), { title: file.name });
            };
        reader.readAsDataURL(file);
        };
        input.click();
    },
    content_style: 'body { font-family:Helvetica,Arial,sans-serif; font-size:15px; line-height: 0.4}'
});
