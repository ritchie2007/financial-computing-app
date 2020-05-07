function goUrl() {
    var txtURL=document.getElementById("txtURL");
    var ifweb=document.getElementById("ifweb");
    ifweb.src=txtURL.value; /* "value", not "nodeValue", not "Value" */
  
}

// Filter table

$(document).ready(function(){
    $("#tableSearch").on("keyup", function() {
      var value = $(this).val().toLowerCase();
      $("#myTable tr").filter(function() {
        $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
      });
    });
  });
  