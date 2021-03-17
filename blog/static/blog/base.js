function check(){
    ans = $($('.time').find('input')[0]).val().length>0 || $($('.time').find('input')[1]).val().length>0
    for(var i=0; i<$('.checkbox').length; i++){
        ans = ans || $($('.checkbox')[i]).find('input').is(':checked')
    }
    return ans
}


var timer;
$('#toggleAdvSearch').mouseenter(function() {
    clearTimeout( timer )
    timer = window.setTimeout(function(){
        $('.advSearch').show();
        $('.show').addClass('d-none')
        $('.hide').removeClass('d-none')
    }, 1500)
}).mouseleave(function() {
    if(!check()){
        $('.advSearch').hide();
        $('.show').removeClass('d-none')
        $('.hide').addClass('d-none')
    }
    clearTimeout( timer )
});

$('.advSearch').mouseover(function() {
    $('.advSearch').show();
    $('.show').addClass('d-none')
    $('.hide').removeClass('d-none')
    clearTimeout( timer )
}).mouseleave(function() {
    if(!check()){
        $('.advSearch').hide();
        $('.show').removeClass('d-none')
        $('.hide').addClass('d-none')
    }
    clearTimeout( timer )
})

$('.show').click(function() {
    $('.advSearch').show();
    $('.show').addClass('d-none')
    $('.hide').removeClass('d-none')
    clearTimeout( timer )
});

$('.hide').click(function() {
    $('.advSearch').hide();
    $('.show').removeClass('d-none')
    $('.hide').addClass('d-none')
    clearTimeout( timer )
});

$('#openSearch').click(function(){
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

$('#closeSearch').click(function(){
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
