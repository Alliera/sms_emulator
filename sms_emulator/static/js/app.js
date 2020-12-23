$(function () {

    function refreshMessages() {
        var phone_number = $("#phone_number").val();
        var enterprise = $("#enterprise").val();
        if (enterprise && phone_number) {
            var csrf_token = $("input[name=csrfmiddlewaretoken]").val();
            $.ajax({
                headers: {"X-CSRFToken": csrf_token},
                url: '/',
                type: "POST",
                data: {
                    'phone_number': phone_number,
                    'enterprise': enterprise
                },
                success: function (result) {
                    $("#messages_list").empty().html(result);
                },
                error: function (xhr, resp, text) {
                    console.log(xhr, resp, text);
                }
            })
        }
    }

    setInterval(function () {
        refreshMessages()
    }, 7000);


    $("#btn_search_phone").on('click', function () {
        var csrf_token = $("input[name=csrfmiddlewaretoken]").val();
        $.ajax({
            headers: {"X-CSRFToken": csrf_token},
            url: '/',
            type: "POST",
            // dataType: 'json', // data type
            data: $("#form_search_phone").serialize(),
            success: function (result) {
                $("#messages_list").empty().html(result);
            },
            error: function (xhr, resp, text) {
                console.log(xhr, resp, text);
            }
        })
    });

    $("#btn_send_message").on('click', function () {
        var csrf_token = $("input[name=csrfmiddlewaretoken]").val();
        var sms_message = $("#text_to_send").val();
        var phone_number = $("#phone_number").val();
        var enterprise = $("#enterprise").val()

        $.ajax({
            headers: {"X-CSRFToken": csrf_token},
            url: '/outbox_message',
            type: "POST",
            data: {
                'sms_message': sms_message,
                'phone_number': phone_number,
                'enterprise': enterprise
            },
            success: function (result) {
                $("#messaging_area").empty().html(result);
                $.ajax({
                    headers: {"X-CSRFToken": csrf_token},
                    url: '/',
                    type: "POST",
                    data: {
                        'phone_number': $("#phone_number").val(),
                        'enterprise': $("#enterprise").val()
                    },
                    success: function (result) {
                        $("#messages_list").empty().html(result);
                    },
                    error: function (xhr, resp, text) {
                        console.log(xhr, resp, text);
                    }
                })
            },
            error: function (xhr, resp, text) {
                console.log(xhr, resp, text);
            }
        })
    });

});
