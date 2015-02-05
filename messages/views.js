$(document).ready(function(){
  var upload_ids = [];
  $('#fileupload').bind('fileuploaddone', function (e, data) {
    console.log('Done uploading product images');
    $(data.result).each(function(){
      upload_ids.push(this.id);
    });
    console.log( upload_ids.join(',') );
    $('#file_ids').val( upload_ids.join(',') );

    if ($('#fileupload td.preview').length == upload_ids.length) {
      console.log('Enabling input');
      $('#reply-form button[type="submit"]').removeAttr('disabled');
    };
  });

  $('#fileupload').bind('fileuploadstart', function (e, data) {
    console.log('Disabling input');
    $('#reply-form button[type="submit"]').attr('disabled','disabled');
  });

  $('#fileupload').bind('fileuploadpreviewdone', function (e, data) {
    if ($('#fileupload-attachments td.preview').length == product_image_ids.length) {
      $('#fileupload-attachments tbody.files tr').remove();
    };
  });
});

$(function () {
    $('#fileupload').fileupload({
        dataType: 'json',
        add: function (e, data) {
            data.context = $('<button/>').text('Upload')
                .appendTo(document.body)
                .click(function () {
                    data.context = $('<p/>').text('Uploading...').replaceAll($(this));
                    data.submit();
                });
        },
        done: function (e, data) {
            data.context.text('Upload finished.');
        }
    });
});