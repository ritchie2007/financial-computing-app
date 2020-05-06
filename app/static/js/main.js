function goUrl() {
    var txtURL=document.getElementById("txtURL");
    var ifweb=document.getElementById("ifweb");
    ifweb.src=txtURL.value; /* "value", not "nodeValue", not "Value" */
  
}

// Filter table

$(document).ready(function () {
    $('#dtBasicExample').DataTable();
    $('.dataTables_length').addClass('bs-select');
    });

// // Sorting
// $(document).ready(function () {
//     $('#dtBasicExample').DataTable({
//     "ordering": false // false to disable sorting (or any other option)
//     });
//     $('.dataTables_length').addClass('bs-select');
//     });

// // Sorting
// $(document).ready(function () {
//     $('#dtOrderExample').DataTable({
//     "order": [[ 3, "desc" ]]
//     });
//     $('.dataTables_length').addClass('bs-select');
//     });

