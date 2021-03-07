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
    images_upload_url: 'http://127.0.0.1:8000/',
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

var i = 0;
function addTag(){
    $(".addTag").click(function() {
        console.log(111111111);
        selected = `<input name='tags' style='background-color:#D3D3D3; margin:1px 3px; display:inline; border:none;' value='${$('#tag').val()}' disabled>`;
        i++;
        $('#selectedTags').append(selected);
        // $(selected).insertAfter('#selectedTags');
        $('#tag').val("");
        $('#allTags').empty();
    });
}

$("#tag").on('input' ,function() {
    console.log(22222222222)
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    $('#allTags').empty()
    if($("#tag").val().length > 0){
        result = "<div class='addTag' style='background-color:gray; margin-bottom:1px;'>افزودن تگ</div>"
        $('#allTags').prepend(result)
    }
    addTag()
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
                    // $('#allTags').empty()
                    // console.log(response["result"])
                    JSON.parse(response["result"]).forEach(
                    function myFunction(item) {
                        // console.log(item)
                        result = `<div id='result_${item['pk']}' class='tagResult' style='background-color:gray; margin-bottom:1px;'>${item['fields']['name']}</div>`
                        $('#allTags').append(result)
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
        selected = `<input name='tags' id='selected_${id}' style='background-color:#D3D3D3; margin:1px 3px; border:none;' value='${$(this).html()}' disabled>`;
        // $(selected).insertAfter('#selectedTags');
        $('#selectedTags').append(selected);
        $('#tag').val("");
        $('#allTags').empty();
    });
}

$('#newPostForm').submit(function(){
    $("#newPostForm :disabled").removeAttr('disabled');
});


console.log(11111112)

function start(){
    arr = window.location.href.split('/').filter(function (i) { return i })
    postId = arr[arr.length-2]
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    console.log(1111111)
    $.post({
        url: 'http://127.0.0.1:8000/blog/api/gettag/',
        headers: { 'X-CSRFToken': csrftoken }
    },
        {
            'id':postId
        },
        function (response, status) {
            if (status == "success") {
                // console.log(JSON.parse(response['tags']))
                // console.log(response['tags'])
                response['tags'].forEach(
                    function myFunction(item) {
                    console.log(item)
                    result = `<input id='result_${item[0]}' class='tagResult' style='color:black; background-color:gray; margin-bottom:1px;' value='${item[1]}' disabled>`
                    $('#selectedTags').append(result);
                });
                // divClicked()
            } else if (status != "success") {
                console.log(333333)
                console.log('eerrrror')
            }
        }
    );
}

start()
