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
