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

function invalid_input(){
    $('.has-error').each(function(){
        $(this).find('input').addClass('border border-danger')
    });
}


invalid_input()
$(document).ready(function(){
    setTimeout(function() {
        $('.has-error').find('.tox').addClass('border border-danger');}, 10000);
    }
);

$("#tag").on('input' ,function() {
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    $('#allTags').empty()
    if($("#tag").val().length > 2){
        $.post({
            url: 'http://127.0.0.1:8000/blog/api/addtag/',
            headers: { 'X-CSRFToken': csrftoken }
        },
            {
                'tag': $("#tag").val(),
            },
            function (response, status) {
                if (status == "success") {
                    $('#allTags').empty()
                    // console.log(response["result"])
                    JSON.parse(response["result"]).forEach(
                    function myFunction(item) {
                        // console.log(item)
                        result = "<div id='result_" + item['pk'] + "' class='tagResult' style='background-color: gray;margin-bottom:1px'>" + item['fields']['name'] + "</div>"
                        $('#allTags').prepend(result)
                    });
                    divClicked()
                } else if (status != "success") {
                    console.log(333333)
                    console.log('eerrrror')
                }
            }
        );
    }
});

function divClicked(){
    $(".tagResult").click(function() {
        id = $(this).attr('id').substring(7);
        // console.log(id);
        selected = "<div id='selected_" + id + "' style='background-color:#D3D3D3;margin:1px 3px; display:inline;'>" + $(this).html() + "</div>";
        $('#selectedTags').prepend(selected);
        $('#tag').val("");
        $('#allTags').empty();
    });
}

