function process() {
  const params = new URLSearchParams(location.search);

  if (
      params.get("screen") !== "ally" ||
      (params.get("mode") !== "members_defense" &&
          params.get("mode") !== "members_troops")
  ) {
      UI.ErrorMessage("Przejdz do Plemie -> Czlonkowie -> Wojska/Obrona", "2e3");
  } else {
      const cacheTime = Data.cacheTime * 60 * 1000;
      let output = "";
      let lackAccessPlayers = "";
      let players = [];
      let scriptName;
      let firstLine;
      let showFirstLine;
      let showNicknames;
      let mode;
      if (params.get("mode") === "members_troops") {
          scriptName = "Zbiorka Wojska";
          firstLine = Data.firstLineTroops;
          showFirstLine = Data.showFirstLineTroops;
          showNicknames = Data.showNicknamesTroops;
          mode = "troops";
      } else {
          scriptName = "Zbiorka Deffa";
          firstLine = Data.firstLineDeff;
          showFirstLine = Data.showFirstLineDeff;
          showNicknames = Data.showNicknamesDeff;
          mode = "defence";
      }

      // Adds players from current html to get array with players nicknames and ids
      const AllPlayersList = () => {
          Array.from(
              document.querySelector("#ally_content .input-nicer").options
          ).forEach((option_element, index) => {
              if (index !== 0) {
                  players.push({
                      id: option_element.value,
                      nick: option_element.text.trim(),
                      disabled: option_element.disabled,
                  });
              }
          });
      };

      // Uses some methods to get all stuff from table with units from current html player page
      const AddPlayerPageToOutput = (playerPageDocument, playerNick, useNick) => {
          const tableRows = playerPageDocument.querySelectorAll(
              ".table-responsive .vis tr"
          );
          let noAccess = false;
          let playerOutputTroops = "";
          let coord = "";
          tableRows.forEach((oneVillageNode, rowIndex) => {
              if (rowIndex === 0) {
                  return;
              }
              if (output !== "" || playerOutputTroops !== "") {
                  playerOutputTroops += "\r\n";
              }
              if (useNick) {
                  playerOutputTroops += playerNick + ",";
              }
              let unitRow = oneVillageNode.querySelectorAll("td");
              unitRow.forEach((col, colIndex) => {
                  let value = String(col.innerHTML).trim();
                  if (value === "?") {
                      noAccess = true;
                  }
                  if (colIndex === 0) {
                      if (value.includes("|")) {
                          value = value.split("").reverse().join("");
                          const coordIndex1 = value.search("[)]");
                          const coordIndex2 = value.search("[(]");
                          value = value.slice(coordIndex1 + 1, coordIndex2);
                          value = value.split("").reverse().join("");
                          coord = value;
                      } else {
                          playerOutputTroops += coord + ",";
                      }
                  }
                  playerOutputTroops += value + ",";
              });
          });
          if (noAccess) {
              lackAccessPlayers += `<p style="margin:0">${playerNick}</p>`;
          } else {
              output += playerOutputTroops;
          }
      };
      // To add player_id to current path
      const GetURL = (id) => {
          const params = new URLSearchParams(window.location.search);
          params.set("player_id", id);
          return ""
              .concat(window.location.origin)
              .concat(window.location.pathname, "?")
              .concat(params.toString());
      };
      // Used to parse string from fetch func to html
      const ConvertToHTML = (pageText) => {
          const parser = new DOMParser();
          const playerPageDocument = parser.parseFromString(pageText, "text/html");
          return playerPageDocument.body;
      };

      // 0. If cacheTime smaller than actual Time, use localStorage output.
      // 1. Use AllPlayersList to get Players.
      // 2. If no access to a player, his nick goes to lackAccess variable.
      // 3. ForLoop players with access.
      // 3.1 Fetch a player page.
      // 3.2 Add his troops to output -> AddPlayerPageToOutput.
      // 4. Add results to localStorage.
      // 5. Dialog with results.

      async function RenderPlayerTroops() {
          const removedPlayers = Data.removedPlayers.split(";");
          const today = new Date().getTime();
          const afterCacheTime = today + cacheTime;
          const storageDate = localStorage.getItem("troops-storageDate" + mode);
          let parseTime;

          if (today < storageDate && Data.cache) {
              output = localStorage.getItem("troops-output" + mode);
              lackAccessPlayers = localStorage.getItem(
                  "troops-lackAccessPlayers" + mode
              );
              parseTime = new Date(
                  parseInt(localStorage.getItem("troops-parseTime" + mode))
              );
              parseTime = parseTime.toLocaleTimeString();
          } else {
              parseTime = new Date(today);
              parseTime = parseTime.toLocaleTimeString();
              AllPlayersList();
              players
                  .filter((player) => {
                      return player.disabled === true;
                  })
                  .map((player) => {
                      let nick = player.nick;
                      const index = nick.search("[(]");
                      nick = nick.slice(0, index).trim();
                      lackAccessPlayers += `<p style="margin:0">${nick}</p>`;
                  });

              const notDisabledPlayers = players.filter((player) => {
                  return (
                      player.disabled === false && !removedPlayers.includes(player.nick)
                  );
              });

              let i = 0
              const len = notDisabledPlayers.length
              const newProgesPar = (i, len) => {
                  return (`<h1 style="margin-top:10px;font-size:40px">${i}/${len}</h1><h1>Czekaj...</h1>`)
              }

              const progress = document.createElement("div");
              progress.setAttribute("id", "super-simple-progress-bar")
              progress.style.width = "300px";
              progress.style.height = "200px";
              progress.style.position = "absolute";
              progress.style.background = "#f4e4bc";
              progress.style.margin = "auto";
              progress.style.color = "#803000";
              progress.style.top = 0;
              progress.style.bottom = "20%";
              progress.style.left = 0;
              progress.style.right = 0;
              progress.style.border = "5px solid #804000";
              progress.style.textAlign = "center";
              progress.style.fontSize = "40px";
              progress.innerHTML = newProgesPar(i, len);
              document.body.appendChild(progress);

              for (player of notDisabledPlayers) {
                  progress.innerHTML = newProgesP(i, len);
                  const response = await fetch(GetURL(player.id));
                  const html = await response.text();
                  const playerPageDocument = ConvertToHTML(html);
                  const useNick = showNicknames ? true : false;
                  AddPlayerPageToOutput(playerPageDocument, player.nick, useNick);
                  await new Promise(resolve => setTimeout(resolve, 300));
                  i += 1;
              }
              progress.style.display = "none";

              localStorage.setItem("troops-parseTime" + mode, String(today));
              localStorage.setItem("troops-storageDate" + mode, afterCacheTime);
              localStorage.setItem("troops-output" + mode, output);
              localStorage.setItem(
                  "troops-lackAccessPlayers" + mode,
                  lackAccessPlayers
              );
          }
          Dialog.show(
              "scriptFinalContent",
              `<h2 style="width:600px;">${scriptName}:</h2>
            ${Data.removedPlayers === ""
                  ? ""
                  : `<p>Nieuwzglednieni: ${Data.removedPlayers}</p>`
              }${lackAccessPlayers === ""
                  ? ``
                  : `<h4>Uwaga, czesciowy lub calkowity brak podgladu:</h4>` +
                  lackAccessPlayers
              }<textarea rows="15" style="width:95%;margin-top:15px;margin-bottom:25px;">${showFirstLine ? firstLine + "\r\n" : ""
              }${output}</textarea>
                <p style="text-align:right"><small>Wygenerowano ${parseTime}.</small></p>`
          );
      }

      RenderPlayerTroops();
  }
}
process();