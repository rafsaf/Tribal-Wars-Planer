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

const handleClickButton = (element, message, formId) => {
    element.disabled = true;
    element.innerHTML = `<span class='spinner-border mr-1 spinner-border-sm text-dark my-auto' role='status'></span>${message}`;
    const form = document.getElementById(formId);
    form.submit();
}

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const changeTargetTime = async (target_id, time_id) => {
    const id1 = parseInt(target_id);
    const id2 = parseInt(time_id);
    const timeSelector = String(target_id) + "-time-" + String(time_id);
    const newTime = document.getElementById(timeSelector);
    const actualInnerHTML = newTime.innerHTML
    newTime.innerHTML = `<div class="spinner-border spinner-border-sm text-secondary" role="status"></div>`

    const response = await fetch(`/api/target-time-update/${id1}/${id2}/`, {
        method: "PUT",
        credentials: "same-origin",
        headers: {
            "X-CSRFToken": getCookie("csrftoken"),
            "Accept": "application/json",
            "Content-Type": "application/json"
        },
    })
    if (response.status !== 200) {
        newTime.innerHTML = `<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-exclamation-square" viewBox="0 0 16 16"><path d="M14 1a1 1 0 0 1 1 1v12a1 1 0 0 1-1 1H2a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1h12zM2 0a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V2a2 2 0 0 0-2-2H2z"/><path d="M7.002 11a1 1 0 1 1 2 0 1 1 0 0 1-2 0zM7.1 4.995a.905.905 0 1 1 1.8 0l-.35 3.507a.552.552 0 0 1-1.1 0L7.1 4.995z"/></svg>`
        const oldClassName = newTime.className
        newTime.className = 'btn btn-lg btn-danger my-1 py-0 px-1'
        
        setTimeout(() => {
            newTime.className = oldClassName
            newTime.innerHTML = actualInnerHTML
            newTime.blur()
        }, 2000)
    } else {
        const data = await response.json();
        newTime.className = "btn btn-lg btn-primary my-1 py-0 px-1"
        newTime.innerHTML = actualInnerHTML
        newTime.blur();
        if (data.old !== "none" && data.old !== data.new) {
            const oldTime = document.getElementById(data.old);
            oldTime.className = 'btn btn-lg btn-light my-1 py-0 px-1'
        }
    }
}

const deleteTarget = async (target_id) => {
    const id1 = parseInt(target_id);
    const targetButtonSelector = "target-btn-" + String(target_id);
    const targetRowSelector = "target-row-" + String(target_id);
    const targetButton = document.getElementById(targetButtonSelector);
    const targetRow = document.getElementById(targetRowSelector);

    const targetButtonOldInnerHTML = targetButton.innerHTML
    targetButton.disabled = true;
    targetButton.innerHTML = `<div class="spinner-border spinner-border-sm text-secondary" role="status"></div>`

    const response = await fetch(`/api/target-delete/${id1}/`, {
        method: "DELETE",
        credentials: "same-origin",
        headers: {
            "X-CSRFToken": getCookie("csrftoken"),
            "Accept": "application/json",
            "Content-Type": "application/json"
        },
    })
    if (response.status !== 204) {
        targetButton.innerHTML = `<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-exclamation-square" viewBox="0 0 16 16"><path d="M14 1a1 1 0 0 1 1 1v12a1 1 0 0 1-1 1H2a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1h12zM2 0a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V2a2 2 0 0 0-2-2H2z"/><path d="M7.002 11a1 1 0 1 1 2 0 1 1 0 0 1-2 0zM7.1 4.995a.905.905 0 1 1 1.8 0l-.35 3.507a.552.552 0 0 1-1.1 0L7.1 4.995z"/></svg>`
        setTimeout(() => {
            targetButton.innerHTML = targetButtonOldInnerHTML
            targetButton.blur()
        }, 2000)
    } else {
        targetRow.style.display = 'none';
    }
}

const submitGoBackButton = (text) => {
    const buttonForm1 = document.getElementById("form1-btn")
    const buttonDismiss = document.getElementById("dismiss-btn")
    buttonForm1.onclick = () => {
        buttonForm1.disabled = true
        buttonDismiss.disabled = true
        buttonForm1.innerHTML = `<span class='spinner-border mr-1 spinner-border-sm text-dark my-auto' role='status'></span>${text}`
        const form1 = document.getElementById("form1-form")
        form1.submit()
      }
}

const activateFixedScrollbarContainer = () => {
    document.addEventListener("DOMContentLoaded", function (event) {
    $(function($) {
        var fixedBarTemplate = '<div class="fixed-scrollbar"><div></div></div>';
        var fixedBarCSS = { display: 'none', overflowX: 'scroll', position: 'fixed', width: '100%', bottom: 0 };

        $('.fixed-scrollbar-container').each(function() {
            var $container = $(this);
            var $bar = $(fixedBarTemplate).appendTo($container).css(fixedBarCSS);

            $bar.scroll(function() {
                $container.scrollLeft($bar.scrollLeft());
            });

            $bar.data("status", "off");
        });

        var fixSize = function() {
            $('.fixed-scrollbar').each(function() {
                var $bar = $(this);
                var $container = $bar.parent();

                $bar.children('div').height(1).width($container[0].scrollWidth);
                $bar.width($container.width()).scrollLeft($container.scrollLeft());
            });
        };

        $(window).on("load.fixedbar resize.fixedbar", function() {
            fixSize();
        });

        var scrollTimeout = null;

        $(window).on("scroll.fixedbar", function() {
            clearTimeout(scrollTimeout);
            scrollTimeout = setTimeout(function() {
                $('.fixed-scrollbar-container').each(function() {
                    var $container = $(this);
                    var $bar = $container.children('.fixed-scrollbar');

                    if ($bar.length) {
                        var containerOffset = { top: $container.offset().top, bottom: $container.offset().top + $container.height() };
                        var windowOffset = { top: $(window).scrollTop(), bottom: $(window).scrollTop() + $(window).height() };

                        if ((containerOffset.top > windowOffset.bottom) || (windowOffset.bottom > containerOffset.bottom)) {
                            if ($bar.data("status") == "on") {
                                $bar.hide().data("status", "off");
                            }
                        } else {
                            if ($bar.data("status") == "off") {
                                $bar.show().data("status", "on");
                                $bar.scrollLeft($container.scrollLeft());
                            }
                        }
                    }
                });
            }, 50);
        });

        $(window).trigger("scroll.fixedbar");
    });});
}

const changeIsHiddenState = async (outline_id, token) => {
    const overview = document.getElementById(token);
    const actualInnerHTML = overview.innerHTML;
    overview.disabled = true;
    overview.innerHTML = `<div class="spinner-border spinner-border-sm text-secondary" role="status"></div>`

    const response = await fetch(`/api/overview-hide-state-update/${outline_id}/${token}/`, {
        method: "PUT",
        credentials: "same-origin",
        headers: {
            "X-CSRFToken": getCookie("csrftoken"),
            "Accept": "application/json",
            "Content-Type": "application/json"
        },
    })
    if (response.status !== 200) {
        overview.innerHTML = `<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-exclamation-square" viewBox="0 0 16 16"><path d="M14 1a1 1 0 0 1 1 1v12a1 1 0 0 1-1 1H2a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1h12zM2 0a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V2a2 2 0 0 0-2-2H2z"/><path d="M7.002 11a1 1 0 1 1 2 0 1 1 0 0 1-2 0zM7.1 4.995a.905.905 0 1 1 1.8 0l-.35 3.507a.552.552 0 0 1-1.1 0L7.1 4.995z"/></svg>`
        setTimeout(() => {
            overview.innerHTML = actualInnerHTML;
            overview.blur();
        }, 2000)
    } else {
        const data = await response.json();
        overview.innerHTML = data.name;
        overview.className = data.class;
        overview.disabled = false;
        overview.blur();

    }
}


const codemirrorValidation = (json_errors, selectorClass) => {
    document.addEventListener("DOMContentLoaded", function(event) {
        $(selectorClass).addClass('CodeMirror-Invalid');
        const codemirror = $(selectorClass);
        const codeMirrorEditor = codemirror[0].CodeMirror;
        const errors = JSON.parse(json_errors)
        
        Object.entries(errors).forEach(([key, value], index) => {
            if (index === 0) {
                codeMirrorEditor.scrollIntoView(parseInt(value.message));
            }
            codeMirrorEditor.addLineClass(parseInt(value.message), 'wrap', 'line-error');
        });
    });

}