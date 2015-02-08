/*jslint unparam: true */
/*global window, $ */
function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
 var upload_ids = [];

$(function () {
    'use strict';
    // Change this to the location of your server-side upload handler:
    var url = '/messages/upload/';
    var csrftoken = $.cookie('csrftoken');
    $('#fileupload').fileupload({
        url: url,
        crossDomain: false,
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type)) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        },
        dataType: 'json',
        done: function (e, data) {
            //console.log('Upload complete');
            $.each(data.result.files, function (index, file) {
                 upload_ids.push(file.name);
                 //console.log( file.url);
                 // console.log( upload_ids.join(',') );
            $('#id_file_ids').val( upload_ids.join(',') );
            $('<p/>').text(file.name).appendTo('#files');
            });

        },
        progressall: function (e, data) {
            var progress = parseInt(data.loaded / data.total * 100, 10);
            $('#progress .progress-bar').css(
                'width',
                progress + '%'
            );
        }
    }).prop('disabled', !$.support.fileInput)
        .parent().addClass($.support.fileInput ? undefined : 'disabled');
});