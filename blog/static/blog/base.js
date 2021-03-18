function check() {
    ans = $($('.time').find('input')[0]).val().length > 0 || $($('.time').find('input')[1]).val().length > 0
    for (var i = 0; i < $('.checkbox').length; i++) {
        ans = ans || $($('.checkbox')[i]).find('input').is(':checked')
    }
    return ans
}


var timer;
var counterBack;
var delay=1500;

var i = 1;
$('#toggleAdvSearch').mouseenter(function () {
    clearTimeout(timer)
    // counterBack = setInterval(function () {
    //     console.log(i);
    //     if (i > 0 && i < 102) {
    //         i+=12;
    //         $('.progress-bar').css('width', i + '%');
    //     } else {
    //         // $('.progress-bar').css('width', 1 + '%');
    //         // counterBack.stop
    //         // clearInterval(counterBack);
    //         // i=1;
    //     }
    // }, delay/15);
    timer = window.setTimeout(function () {
        $('.advSearch').show();
        $('.show').addClass('d-none')
        $('.hide').removeClass('d-none')
    }, delay)
}).mouseleave(function () {
    if (!check()) {
        $('.advSearch').hide();
        $('.show').removeClass('d-none')
        $('.hide').addClass('d-none')
    }
    clearTimeout(timer)
    // i=1;
    // $('.progress-bar').css('width', i + '%');
    // counterBack.stop
    // clearInterval(counterBack);
});


$('.advSearch').mouseover(function () {
    $('.advSearch').show();
    $('.show').addClass('d-none')
    $('.hide').removeClass('d-none')
    // clearTimeout(timer)
    // i=1;
    // $('.progress-bar').css('width', i + '%');
    // clearInterval(counterBack);
}).mouseleave(function () {
    if (!check()) {
        $('.advSearch').hide();
        $('.show').removeClass('d-none')
        $('.hide').addClass('d-none')
    }
    clearTimeout(timer)
    // i=1;
    // $('.progress-bar').css('width', i + '%');
    // counterBack.stop
    // clearInterval(counterBack);
})


$('.show').click(function () {
    $('.advSearch').show();
    $('.show').addClass('d-none')
    $('.hide').removeClass('d-none')
    clearTimeout(timer)
    // i=1;
    // $('.progress-bar').css('width', i + '%');
    // counterBack.stop
    // clearInterval(counterBack);
});


$('.hide').click(function () {
    $('.advSearch').hide();
    $('.show').removeClass('d-none')
    $('.hide').addClass('d-none')
    clearTimeout(timer)
    // i=1;
    // $('.progress-bar').css('width', i + '%');
    // counterBack.stop
    // clearInterval(counterBack);
});


$('#openSearch').click(function () {
    $('#searchForm').removeClass('d-none')
    $('#searchForm').addClass('d-flex')
    $('#searchForm').addClass('col-12')

    $('#blog').removeClass('col-2')
    $('#blog').addClass('d-none')

    $('#searchFormParent').addClass('col-12')
    $('#searchFormParent').removeClass('col-10')

    $('#searchBtn').removeClass('d-flex')
    $('#searchBtn').addClass('d-none')
})


$('#closeSearch').click(function () {
    $('#searchForm').addClass('d-none')
    $('#searchForm').removeClass('d-flex')
    $('#searchForm').removeClass('col-12')

    $('#blog').addClass('col-2')
    $('#blog').removeClass('d-none')

    $('#searchFormParent').removeClass('col-12')
    $('#searchFormParent').addClass('col-10')

    $('#searchBtn').addClass('d-flex')
    $('#searchBtn').removeClass('d-none')
})


if ($('.advSearch').find('.errorlist').length) {
    $('.advSearch').css('display', 'block')
}