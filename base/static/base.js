

var modal = function(){
        document.addEventListener("DOMContentLoaded", function (event) {
        $('#form-modal').on('show.bs.modal', function (event) {
          var button = $(event.relatedTarget) // Button that triggered the modal
          var start = button.data('start')
          var off = button.data('off')
          var nobleman = button.data('nobleman')
          var id = button.data('id')
          var modal = $(this)
          modal.find('.modal-title').text(start)
          modal.find('#id_off').val(off)
          modal.find('#id_nobleman').val(nobleman)
          modal.find('#id_weight_id').val(id)
        })
    
        $('.popoverData').popover();
        $('.popoverOption').popover({ trigger: "hover" });
        })};

var scroll_content_outline = function(){
        $(window).on("load", function () {
                // weave your magic here.
            
                if (localStorage.getItem("my_app_name_here-quote-scroll") != null) {
                  $(window).scrollTop(localStorage.getItem("my_app_name_here-quote-scroll"));
            
            
                };
                if (localStorage.getItem("my_app_name_here-left-scroll") != null) {
                  $('#leftscroll').scrollTop(localStorage.getItem("my_app_name_here-left-scroll"));
                };
            
            
                $(window).on("scroll", function () {
                  localStorage.setItem("my_app_name_here-quote-scroll", $(window).scrollTop());
                });
            
                $('#leftscroll').on("scroll", function () {
                  var scroll = $('#leftscroll').scrollTop();
                  localStorage.setItem("my_app_name_here-left-scroll", scroll);
                });
              });
}

var menu_toggle = function(){
        $("#menu-toggle").click(function (e) {
                e.preventDefault();
                $("#wrapper").toggleClass("toggled");
            });
            $(document).ready(function() {
                $('#id_date').addClass('data-picker')
                $('.data-picker').datepicker({
                    format: "yyyy-mm-dd"
                });
            });
    
            $('.carousel').carousel({
                interval: 2500
              });
}