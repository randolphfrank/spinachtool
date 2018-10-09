$(document).ready(function() {

    $('#imgA').click(function(){
        $("#imgA").hide();
        $("#imgOutA").show();
        $("#p1").show();
    })

    $('#imgOutA').click(function(){
        $("#imgOutA").hide();
        $("#imgA").show();
        $("#p1").hide();
    })

    $('#imgB').click(function(){
        $("#imgB").hide();
        $("#imgOutB").show();
        $("#p3").show();
    })

    $('#imgOutB').click(function(){
        $("#imgOutB").hide();
        $("#imgB").show();
        $("#p3").hide();
    })

    $('#imgC').click(function(){
        $("#imgC").hide();
        $("#imgOutC").show();
        $("#p2").show();
    })

    $('#imgOutC').click(function(){
        $("#imgOutC").hide();
        $("#imgC").show();
        $("#p2").hide();
    })

});





