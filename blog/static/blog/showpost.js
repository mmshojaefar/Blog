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


function likePost() {
    $("#like").click(function () {
        const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        $postId = window.location.href.split('/').filter(function (i) { return i }).pop();
        // $userName = $('#username').html();
        console.log($postId)
        $.post({
            url: 'http://127.0.0.1:8000/blog/api/likepost/',
            headers: { 'X-CSRFToken': csrftoken }
        },
            {
                'post': $postId,
                // 'user': $userName,
            },
            function (response, status) {
                console.log(response, status)
                likesNumber = parseInt($('#like').val())
                dislikesNumber = parseInt($('#dislike').val())
                if (status == "success" && response["ok"] == "like") {
                    $('#like').val(likesNumber+1)
                    // $('#like').css('fontWeight', 'bold')
                } else if (status == "success" && response["ok"] == "removedislike") {
                    $('#dislike').val(dislikesNumber-1)
                } else if (status != "success"){
                    console.log(333333)
                    console.log('eerrrror')
                    // $("#editFinalError").html(
                    //     "ارتباط با سرور قطع شده است. لطفا مجددا تلاش کنید"
                    // );
                    // $("#editFinalError").addClass("form-control is-invalid");
                }
            }
        );
    })
}

likePost()

function dislikePost() {
    $("#dislike").click(function () {
        const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        $postId = window.location.href.split('/').filter(function (i) { return i }).pop();
        console.log($postId)
        $.post({
            url: 'http://127.0.0.1:8000/blog/api/dislikepost/',
            headers: { 'X-CSRFToken': csrftoken }
        },
            {
                'post': $postId,
            },
            function (response, status) {
                console.log(response, status)
                likesNumber = parseInt($('#like').val())
                dislikesNumber = parseInt($('#dislike').val())
                if (status == "success" && response["ok"] == "dislike") {
                    $('#dislike').val(dislikesNumber+1)
                } else if (status == "success" && response["ok"] == "removelike") {
                    $('#like').val(likesNumber-1)
                } else if (status != "success"){
                    console.log(333333)
                    console.log('eerrrror')
                }
            }
        );
    })
}

dislikePost()

function acceptPost() {
    $("#accept_post").click(function () {
        const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        $postId = window.location.href.split('/').filter(function (i) { return i }).pop();
        console.log($postId)
        $.post({
            url: 'http://127.0.0.1:8000/blog/api/acceptpost/',
            headers: { 'X-CSRFToken': csrftoken }
        },
            {
                'post': $postId,
            },
            function (response, status) {
                if (status == "success" && response["ok"] == "ok") {
                    $('#accept_post').val($('#accept_post').val() == 'تایید' ? 'عدم تایید' : 'تایید')
                } else if (status != "success"){
                    console.log(333333)
                    console.log('eerrrror')
                }
            }
        );
    })
}

acceptPost()

function acceptComment() {
    $(".accept_comment").click(function () {
        const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        $comment = $(this)
        $commentId = $comment.closest('tr').attr('id').substring(8)
        console.log($commentId)
        $.post({
            url: 'http://127.0.0.1:8000/blog/api/acceptcomment/',
            headers: { 'X-CSRFToken': csrftoken }
        },
            {
                'comment': $commentId,
            },
            function (response, status) {
                if (status == "success" && response["ok"] == "ok") {
                    console.log($comment)
                    $comment.val($comment.val() == 'تایید' ? 'عدم تایید' : 'تایید')
                } else if (status != "success"){
                    console.log(333333)
                    console.log('eerrrror')
                }
            }
        );
    })
}

acceptComment()

function likeComment() {
    $(".like_comment").click(function () {
        const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        $comment = $(this).closest('tr')
        $like = $comment.find('.like_comment')
        $dislike = $comment.find('.dislike_comment')
        likesNumber = parseInt($like.val())
        dislikesNumber = parseInt($dislike.val())
        $commentId = $comment.attr('id').substring(8)
        $.post({
            url: 'http://127.0.0.1:8000/blog/api/likecomment/',
            headers: { 'X-CSRFToken': csrftoken }
        },
            {
                'comment': $commentId,
            },
            function (response, status) {
                if (status == "success" && response["ok"] == "like") {
                    $like.val(likesNumber+1)
                } else if (status == "success" && response["ok"] == "removedislike") {
                    $dislike.val(dislikesNumber-1)
                } else if (status != "success"){
                    console.log(333333)
                    console.log('eerrrror')
                }
            }
        );
    })
}

likeComment()

function dislikeComment() {
    $(".dislike_comment").click(function () {
        const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        $comment = $(this).closest('tr')
        $like = $comment.find('.like_comment')
        $dislike = $comment.find('.dislike_comment')
        likesNumber = parseInt($like.val())
        dislikesNumber = parseInt($dislike.val())
        $commentId = $comment.attr('id').substring(8)
        $.post({
            url: 'http://127.0.0.1:8000/blog/api/dislikecomment/',
            headers: { 'X-CSRFToken': csrftoken }
        },
            {
                'comment': $commentId,
            },
            function (response, status) {
                if (status == "success" && response["ok"] == "dislike") {
                    $dislike.val(dislikesNumber+1)
                } else if (status == "success" && response["ok"] == "removelike") {
                    $like.val(likesNumber-1)
                } else if (status != "success"){
                    console.log(333333)
                    console.log('eerrrror')
                }
            }
        );
    })
}

dislikeComment()
