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
//根据窗口大小设置动态CSS，注意var height_val得到的结果总是固定的(CSS文件中设定的值)，
//如果这个函数里使用location.reload(); 则是死循环，屏幕一直抖动
//height: '100%' 目的是 去掉窗口太大时，下面漏出的背景
//height: 'fit-content' 目的是 窗口缩小出现滚动条时，而此时滚动窗口尺寸大于屏幕尺寸，下面出现背景
$(document).ready(function () {
    $(function () {  
        var height_window=$(window).height();
        var height_val = $('.tbl-field').css("height");
           //此处不严谨，可以通过$(window).height()获取整个屏幕高度后，结合屏幕的内容高度$（‘’）.height()，相减得出判断条件。
        if(height_window>880){
                $('.tbl-field').css({height: '100%'});
        } else {
            $('.tbl-field').css({height: 'fit-content'});
        };
        console.log(height_window);
        console.log(height_val);
    });
})
//改变窗口大小后，自动刷新，如想清楚cache则需要location.reload(true);，这是配合上面的动态CSS使用的
$(document).ready(function () {
    $(window).bind('resize', function() {
        location.reload();
    });
});