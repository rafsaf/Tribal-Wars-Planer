const modal = () => {
  document.addEventListener("DOMContentLoaded", function (event) {
    $("#form-modal").on("show.bs.modal", function (event) {
      var button = $(event.relatedTarget); // Button that triggered the modal
      var start = button.data("start");
      var off = button.data("off");
      var leftOff = button.data("leftoff");
      var nobleman = button.data("nobleman");
      var leftNobleman = button.data("leftnobleman");
      var id = button.data("id");
      var modal = $(this);
      modal.find(".modal-title").text(start);
      modal.find("#id_off").val(off);
      modal.find("#id_off").attr("max", parseInt(off) + parseInt(leftOff));
      modal.find("#id_nobleman").val(nobleman);
      modal
        .find("#id_nobleman")
        .attr("max", parseInt(nobleman) + parseInt(leftNobleman));
      modal.find("#id_weight_id").val(id);
    });

    $(".popoverData").popover();
    $(".popoverOption").popover({ trigger: "hover" });
  });
};

const loadDocsPage = (
  uniqueNumber,
  elementId,
  staticPath,
  handleScrollTop = false
) => {
  // tries to load cached markdown file from localStorage
  // if not exists, fetch and save it
  // if staticPath for specific document is changed (and it must be refetched),
  // we remove old cached markdown, fetch new and save, alongside with path
  const element = document.getElementById(elementId);
  if (localStorage.getItem(staticPath) != null) {
    element.innerHTML = marked.parse(localStorage.getItem(staticPath));
  } else {
    fetch(staticPath)
      .then((res) => res.text())
      .then((codeText) => {
        if (localStorage.getItem(String(uniqueNumber)) != null) {
          localStorage.removeItem(localStorage.getItem(String(uniqueNumber)));
        }
        document.getElementById(elementId).innerHTML = marked.parse(codeText);
        localStorage.setItem(staticPath, codeText);
        localStorage.setItem(String(uniqueNumber), staticPath);
        if (handleScrollTop) {
          wholePageContentScroll(`${uniqueNumber}-scroll-id`);
        }
      });
  }
};

const wholePageContentScroll = (key) => {
  if (localStorage.getItem(key) != null) {
    $(window).scrollTop(localStorage.getItem(key));
  }
  $(window).on("scroll", function () {
    localStorage.setItem(key, $(window).scrollTop());
  });
};

const scroll_content_outline = () => {
  $(window).on("load", function () {
    if (localStorage.getItem("my_app_name_here-quote-scroll") != null) {
      $(window).scrollTop(
        localStorage.getItem("my_app_name_here-quote-scroll")
      );
    }
    if (localStorage.getItem("my_app_name_here-left-scroll") != null) {
      $("#leftscroll").scrollTop(
        localStorage.getItem("my_app_name_here-left-scroll")
      );
    }
    $(window).on("scroll", function () {
      localStorage.setItem(
        "my_app_name_here-quote-scroll",
        $(window).scrollTop()
      );
    });
    $("#leftscroll").on("scroll", function () {
      var scroll = $("#leftscroll").scrollTop();
      localStorage.setItem("my_app_name_here-left-scroll", scroll);
    });
  });
};

const menu_toggle = () => {
  $("#menu-toggle").click(function (e) {
    e.preventDefault();
    $("#sidebar-wrapper").toggleClass("toggled");
  });
  $(document).ready(function () {
    $("#id_date").addClass("data-picker");
    $(".data-picker").datepicker({
      format: "yyyy-mm-dd",
    });
  });
};

const calculate_distance = (element) => {
  const world_speed = parseFloat(
    String(document.getElementById("speed_world").value).replace(",", ".")
  );
  const units_speed = parseFloat(
    String(document.getElementById("speed_units").value).replace(",", ".")
  );

  if (element.clicked) {
    element.innerHTML = element.distance;
    element.clicked = false;
  } else {
    element.distance = parseFloat(element.innerHTML);
    let fixed_ram = (element.distance / units_speed / world_speed / 60) * 30;
    if (fixed_ram > 99.9) {
      fixed_ram = fixed_ram.toFixed(0);
    } else {
      fixed_ram = fixed_ram.toFixed(1);
    }

    let fixed_noble = (element.distance / units_speed / world_speed / 60) * 35;
    if (fixed_noble > 99.9) {
      fixed_noble = fixed_noble.toFixed(0);
    } else {
      fixed_noble = fixed_noble.toFixed(1);
    }

    element.innerHTML = `<span class='text-nowrap'>${fixed_ram}h / ${fixed_noble}h</span>`;
    element.clicked = true;
  }
};

const activateTooltips = () => {
  document.addEventListener("DOMContentLoaded", function (event) {
    $(".popoverData").popover();
  });
  $(function () {
    $('[data-toggle="tooltip"]').tooltip();
  });
};

const onPlanerLinkClick = (text) => {
  setTimeout(() => {
    const planerLink = document.getElementById("planer-link");
    planerLink.innerHTML = `<span class='spinner-border mr-1 spinner-border-sm text-info my-auto' role='status'></span>${text}`;
  }, 800);
};

const handleAllFormsetSelect = () => {
  document.addEventListener("DOMContentLoaded", function (event) {
    val = $("#id_form-0-status").val();
    if (val === "all") {
      $("#id_form-0-from_number").val("");
      $("#id_form-0-from_number").prop("disabled", true);

      $("#id_form-0-to_number").val("");
      $("#id_form-0-to_number").prop("disabled", true);
    } else if (val === "exact") {
      $("#id_form-0-from_number").val("");
      $("#id_form-0-from_number").prop("disabled", true);

      $("#id_form-0-to_number").prop("disabled", false);
    }

    val = $("#id_form-1-status").val();
    if (val === "all") {
      $("#id_form-1-from_number").val("");
      $("#id_form-1-from_number").prop("disabled", true);

      $("#id_form-1-to_number").val("");
      $("#id_form-1-to_number").prop("disabled", true);
    } else if (val === "exact") {
      $("#id_form-1-from_number").val("");
      $("#id_form-1-from_number").prop("disabled", true);

      $("#id_form-1-to_number").prop("disabled", false);
    }

    val = $("#id_form-2-status").val();
    if (val === "all") {
      $("#id_form-2-from_number").val("");
      $("#id_form-2-from_number").prop("disabled", true);

      $("#id_form-2-to_number").val("");
      $("#id_form-2-to_number").prop("disabled", true);
    } else if (val === "exact") {
      $("#id_form-2-from_number").val("");
      $("#id_form-2-from_number").prop("disabled", true);

      $("#id_form-2-to_number").prop("disabled", false);
    }

    val = $("#id_form-3-status").val();
    if (val === "all") {
      $("#id_form-3-from_number").val("");
      $("#id_form-3-from_number").prop("disabled", true);

      $("#id_form-3-to_number").val("");
      $("#id_form-3-to_number").prop("disabled", true);
    } else if (val === "exact") {
      $("#id_form-3-from_number").val("");
      $("#id_form-3-from_number").prop("disabled", true);

      $("#id_form-3-to_number").prop("disabled", false);
    }

    val = $("#id_form-4-status").val();
    if (val === "all") {
      $("#id_form-4-from_number").val("");
      $("#id_form-4-from_number").prop("disabled", true);

      $("#id_form-4-to_number").val("");
      $("#id_form-4-to_number").prop("disabled", true);
    } else if (val === "exact") {
      $("#id_form-4-from_number").val("");
      $("#id_form-4-from_number").prop("disabled", true);

      $("#id_form-4-to_number").prop("disabled", false);
    }

    val = $("#id_form-5-status").val();
    if (val === "all") {
      $("#id_form-5-from_number").val("");
      $("#id_form-5-from_number").prop("disabled", true);

      $("#id_form-5-to_number").val("");
      $("#id_form-5-to_number").prop("disabled", true);
    } else if (val === "exact") {
      $("#id_form-5-from_number").val("");
      $("#id_form-5-from_number").prop("disabled", true);

      $("#id_form-5-to_number").prop("disabled", false);
    }
  });

  document.addEventListener("DOMContentLoaded", function (event) {
    $(".time-timepicker").each(function () {
      $(this).timepicker({
        minuteStep: 1,
        secondStep: 1,
        showSeconds: true,
        showMeridian: false,
        defaultTime: false,
        icons: {
          up: "fa fa-angle-up",
          down: "fa fa-angle-down",
        },
      });
    });

    $("#id_form-0-status").change(function () {
      val = $("#id_form-0-status").val();
      if (val === "all") {
        $("#id_form-0-from_number").val("");
        $("#id_form-0-from_number").prop("disabled", true);

        $("#id_form-0-to_number").val("");
        $("#id_form-0-to_number").prop("disabled", true);
      } else if (val === "exact") {
        $("#id_form-0-from_number").val("");
        $("#id_form-0-from_number").prop("disabled", true);

        $("#id_form-0-to_number").prop("disabled", false);
      } else {
        $("#id_form-0-from_number").prop("disabled", false);

        $("#id_form-0-to_number").prop("disabled", false);
      }
    });
    $("#id_form-1-status").change(function () {
      val = $("#id_form-1-status").val();
      if (val === "all") {
        $("#id_form-1-from_number").val("");
        $("#id_form-1-from_number").prop("disabled", true);

        $("#id_form-1-to_number").val("");
        $("#id_form-1-to_number").prop("disabled", true);
      } else if (val === "exact") {
        $("#id_form-1-from_number").val("");
        $("#id_form-1-from_number").prop("disabled", true);

        $("#id_form-1-to_number").prop("disabled", false);
      } else {
        $("#id_form-1-from_number").prop("disabled", false);

        $("#id_form-1-to_number").prop("disabled", false);
      }
    });
    $("#id_form-2-status").change(function () {
      val = $("#id_form-2-status").val();
      if (val === "all") {
        $("#id_form-2-from_number").val("");
        $("#id_form-2-from_number").prop("disabled", true);

        $("#id_form-2-to_number").val("");
        $("#id_form-2-to_number").prop("disabled", true);
      } else if (val === "exact") {
        $("#id_form-2-from_number").val("");
        $("#id_form-2-from_number").prop("disabled", true);

        $("#id_form-2-to_number").prop("disabled", false);
      } else {
        $("#id_form-2-from_number").prop("disabled", false);

        $("#id_form-2-to_number").prop("disabled", false);
      }
    });
    $("#id_form-3-status").change(function () {
      val = $("#id_form-3-status").val();
      if (val === "all") {
        $("#id_form-3-from_number").val("");
        $("#id_form-3-from_number").prop("disabled", true);

        $("#id_form-3-to_number").val("");
        $("#id_form-3-to_number").prop("disabled", true);
      } else if (val === "exact") {
        $("#id_form-3-from_number").val("");
        $("#id_form-3-from_number").prop("disabled", true);

        $("#id_form-3-to_number").prop("disabled", false);
      } else {
        $("#id_form-3-from_number").prop("disabled", false);

        $("#id_form-3-to_number").prop("disabled", false);
      }
    });
    $("#id_form-4-status").change(function () {
      val = $("#id_form-4-status").val();
      if (val === "all") {
        $("#id_form-4-from_number").val("");
        $("#id_form-4-from_number").prop("disabled", true);

        $("#id_form-4-to_number").val("");
        $("#id_form-4-to_number").prop("disabled", true);
      } else if (val === "exact") {
        $("#id_form-4-from_number").val("");
        $("#id_form-4-from_number").prop("disabled", true);

        $("#id_form-4-to_number").prop("disabled", false);
      } else {
        $("#id_form-4-from_number").prop("disabled", false);

        $("#id_form-4-to_number").prop("disabled", false);
      }
    });
    $("#id_form-5-status").change(function () {
      val = $("#id_form-5-status").val();
      if (val === "all") {
        $("#id_form-5-from_number").val("");
        $("#id_form-5-from_number").prop("disabled", true);

        $("#id_form-5-to_number").val("");
        $("#id_form-5-to_number").prop("disabled", true);
      } else if (val === "exact") {
        $("#id_form-5-from_number").val("");
        $("#id_form-5-from_number").prop("disabled", true);

        $("#id_form-5-to_number").prop("disabled", false);
      } else {
        $("#id_form-5-from_number").prop("disabled", false);

        $("#id_form-5-to_number").prop("disabled", false);
      }
    });
  });
};

const handleClickButton = (element, message, formId, percentId = "") => {
  element.disabled = true;
  element.innerHTML = `<span class='spinner-border mr-1 spinner-border-sm text-dark my-auto' role='status'></span> ${message} <span id=${percentId}></span>`;
  const form = document.getElementById(formId);
  form.submit();
};

function getCookie(name) {
  var cookieValue = null;
  if (document.cookie && document.cookie != "") {
    var cookies = document.cookie.split(";");
    for (var i = 0; i < cookies.length; i++) {
      var cookie = jQuery.trim(cookies[i]);
      if (cookie.substring(0, name.length + 1) == name + "=") {
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
  const actualInnerHTML = newTime.innerHTML;
  newTime.innerHTML = `<div class="spinner-border spinner-border-sm text-secondary" role="status"></div>`;

  const response = await fetch(`/api/target-time-update/${id1}/${id2}/`, {
    method: "PUT",
    credentials: "same-origin",
    headers: {
      "X-CSRFToken": getCookie("csrftoken"),
      Accept: "application/json",
      "Content-Type": "application/json",
    },
  });
  if (response.status !== 200) {
    newTime.innerHTML = `<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-exclamation-square" viewBox="0 0 16 16"><path d="M14 1a1 1 0 0 1 1 1v12a1 1 0 0 1-1 1H2a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1h12zM2 0a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V2a2 2 0 0 0-2-2H2z"/><path d="M7.002 11a1 1 0 1 1 2 0 1 1 0 0 1-2 0zM7.1 4.995a.905.905 0 1 1 1.8 0l-.35 3.507a.552.552 0 0 1-1.1 0L7.1 4.995z"/></svg>`;
    const oldClassName = newTime.className;
    newTime.className = "btn btn-lg btn-danger my-1 py-0 px-1 mr-1";

    setTimeout(() => {
      newTime.className = oldClassName;
      newTime.innerHTML = actualInnerHTML;
      newTime.blur();
    }, 2000);
  } else {
    const data = await response.json();
    newTime.className = "btn btn-lg btn-primary my-1 py-0 px-1 mr-1";
    newTime.innerHTML = actualInnerHTML;
    newTime.blur();
    if (data.old !== "none" && data.old !== data.new) {
      const oldTime = document.getElementById(data.old);
      oldTime.className = "btn btn-lg btn-light my-1 py-0 px-1 mr-1";
    }
  }
};

const deleteTarget = async (target_id) => {
  const id1 = parseInt(target_id);
  const targetButtonSelector = "target-btn-" + String(target_id);
  const targetRowSelector = "target-row-" + String(target_id);
  const targetButton = document.getElementById(targetButtonSelector);
  const targetRow = document.getElementById(targetRowSelector);

  const targetButtonOldInnerHTML = targetButton.innerHTML;
  targetButton.disabled = true;
  targetButton.innerHTML = `<div class="spinner-border spinner-border-sm text-secondary" role="status"></div>`;

  const response = await fetch(`/api/target-delete/${id1}/`, {
    method: "DELETE",
    credentials: "same-origin",
    headers: {
      "X-CSRFToken": getCookie("csrftoken"),
      Accept: "application/json",
      "Content-Type": "application/json",
    },
  });
  if (response.status !== 204) {
    targetButton.innerHTML = `<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-exclamation-square" viewBox="0 0 16 16"><path d="M14 1a1 1 0 0 1 1 1v12a1 1 0 0 1-1 1H2a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1h12zM2 0a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V2a2 2 0 0 0-2-2H2z"/><path d="M7.002 11a1 1 0 1 1 2 0 1 1 0 0 1-2 0zM7.1 4.995a.905.905 0 1 1 1.8 0l-.35 3.507a.552.552 0 0 1-1.1 0L7.1 4.995z"/></svg>`;
    setTimeout(() => {
      targetButton.innerHTML = targetButtonOldInnerHTML;
      targetButton.blur();
    }, 2000);
  } else {
    targetRow.style.display = "none";
  }
};

const submitGoBackButton = (text) => {
  const buttonForm1 = document.getElementById("form1-btn");
  const buttonDismiss = document.getElementById("dismiss-btn");
  buttonForm1.onclick = () => {
    buttonForm1.disabled = true;
    buttonDismiss.disabled = true;
    buttonForm1.innerHTML = `<span class='spinner-border mr-1 spinner-border-sm text-dark my-auto' role='status'></span>${text}`;
    const form1 = document.getElementById("form1-form");
    form1.submit();
  };
};

const changeIsHiddenState = async (outline_id, token) => {
  const overview = document.getElementById(token);
  const actualInnerHTML = overview.innerHTML;
  overview.disabled = true;
  overview.innerHTML = `<div class="spinner-border spinner-border-sm text-secondary" role="status"></div>`;

  const response = await fetch(
    `/api/overview-hide-state-update/${outline_id}/${token}/`,
    {
      method: "PUT",
      credentials: "same-origin",
      headers: {
        "X-CSRFToken": getCookie("csrftoken"),
        Accept: "application/json",
        "Content-Type": "application/json",
      },
    }
  );
  if (response.status !== 200) {
    overview.innerHTML = `<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-exclamation-square" viewBox="0 0 16 16"><path d="M14 1a1 1 0 0 1 1 1v12a1 1 0 0 1-1 1H2a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1h12zM2 0a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V2a2 2 0 0 0-2-2H2z"/><path d="M7.002 11a1 1 0 1 1 2 0 1 1 0 0 1-2 0zM7.1 4.995a.905.905 0 1 1 1.8 0l-.35 3.507a.552.552 0 0 1-1.1 0L7.1 4.995z"/></svg>`;
    setTimeout(() => {
      overview.innerHTML = actualInnerHTML;
      overview.blur();
    }, 2000);
  } else {
    const data = await response.json();
    overview.innerHTML = data.name;
    overview.className = data.class;
    overview.disabled = false;
    overview.blur();
  }
};

const changeBuildingsArray = async (outline_id, list) => {
  const overview = document.getElementById("multi-select-spinner");
  overview.innerHTML = `<div class="spinner-border spinner-border-sm text-secondary" role="status"></div>`;
  const buildings = { buildings: list };
  await fetch(`/api/change-buildings-array/${outline_id}/`, {
    method: "PUT",
    credentials: "same-origin",
    headers: {
      "X-CSRFToken": getCookie("csrftoken"),
      Accept: "application/json",
      "Content-Type": "application/json",
    },
    body: JSON.stringify(buildings),
  })
    .then((response) => {
      if (response.status === 200) {
        overview.innerHTML = `<svg xmlns="http://www.w3.org/2000/svg" width="25" height="25" fill="green" class="bi bi-check" viewBox="0 0 16 16"><path d="M10.97 4.97a.75.75 0 0 1 1.07 1.05l-3.99 4.99a.75.75 0 0 1-1.08.02L4.324 8.384a.75.75 0 1 1 1.06-1.06l2.094 2.093 3.473-4.425a.267.267 0 0 1 .02-.022z"/></svg>`;
        setTimeout(() => {
          overview.innerHTML = "";
        }, 400);
      } else {
        overview.innerHTML = `<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="red" class="bi bi-exclamation-square" viewBox="0 0 16 16"><path d="M14 1a1 1 0 0 1 1 1v12a1 1 0 0 1-1 1H2a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1h12zM2 0a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V2a2 2 0 0 0-2-2H2z"/><path d="M7.002 11a1 1 0 1 1 2 0 1 1 0 0 1-2 0zM7.1 4.995a.905.905 0 1 1 1.8 0l-.35 3.507a.552.552 0 0 1-1.1 0L7.1 4.995z"/></svg> <span class="md-error">(Error in connection!)</span>`;
        setTimeout(() => {
          overview.innerHTML = "";
        }, 2000);
      }
    })
    .catch(() => {
      overview.innerHTML = `<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="red" class="bi bi-exclamation-square" viewBox="0 0 16 16"><path d="M14 1a1 1 0 0 1 1 1v12a1 1 0 0 1-1 1H2a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1h12zM2 0a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V2a2 2 0 0 0-2-2H2z"/><path d="M7.002 11a1 1 0 1 1 2 0 1 1 0 0 1-2 0zM7.1 4.995a.905.905 0 1 1 1.8 0l-.35 3.507a.552.552 0 0 1-1.1 0L7.1 4.995z"/></svg> <span class="md-error">(Error in connection!)</span>`;
      setTimeout(() => {
        overview.innerHTML = "";
      }, 2000);
    });
};
const resetUserMessages = async () => {
  const svg = document.getElementById("reset-svg");
  const span = document.getElementById("reset-span");
  await fetch(`/api/reset-user-messages/`, {
    method: "PUT",
    credentials: "same-origin",
    headers: {
      "X-CSRFToken": getCookie("csrftoken"),
      Accept: "application/json",
      "Content-Type": "application/json",
    },
  }).then((response) => {
    if (response.status === 200) {
      svg.style.fill = "rgba(0,0,0,.5)";
      span.style.color = "rgba(0,0,0,.5)";
      span.innerHTML = "0";
    }
  });
};

const codemirrorValidation = (json_errors, selectorClass) => {
  document.addEventListener("DOMContentLoaded", function (event) {
    $(selectorClass).addClass("CodeMirror-Invalid");
    const codemirror = $(selectorClass);
    const codeMirrorEditor = codemirror[0].CodeMirror;
    const errors = JSON.parse(json_errors);

    Object.entries(errors).forEach(([key, value], index) => {
      if (index === 0) {
        codeMirrorEditor.scrollIntoView(parseInt(value.message));
      }
      codeMirrorEditor.addLineClass(
        parseInt(value.message),
        "wrap",
        "line-error"
      );
    });
  });
};

const handleButtonClipboardUpdate = (
  element,
  selector,
  success,
  updatedText
) => {
  const text = document.getElementById(selector);
  const newClip = text.textContent;
  navigator.clipboard.writeText(newClip);

  element.innerHTML = `<svg class='mr-2' width='1.4em' height='1.4em' viewBox='0 0 16 16' class='bi bi-check2-all' fill='green' ><path fill-rule='evenodd' d='M12.354 3.646a.5.5 0 0 1 0 .708l-7 7a.5.5 0 0 1-.708 0l-3.5-3.5a.5.5 0 1 1 .708-.708L5 10.293l6.646-6.647a.5.5 0 0 1 .708 0z'/><path d='M6.25 8.043l-.896-.897a.5.5 0 1 0-.708.708l.897.896.707-.707zm1 2.414l.896.897a.5.5 0 0 0 .708 0l7-7a.5.5 0 0 0-.708-.708L8.5 10.293l-.543-.543-.707.707z'/></svg>${success}`;
  setTimeout(() => {
    element.innerHTML = `<svg class='mr-2'  width='1.3em' height='1.3em' viewBox='0 0 16 16' class='bi bi-arrow-counterclockwise' fill='currentColor'><path fill-rule='evenodd' d='M8 3a5 5 0 1 1-4.546 2.914.5.5 0 0 0-.908-.417A6 6 0 1 0 8 2v1z'/><path d='M8 4.466V.534a.25.25 0 0 0-.41-.192L5.23 2.308a.25.25 0 0 0 0 .384l2.36 1.966A.25.25 0 0 0 8 4.466z'/></svg>${updatedText}`;
    element.blur();
  }, 1800);
};
const copyDataToClipboard = (element, id, form) => {
  const newClip = form
    ? document.getElementById(id).value
    : document.getElementById(id).textContent;
  navigator.clipboard.writeText(newClip);
  element.blur();
  const buttonContent = element.innerHTML;
  element.innerHTML = `<svg xmlns="http://www.w3.org/2000/svg" width="30" height="30" fill="green" class="bi bi-check2-all" viewBox="0 0 16 16"><path d="M12.354 4.354a.5.5 0 0 0-.708-.708L5 10.293 1.854 7.146a.5.5 0 1 0-.708.708l3.5 3.5a.5.5 0 0 0 .708 0l7-7zm-4.208 7l-.896-.897.707-.707.543.543 6.646-6.647a.5.5 0 0 1 .708.708l-7 7a.5.5 0 0 1-.708 0z"/><path d="M5.354 7.146l.896.897-.707.707-.897-.896a.5.5 0 1 1 .708-.708z"/></svg>`;
  setTimeout(() => {
    element.innerHTML = buttonContent;
  }, 600);
};

const removeOutline = (btn, dismissBtn, form, msg) => {
  const buttonDismiss = document.getElementById(dismissBtn);
  const submitForm = document.getElementById(form);
  btn.disabled = true;
  btn.innerHTML = `<span class='spinner-border mr-1 spinner-border-sm text-dark my-auto' role='status'></span> ${msg}`;
  buttonDismiss.disabled = true;
  submitForm.submit();
};
const imagePopupActivate = () => {
  window.onload = function () {
    var crtdv_img_box = document.createElement("div");
    crtdv_img_box.id = "img_box";
    document.getElementsByTagName("body")[0].appendChild(crtdv_img_box);
    idpopup_img_box = document.getElementById("img_box");
    idpopup_img_box.style.top = 0;
    idpopup_img_box.style.left = 0;
    idpopup_img_box.style.opacity = 0;
    idpopup_img_box.style.width = "100%";
    idpopup_img_box.style.height = "100%";
    idpopup_img_box.style.display = "none";
    idpopup_img_box.style.position = "fixed";
    idpopup_img_box.style.cursor = "pointer";
    idpopup_img_box.style.textAlign = "center";
    idpopup_img_box.style.zIndex = z_index_dv_img_box;
    idpopup_img_box.style.backgroundColor = bg_color_img_box;
  };
};
const img_box = (self) => {
  var namepic_img_box = typeof self === "string" ? self : self.src;
  vopa_img_box = 0;
  var hwin_img_box = window.innerHeight;
  var wwin_img_box = window.innerWidth;
  var himg_img_box, padtop_img_box, idfadein_img_box;
  var img_img_box = new Image();
  img_img_box.src = namepic_img_box;
  img_img_box.onload = function () {
    himg_img_box = img_img_box.height;
    wimg_img_box = img_img_box.width;
    idpopup_img_box.innerHTML = "<img src=" + namepic_img_box + ">";

    if (wimg_img_box > wwin_img_box) {
      idpopup_img_box.getElementsByTagName("img")[0].style.width = "90%";
    } else if (himg_img_box > hwin_img_box) {
      idpopup_img_box.getElementsByTagName("img")[0].style.height = "90%";
      himg_img_box = (hwin_img_box * 90) / 100;
    }

    if (himg_img_box < hwin_img_box) {
      padtop_img_box = hwin_img_box / 2 - himg_img_box / 2;
      idpopup_img_box.style.paddingTop = padtop_img_box + "px";
    } else {
      idpopup_img_box.style.paddingTop = "0px";
    }

    if (allow_hide_scroll_img_box == "yes") {
      document.body.style.overflow = "hidden";
    }
    idpopup_img_box.style.display = "block";
  };

  if (use_fade_inout_img_box == "yes") {
    idfadein_img_box = setInterval(function () {
      if (vopa_img_box <= 1.1) {
        idpopup_img_box.style.opacity = vopa_img_box;
        vopa_img_box += speed_img_box;
      } else {
        idpopup_img_box.style.opacity = 1;
        clearInterval(idfadein_img_box);
      }
    }, 10);
  } else {
    idpopup_img_box.style.opacity = 1;
  }
  window.onkeyup = function (event) {
    if (event.keyCode == 27) {
      if (use_fade_inout_img_box == "yes") {
        var idfadeout_img_box = setInterval(function () {
          if (vopa_img_box >= 0) {
            idpopup_img_box.style.opacity = vopa_img_box;
            vopa_img_box -= speed_img_box;
          } else {
            idpopup_img_box.style.opacity = 0;
            clearInterval(idfadeout_img_box);
            idpopup_img_box.style.display = "none";
            idpopup_img_box.innerHTML = "";
            document.body.style.overflow = "visible";
            vopa_img_box = 0;
          }
        }, 10);
      } else {
        idpopup_img_box.style.opacity = 0;
        idpopup_img_box.style.display = "none";
        idpopup_img_box.innerHTML = "";
        document.body.style.overflow = "visible";
      }
    }
  };

  idpopup_img_box.onclick = function () {
    if (use_fade_inout_img_box == "yes") {
      var idfadeout_img_box = setInterval(function () {
        if (vopa_img_box >= 0) {
          idpopup_img_box.style.opacity = vopa_img_box;
          vopa_img_box -= speed_img_box;
        } else {
          idpopup_img_box.style.opacity = 0;
          clearInterval(idfadeout_img_box);
          idpopup_img_box.style.display = "none";
          idpopup_img_box.innerHTML = "";
          document.body.style.overflow = "visible";
          vopa_img_box = 0;
        }
      }, 10);
    } else {
      idpopup_img_box.style.opacity = 0;
      idpopup_img_box.style.display = "none";
      idpopup_img_box.innerHTML = "";
      document.body.style.overflow = "visible";
    }
  };
};
const updateClipboard = (id) => {
  const newClip = document.getElementById(id).textContent;
  navigator.clipboard.writeText(newClip);
};
const updateAfterClick = async (element, ms, message) => {
  const timeout = Number.parseFloat(ms) / 100;
  let it = 0;
  const update = setInterval(() => {
    it += 1;
    element.innerHTML = message + ` ${it}%`;
    if (it === 99) clearInterval(update);
  }, timeout);
};
const createBuildingsOptions = (
  headquarters,
  barracks,
  stable,
  workshop,
  academy,
  smithy,
  rally_point,
  statue,
  market,
  timber_camp,
  clay_pit,
  iron_mine,
  farm,
  warehouse,
  wall
) => {
  return [
    {
      label: headquarters,
      value: "headquarters",
    },
    {
      label: barracks,
      value: "barracks",
    },
    {
      label: stable,
      value: "stable",
    },
    {
      label: workshop,
      value: "workshop",
    },
    {
      label: academy,
      value: "academy",
    },
    {
      label: smithy,
      value: "smithy",
    },
    {
      label: rally_point,
      value: "rally_point",
    },
    {
      label: statue,
      value: "statue",
    },
    {
      label: market,
      value: "market",
    },
    {
      label: timber_camp,
      value: "timber_camp",
    },
    {
      label: clay_pit,
      value: "clay_pit",
    },
    {
      label: iron_mine,
      value: "iron_mine",
    },
    {
      label: farm,
      value: "farm",
    },
    {
      label: warehouse,
      value: "warehouse",
    },
    {
      label: wall,
      value: "wall",
    },
  ];
};
const changeTextToSent = (element, msg) => {
  element.innerHTML = `${msg}`;
};
const fillAndSubmit = (value) => {
  const form = document.getElementById("create-form");
  const inputField = document.getElementsByName("target_type")[0];
  inputField.value = value;
  form.submit();
};

const initialize_payment_process = (amount) => {
  const paymentButton = document.getElementById("payment-button");
  paymentButton.disabled = true;
  fetch(`/api/stripe-key/`, {
    method: "GET",
    credentials: "same-origin",
    headers: {
      "X-CSRFToken": getCookie("csrftoken"),
      Accept: "application/json",
      "Content-Type": "application/json",
    },
  })
    .then((response) => {
      return response.json();
    })
    .then((data) => {
      const stripe = Stripe(data.publicKey);
      paymentButton.onclick = () => {
        fetch(`/api/stripe-session/${amount}`)
          .then((result) => {
            return result.json();
          })
          .then((data) => {
            return stripe.redirectToCheckout({ sessionId: data.sessionId });
          });
      };
      paymentButton.disabled = false;
    });
};
const resetBackgroundBuildingsColors = (weightPk) => {
  document
    .getElementById("headquarters-" + weightPk)
    .classList.remove("fancy-building-True");
  document
    .getElementById("smithy-" + weightPk)
    .classList.remove("fancy-building-True");
  document
    .getElementById("timber_camp-" + weightPk)
    .classList.remove("fancy-building-True");
  document
    .getElementById("clay_pit-" + weightPk)
    .classList.remove("fancy-building-True");
  document
    .getElementById("farm-" + weightPk)
    .classList.remove("fancy-building-True");
  document
    .getElementById("warehouse-" + weightPk)
    .classList.remove("fancy-building-True");
};
const changeWeightBuildingDirect = async (changingElement, outline_id) => {
  const elementId = changingElement.id;
  const [buildingName, weightPk] = elementId.split("-");
  resetBackgroundBuildingsColors(weightPk);
  changingElement.classList.add("fancy-building-True");
  const nameOfBuilding = document.getElementById("building-name-" + weightPk);
  nameOfBuilding.innerHTML = `<div class="spinner-border spinner-border-sm text-secondary" role="status"></div>`;

  const response = await fetch(
    `/api/change-weight-building/${outline_id}/${weightPk}/`,
    {
      method: "PUT",
      credentials: "same-origin",
      headers: {
        "X-CSRFToken": getCookie("csrftoken"),
        Accept: "application/json",
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ building: buildingName }),
    }
  );
  if (response.status !== 200) {
    nameOfBuilding.innerHTML = `<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-exclamation-square" viewBox="0 0 16 16"><path d="M14 1a1 1 0 0 1 1 1v12a1 1 0 0 1-1 1H2a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1h12zM2 0a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V2a2 2 0 0 0-2-2H2z"/><path d="M7.002 11a1 1 0 1 1 2 0 1 1 0 0 1-2 0zM7.1 4.995a.905.905 0 1 1 1.8 0l-.35 3.507a.552.552 0 0 1-1.1 0L7.1 4.995z"/></svg>`;
    setTimeout(() => {
      nameOfBuilding.innerHTML = "Try again";
    }, 2000);
  } else {
    const data = await response.json();
    nameOfBuilding.innerHTML = `<b>${data.name}</b>`;
  }
};
