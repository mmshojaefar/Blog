function check(){
    ans = $($('.time').find('input')[0]).val().length>0 || $($('.time').find('input')[1]).val().length>0
    for(var i=0; i<$('.checkbox').length; i++){
        ans = ans || $($('.checkbox')[i]).find('input').is(':checked')
    }
    return ans
}

// check()

$('#showAdvSearch').mouseenter(function() {
    $('.advSearch').show();
}).mouseleave(function() {
    if(!check()){
        $('.advSearch').hide();
    }
});


$('.advSearch').mouseover(function() {
    $('.advSearch').show();
}).mouseleave(function() {
    if(!check()){
        $('.advSearch').hide();
    }
})


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
