$(document).ready(function(){
    $('.deleterow').unbind('click').bind('click', function(){
        var $r_id = $(this).attr('id');
        if (confirm("Removing snippet " + $r_id + "\nAre you sure?")) {
            var $killrow = $(this).parent('tr');
            $killrow.addClass("danger");
            $killrow.fadeOut(2000, function(){
                $.ajax({
                    url: '/api/' + $r_id,
                    type: 'DELETE',
                    success: function(result) {
                        $(this).remove();
                    }
                });
            });
        }
    });
    $.fn.editable.defaults.mode = 'inline';
    $.fn.editable.defaults.ajaxOptions = {type: "PUT"};
    $('.editable-textbox').editable({
        type: 'textarea',
        pk: $(this.id),
        title: 'Enter snippet text',
    });
    $('.editable-tag').editable({
        select2: {
            placeholder: 'Insert tag',
            minimumInputLenght: 1,
            ajax: {
                url: '/api/tags/',
                dataType: 'json',
                data: function(term, page) {
                    return {query: term};
                },
                results: function(data, page) {
                    return {result: data};
                },
            },
        }
    });
    $('#snippetButton').unbind('click').bind('click', function(){
        if ($("#snippetForm")[0].checkValidity()){
            var payload = {"value": $('#snippetText').val()};
            $.ajax({
                type: 'post',
                url: "/api/",
                dataType: 'json',
                contentType: 'application/json',
                data: JSON.stringify(payload),
                success: function(msg){
                    location.reload();
                },
                error: function(msg){
                    console.log("error "+msg);
                },
            });
        }else console.log("Invalid form");
    });
});
