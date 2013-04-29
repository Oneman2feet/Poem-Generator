$(document).ready(function(){ 
    $("#rhyme").hide();
    $("#numLines").hide();
    $("#type").change(function(e){
	
        if(this.value == "sonnet")
	{
            $("#rhyme").slideDown();
            $("#numLines").slideUp();
        }
        else if (this.value == "haiku")
	{
            $("#rhyme").slideUp();
            $("#numLines").slideUp();
        }
        else if (this.value == "free verse")
	{
            $("#rhyme").slideDown();
            $("#numLines").slideDown();
        }
        else
	{
            $("#rhyme").slideUp();
            $("#numLines").slideDown();
        }
    });
});