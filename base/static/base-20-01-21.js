const modal = () => {
  document.addEventListener("DOMContentLoaded", function(event) {
      $('#form-modal').on('show.bs.modal', function(event) {
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
  })
};

const scroll_content_outline = () => {
  $(window).on("load", function() {
      if (localStorage.getItem("my_app_name_here-quote-scroll") != null) {
          $(window).scrollTop(localStorage.getItem("my_app_name_here-quote-scroll"));
      };
      if (localStorage.getItem("my_app_name_here-left-scroll") != null) {
          $('#leftscroll').scrollTop(localStorage.getItem("my_app_name_here-left-scroll"));
      };
      $(window).on("scroll", function() {
          localStorage.setItem("my_app_name_here-quote-scroll", $(window).scrollTop());
      });
      $('#leftscroll').on("scroll", function() {
          var scroll = $('#leftscroll').scrollTop();
          localStorage.setItem("my_app_name_here-left-scroll", scroll);
      });
  });
}

const menu_toggle = () => {
  $("#menu-toggle").click(function(e) {
      e.preventDefault();
      $("#sidebar-wrapper").toggleClass("toggled");
  });
  $(document).ready(function() {
      $('#id_date').addClass('data-picker')
      $('.data-picker').datepicker({
          format: "yyyy-mm-dd"
      });
  });
}

const calculate_distance = (element) => {
      const world_speed = parseFloat(String(document.getElementById('speed_world').value).replace(",", "."));
      const units_speed = parseFloat(String(document.getElementById('speed_units').value).replace(",", "."));

      if (element.clicked) {
          element.innerHTML = element.distance;
          element.clicked = false
      } else {
          element.distance = parseFloat(element.innerHTML);
          let fixed_ram = (element.distance / units_speed / world_speed / 60 * 30)
          if (fixed_ram > 99.9) {
              fixed_ram = fixed_ram.toFixed(0)
          } else {
              fixed_ram = fixed_ram.toFixed(1)
          }

          let fixed_noble = (element.distance / units_speed / world_speed / 60 * 35)
          if (fixed_noble > 99.9) {
              fixed_noble = fixed_noble.toFixed(0)
          } else {
              fixed_noble = fixed_noble.toFixed(1)
          }

          element.innerHTML = `<span class='text-nowrap'>${fixed_ram}h / ${fixed_noble}h</span>`;
          element.clicked = true;
      }
  }
  /*
   * Light YouTube Embeds by @labnol
   * Credit: https://www.labnol.org/
   */

function labnolIframe(div) {
  var iframe = document.createElement('iframe');
  iframe.setAttribute(
      'src',
      'https://www.youtube.com/embed/' + div.dataset.id + '?autoplay=1&rel=0'
  );
  iframe.setAttribute('frameborder', '0');
  iframe.setAttribute('allowfullscreen', '1');
  iframe.setAttribute(
      'allow',
      'accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture'
  );
  div.parentNode.replaceChild(iframe, div);
}

function initYouTubeVideos() {
  var playerElements = document.getElementsByClassName('youtube-player');
  for (var n = 0; n < playerElements.length; n++) {
      var videoId = playerElements[n].dataset.id;
      var div = document.createElement('div');
      div.setAttribute('data-id', videoId);
      var thumbNode = document.createElement('img');
      thumbNode.src = '//i.ytimg.com/vi/ID/hqdefault.jpg'.replace(
          'ID',
          videoId
      );
      div.appendChild(thumbNode);
      var playButton = document.createElement('div');
      playButton.setAttribute('class', 'play');
      div.appendChild(playButton);
      div.onclick = function() {
          labnolIframe(this);
      };
      playerElements[n].appendChild(div);
  }
}

const activateTooltips = () => {
  document.addEventListener("DOMContentLoaded", function(event) {
      $('.popoverData').popover();
  });
  $(function() {
      $('[data-toggle="tooltip"]').tooltip()
  })
}

const onPlanerLinkClick = (text) => {
  setTimeout(() => {
      const planerLink = document.getElementById("planer-link")
      planerLink.innerHTML = `<span class='spinner-border mr-1 spinner-border-sm text-info my-auto' role='status'></span>${text}`
  }, 800)
}

const handleAllFormsetSelect = () => {
  document.addEventListener("DOMContentLoaded", function (event) {
      val = $('#id_form-0-status').val();
      if (val === 'all') {
          $('#id_form-0-from_number').val('');
          $('#id_form-0-from_number').prop("disabled", true);

          $('#id_form-0-to_number').val('');
          $('#id_form-0-to_number').prop("disabled", true);

      } else if (val === 'exact') {
          $('#id_form-0-from_number').val('');
          $('#id_form-0-from_number').prop("disabled", true);

          $('#id_form-0-to_number').prop("disabled", false);

      };

      val = $('#id_form-1-status').val();
      if (val === 'all') {
          $('#id_form-1-from_number').val('');
          $('#id_form-1-from_number').prop("disabled", true);

          $('#id_form-1-to_number').val('');
          $('#id_form-1-to_number').prop("disabled", true);

      } else if (val === 'exact') {
          $('#id_form-1-from_number').val('');
          $('#id_form-1-from_number').prop("disabled", true);

          $('#id_form-1-to_number').prop("disabled", false);

      };

      val = $('#id_form-2-status').val();
      if (val === 'all') {
          $('#id_form-2-from_number').val('');
          $('#id_form-2-from_number').prop("disabled", true);

          $('#id_form-2-to_number').val('');
          $('#id_form-2-to_number').prop("disabled", true);

      } else if (val === 'exact') {
          $('#id_form-2-from_number').val('');
          $('#id_form-2-from_number').prop("disabled", true);

          $('#id_form-2-to_number').prop("disabled", false);

      };

      val = $('#id_form-3-status').val();
      if (val === 'all') {
          $('#id_form-3-from_number').val('');
          $('#id_form-3-from_number').prop("disabled", true);

          $('#id_form-3-to_number').val('');
          $('#id_form-3-to_number').prop("disabled", true);

      } else if (val === 'exact') {
          $('#id_form-3-from_number').val('');
          $('#id_form-3-from_number').prop("disabled", true);

          $('#id_form-3-to_number').prop("disabled", false);

      };

      val = $('#id_form-4-status').val();
      if (val === 'all') {
          $('#id_form-4-from_number').val('');
          $('#id_form-4-from_number').prop("disabled", true);

          $('#id_form-4-to_number').val('');
          $('#id_form-4-to_number').prop("disabled", true);

      } else if (val === 'exact') {
          $('#id_form-4-from_number').val('');
          $('#id_form-4-from_number').prop("disabled", true);

          $('#id_form-4-to_number').prop("disabled", false);

      };

      val = $('#id_form-5-status').val();
      if (val === 'all') {
          $('#id_form-5-from_number').val('');
          $('#id_form-5-from_number').prop("disabled", true);

          $('#id_form-5-to_number').val('');
          $('#id_form-5-to_number').prop("disabled", true);

      } else if (val === 'exact') {
          $('#id_form-5-from_number').val('');
          $('#id_form-5-from_number').prop("disabled", true);

          $('#id_form-5-to_number').prop("disabled", false);

      };
  });

  document.addEventListener("DOMContentLoaded", function (event) {
      $('.time-timepicker').each(function () {
          $(this).timepicker({
              minuteStep: 1,
              secondStep: 1,
              showSeconds: true,
              showMeridian: false,
              defaultTime: false,
              icons: {
                  up: 'fa fa-angle-up',
                  down: 'fa fa-angle-down'
              }
          })
      });

      $('#id_form-0-status').change(function () {
          val = $('#id_form-0-status').val();
          if (val === 'all') {
              $('#id_form-0-from_number').val('');
              $('#id_form-0-from_number').prop("disabled", true);

              $('#id_form-0-to_number').val('');
              $('#id_form-0-to_number').prop("disabled", true);

          } else if (val === 'exact') {
              $('#id_form-0-from_number').val('');
              $('#id_form-0-from_number').prop("disabled", true);

              $('#id_form-0-to_number').prop("disabled", false);

          } else {
              $('#id_form-0-from_number').prop("disabled", false);

              $('#id_form-0-to_number').prop("disabled", false);

          };
      });
      $('#id_form-1-status').change(function () {
          val = $('#id_form-1-status').val();
          if (val === 'all') {
              $('#id_form-1-from_number').val('');
              $('#id_form-1-from_number').prop("disabled", true);

              $('#id_form-1-to_number').val('');
              $('#id_form-1-to_number').prop("disabled", true);

          } else if (val === 'exact') {
              $('#id_form-1-from_number').val('');
              $('#id_form-1-from_number').prop("disabled", true);

              $('#id_form-1-to_number').prop("disabled", false);

          } else {
              $('#id_form-1-from_number').prop("disabled", false);

              $('#id_form-1-to_number').prop("disabled", false);

          };
      });
      $('#id_form-2-status').change(function () {
          val = $('#id_form-2-status').val();
          if (val === 'all') {
              $('#id_form-2-from_number').val('');
              $('#id_form-2-from_number').prop("disabled", true);

              $('#id_form-2-to_number').val('');
              $('#id_form-2-to_number').prop("disabled", true);

          } else if (val === 'exact') {
              $('#id_form-2-from_number').val('');
              $('#id_form-2-from_number').prop("disabled", true);

              $('#id_form-2-to_number').prop("disabled", false);

          } else {
              $('#id_form-2-from_number').prop("disabled", false);

              $('#id_form-2-to_number').prop("disabled", false);

          };
      });
      $('#id_form-3-status').change(function () {
          val = $('#id_form-3-status').val();
          if (val === 'all') {
              $('#id_form-3-from_number').val('');
              $('#id_form-3-from_number').prop("disabled", true);

              $('#id_form-3-to_number').val('');
              $('#id_form-3-to_number').prop("disabled", true);

          } else if (val === 'exact') {
              $('#id_form-3-from_number').val('');
              $('#id_form-3-from_number').prop("disabled", true);

              $('#id_form-3-to_number').prop("disabled", false);

          } else {
              $('#id_form-3-from_number').prop("disabled", false);

              $('#id_form-3-to_number').prop("disabled", false);

          };
      });
      $('#id_form-4-status').change(function () {
          val = $('#id_form-4-status').val();
          if (val === 'all') {
              $('#id_form-4-from_number').val('');
              $('#id_form-4-from_number').prop("disabled", true);

              $('#id_form-4-to_number').val('');
              $('#id_form-4-to_number').prop("disabled", true);

          } else if (val === 'exact') {
              $('#id_form-4-from_number').val('');
              $('#id_form-4-from_number').prop("disabled", true);

              $('#id_form-4-to_number').prop("disabled", false);

          } else {
              $('#id_form-4-from_number').prop("disabled", false);

              $('#id_form-4-to_number').prop("disabled", false);

          };
      });
      $('#id_form-5-status').change(function () {
          val = $('#id_form-5-status').val();
          if (val === 'all') {
              $('#id_form-5-from_number').val('');
              $('#id_form-5-from_number').prop("disabled", true);

              $('#id_form-5-to_number').val('');
              $('#id_form-5-to_number').prop("disabled", true);

          } else if (val === 'exact') {
              $('#id_form-5-from_number').val('');
              $('#id_form-5-from_number').prop("disabled", true);

              $('#id_form-5-to_number').prop("disabled", false);

          } else {
              $('#id_form-5-from_number').prop("disabled", false);

              $('#id_form-5-to_number').prop("disabled", false);

          };
      });
  });
}

const handleButtonClicks = (save, processing, armyUpdate, reloading) => {
  document.addEventListener("DOMContentLoaded", function () {
      const buttonForm1 = document.getElementById("form1-btn")
      const buttonFormComplete = document.getElementById("form-complete-btn")
      const buttonFormUpdate = document.getElementById("form-update-btn")
      const buttonForm2 = document.getElementById("form2-btn")
      const buttonForm3 = document.getElementById("form3-btn")
      const buttonForm4 = document.getElementById("form4-btn")
      const buttonFormset = document.getElementById("formset-btn")

      buttonForm1.onclick = () => {
      buttonForm1.disabled = true
      buttonFormComplete.disabled = true
      buttonForm1.innerHTML = `<span class='spinner-border mr-1 spinner-border-sm text-dark my-auto' role='status'></span>${save}`
      const form1 = document.getElementById("form1-form")
      form1.submit()
      }

      buttonFormComplete.onclick = () => {
      buttonForm1.disabled = true
      buttonFormComplete.disabled = true
      buttonFormComplete.innerHTML = `<span class='spinner-border mr-1 spinner-border-sm text-dark my-auto' role='status'></span>${processing}`
      const formComplete = document.getElementById("form-complete")
      formComplete.submit()
      }

      buttonFormUpdate.onclick = () => {
      buttonFormUpdate.disabled = true
      buttonForm2.disabled = true

      buttonFormUpdate.innerHTML = `<span class='spinner-border mr-1 spinner-border-sm text-dark my-auto' role='status'></span>${armyUpdate}`
      const formUpdate = document.getElementById("form-update")
      formUpdate.submit()
      }

      buttonForm2.onclick = () => {
      buttonFormUpdate.disabled = true
      buttonForm2.disabled = true

      buttonForm2.innerHTML = `<span class='spinner-border mr-1 spinner-border-sm text-dark my-auto' role='status'></span>${reloading}`
      const form2 = document.getElementById("form2-form")
      form2.submit()
      }
      buttonForm3.onclick = () => {
      buttonForm3.disabled = true
      buttonForm3.innerHTML = `<span class='spinner-border mr-1 spinner-border-sm text-dark my-auto' role='status'></span>${save}`
      const form3 = document.getElementById("form3-form")
      form3.submit()
      }
      buttonForm4.onclick = () => {
      buttonForm4.disabled = true
      buttonForm4.innerHTML = `<span class='spinner-border mr-1 spinner-border-sm text-dark my-auto' role='status'></span>${save}`
      const form4 = document.getElementById("form4-form")
      form4.submit()
      }
      buttonFormset.onclick = () => {
      buttonFormset.disabled = true
      buttonFormset.innerHTML = `<span class='spinner-border mr-1 spinner-border-sm text-dark my-auto' role='status'></span>${save}`
      const formset = document.getElementById("formset-form")
      formset.submit()
      }
  });
}