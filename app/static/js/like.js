$(".btn-like").click(function () {
    var b = $(this);
    if(b.attr('flag')==='0'){
        $.ajax({
        type: 'POST',
        url: '/like',
        data: {id: b.prop('id')},
        success: function (data) {
            console.log(data)
        },
        });
        // $(this).text("已赞");
        $(this).css('color','red');
        b.attr('flag','1');
    }else {
        $.ajax({
                type: 'POST',
                url: '/unlike',
                data: {id: b.prop('id')},
                success: function (data) {
                    console.log(data)
                },
            });
        b.attr('flag','0');
        $(this).css('color','');
        // $(this).text("赞");
    }
});