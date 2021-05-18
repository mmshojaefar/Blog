$('[name="username"]').on('input' ,function() {
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    if($('[name="username"]').val().length == 0){
        if ($('[name="username"]').closest('div').next().find('input').length == 0)
                $('[name="username"]').closest('div').next().remove()
    }
    if($('[name="username"]').val().length > 0){
        $.post({
            url: 'http://127.0.0.1:8000/api/checkusername/',
            headers: { 'X-CSRFToken': csrftoken }
        },
            {
                'username': $('[name="username"]').val(),
            },
            function (response, status) {
                if (status == "success" && response['ok']==true) {
                    if ($('[name="username"]').closest('div').next().find('input').length == 0)
                        $('[name="username"]').closest('div').next().remove()
                    $("<div class='bg-success bg-gradient py-0'><p>این نام کاربری قابل قبول است.</p></div>").insertAfter($('[name="username"]').closest('div'));
                } else if (status == "success" && response['ok']==false) {
                    if ($('[name="username"]').closest('div').next().find('input').length == 0)
                        $('[name="username"]').closest('div').next().remove()
                    $("<div class='bg-danger bg-gradient py-0'><p>این نام کاربری قبلا انتخاب شده است.</p></div>").insertAfter($('[name="username"]').closest('div'));
                } else if (status == "success" && response['ok']==null) {
                    if ($('[name="username"]').closest('div').next().find('input').length == 0)
                        $('[name="username"]').closest('div').next().remove()
                    $("<div class='bg-warning bg-gradient py-0'><p>نام کاربری باید حداقل 4 کاراکتر باشد و فقط می تواند شامل حروف انگلیسی و اعداد باشد.</p></div>").insertAfter($('[name="username"]').closest('div'));
                }
            }
        );
    }
});
