tinymce.init({
    selector: 'textarea',
    branding: false,
    // directionality : 'rtl',
    // width : "200%",
    height: "600",
    language: 'fa',
    menubar: 'format edit view',
    entity_encoding: "raw",
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
                var blobCache = tinymce.activeEditor.editorUpload.blobCache;
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


function invalid_input() {
    $('.has-error').each(function () {
        $(this).find('input').addClass('border border-danger')
    });
}

invalid_input()
$(document).ready(function () {
    setTimeout(function () {
        $('.has-error').find('.tox').addClass('border border-danger');
    }, 10000);
}
);


function addTag() {
    $(".addTag").click(function () {
        selected = `<input class="pb-1 pt-2" name='tags' style='text-align: center; color: black; background-color:#a5a5a5; margin:2px 3px; display:inline; border:none;' value='${$('#tag').val()}' disabled>`;
        input = $(selected)[0];
        width = ((input.value.length + 2) * 8).toString() + 'px';
        $('#selectedTags').append('<div class="oneTag" style="display:inline-block; position:relative;">' + selected + '<div style="position:absolute; left:0; right:0; top:0; bottom:0;"></div></div>');
        $('#selectedTags div input').last().css("width", width);
        deleteTag();

        $('#tag').val("");
        $('#allTags').empty();
    });
}

$("#tag").on('input', function () {
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    $('#allTags').empty()
    if ($("#tag").val().length > 0) {
        result = "<div class='addTag pb-1 pt-1' style='color: black; background-color:#a5a5a5; margin-bottom:2px;'>افزودن تگ</div>";
        $('#allTags').prepend(result);
    }
    addTag();
    if ($("#tag").val().length > 2) {
        $.post({
            url: 'http://127.0.0.1:8000/blog/api/addtag/',
            headers: { 'X-CSRFToken': csrftoken }
        },
            {
                'tag': $("#tag").val(),
            },
            function (response, status) {
                if (status == "success") {
                    JSON.parse(response["result"]).forEach(
                        function myFunction(item) {
                            result = `<div id='result_${item['pk']}' class='tagResult pb-1 pt-1' style='color: black; background-color:#a5a5a5; margin-bottom:2px;'>${item['fields']['name']}</div>`;
                            $('#allTags').append(result);
                        });
                    divClicked()
                } else if (status != "success") {
                    console.log('eerrrror')
                }
            }
        );
    }
});

function divClicked() {
    $(".tagResult").click(function () {
        selected = `<input name='tags' class="pb-1 pt-2" style='text-align: center; color: black; background-color:#a5a5a5; margin:2px 3px; border:none;' value='${$(this).html()}' disabled>`;
        input = $(selected)[0];
        width = ((input.value.length + 2) * 8).toString() + 'px';
        $('#selectedTags').append('<div class="oneTag" style="display:inline-block; position:relative;">' + selected + '<div style="position:absolute; left:0; right:0; top:0; bottom:0;"></div></div>');
        $('#selectedTags input').last().css("width", width);
        deleteTag();

        $('#tag').val("");
        $('#allTags').empty();
    });
}


function deleteTag() {
    $('.oneTag').click(function () {
        console.log(this);
        $(this).remove();
    })
}

deleteTag();

$('#newPostForm').submit(function () {
    $("#newPostForm :disabled").removeAttr('disabled');
});

$('#id_show_post').parent().addClass("mt-3 mb-1");
$('#id_show_post').addClass('form-check-input');
$('#id_show_post').parent().wrap('<span class="checkbox form-check form-switch"></span>');