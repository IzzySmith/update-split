// specify form behaviour
$(document).ready(function(){
	$('#url').focus(function() { 
  		$(this).val(''); 
	});
	$('#url').keypress(function(e){
		if (e.keyCode == 13){
			e.preventDefault();
			$('#submit_button').click();
		}
	});

});
