
$(document).ready(function(){
    $.fn.editable.defaults.mode = 'inline';
    $.fn.editable.defaults.ajaxOptions = {type: "PUT"};
    $('.editable-textbox').editable({
        type: 'textarea',
        pk: $(this.id),
        url: '/api/' + $(this.id),
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
});
