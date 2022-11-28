
(function ($) {
    "use strict";

    
    /*==================================================================
    [ Validate ]*/
    var input = $('.validate-input .input100');

    $('.validate-form').on('submit',function(){
        var check = true;

        for(var i=0; i<input.length; i++) {
            if(validate(input[i]) == false){
                showValidate(input[i]);
                check=false;
            }
        }

        return check;
    });


    $('.validate-form .input100').each(function(){
        $(this).focus(function(){
           hideValidate(this);
        });
    });

    function validate (input) {
        if($(input).attr('type') == 'email' || $(input).attr('name') == 'email') {
            if($(input).val().trim().match(/^([a-zA-Z0-9_\-\.]+)@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.)|(([a-zA-Z0-9\-]+\.)+))([a-zA-Z]{1,5}|[0-9]{1,3})(\]?)$/) == null) {
                return false;
            }
        }
        else {
            if($(input).val().trim() == ''){
                return false;
            }
        }
    }


})(jQuery);




function setClipboard(text) {
    const type = "text/plain";
    const blob = new Blob([text], { type });
    const data = [new ClipboardItem({ [type]: blob })];

    navigator.clipboard.write(data).then(
        () => {
        /* success */
        },
        () => {
        /* failure */
        }
    );
}

// var cp = document.querySelector('login100-form-btn2')

// cp.addEventListener('click', function(event) {
// 	var jobValue = document.getElementsById('output')[0].value;
// 	copyTextToClipboard(jobValue);
// });

function to(){ x.className = x.className.replace("show", ""); };

function myFunction() {

    // After 3 seconds, remove the show class from DIV
    var jobValue = document.getElementsByClassName("input1001")[0].value;
    // alert(jobValue);
	setClipboard(jobValue);

  }

  function generateB(){
    document.getElementsByClassName("input1001")[0].value = "";
  }