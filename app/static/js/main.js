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
  
$(document).ready(function($) {
    $(".table-row").click(function() {
        window.document.location = $(this).data("href");
    });
});
//Corp_spec.html ** right view showing by page, click left-sidebar, showing cooresponding div page
$(document).ready(function() {
  $(".links").click(function(){
  $(".divs:visible").hide();
  $("#"+$(this).attr("data-showdiv")).show();
  });
});
//TimeSheet.html ** select Daily entry or SheetList
$(document).ready(function() {
    $("#select-btn button").click(function(){
    $(".timesheettbl:visible").hide();
    $(".timesheetbtn").removeClass("active");
    $("#"+$(this).attr("data-showdiv")).show();
    $(this).addClass("active");
    });
  });

//TimeSheet.html ** Stopwatch function: start & stop
// $(document).ready(function() {
//     $("button.inputgroupStart").click(function(){
//     $(("#"+$(this).attr("targetgroup"))+" form input.form-control").removeAttr('disabled');
//     $(("#"+$(this).attr("targetgroup"))+" form textarea.form-control").removeAttr('disabled');
//     $(("#"+$(this).attr("targetgroup"))+" form #timesheet1-1").val(new Date().toISOString().slice(0,10));
//     var u = '{{title}}';
//     //$(("#"+$(this).attr("targetgroup"))+" form #timesheet1-1").val({{current_user[1]}}');
//     console.log(u);
//     });
//   });

//Corp_spec.html ** right view showing by Scrolling, click left-sidebar, scroll right 
$(document).ready(function () {
  window.addEventListener("scroll", function(event) {
      var scrollTop = document.documentElement.scrollTop || window.pageYOffset || document.body.scrollTop;
      $(window).scroll(function () {
          var top = $(document).scrollTop();          //定义变量，获取滚动条的高度
          //var menu = $("#menu");                      //定义变量，抓取#menu
          var items = $("#content").find(".item");    //定义变量，查找.item
          var curId = "";                             //定义变量，当前所在的楼层item #id
          items.each(function () {
              var m = $(this);                        //定义变量，获取当前类
              var mHeight = m.height();
              var itemsTop = m.offset().top;        //定义变量，获取当前类的top偏移量
              if (top >= itemsTop - mHeight/2) {
                  curId = "#" + m.attr("id");
                  if(curId == "#item7"){
                      var menu = $("#menu");
                      var curLink = menu.find(".sidenav");
                      curLink.removeClass("sidenav");
                      menu.find("[href='#item7']").addClass("sidenav");
                  }else{
                      //给相应的楼层设置cur,取消其他楼层的cur
                      var menu = $("#menu");
                      var curLink = menu.find(".sidenav");
                      if (curId && curLink.attr("href") != curId) {
                          curLink.removeClass("sidenav");
                          menu.find("[href=" + curId + "]").addClass("sidenav");
                      }
                  }
              } else {
                  return false;
              }
          });
      });
  });
});

