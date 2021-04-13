function likePost() {
    $("#like").click(function () {
        const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        $postId = window.location.href.split('/').filter(function (i) { return i }).pop();
        $.post({
            url: 'http://127.0.0.1:8000/blog/api/likepost/',
            headers: { 'X-CSRFToken': csrftoken }
        },
            {
                'post': $postId,
            },
            function (response, status) {
                likesNumber = parseInt($('#like').next().text())
                dislikesNumber = parseInt($('#dislike').next().text())

                console.log(likesNumber)
                console.log(dislikesNumber)
                
                if (status == "success" && response["ok"] == "like") {
                    $like = $('#like').next().next();
                    $like.text(toFarsiNumber(likesNumber + 1));
                    $like.css('font-weight', '900');
                    $('#like').next().text(likesNumber + 1);

                } else if (status == "success" && response["ok"] == "removedislike") {
                    $dislike = $('#dislike').next().next();
                    $dislike.text(toFarsiNumber(dislikesNumber - 1));
                    $dislike.css('font-weight', 'normal');
                    $('#dislike').next().text(dislikesNumber - 1);

                } else if (status != "success") {
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


function dislikePost() {
    $("#dislike").click(function () {
        const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        $postId = window.location.href.split('/').filter(function (i) { return i }).pop();
        $.post({
            url: 'http://127.0.0.1:8000/blog/api/dislikepost/',
            headers: { 'X-CSRFToken': csrftoken }
        },
            {
                'post': $postId,
            },
            function (response, status) {
                likesNumber = parseInt($('#like').next().text())
                dislikesNumber = parseInt($('#dislike').next().text())   

                if (status == "success" && response["ok"] == "dislike") {
                    $dislike = $('#dislike').next().next();
                    $dislike.text(toFarsiNumber(dislikesNumber + 1));
                    $dislike.css('font-weight', '900');
                    $('#dislike').next().text(dislikesNumber + 1);
                    
                } else if (status == "success" && response["ok"] == "removelike") {
                    $like = $('#like').next().next();
                    $like.text(toFarsiNumber(likesNumber - 1));
                    $like.css('font-weight', 'normal');
                    $('#like').next().text(likesNumber - 1);

                } else if (status != "success") {
                    console.log(333333)
                    console.log('eerrrror')
                }
            }
        );
    })
}


function acceptPost() {
    $("#accept_post").click(function () {
        const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        $postId = window.location.href.split('/').filter(function (i) { return i }).pop();
        $.post({
            url: 'http://127.0.0.1:8000/blog/api/acceptpost/',
            headers: { 'X-CSRFToken': csrftoken }
        },
            {
                'post': $postId,
            },
            function (response, status) {
                if (status == "success" && response["ok"] == "ok") {
                    $('#accept_post').val($('#accept_post').val() == 'تایید پست' ? 'حذف تایید پست' : 'تایید پست')
                } else if (status != "success") {
                    console.log(333333)
                    console.log('eerrrror')
                }
            }
        );
    })
}


function acceptComment() {
    $(".accept_comment").click(function () {
        const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        $comment = $(this)
        $commentId = $comment.closest('.comment').attr('id').substring(2)
        $.post({
            url: 'http://127.0.0.1:8000/blog/api/acceptcomment/',
            headers: { 'X-CSRFToken': csrftoken }
        },
            {
                'comment': $commentId,
            },
            function (response, status) {
                if (status == "success" && response["ok"] == "ok") {
                    $comment.val($comment.val() == 'تایید نظر' ? 'حذف تایید نظر' : 'تایید نظر')
                } else if (status != "success") {
                    console.log(333333)
                    console.log('eerrrror')
                }
            }
        );
    })
}


function likeComment() {
    $(".like_comment_btn").click(function () {
        const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        $comment = $(this).closest('.comment')
        $like = $comment.find('.like_comment')
        $dislike = $comment.find('.dislike_comment')
        likesNumber = parseInt($like.next().html())
        dislikesNumber = parseInt($dislike.next().html())
        $commentId = $comment.attr('id').substring(2)

        $.post({
            url: 'http://127.0.0.1:8000/blog/api/likecomment/',
            headers: { 'X-CSRFToken': csrftoken }
        },
            {
                'comment': $commentId,
            },
            function (response, status) {
                if (status == "success" && response["ok"] == "like") {
                    $like.html(toFarsiNumber(likesNumber + 1))
                    $like.css('font-weight', '900');
                    $like.next().html(likesNumber + 1)

                } else if (status == "success" && response["ok"] == "removedislike") {
                    $dislike.html(toFarsiNumber(dislikesNumber - 1))
                    $dislike.css('font-weight', 'normal');
                    $dislike.next().html(dislikesNumber - 1)

                } else if (status != "success") {
                    console.log(333333)
                    console.log('eerrrror')
                }
            }
        );
    })
}


function dislikeComment() {
    $(".dislike_comment_btn").click(function () {
        const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        $comment = $(this).closest('.comment')
        $like = $comment.find('.like_comment')
        $dislike = $comment.find('.dislike_comment')
        likesNumber = parseInt($like.next().html())
        dislikesNumber = parseInt($dislike.next().html())
        $commentId = $comment.attr('id').substring(2)

        $.post({
            url: 'http://127.0.0.1:8000/blog/api/dislikecomment/',
            headers: { 'X-CSRFToken': csrftoken }
        },
            {
                'comment': $commentId,
            },
            function (response, status) {
                if (status == "success" && response["ok"] == "dislike") {
                    $dislike.html(toFarsiNumber(dislikesNumber + 1))
                    $dislike.css('font-weight', '900');
                    $dislike.next().html(dislikesNumber + 1)

                } else if (status == "success" && response["ok"] == "removelike") {
                    $like.html(toFarsiNumber(likesNumber - 1))
                    $like.css('font-weight', 'normal');
                    $like.next().html(likesNumber - 1)

                } else if (status != "success") {
                    console.log(333333)
                    console.log('eerrrror')
                }
            }
        );
    })
}


likePost()
dislikePost()
acceptPost()
likeComment()
dislikeComment()
acceptComment()

$('[name=tag]').each(
    function myFunction(tag) {
        width = ((this.value.length + 2) * 8).toString() + 'px';
        $(this).css("width", width);
    })

function toFarsiNumber(n) {
    const farsiDigits = ['۰', '۱', '۲', '۳', '۴', '۵', '۶', '۷', '۸', '۹'];

    return n
        .toString()
        .replace(/\d/g, x => farsiDigits[x]);
}
        

// persian={0:'۰',1:'۱',2:'۲',3:'۳',4:'۴',5:'۵',6:'۶',7:'۷',8:'۸',9:'۹'};

// persianNumbers = [/۰/g, /۱/g, /۲/g, /۳/g, /۴/g, /۵/g, /۶/g, /۷/g, /۸/g, /۹/g],
// // arabicNumbers  = [/٠/g, /١/g, /٢/g, /٣/g, /٤/g, /٥/g, /٦/g, /٧/g, /٨/g, /٩/g],
// fixNumbers = function (str)
// {
//     console.log(str)
//     console.log(typeof str)
//   if(typeof str === 'string')
//   {
//       console.log(555555)
//     for(var i=0; i<10; i++)
//     {
//       str = str.replace(persianNumbers[i], i);
//     }
//   }
// console.log(str)
//   return str;
// };
/*
String.prototype.toPersianDigits = function(){
    var id= ['۰','۱','۲','۳','۴','۵','۶','۷','۸','۹'];
    ans = "";
    for (let index = 0; index < this.length; index++) {
        ans+= id[ans[index]-'0'];
        
    }
    console.log(ans);
    return ans;
    // console.log(this)
    // return this.replace(/[0-9]/g, function(w){
    //     console.log(w)
    //     return id[+w]
    // });
}*/