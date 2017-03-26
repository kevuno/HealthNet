//Functions to be called here
function functionOne(){
  console.log("one");
}

function toggle_forms_and_buttons(){
  $("#medical_form_register").toggle();
  $("#personal_form_register").toggle();
  $("#medical_link").toggle();
  $("#personal_link").toggle();

}

//Place jquery in here
$( document ).ready(function() {
  //Registration form stuff
  $("#medical_form_register").hide();
  $("#personal_link").hide();

  $("#switch_to_personal_form").click(function(){

    toggle_forms_and_buttons();
  });
  $("#switch_to_medical_form").click(function(){

    toggle_forms_and_buttons();
  });

  $("#show_prescription_form_modal").click(function(){
    $("#prescription_form_modal").toggle();
  });

});