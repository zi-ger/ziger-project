$(function() {
    $('[id^="like"]').click(function(e) {
        e.preventDefault();
        url = $(this).attr('href');
        console.log(url);

        id = $(this).attr('data-id');

        $.get(url, function(data) {
            if (data.status) {
                $("#numlikes"+id).text(data.likesCount);
                if (data.liked) {
                    $("#icon"+id).text('favorite');
                } else {
                    $("#icon"+id).text('favorite_border');
                }     
            }
        });
    });
});