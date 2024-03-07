

$("#leadForm").validationEngine({
    maxErrorsPerField: true,
    showOneMessage: true,
    promptPosition: "right",
    onValidationComplete: function(form, status) {
        if (status == true) {
            $("#questionForm").val($("#saveQuestionsForm").serialize());
            $("#questionModal").modal("hide");
        } else {
            return false;
        }
    }
});



$("#closeQuestionModal").on("click", function() {
    $("#questionModal").modal("hide");
    $("#questionForm").val("");
});

$("#filterLeadFormId").validationEngine({
    maxErrorsPerField: true,
    showOneMessage: true,
   // promptPosition : "topRight:-100"

});

let campaign_schedule_date = "";
let campaign_start_date = "";
let campaign_end_date = "";

if ($('#campaign_schedule_date').val()) {
    campaign_schedule_date = $.trim($('#campaign_schedule_date').val());
}

if ($('#campaign_start_date').val()) {
    campaign_start_date = $.trim($('#campaign_start_date').val());
}

if ($('#campaign_end_date').val()) {
    campaign_end_date = $.trim($('#campaign_end_date').val());
}



$('.dateTimePickerClass').datetimepicker({
    format:'Y-m-d H:i',
    minDate: new Date(),
    step: 15
});



$('.recc_schedule_date').datetimepicker({
    format:'Y-m-d H:i',
    minDate: new Date(),
    step: 15
});

$("html").on('focus', ".recc_schedule_date", function() {
    $(this).datetimepicker({
        format:'Y-m-d H:i',
        minDate: new Date(),
        step: 15
    });
});


$('#campaign_schedule_date').datetimepicker({
    format:'Y-m-d H:i',
    minDate: new Date(),
    value: campaign_schedule_date,
    step: 15

});

$('#campaign_start_date').datetimepicker({
    format:'Y-m-d',
    minView: 2,
    timepicker: false,
    dateonly: true,
    value: campaign_start_date,
});

$('#campaign_end_date').datetimepicker({
    format:'Y-m-d',
    minView: 2,
    timepicker: false,
    dateonly: true,
    value: campaign_end_date
});

$(".select2").select2();



tinymce.init({
    selector: 'textarea.tinymce',
    height: 300,
    menubar: false,
    plugins: [
      'advlist autolink lists link image charmap print preview anchor',
      'searchreplace visualblocks code fullscreen',
      'insertdatetime media table paste code wordcount'
    ],
    toolbar: 'undo redo | formatselect | ' +
    'bold italic backcolor | alignleft aligncenter ' +
    'alignright alignjustify | bullist numlist outdent indent | ' +
    'removeformat',

  });


  $('#date_time_field').daterangepicker({
    singleDatePicker: true,

  });


