$('[name="username"]').on('input' ,function() {
    // console.log($('[name="username"]').val())
    // console.log($('[name="username"]').val().length)
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    if($('[name="username"]').val().length > 0){
        $.post({
            url: 'http://127.0.0.1:8000/blog/api/checkusername/',
            headers: { 'X-CSRFToken': csrftoken }
        },
            {
                'username': $('[name="username"]').val(),
            },
            function (response, status) {
                if (status == "success" && response['ok']==true) {
                    $('[name="username"]').closest('tr').next().remove()
                    $("<tr><td></td><td><p>این نام کاربری قابل قبول است.</p></td></tr>").insertAfter($('[name="username"]').closest('tr'));
                } else if (status == "success" && response['ok']==false) {
                    $('[name="username"]').closest('tr').next().remove()
                    $("<tr><td></td><td><p>این نام کاربری قبلا انتخاب شده است.</p></td></tr>").insertAfter($('[name="username"]').closest('tr'));
                } else if (status == "success" && response['ok']==null) {
                    $('[name="username"]').closest('tr').next().remove()
                    $("<tr><td></td><td><p>نام کاربری باید حداقل 4 کاراکتر باشد و فقط می تواند شامل حروف انگلیسی و اعداد باشد.</p></td></tr>").insertAfter($('[name="username"]').closest('tr'));
                }
            }
        );
    }
});
