// tinymce.init({
//     selector: 'textarea',
//     branding: false,
//     // directionality : 'rtl',
//     // width : "200%",
//     language: 'fa',
//     menubar : 'format edit view',
//     entity_encoding : "raw",
//     elementpath: false,
//     plugins: 'formattingcode  link image alignment directionality preview code table',
//     toolbar: 'undo redo | bold italic | alignleft aligncenter alignright alignjustify | indent outdent | ltr rtl | code link image table | preview',
//     image_title: true,
//     automatic_uploads: true,
//     images_upload_url: 'http://localhost',
//     file_picker_types: 'image',

//     file_picker_callback: function (cb, value, meta) {
//         var input = document.createElement('input');
//         input.setAttribute('type', 'file');
//         input.setAttribute('accept', 'image/*');
//         input.onchange = function () {
//             var file = this.files[0];
//             var reader = new FileReader();
//             reader.onload = function () {
//                 var id = 'blobid' + (new Date()).getTime();
//                 var blobCache =  tinymce.activeEditor.editorUpload.blobCache;
//                 var base64 = reader.result.split(',')[1];
//                 var blobInfo = blobCache.create(id, file, base64);
//                 blobCache.add(blobInfo);
//                 cb(blobInfo.blobUri(), { title: file.name });
//             };
//         reader.readAsDataURL(file);
//         };
//         input.click();
//     },
//     content_style: 'body { font-family:Helvetica,Arial,sans-serif; font-size:15px; line-height: 0.4}'
// });

// function invalid_input(){
//     $('.has-error').each(function(){
//         $(this).find('input').addClass('border border-danger')
//     });
// }


// invalid_input()
// $(document).ready(function(){
//     setTimeout(function() {
//         $('.has-error').find('.tox').addClass('border border-danger');}, 10000);
//     }
// );


function like(){
    console.log(111111)
    $("#like").click(function () {
        $postId = window.location.href.split('/').filter(function(i){return i}).pop()
        $userName = $('#username').html();
        console.log($postId, $userName)
        $.post(
            'http://127.0.0.1:8000/blog/api/like/',
            {
            'post': $postId,
            'user': $userName,
            'csrftoken' : csrftoken
            },
            function (response, status) {
                console.log(response, status)
            //   if (status == "success" && response["response"] == "SUCCESS") {
            //     $($row[2]).text($price);
            //     $($row[3]).text($count);
            //     $("#editModal").modal("hide");
            //   } else if (status == "success" && response["response"] != "SUCCESS") {
            //     if (response["response"] != "FAILED") {
            //       $(response["response"]).addClass("form-control is-invalid");
            //       $(response["response"]).next().html(response["msg"]);
            //     } else {
            //       $("#editFinalError").html(response["msg"]);
            //       $("#editFinalError").addClass("form-control is-invalid");
            //     }
            //   } else {
            //     $("#editFinalError").html(
            //       "ارتباط با سرور قطع شده است. لطفا مجددا تلاش کنید"
            //     );
            //     $("#editFinalError").addClass("form-control is-invalid");
            //   }
            }
        );
    })
}

like()
