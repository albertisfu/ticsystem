$(document).ready(function(){
  var upload_ids = [];
  $('#fileupload-attachments').bind('fileuploaddone', function (e, data) {
    console.log('Done uploading product images');
    $(data.result).each(function(){
      upload_ids.push(this.id);
    });
    console.log( upload_ids.join(',') );
    $('#id_file_ids').val( upload_ids.join(',') );

    if ($('#fileupload-attachments td.preview').length == upload_ids.length) {
      console.log('Enabling input');
      $('#reply-form button[type="submit"]').removeAttr('disabled');
    };
  });

  $('#fileupload-attachments').bind('fileuploadstart', function (e, data) {
    console.log('Disabling input');
    $('#reply-form button[type="submit"]').attr('disabled','disabled');
  });

  $('#fileupload-attachments').bind('fileuploadpreviewdone', function (e, data) {
    if ($('#fileupload-attachments td.preview').length == product_image_ids.length) {
      $('#fileupload-attachments tbody.files tr').remove();
    };
  });
});