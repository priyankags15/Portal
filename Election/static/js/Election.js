$(document).ready(function() {
  $("#confirm").click(function(){

    if(!$("#cultural .ui-selected").attr('id') || !$("#president .ui-selected").attr('id') || !$("#vp .ui-selected").attr('id') || !$("#sports .ui-selected").attr('id'))
    {
      swal("Vote in each Poll","Select atleast one option from each poll", "error");
      return;
    }
    data = new FormData()
    ids = [];
    ids.push($("#cultural .ui-selected").attr('id'));
    ids.push($("#president .ui-selected").attr('id'));
    ids.push($("#vp .ui-selected").attr('id'));
    ids.push($("#sports .ui-selected").attr('id'));
    data.append("user_id",JSON.stringify(ids));
    swal({
                    title: "Are you sure?",
                    text: "You will not be able to revert your vote!",
                    type: "warning",
                    showCancelButton: true,
                    confirmButtonColor: '#DD6B55',
                    confirmButtonText: 'confirm',
                    cancelButtonText: "No, cancel plzz!",
                    closeOnConfirm: false,
                    closeOnCancel: true
                  },
                  function(isConfirm){
                      if (isConfirm){
                        $.ajax({
                                  url: '/confirmation',
                                  data: data,
                                  cache: false,
                                  contentType: false,
                                  processData: false,
                                  type: 'POST',
                                  success: function(data){
                                    dataset = JSON.parse(data);
                                    if(dataset.success){
                                      sweetAlert({
                                                title: "Successfully voted ",
                                                text: "Your vote has been casted!",
                                                type: "success"
                                            },

                                            function () {
                                                window.location.href = 'portal';
                                            });// window.location.href = "/portal";
                                    }
                                    else{
                                      sweetAlert({
                                                title: "Unexpected error occured ",
                                                text: "please try after sometime!",
                                                type: "error"
                                            },

                                            function () {
                                                window.location.href = 'portal';
                                            });
                                    }

                                  },
                                  error: function(errors) {

                                    sweetAlert({
                                              title: "Unexpected error occured ",
                                              text: "please try after sometime!",
                                              type: "error"
                                          },

                                          function () {
                                              window.location.href = 'portal';
                                          });
                                  }
                              });

                        }
                      }
                  );
                });
                $("#confirm_delete").click(function(){

                  if(!$("#cultural .ui-selected").attr('id') && !$("#president .ui-selected").attr('id') && !$("#vp .ui-selected").attr('id') && !$("#sports .ui-selected").attr('id'))
                  {
                    swal("Nothing is selected","Select atleast atleast one option", "error");
                    return;
                  }
                  data = new FormData()
                  ids = [];
                  $.each($(".ui-selected"), function( index, value ) {
                      ids.push(value.id);
                    });
                  data.append("user_id",JSON.stringify(ids));
                  swal({
                                  title: "Are you sure?",
                                  text: "You will not be able to revert your action!",
                                  type: "warning",
                                  showCancelButton: true,
                                  confirmButtonColor: '#DD6B55',
                                  confirmButtonText: 'confirm',
                                  cancelButtonText: "No, cancel plzz!",
                                  closeOnConfirm: false,
                                  closeOnCancel: true
                                },
                                function(isConfirm){
                                    if (isConfirm){
                                      $.ajax({
                                                url: '/discard',
                                                data: data,
                                                cache: false,
                                                contentType: false,
                                                processData: false,
                                                type: 'POST',
                                                success: function(data){
                                                  dataset = JSON.parse(data);
                                                  if(dataset.success){
                                                    sweetAlert({
                                                      title: "Successfully discarded",
                                                      text: "Candidature has been discarded!",
                                                      type: "success"
                                                          },

                                                          function () {
                                                              window.location.href = 'portal';
                                                          });// window.location.href = "/portal";
                                                  }
                                                  else{
                                                    sweetAlert({
                                                              title: "Unexpected error occured ",
                                                              text: "please try after sometime!",
                                                              type: "error"
                                                          },

                                                          function () {
                                                              window.location.href = 'portal';
                                                          });
                                                  }

                                                },
                                                error: function(errors) {

                                                  sweetAlert({
                                                            title: "Unexpected error occured ",
                                                            text: "please try after sometime!",
                                                            type: "error"
                                                        },

                                                        function () {
                                                            window.location.href = 'portal';
                                                        });
                                                }
                                            });

                                      }
                                    }
                                );
                              });
    $("#register").click(function(){

    if($("#desig").val()=="" || $("#roll-no").val()=="Roll no" || $("#agenda").val()=="")
    {
    swal("fill all input section","Select a designation", "error");
    return;
    }
    data = new FormData()
    data.append("post",$("#desig").val());
    data.append("user",$("#roll-no").val());
    data.append("agenda",$("#agenda").val());
    console.log($("#desig").val());
    console.log($("#roll-no").val());
    console.log($("#agenda").val());


    swal({
          title: "Are you sure?",
          text: "You will not be able to revert your action!",
          type: "warning",
          showCancelButton: true,
          confirmButtonColor: '#DD6B55',
          confirmButtonText: 'confirm',
          cancelButtonText: "No, cancel plzz!",
          closeOnConfirm: false,
          closeOnCancel: true
        },
        function(isConfirm){
            if (isConfirm){
              $.ajax({
                        url: '/enroll',
                        data: data,
                        cache: false,
                        contentType: false,
                        processData: false,
                        type: 'POST',
                        success: function(data){
                          dataset = JSON.parse(data);
                          if(dataset.success){
                            sweetAlert({
                              title: "Successfully enrolled",
                              text: "Candidature has been added!",
                              type: "success"
                                  },

                                  function () {
                                      window.location.href = 'portal';
                                  });// window.location.href = "/portal";
                          }
                          else if(dataset.able){
                            sweetAlert({
                                      title: "Already enrolled for some designation",
                                      text: "Can't enroll!",
                                      type: "error"
                                  },

                                  function () {
                                    window.location.href = 'portal';
                                  });
                          }
                          else if(dataset.athourized){
                            sweetAlert({
                                      title: "Unidentified roll",
                                      text: "Can't enroll!",
                                      type: "error"
                                  },

                                  function () {
                                    window.location.href = 'portal';
                                  });
                          }

                        },
                        error: function(errors) {

                          sweetAlert({
                                    title: "Unexpected error occured ",
                                    text: "please try after sometime!",
                                    type: "error"
                                },

                                function () {
                                    window.location.href = 'portal';
                                });
                        }
                    });

              }
            }
        );
      });
});
