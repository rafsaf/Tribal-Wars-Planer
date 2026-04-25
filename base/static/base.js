const takeChildrenSnapshot = (element) =>
  Array.from(element.childNodes).map((node) => node.cloneNode(true));

const restoreChildrenSnapshot = (element, snapshot) => {
  element.replaceChildren(...snapshot.map((node) => node.cloneNode(true)));
};

const setSpinner = (element, textClass = "text-secondary") => {
  const spinner = document.createElement("span");
  spinner.className = `spinner-border spinner-border-sm ${textClass}`;
  spinner.setAttribute("role", "status");
  element.replaceChildren(spinner);
};

const setIconWithText = (
  element,
  iconClass,
  iconColor = "",
  text = "",
  textClass = ""
) => {
  const icon = document.createElement("i");
  icon.className = `bi ${iconClass}`;
  if (iconColor !== "") {
    icon.style.color = iconColor;
  }

  if (textClass !== "") {
    const span = document.createElement("span");
    span.className = textClass;
    span.textContent = ` ${text}`;
    element.replaceChildren(icon, span);
    return;
  }

  element.replaceChildren(icon);
  if (text !== "") {
    element.appendChild(document.createTextNode(` ${text}`));
  }
};

const modal = () => {
  document.addEventListener("DOMContentLoaded", function (event) {
    const formModal = document.getElementById("form-modal");
    if (formModal) {
      formModal.addEventListener("show.bs.modal", function (event) {
        const button = event.relatedTarget;
        if (!button) {
          return;
        }

        const attackNumber = button.dataset.attacknumber || "";
        const start = button.dataset.start || "";
        const intOrZero = (value) => {
          const parsed = parseInt(value || "0", 10);
          return Number.isNaN(parsed) ? 0 : parsed;
        };
        const off = intOrZero(button.dataset.off);
        const leftOff = intOrZero(button.dataset.leftoff);
        const deff = intOrZero(button.dataset.deff);
        const leftDeff = intOrZero(button.dataset.leftdeff);
        const nobleman = intOrZero(button.dataset.nobleman);
        const leftNobleman = intOrZero(button.dataset.leftnobleman);
        const catapult = intOrZero(button.dataset.catapult);
        const leftCatapult = intOrZero(button.dataset.leftcatapult);
        const id = button.dataset.id || "";

        const modalRoot = this;
        const getBySelector = (selector) => modalRoot.querySelector(selector);
        const setInputHintText = (input, text) => {
          if (!input) {
            return;
          }

          const describedBy = input.getAttribute("aria-describedby") || "";
          describedBy.split(" ").forEach((elementId) => {
            if (!elementId.endsWith("_helptext")) {
              return;
            }

            const element = getBySelector(`#${elementId}`);
            if (element) {
              element.textContent = text;
            }
          });
        };

        const currentOther = off - catapult * 8;
        const currentCatapult = catapult;
        const currentDeff = deff;

        const currentOtherLeft = leftOff - leftCatapult * 8;
        const currentCatapultLeft = leftCatapult;
        const currentDeffLeft = leftDeff;

        const currentOtherMax = currentOther + currentOtherLeft;
        const currentCatapultMax = currentCatapult + currentCatapultLeft;
        const currentDeffMax = currentDeff + currentDeffLeft;

        getBySelector(".modal-title").textContent = start;
        getBySelector("#attack-number").textContent = attackNumber;
        getBySelector("#id_weight_id").value = id;
        getBySelector("#id_off").value = off;

        const offNoCatapultInput = getBySelector("#id_off_no_catapult");
        const deffInput = getBySelector("#id_deff");
        const catapultInput = getBySelector("#id_catapult");
        const offInput = getBySelector("#id_off");

        offNoCatapultInput.value = currentOther;
        offNoCatapultInput.max = String(currentOtherMax);
        setInputHintText(offNoCatapultInput, `0-${currentOtherMax}`);
        offNoCatapultInput.onchange = function () {
          const cat = parseInt(catapultInput.value, 10) || 0;
          const offNoCats = parseInt(offNoCatapultInput.value, 10) || 0;
          offInput.value = String(offNoCats + cat * 8);
        };

        deffInput.value = String(currentDeff);
        deffInput.max = String(currentDeffMax);
        setInputHintText(deffInput, `0-${currentDeffMax}`);

        catapultInput.value = String(currentCatapult);
        catapultInput.max = String(currentCatapultMax);
        setInputHintText(catapultInput, `0-${currentCatapultMax}`);
        catapultInput.onchange = function () {
          const cat = parseInt(catapultInput.value, 10) || 0;
          const offNoCats = parseInt(offNoCatapultInput.value, 10) || 0;
          offInput.value = String(offNoCats + cat * 8);
        };

        const noblemanInput = getBySelector("#id_nobleman");
        noblemanInput.value = String(nobleman);
        noblemanInput.max = String(nobleman + leftNobleman);
        setInputHintText(noblemanInput, `0-${nobleman + leftNobleman}`);
      });
    }

    document.querySelectorAll(".popoverData").forEach((element) => {
      new bootstrap.Popover(element);
    });
    document.querySelectorAll(".popoverOption").forEach((element) => {
      new bootstrap.Popover(element, { trigger: "hover" });
    });
  });
};

const isLocalhost = () => {
  if (location.hostname === "localhost" || location.hostname === "127.0.0.1") {
    return true;
  }
  return false;
};

const getLanguage = () => {
  const pathParams = location.pathname.split("/");
  try {
    return pathParams[1];
  } catch (error) {
    console.error(error);
    return "en";
  }
};

const loadDocsPage = (uniqueNumber, elementId, docsPath) => {
  // tries to load cached markdown file from localStorage
  // if not exists, fetch and save it
  // if docsPath for specific document is changed (and it must be refetched),
  // we remove old cached markdown, fetch new and save, alongside with path
  const element = document.getElementById(elementId);
  if (localStorage.getItem(docsPath) !== null && !isLocalhost()) {
    element.innerHTML = marked.parse(localStorage.getItem(docsPath));
  } else {
    fetch(docsPath)
      .then((res) => res.text())
      .then((codeText) => {
        if (localStorage.getItem(String(uniqueNumber)) != null) {
          localStorage.removeItem(localStorage.getItem(String(uniqueNumber)));
        }
        document.getElementById(elementId).innerHTML = marked.parse(codeText);
        if (!isLocalhost()) {
          localStorage.setItem(docsPath, codeText);
          localStorage.setItem(String(uniqueNumber), docsPath);
        }
      });
  }
};

const activateEditTargetMenuScroll = () => {
  window.addEventListener("load", function () {
    const leftScrollElement = document.getElementById("leftscroll");
    if (localStorage.getItem("edit-target-menu-quote-scroll") != null) {
      window.scrollTo(
        0,
        parseInt(localStorage.getItem("edit-target-menu-quote-scroll"), 10)
      );
    }
    if (
      leftScrollElement &&
      localStorage.getItem("edit-target-menu-left-scroll") != null
    ) {
      leftScrollElement.scrollTop = parseInt(
        localStorage.getItem("edit-target-menu-left-scroll"),
        10
      );
    }
    window.addEventListener("scroll", function () {
      localStorage.setItem(
        "edit-target-menu-quote-scroll",
        String(window.scrollY)
      );
    });
    if (leftScrollElement) {
      leftScrollElement.addEventListener("scroll", function () {
        localStorage.setItem(
          "edit-target-menu-left-scroll",
          String(leftScrollElement.scrollTop)
        );
      });
    }
  });
};

const menuToggle = () => {
  const menuToggleButton = document.getElementById("menu-toggle");
  const sidebarWrapper = document.getElementById("sidebar-wrapper");
  if (menuToggleButton && sidebarWrapper) {
    menuToggleButton.addEventListener("click", function (e) {
      e.preventDefault();
      sidebarWrapper.classList.toggle("toggled");
    });
  }

  document.addEventListener("DOMContentLoaded", function () {
    const dateInput = document.getElementById("id_date");
    if (dateInput) {
      dateInput.classList.add("data-picker");
    }
    document.querySelectorAll(".data-picker").forEach((element) => {
      if (element.tagName === "INPUT") {
        element.setAttribute("type", "date");
      }
    });
  });
};

const prettifyTimeDistance = (secs) => {
  secs = Math.round(secs);
  const hours = Math.floor(secs / 3600);
  secs %= 3600;
  const minutes = Math.floor(secs / 60);
  const seconds = secs % 60;

  let hh = hours.toString();
  let mm = minutes.toString();
  let ss = seconds.toString();

  if (mm.length < 2) {
    mm = "0" + mm;
  }
  if (ss.length < 2) {
    ss = "0" + ss;
  }
  return `${hh}:${mm}:${ss}`;
};

const calculateVillagesDistance = (element) => {
  const world_speed = parseFloat(
    String(document.getElementById("speed_world").value)
  );
  const units_speed = parseFloat(
    String(document.getElementById("speed_units").value)
  );
  let distance = parseFloat(element.dataset.distance);

  if (element.clicked) {
    element.innerText = String(distance.toFixed(1));
    element.clicked = false;
    element.style.cursor = "zoom-in";
  } else {
    let secs_ram = (distance / units_speed / world_speed) * 30 * 60;
    let secs_noble = (distance / units_speed / world_speed) * 35 * 60;
    const textWrapper = document.createElement("span");
    textWrapper.className = "text-nowrap";
    textWrapper.appendChild(document.createTextNode(prettifyTimeDistance(secs_ram)));
    textWrapper.appendChild(document.createTextNode(" /"));
    textWrapper.appendChild(document.createElement("br"));
    textWrapper.appendChild(document.createTextNode(` ${prettifyTimeDistance(secs_noble)}`));
    element.replaceChildren(textWrapper);
    element.clicked = true;
    element.style.cursor = "zoom-out";
  }
};

const activateTooltips = () => {
  document.addEventListener("DOMContentLoaded", function (event) {
    document.querySelectorAll(".popoverData").forEach((element) => {
      new bootstrap.Popover(element);
    });
  });
  document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll('[data-bs-toggle="tooltip"]').forEach((element) => {
      new bootstrap.Tooltip(element);
    });
  });
};

const onPlanerLinkClick = (text) => {
  setTimeout(() => {
    const planerLink = document.getElementById("planer-link");
    const spinner = document.createElement("span");
    spinner.className = "spinner-border me-1 spinner-border-sm text-info my-auto";
    spinner.setAttribute("role", "status");
    planerLink.replaceChildren(spinner, document.createTextNode(String(text)));
  }, 800);
};

const handleAllFormsetSelect = () => {
  const applyStatusToInputs = (index, allowRangeOnElse) => {
    const statusElement = document.getElementById(`id_form-${index}-status`);
    const fromInput = document.getElementById(`id_form-${index}-from_number`);
    const toInput = document.getElementById(`id_form-${index}-to_number`);

    if (!statusElement || !fromInput || !toInput) {
      return;
    }

    const val = statusElement.value;
    if (val === "all") {
      fromInput.value = "";
      fromInput.disabled = true;
      toInput.value = "";
      toInput.disabled = true;
      return;
    }

    if (val === "exact") {
      fromInput.value = "";
      fromInput.disabled = true;
      toInput.disabled = false;
      return;
    }

    if (allowRangeOnElse) {
      fromInput.disabled = false;
      toInput.disabled = false;
    }
  };

  document.addEventListener("DOMContentLoaded", function (event) {
    for (let index = 0; index <= 5; index += 1) {
      applyStatusToInputs(index, false);
    }

    document.querySelectorAll(".time-timepicker").forEach((element) => {
      if (element.tagName === "INPUT") {
        element.setAttribute("type", "time");
        element.setAttribute("step", "1");
      }
    });

    for (let index = 0; index <= 5; index += 1) {
      const statusElement = document.getElementById(`id_form-${index}-status`);
      if (!statusElement) {
        continue;
      }
      statusElement.addEventListener("change", function () {
        applyStatusToInputs(index, true);
      });
    }
  });
};

const handleClickButton = (
  element,
  message,
  formId,
  percentId = "",
  disableAllButtons = false
) => {
  const buttons = document.getElementsByTagName("button");
  const links = document.getElementsByTagName("a");
  if (disableAllButtons) {
    for (const i of buttons) {
      i.disabled = true;
    }
    for (const i of links) {
      i.classList.add("disabled-link");
    }
  }
  element.disabled = true;
  const spinner = document.createElement("span");
  spinner.className = "spinner-border me-1 spinner-border-sm text-dark my-auto";
  spinner.setAttribute("role", "status");
  const percentSpan = document.createElement("span");
  if (percentId !== "") {
    percentSpan.id = percentId;
  }
  element.replaceChildren(
    spinner,
    document.createTextNode(` ${String(message)} `),
    percentSpan
  );
  try {
    const form = document.getElementById(formId);
    form.submit();
  } catch (error) {
    console.error(error);
    element.disabled = false;
    if (disableAllButtons) {
      for (const i of buttons) {
        i.disabled = false;
      }
      for (const i of links) {
        i.classList.remove("disabled-link");
      }
    }
  }
};

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie != "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
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
  const actualChildren = takeChildrenSnapshot(newTime);
  setSpinner(newTime);

  const response = await fetch(`/api/target-time-update/`, {
    method: "PUT",
    credentials: "same-origin",
    body: JSON.stringify({ target_id: id1, time_id: id2 }),
    headers: {
      "X-CSRFToken": getCookie("csrftoken"),
      Accept: "application/json",
      "Content-Type": "application/json",
    },
  });
  if (response.status !== 200) {
    setIconWithText(newTime, "bi-exclamation-square");
    const oldClassName = newTime.className;
    newTime.className = "btn btn-lg btn-danger my-1 py-0 px-1 me-1";

    setTimeout(() => {
      newTime.className = oldClassName;
      restoreChildrenSnapshot(newTime, actualChildren);
      newTime.blur();
    }, 2000);
  } else {
    const data = await response.json();
    newTime.className = "btn btn-lg btn-primary my-1 py-0 px-1 me-1";
    restoreChildrenSnapshot(newTime, actualChildren);
    newTime.blur();
    if (data.old !== "none" && data.old !== data.new) {
      const oldTime = document.getElementById(data.old);
      oldTime.className = "btn btn-lg btn-light my-1 py-0 px-1 me-1";
    }
  }
};

const deleteTarget = async (target_id) => {
  const id1 = parseInt(target_id);
  const targetButtonSelector = "target-btn-" + String(target_id);
  const targetRowSelector = "target-row-" + String(target_id);
  const targetButton = document.getElementById(targetButtonSelector);
  const targetRow = document.getElementById(targetRowSelector);

  const targetButtonSnapshot = takeChildrenSnapshot(targetButton);
  targetButton.disabled = true;
  setSpinner(targetButton);

  const response = await fetch(`/api/target-delete/`, {
    method: "DELETE",
    credentials: "same-origin",
    body: JSON.stringify({ target_id: id1 }),
    headers: {
      "X-CSRFToken": getCookie("csrftoken"),
      Accept: "application/json",
      "Content-Type": "application/json",
    },
  });
  if (response.status !== 204) {
    setIconWithText(targetButton, "bi-exclamation-square");
    setTimeout(() => {
      restoreChildrenSnapshot(targetButton, targetButtonSnapshot);
      targetButton.blur();
    }, 2000);
  } else {
    targetRow.style.display = "none";
  }
};

const handlePlanerMenuVisibilityChange = () => {
  if (document.hidden) {
    tabPlanerMenuHasBeenHidden = true;
  } else {
    if (tabPlanerMenuHasBeenHidden) {
      window.location.reload();
    }
  }
};

const changeIsHiddenState = async (outline_id, token) => {
  const overview = document.getElementById(token);
  const actualChildren = takeChildrenSnapshot(overview);
  overview.disabled = true;
  setSpinner(overview);

  const response = await fetch(`/api/overview-hide-state-update/`, {
    method: "PUT",
    credentials: "same-origin",
    body: JSON.stringify({ outline_id: outline_id, token: token }),
    headers: {
      "X-CSRFToken": getCookie("csrftoken"),
      Accept: "application/json",
      "Content-Type": "application/json",
    },
  });
  if (response.status !== 200) {
    setIconWithText(overview, "bi-exclamation-square");
    setTimeout(() => {
      restoreChildrenSnapshot(overview, actualChildren);
      overview.blur();
    }, 2000);
  } else {
    const data = await response.json();
    overview.textContent = String(data.name);
    overview.className = data.class;
    overview.disabled = false;
    overview.blur();
  }
};

const changeBuildingsArray = async (outline_id, list) => {
  const overview = document.getElementById("multi-select-spinner");
  setSpinner(overview);
  const body = { buildings: list, outline_id: outline_id };
  await fetch(`/api/change-buildings-array/`, {
    method: "PUT",
    credentials: "same-origin",
    headers: {
      "X-CSRFToken": getCookie("csrftoken"),
      Accept: "application/json",
      "Content-Type": "application/json",
    },
    body: JSON.stringify(body),
  })
    .then((response) => {
      if (response.status === 200) {
        setIconWithText(overview, "bi-check", "green");
        setTimeout(() => {
          overview.replaceChildren();
        }, 400);
      } else {
        setIconWithText(
          overview,
          "bi-exclamation-square",
          "red",
          "(Error in connection!)",
          "md-error"
        );
        setTimeout(() => {
          overview.replaceChildren();
        }, 2000);
      }
    })
    .catch(() => {
      setIconWithText(
        overview,
        "bi-exclamation-square",
        "red",
        "(Error in connection!)",
        "md-error"
      );
      setTimeout(() => {
        overview.replaceChildren();
      }, 2000);
    });
};
const codemirrorValidation = (json_errors, selectorClass) => {
  document.addEventListener("DOMContentLoaded", function (event) {
    const codemirror = document.querySelectorAll(selectorClass);
    codemirror.forEach((element) => {
      element.classList.add("CodeMirror-Invalid");
    });
    if (codemirror.length === 0 || !codemirror[0].CodeMirror) {
      return;
    }
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
  updatedText,
  errorMessage
) => {
  const text = document.getElementById(selector);
  const currentSnapshot = takeChildrenSnapshot(element);
  setTimeout(() => {
    element.blur();
  }, 100);
  try {
    const newClip = text.textContent;
    navigator.clipboard.writeText(newClip);
    setIconWithText(element, "bi-check2-circle", "green", String(success));
    setTimeout(() => {
      setIconWithText(element, "bi-arrow-counterclockwise", "", String(updatedText));
    }, 1800);
  } catch (error) {
    console.error(error);
    setIconWithText(element, "bi-x-circle", "red", String(errorMessage), "text-danger");
    setTimeout(() => {
      restoreChildrenSnapshot(element, currentSnapshot);
    }, 5000);
  }
};
const copyDataToClipboard = (element, id, form) => {
  const newClip = form
    ? document.getElementById(id).value
    : document.getElementById(id).textContent;
  navigator.clipboard.writeText(newClip);
  element.blur();
  const buttonSnapshot = takeChildrenSnapshot(element);
  setIconWithText(element, "bi-check2-all", "green");
  setTimeout(() => {
    restoreChildrenSnapshot(element, buttonSnapshot);
  }, 600);
};

const removeOutline = (btn, dismissBtn, form, msg) => {
  const buttonDismiss = document.getElementById(dismissBtn);
  const submitForm = document.getElementById(form);
  btn.disabled = true;
  const spinner = document.createElement("span");
  spinner.className = "spinner-border me-1 spinner-border-sm text-dark my-auto";
  spinner.setAttribute("role", "status");
  btn.replaceChildren(spinner, document.createTextNode(` ${String(msg)}`));
  buttonDismiss.disabled = true;
  submitForm.submit();
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
    element.textContent = String(message) + ` ${it}%`;
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
  wall,
  watchtower
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
    {
      label: watchtower,
      value: "watchtower",
    },
  ];
};
const changeTextToSent = (element, msg) => {
  element.textContent = String(msg);
};
const fillAndSubmit = (value) => {
  const form = document.getElementById("create-form");
  const inputField = document.getElementsByName("target_type")[0];
  inputField.value = value;
  form.submit();
};

const initializePaymentProcess = async (amount, currency) => {
  const paymentButton = document.getElementById("payment-button");
  paymentButton.disabled = true;
  const stripeKey = await (await fetch(`/api/stripe-key/`)).json();
  const stripe = Stripe(stripeKey.publicKey);

  paymentButton.onclick = () => {
    const originalSnapshot = takeChildrenSnapshot(paymentButton);
    const spinner = document.createElement("span");
    spinner.className = "spinner-border me-1 spinner-border-sm text-info my-auto";
    spinner.setAttribute("role", "status");
    paymentButton.replaceChildren(spinner);
    fetch(`/api/stripe-session/`, {
      method: "POST",
      credentials: "same-origin",
      headers: {
        "X-CSRFToken": getCookie("csrftoken"),
        Accept: "application/json",
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        amount: parseInt(amount),
        currency: currency,
      }),
    })
      .then((res) => {
        if (res.status === 200) {
          return res.json();
        } else if (res.status === 400) {
          restoreChildrenSnapshot(paymentButton, originalSnapshot);
          res.json().then((res) => {
            console.error(res);
            alert(`Something went wrong. Message: ${res.error}`);
            throw res.error;
          });
        } else {
          restoreChildrenSnapshot(paymentButton, originalSnapshot);
          console.error(res);
          alert(`Something went wrong. unknown error`);
          throw "unknown error";
        }
      })
      .then((data) => {
        console.log(data);
        window.location.href = data.url;
      });
  };
  paymentButton.disabled = false;
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
  setSpinner(nameOfBuilding);

  const response = await fetch(`/api/change-weight-building/`, {
    method: "PUT",
    credentials: "same-origin",
    headers: {
      "X-CSRFToken": getCookie("csrftoken"),
      Accept: "application/json",
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      building: buildingName,
      outline_id: outline_id,
      weight_id: weightPk,
    }),
  });
  if (response.status !== 200) {
    setIconWithText(nameOfBuilding, "bi-exclamation-square");
    setTimeout(() => {
      nameOfBuilding.textContent = "Try again";
    }, 2000);
  } else {
    const data = await response.json();
    const bold = document.createElement("b");
    bold.textContent = String(data.name);
    nameOfBuilding.replaceChildren(bold);
  }
};

const activateTimezoneInfo = () => {
  let tz = Intl.DateTimeFormat().resolvedOptions().timeZone;
  if (!tz) {
    tz = "UTC";
  }
  document.cookie = "mytz=" + tz + ";path=/";
};

const setFooterYears = () => {
  const footerYearEl = document.getElementById("footer-years");
  if (!footerYearEl) {
    return;
  }
  footerYearEl.innerText = `2020-${new Date().getFullYear()} `;
};

const setupDataTable = (elementId) => {
  const data = {};
  if (getLanguage() === "pl") {
    data["language"] = {
      url: "https://cdn.datatables.net/plug-ins/2.3.7/i18n/pl.json",
    };
  }
  if (getLanguage() === "hu") {
    data["language"] = {
      url: "https://cdn.datatables.net/plug-ins/2.3.7/i18n/hu.json",
    };
  }
  if (getLanguage() === "cs") {
    data["language"] = {
      url: "https://cdn.datatables.net/plug-ins/2.3.7/i18n/cs.json",
    };
  }
  new DataTable(elementId, data);
};
