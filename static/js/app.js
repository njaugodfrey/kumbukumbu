$(document).ready(
    function(){
        //get the _xsrf token
        function getCookie(name) {
            let cookieValue = null;
            if (document.cookie && document.cookie !== '') {
                const cookies = document.cookie.split(';');
                for (let i = 0; i < cookies.length; i++) {
                    const cookie = cookies[i].trim();
                    // Does this cookie string begin with the name we want?
                    if (cookie.substring(0, name.length + 1) === (name + '=')) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }
            return cookieValue;
        }
        const xsrftoken = getCookie('_xsrf');


        $('#date_field').datetimepicker({
            inline:false,
        });

        function update_status(item_id) {
            $.ajax({
                url: '/update_status',
                headers: {'X-CSRFToken': xsrftoken},
                type: 'POST',
                data: item_id,

                success: function (response_data) {
                    console.log(response_data);
                },
                error: function () {
                    console.log('error');
                }
            });
        };

        $("#list-of-things").on('click', 'a[id^=change-this-]', function(){
            var item_id = $(this).attr('id').split('-')[2];
            console.log(item_id)
            update_status(item_id);
        });
    }
);