var bg_color_img_box="rgba(0,0,0,0.9)",allow_hide_scroll_img_box="yes",use_fade_inout_img_box="yes",speed_img_box=.08,z_index_dv_img_box=999,vopa_img_box,idpopup_img_box;const DOCS_RE=/\!\[\]\([a-zA-Z0-9.\/_-]*\)/g,modal=()=>{document.addEventListener("DOMContentLoaded",function(e){$("#form-modal").on("show.bs.modal",function(o){var t=$(o.relatedTarget),i=t.data("attacknumber"),r=t.data("start"),a=parseInt(t.data("off")),n=parseInt(t.data("leftoff")),l=parseInt(t.data("nobleman")),s=parseInt(t.data("leftnobleman")),m=parseInt(t.data("catapult")),c=parseInt(t.data("leftcatapult")),u=t.data("id"),d=$(this),f=a-m*8,p=m,b=n-c*8,y=c,v=f+b,h=p+y;d.find(".modal-title").text(r),d.find("#attack-number").text(i),d.find("#id_weight_id").val(u),d.find("#id_off").val(a),d.find("#id_off_no_catapult").val(f),d.find("#id_off_no_catapult").attr("max",v),d.find("#hint_id_off_no_catapult").text(`0-${v}`),d.find("#id_off_no_catapult").change(function(){var _=parseInt(d.find("#id_catapult").val()),g=parseInt(d.find("#id_off_no_catapult").val());d.find("#id_off").val(g+_*8)}),d.find("#id_catapult").val(p),d.find("#id_catapult").attr("max",h),d.find("#hint_id_catapult").text(`0-${h}`),d.find("#id_catapult").change(function(){var _=parseInt(d.find("#id_catapult").val()),g=parseInt(d.find("#id_off_no_catapult").val());d.find("#id_off").val(g+_*8)}),d.find("#id_nobleman").val(l),d.find("#id_nobleman").attr("max",l+s),d.find("#hint_id_nobleman").text(`0-${l+s}`)}),$(".popoverData").popover(),$(".popoverOption").popover({trigger:"hover"})})},isLocalhost=()=>location.hostname==="localhost"||location.hostname==="127.0.0.1",getLanguage=()=>{const e=location.pathname.split("/");try{return e[1]}catch(o){return console.error(o),"en"}},loadDocsPage=(e,o,t,i=!1)=>{const r=document.getElementById(o),a=`/static/markdown/${getLanguage()}`;localStorage.getItem(t)!==null&&!isLocalhost()?r.innerHTML=marked.parse(localStorage.getItem(t)):fetch(t).then(n=>n.text()).then(n=>{const l=[...n.matchAll(DOCS_RE)];for(const s of l){const m=s[0];let c=m.slice(4,-1);c=`${a}/${c}`;const u=`<img id="large" class="img-thumbnail" style="height: 250px;" onclick="img_box(this)" src="${c}">`;n=n.replaceAll(m,u)}return n}).then(n=>{localStorage.getItem(String(e))!=null&&localStorage.removeItem(localStorage.getItem(String(e))),document.getElementById(o).innerHTML=marked.parse(n),isLocalhost()||(localStorage.setItem(t,n),localStorage.setItem(String(e),t))}).then(()=>{const n=new URLSearchParams(location.search);location.hash!==""?setTimeout(()=>{localStorage.setItem(`${e}-scroll-id`,String(document.getElementById(location.hash.slice(1)).offsetTop)),location.search=""},300):i&&wholePageContentScroll(`${e}-scroll-id`)})},wholePageContentScroll=e=>{localStorage.getItem(e)!=null&&$(window).scrollTop(localStorage.getItem(e)),$(window).on("scroll",function(){localStorage.setItem(e,$(window).scrollTop())})},scroll_content_outline=()=>{$(window).on("load",function(){localStorage.getItem("my_app_name_here-quote-scroll")!=null&&$(window).scrollTop(localStorage.getItem("my_app_name_here-quote-scroll")),localStorage.getItem("my_app_name_here-left-scroll")!=null&&$("#leftscroll").scrollTop(localStorage.getItem("my_app_name_here-left-scroll")),$(window).on("scroll",function(){localStorage.setItem("my_app_name_here-quote-scroll",$(window).scrollTop())}),$("#leftscroll").on("scroll",function(){var e=$("#leftscroll").scrollTop();localStorage.setItem("my_app_name_here-left-scroll",e)})})},menu_toggle=()=>{$("#menu-toggle").click(function(e){e.preventDefault(),$("#sidebar-wrapper").toggleClass("toggled")}),$(document).ready(function(){$("#id_date").addClass("data-picker"),$(".data-picker").datepicker({format:"yyyy-mm-dd",weekStart:1,language:getLanguage(),todayHighlight:!0})})},prettifyTimeDistance=e=>{e=Math.round(e);const o=Math.floor(e/3600);e%=3600;const t=Math.floor(e/60),i=e%60;let r=o.toString(),a=t.toString(),n=i.toString();return a.length<2&&(a="0"+a),n.length<2&&(n="0"+n),`${r}:${a}:${n}`},calculate_distance=e=>{const o=parseFloat(String(document.getElementById("speed_world").value).replace(",",".")),t=parseFloat(String(document.getElementById("speed_units").value).replace(",","."));if(e.clicked)e.innerHTML=String(e.distance).replace(".",","),e.clicked=!1,e.style.cursor="zoom-in";else{e.distance=parseFloat(e.innerHTML.replace(",","."));let i=e.distance/t/o*30*60,r=e.distance/t/o*35*60;e.innerHTML=`<span class='text-nowrap'>${prettifyTimeDistance(i)} /<br/> ${prettifyTimeDistance(r)}</span>`,e.clicked=!0,e.style.cursor="zoom-out"}},activateTooltips=()=>{document.addEventListener("DOMContentLoaded",function(e){$(".popoverData").popover()}),$(function(){$('[data-toggle="tooltip"]').tooltip()})},onPlanerLinkClick=e=>{setTimeout(()=>{const o=document.getElementById("planer-link");o.innerHTML=`<span class='spinner-border mr-1 spinner-border-sm text-info my-auto' role='status'></span>${e}`},800)},handleAllFormsetSelect=()=>{document.addEventListener("DOMContentLoaded",function(e){val=$("#id_form-0-status").val(),val==="all"?($("#id_form-0-from_number").val(""),$("#id_form-0-from_number").prop("disabled",!0),$("#id_form-0-to_number").val(""),$("#id_form-0-to_number").prop("disabled",!0)):val==="exact"&&($("#id_form-0-from_number").val(""),$("#id_form-0-from_number").prop("disabled",!0),$("#id_form-0-to_number").prop("disabled",!1)),val=$("#id_form-1-status").val(),val==="all"?($("#id_form-1-from_number").val(""),$("#id_form-1-from_number").prop("disabled",!0),$("#id_form-1-to_number").val(""),$("#id_form-1-to_number").prop("disabled",!0)):val==="exact"&&($("#id_form-1-from_number").val(""),$("#id_form-1-from_number").prop("disabled",!0),$("#id_form-1-to_number").prop("disabled",!1)),val=$("#id_form-2-status").val(),val==="all"?($("#id_form-2-from_number").val(""),$("#id_form-2-from_number").prop("disabled",!0),$("#id_form-2-to_number").val(""),$("#id_form-2-to_number").prop("disabled",!0)):val==="exact"&&($("#id_form-2-from_number").val(""),$("#id_form-2-from_number").prop("disabled",!0),$("#id_form-2-to_number").prop("disabled",!1)),val=$("#id_form-3-status").val(),val==="all"?($("#id_form-3-from_number").val(""),$("#id_form-3-from_number").prop("disabled",!0),$("#id_form-3-to_number").val(""),$("#id_form-3-to_number").prop("disabled",!0)):val==="exact"&&($("#id_form-3-from_number").val(""),$("#id_form-3-from_number").prop("disabled",!0),$("#id_form-3-to_number").prop("disabled",!1)),val=$("#id_form-4-status").val(),val==="all"?($("#id_form-4-from_number").val(""),$("#id_form-4-from_number").prop("disabled",!0),$("#id_form-4-to_number").val(""),$("#id_form-4-to_number").prop("disabled",!0)):val==="exact"&&($("#id_form-4-from_number").val(""),$("#id_form-4-from_number").prop("disabled",!0),$("#id_form-4-to_number").prop("disabled",!1)),val=$("#id_form-5-status").val(),val==="all"?($("#id_form-5-from_number").val(""),$("#id_form-5-from_number").prop("disabled",!0),$("#id_form-5-to_number").val(""),$("#id_form-5-to_number").prop("disabled",!0)):val==="exact"&&($("#id_form-5-from_number").val(""),$("#id_form-5-from_number").prop("disabled",!0),$("#id_form-5-to_number").prop("disabled",!1))}),document.addEventListener("DOMContentLoaded",function(e){$(".time-timepicker").each(function(){$(this).timepicker({minuteStep:1,secondStep:1,showSeconds:!0,showMeridian:!1,defaultTime:!1,icons:{up:"fa fa-angle-up",down:"fa fa-angle-down"}})}),$("#id_form-0-status").change(function(){val=$("#id_form-0-status").val(),val==="all"?($("#id_form-0-from_number").val(""),$("#id_form-0-from_number").prop("disabled",!0),$("#id_form-0-to_number").val(""),$("#id_form-0-to_number").prop("disabled",!0)):val==="exact"?($("#id_form-0-from_number").val(""),$("#id_form-0-from_number").prop("disabled",!0),$("#id_form-0-to_number").prop("disabled",!1)):($("#id_form-0-from_number").prop("disabled",!1),$("#id_form-0-to_number").prop("disabled",!1))}),$("#id_form-1-status").change(function(){val=$("#id_form-1-status").val(),val==="all"?($("#id_form-1-from_number").val(""),$("#id_form-1-from_number").prop("disabled",!0),$("#id_form-1-to_number").val(""),$("#id_form-1-to_number").prop("disabled",!0)):val==="exact"?($("#id_form-1-from_number").val(""),$("#id_form-1-from_number").prop("disabled",!0),$("#id_form-1-to_number").prop("disabled",!1)):($("#id_form-1-from_number").prop("disabled",!1),$("#id_form-1-to_number").prop("disabled",!1))}),$("#id_form-2-status").change(function(){val=$("#id_form-2-status").val(),val==="all"?($("#id_form-2-from_number").val(""),$("#id_form-2-from_number").prop("disabled",!0),$("#id_form-2-to_number").val(""),$("#id_form-2-to_number").prop("disabled",!0)):val==="exact"?($("#id_form-2-from_number").val(""),$("#id_form-2-from_number").prop("disabled",!0),$("#id_form-2-to_number").prop("disabled",!1)):($("#id_form-2-from_number").prop("disabled",!1),$("#id_form-2-to_number").prop("disabled",!1))}),$("#id_form-3-status").change(function(){val=$("#id_form-3-status").val(),val==="all"?($("#id_form-3-from_number").val(""),$("#id_form-3-from_number").prop("disabled",!0),$("#id_form-3-to_number").val(""),$("#id_form-3-to_number").prop("disabled",!0)):val==="exact"?($("#id_form-3-from_number").val(""),$("#id_form-3-from_number").prop("disabled",!0),$("#id_form-3-to_number").prop("disabled",!1)):($("#id_form-3-from_number").prop("disabled",!1),$("#id_form-3-to_number").prop("disabled",!1))}),$("#id_form-4-status").change(function(){val=$("#id_form-4-status").val(),val==="all"?($("#id_form-4-from_number").val(""),$("#id_form-4-from_number").prop("disabled",!0),$("#id_form-4-to_number").val(""),$("#id_form-4-to_number").prop("disabled",!0)):val==="exact"?($("#id_form-4-from_number").val(""),$("#id_form-4-from_number").prop("disabled",!0),$("#id_form-4-to_number").prop("disabled",!1)):($("#id_form-4-from_number").prop("disabled",!1),$("#id_form-4-to_number").prop("disabled",!1))}),$("#id_form-5-status").change(function(){val=$("#id_form-5-status").val(),val==="all"?($("#id_form-5-from_number").val(""),$("#id_form-5-from_number").prop("disabled",!0),$("#id_form-5-to_number").val(""),$("#id_form-5-to_number").prop("disabled",!0)):val==="exact"?($("#id_form-5-from_number").val(""),$("#id_form-5-from_number").prop("disabled",!0),$("#id_form-5-to_number").prop("disabled",!1)):($("#id_form-5-from_number").prop("disabled",!1),$("#id_form-5-to_number").prop("disabled",!1))})})},handleClickButton=(e,o,t,i="",r=!1)=>{const a=document.getElementsByTagName("button"),n=document.getElementsByTagName("a");if(r){for(const l of a)l.disabled=!0;for(const l of n)l.classList.add("disabled-link")}e.disabled=!0,e.innerHTML=`<span class='spinner-border mr-1 spinner-border-sm text-dark my-auto' role='status'></span> ${o} <span id=${i}></span>`;try{document.getElementById(t).submit()}catch(l){if(console.error(l),e.disabled=!1,r){for(const s of a)s.disabled=!1;for(const s of n)s.classList.remove("disabled-link")}}};function getCookie(e){var o=null;if(document.cookie&&document.cookie!="")for(var t=document.cookie.split(";"),i=0;i<t.length;i++){var r=jQuery.trim(t[i]);if(r.substring(0,e.length+1)==e+"="){o=decodeURIComponent(r.substring(e.length+1));break}}return o}const changeTargetTime=async(e,o)=>{const t=parseInt(e),i=parseInt(o),r=String(e)+"-time-"+String(o),a=document.getElementById(r),n=a.innerHTML;a.innerHTML='<div class="spinner-border spinner-border-sm text-secondary" role="status"></div>';const l=await fetch("/api/target-time-update/",{method:"PUT",credentials:"same-origin",body:JSON.stringify({target_id:t,time_id:i}),headers:{"X-CSRFToken":getCookie("csrftoken"),Accept:"application/json","Content-Type":"application/json"}});if(l.status!==200){a.innerHTML='<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-exclamation-square" viewBox="0 0 16 16"><path d="M14 1a1 1 0 0 1 1 1v12a1 1 0 0 1-1 1H2a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1h12zM2 0a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V2a2 2 0 0 0-2-2H2z"/><path d="M7.002 11a1 1 0 1 1 2 0 1 1 0 0 1-2 0zM7.1 4.995a.905.905 0 1 1 1.8 0l-.35 3.507a.552.552 0 0 1-1.1 0L7.1 4.995z"/></svg>';const s=a.className;a.className="btn btn-lg btn-danger my-1 py-0 px-1 mr-1",setTimeout(()=>{a.className=s,a.innerHTML=n,a.blur()},2e3)}else{const s=await l.json();if(a.className="btn btn-lg btn-primary my-1 py-0 px-1 mr-1",a.innerHTML=n,a.blur(),s.old!=="none"&&s.old!==s.new){const m=document.getElementById(s.old);m.className="btn btn-lg btn-light my-1 py-0 px-1 mr-1"}}},deleteTarget=async e=>{const o=parseInt(e),t="target-btn-"+String(e),i="target-row-"+String(e),r=document.getElementById(t),a=document.getElementById(i),n=r.innerHTML;r.disabled=!0,r.innerHTML='<div class="spinner-border spinner-border-sm text-secondary" role="status"></div>',(await fetch("/api/target-delete/",{method:"DELETE",credentials:"same-origin",body:JSON.stringify({target_id:o}),headers:{"X-CSRFToken":getCookie("csrftoken"),Accept:"application/json","Content-Type":"application/json"}})).status!==204?(r.innerHTML='<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-exclamation-square" viewBox="0 0 16 16"><path d="M14 1a1 1 0 0 1 1 1v12a1 1 0 0 1-1 1H2a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1h12zM2 0a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V2a2 2 0 0 0-2-2H2z"/><path d="M7.002 11a1 1 0 1 1 2 0 1 1 0 0 1-2 0zM7.1 4.995a.905.905 0 1 1 1.8 0l-.35 3.507a.552.552 0 0 1-1.1 0L7.1 4.995z"/></svg>',setTimeout(()=>{r.innerHTML=n,r.blur()},2e3)):a.style.display="none"},handlePlanerMenuVisibilityChange=()=>{document.hidden?tabPlanerMenuHasBeenHidden=!0:tabPlanerMenuHasBeenHidden&&window.location.reload()},changeIsHiddenState=async(e,o)=>{const t=document.getElementById(o),i=t.innerHTML;t.disabled=!0,t.innerHTML='<div class="spinner-border spinner-border-sm text-secondary" role="status"></div>';const r=await fetch("/api/overview-hide-state-update/",{method:"PUT",credentials:"same-origin",body:JSON.stringify({outline_id:e,token:o}),headers:{"X-CSRFToken":getCookie("csrftoken"),Accept:"application/json","Content-Type":"application/json"}});if(r.status!==200)t.innerHTML='<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-exclamation-square" viewBox="0 0 16 16"><path d="M14 1a1 1 0 0 1 1 1v12a1 1 0 0 1-1 1H2a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1h12zM2 0a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V2a2 2 0 0 0-2-2H2z"/><path d="M7.002 11a1 1 0 1 1 2 0 1 1 0 0 1-2 0zM7.1 4.995a.905.905 0 1 1 1.8 0l-.35 3.507a.552.552 0 0 1-1.1 0L7.1 4.995z"/></svg>',setTimeout(()=>{t.innerHTML=i,t.blur()},2e3);else{const a=await r.json();t.innerHTML=a.name,t.className=a.class,t.disabled=!1,t.blur()}},changeBuildingsArray=async(e,o)=>{const t=document.getElementById("multi-select-spinner");t.innerHTML='<div class="spinner-border spinner-border-sm text-secondary" role="status"></div>';const i={buildings:o,outline_id:e};await fetch("/api/change-buildings-array/",{method:"PUT",credentials:"same-origin",headers:{"X-CSRFToken":getCookie("csrftoken"),Accept:"application/json","Content-Type":"application/json"},body:JSON.stringify(i)}).then(r=>{r.status===200?(t.innerHTML='<svg xmlns="http://www.w3.org/2000/svg" width="25" height="25" fill="green" class="bi bi-check" viewBox="0 0 16 16"><path d="M10.97 4.97a.75.75 0 0 1 1.07 1.05l-3.99 4.99a.75.75 0 0 1-1.08.02L4.324 8.384a.75.75 0 1 1 1.06-1.06l2.094 2.093 3.473-4.425a.267.267 0 0 1 .02-.022z"/></svg>',setTimeout(()=>{t.innerHTML=""},400)):(t.innerHTML='<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="red" class="bi bi-exclamation-square" viewBox="0 0 16 16"><path d="M14 1a1 1 0 0 1 1 1v12a1 1 0 0 1-1 1H2a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1h12zM2 0a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V2a2 2 0 0 0-2-2H2z"/><path d="M7.002 11a1 1 0 1 1 2 0 1 1 0 0 1-2 0zM7.1 4.995a.905.905 0 1 1 1.8 0l-.35 3.507a.552.552 0 0 1-1.1 0L7.1 4.995z"/></svg> <span class="md-error">(Error in connection!)</span>',setTimeout(()=>{t.innerHTML=""},2e3))}).catch(()=>{t.innerHTML='<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="red" class="bi bi-exclamation-square" viewBox="0 0 16 16"><path d="M14 1a1 1 0 0 1 1 1v12a1 1 0 0 1-1 1H2a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1h12zM2 0a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V2a2 2 0 0 0-2-2H2z"/><path d="M7.002 11a1 1 0 1 1 2 0 1 1 0 0 1-2 0zM7.1 4.995a.905.905 0 1 1 1.8 0l-.35 3.507a.552.552 0 0 1-1.1 0L7.1 4.995z"/></svg> <span class="md-error">(Error in connection!)</span>',setTimeout(()=>{t.innerHTML=""},2e3)})},resetUserMessages=async()=>{const e=document.getElementById("reset-svg"),o=document.getElementById("reset-span");await fetch("/api/reset-user-messages/",{method:"PUT",credentials:"same-origin",headers:{"X-CSRFToken":getCookie("csrftoken"),Accept:"application/json","Content-Type":"application/json"}}).then(t=>{t.status===200&&(e.style.fill="rgba(0,0,0,.5)",o.style.color="rgba(0,0,0,.5)",o.innerHTML="0")})},codemirrorValidation=(e,o)=>{document.addEventListener("DOMContentLoaded",function(t){$(o).addClass("CodeMirror-Invalid");const r=$(o)[0].CodeMirror,a=JSON.parse(e);Object.entries(a).forEach(([n,l],s)=>{s===0&&r.scrollIntoView(parseInt(l.message)),r.addLineClass(parseInt(l.message),"wrap","line-error")})})},handleButtonClipboardUpdate=(e,o,t,i,r)=>{const a=document.getElementById(o),n=e.innerHTML;setTimeout(()=>{e.blur()},100);try{const l=a.textContent;navigator.clipboard.writeText(l),e.innerHTML=`<i class="bi bi-check2-circle" style="color: green"></i> ${t}`,setTimeout(()=>{e.innerHTML=`<i class="bi bi-arrow-counterclockwise"></i> ${i}`},1800)}catch(l){e.innerHTML=`<span style="color: red"><i class="bi bi-x-circle"></i> ${r} (${l})</span>`,setTimeout(()=>{e.innerHTML=n},5e3)}},copyDataToClipboard=(e,o,t)=>{const i=t?document.getElementById(o).value:document.getElementById(o).textContent;navigator.clipboard.writeText(i),e.blur();const r=e.innerHTML;e.innerHTML='<svg xmlns="http://www.w3.org/2000/svg" width="30" height="30" fill="green" class="bi bi-check2-all" viewBox="0 0 16 16"><path d="M12.354 4.354a.5.5 0 0 0-.708-.708L5 10.293 1.854 7.146a.5.5 0 1 0-.708.708l3.5 3.5a.5.5 0 0 0 .708 0l7-7zm-4.208 7l-.896-.897.707-.707.543.543 6.646-6.647a.5.5 0 0 1 .708.708l-7 7a.5.5 0 0 1-.708 0z"/><path d="M5.354 7.146l.896.897-.707.707-.897-.896a.5.5 0 1 1 .708-.708z"/></svg>',setTimeout(()=>{e.innerHTML=r},600)},removeOutline=(e,o,t,i)=>{const r=document.getElementById(o),a=document.getElementById(t);e.disabled=!0,e.innerHTML=`<span class='spinner-border mr-1 spinner-border-sm text-dark my-auto' role='status'></span> ${i}`,r.disabled=!0,a.submit()},imagePopupActivate=()=>{window.onload=function(){var e=document.createElement("div");e.id="img_box",document.getElementsByTagName("body")[0].appendChild(e),idpopup_img_box=document.getElementById("img_box"),idpopup_img_box.style.top=0,idpopup_img_box.style.left=0,idpopup_img_box.style.opacity=0,idpopup_img_box.style.width="100%",idpopup_img_box.style.height="100%",idpopup_img_box.style.display="none",idpopup_img_box.style.position="fixed",idpopup_img_box.style.cursor="pointer",idpopup_img_box.style.textAlign="center",idpopup_img_box.style.zIndex=z_index_dv_img_box,idpopup_img_box.style.backgroundColor=bg_color_img_box}},img_box=e=>{var o=typeof e=="string"?e:e.src;vopa_img_box=0;var t=window.innerHeight,i=window.innerWidth,r,a,n,l=new Image;l.src=o,l.onload=function(){r=l.height,wimg_img_box=l.width,idpopup_img_box.innerHTML="<img src="+o+">",wimg_img_box>i?idpopup_img_box.getElementsByTagName("img")[0].style.width="90%":r>t&&(idpopup_img_box.getElementsByTagName("img")[0].style.height="90%",r=t*90/100),r<t?(a=t/2-r/2,idpopup_img_box.style.paddingTop=a+"px"):idpopup_img_box.style.paddingTop="0px",allow_hide_scroll_img_box=="yes"&&(document.body.style.overflow="hidden"),idpopup_img_box.style.display="block"},use_fade_inout_img_box=="yes"?n=setInterval(function(){vopa_img_box<=1.1?(idpopup_img_box.style.opacity=vopa_img_box,vopa_img_box+=speed_img_box):(idpopup_img_box.style.opacity=1,clearInterval(n))},10):idpopup_img_box.style.opacity=1,window.onkeyup=function(s){if(s.keyCode==27)if(use_fade_inout_img_box=="yes")var m=setInterval(function(){vopa_img_box>=0?(idpopup_img_box.style.opacity=vopa_img_box,vopa_img_box-=speed_img_box):(idpopup_img_box.style.opacity=0,clearInterval(m),idpopup_img_box.style.display="none",idpopup_img_box.innerHTML="",document.body.style.overflow="visible",vopa_img_box=0)},10);else idpopup_img_box.style.opacity=0,idpopup_img_box.style.display="none",idpopup_img_box.innerHTML="",document.body.style.overflow="visible"},idpopup_img_box.onclick=function(){if(use_fade_inout_img_box=="yes")var s=setInterval(function(){vopa_img_box>=0?(idpopup_img_box.style.opacity=vopa_img_box,vopa_img_box-=speed_img_box):(idpopup_img_box.style.opacity=0,clearInterval(s),idpopup_img_box.style.display="none",idpopup_img_box.innerHTML="",document.body.style.overflow="visible",vopa_img_box=0)},10);else idpopup_img_box.style.opacity=0,idpopup_img_box.style.display="none",idpopup_img_box.innerHTML="",document.body.style.overflow="visible"}},updateClipboard=e=>{const o=document.getElementById(e).textContent;navigator.clipboard.writeText(o)},updateAfterClick=async(e,o,t)=>{const i=Number.parseFloat(o)/100;let r=0;const a=setInterval(()=>{r+=1,e.innerHTML=t+` ${r}%`,r===99&&clearInterval(a)},i)},createBuildingsOptions=(e,o,t,i,r,a,n,l,s,m,c,u,d,f,p,b)=>[{label:e,value:"headquarters"},{label:o,value:"barracks"},{label:t,value:"stable"},{label:i,value:"workshop"},{label:r,value:"academy"},{label:a,value:"smithy"},{label:n,value:"rally_point"},{label:l,value:"statue"},{label:s,value:"market"},{label:m,value:"timber_camp"},{label:c,value:"clay_pit"},{label:u,value:"iron_mine"},{label:d,value:"farm"},{label:f,value:"warehouse"},{label:p,value:"wall"},{label:b,value:"watchtower"}],changeTextToSent=(e,o)=>{e.innerHTML=`${o}`},fillAndSubmit=e=>{const o=document.getElementById("create-form"),t=document.getElementsByName("target_type")[0];t.value=e,o.submit()},initializePaymentProcess=async e=>{const o=document.getElementById("payment-button");o.disabled=!0;const t=await(await fetch("/api/stripe-key/")).json(),i=Stripe(t.publicKey);o.onclick=()=>{const r=o.innerHTML;o.innerHTML="<span class='spinner-border mr-1 spinner-border-sm text-info my-auto' role='status'></span>",fetch("/api/stripe-session/",{method:"POST",credentials:"same-origin",headers:{"X-CSRFToken":getCookie("csrftoken"),Accept:"application/json","Content-Type":"application/json"},body:JSON.stringify({amount:parseInt(e)})}).then(a=>{if(a.status===200)return a.json();if(a.status===400)o.innerHTML=r,a.json().then(n=>{throw console.error(n),alert(`Something went wrong. Message: ${n.error}`),n.error});else throw o.innerHTML=r,console.error(a),alert("Something went wrong. unknown error"),"unknown error"}).then(a=>(console.log(a),i.redirectToCheckout({sessionId:a.sessionId})))},o.disabled=!1},resetBackgroundBuildingsColors=e=>{document.getElementById("headquarters-"+e).classList.remove("fancy-building-True"),document.getElementById("smithy-"+e).classList.remove("fancy-building-True"),document.getElementById("timber_camp-"+e).classList.remove("fancy-building-True"),document.getElementById("clay_pit-"+e).classList.remove("fancy-building-True"),document.getElementById("farm-"+e).classList.remove("fancy-building-True"),document.getElementById("warehouse-"+e).classList.remove("fancy-building-True")},changeWeightBuildingDirect=async(e,o)=>{const t=e.id,[i,r]=t.split("-");resetBackgroundBuildingsColors(r),e.classList.add("fancy-building-True");const a=document.getElementById("building-name-"+r);a.innerHTML='<div class="spinner-border spinner-border-sm text-secondary" role="status"></div>';const n=await fetch("/api/change-weight-building/",{method:"PUT",credentials:"same-origin",headers:{"X-CSRFToken":getCookie("csrftoken"),Accept:"application/json","Content-Type":"application/json"},body:JSON.stringify({building:i,outline_id:o,weight_id:r})});if(n.status!==200)a.innerHTML='<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-exclamation-square" viewBox="0 0 16 16"><path d="M14 1a1 1 0 0 1 1 1v12a1 1 0 0 1-1 1H2a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1h12zM2 0a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V2a2 2 0 0 0-2-2H2z"/><path d="M7.002 11a1 1 0 1 1 2 0 1 1 0 0 1-2 0zM7.1 4.995a.905.905 0 1 1 1.8 0l-.35 3.507a.552.552 0 0 1-1.1 0L7.1 4.995z"/></svg>',setTimeout(()=>{a.innerHTML="Try again"},2e3);else{const l=await n.json();a.innerHTML=`<b>${l.name}</b>`}},activateTimezoneInfo=()=>{let e=Intl.DateTimeFormat().resolvedOptions().timeZone;e||(e="UTC"),document.cookie="mytz="+e+";path=/"};
