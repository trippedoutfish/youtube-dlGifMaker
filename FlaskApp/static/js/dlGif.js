 $(function() {
    $('#btndlGif').click(function() {
 
        $.ajax({
            url: '/dlGif',
            data: $('form').serialize(),
            type: 'POST',
            success: function(response) {
                console.log(response);
				console.log("Hello!1");
            },
            error: function(error) {
                console.log(error);
				console.log("Hello!2");
            }
        });
    });
});