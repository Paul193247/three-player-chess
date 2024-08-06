var canvas = document.getElementById("canvas");
var length = canvas.height / 2;
var center = canvas.width / 2;

var rotation = ToRadians(60);
var angle = ToRadians(30);
var height = length * Math.cos(angle);
var width = length * Math.sin(angle);

const debug = document.getElementById("debug");
const URL = "http://127.0.0.1:5000/";
var KEY;
var PLAYER_KEY;
const new_game_button = document.getElementById("new-game");
const join_game_button = document.getElementById("join-game");
const reloade_button = document.getElementById("reload");
const key_input = document.getElementById("key");
var PLAYER;

equivalent_cell = {
  H4: "A1",
  H3: "A2",
  H2: "A3",
  H1: "A4",
  I4: "A5",
  J4: "A6",
  K4: "A7",
  L4: "A8",
  G4: "B1",
  G3: "B2",
  G2: "B3",
  G1: "B4",
  I3: "B5",
  J3: "B6",
  K3: "B7",
  L3: "B8",
  F4: "C1",
  F3: "C2",
  F2: "C3",
  F1: "C4",
  I2: "C5",
  J2: "C6",
  K2: "C7",
  L2: "C8",
  E4: "D1",
  E3: "D2",
  E2: "D3",
  E1: "D4",
  I1: "D5",
  J1: "D6",
  K1: "D7",
  L1: "D8",
  D1: "E1",
  C1: "E2",
  B1: "E3",
  A1: "E4",
  U1: "E9",
  U2: "E10",
  U3: "E11",
  U4: "E12",
  D2: "F1",
  C2: "F2",
  B2: "F3",
  A2: "F4",
  V1: "F9",
  V2: "F10",
  V3: "F11",
  V4: "F12",
  D3: "G1",
  C3: "G2",
  B3: "G3",
  A3: "G4",
  W1: "G9",
  W2: "G10",
  W3: "G11",
  W4: "G12",
  D4: "H1",
  C4: "H2",
  B4: "H3",
  A4: "H4",
  X1: "H9",
  X2: "H10",
  X3: "H11",
  X4: "H12",
  M4: "I8",
  M3: "I7",
  M2: "I6",
  M1: "I5",
  Q1: "I9",
  R1: "I10",
  S1: "I11",
  T1: "I12",
  N4: "J8",
  N3: "J7",
  N2: "J6",
  N1: "J5",
  Q2: "J9",
  R2: "J10",
  S2: "J11",
  T2: "J12",
  O4: "K8",
  O3: "K7",
  O2: "K6",
  O1: "K5",
  Q3: "K9",
  R3: "K10",
  S3: "K11",
  T3: "K12",
  P4: "L8",
  P3: "L7",
  P2: "L6",
  P1: "L5",
  Q4: "L9",
  R4: "L10",
  S4: "L11",
  T4: "L12",
};

var w = canvas.width, // width
  h = canvas.height, // height
  cx = w * 0.5, // center of board
  cy = h * 0.5,
  r = cx * 0.9, // radius of board
  pi2 = Math.PI * 2, // cache
  segments = 6, // a hexagon based shape so 6
  segment = pi2 / segments, // angle of each segment
  hSegment = segment * 0.5, // half segment for center line
  ul,
  ur,
  bl,
  br, // quad. corners
  check = 0.25, // interpolation interval (one check)
  yc = 0,
  xc = 0, // interpolation counters
  toggle = false, // for color
  x,
  y = 0,
  i = 0; // counters...

var ul = { x: cx, y: cy };
ur = {
  x: cx + r * Math.cos(hSegment) * 0.865,
  y: cy + r * Math.sin(hSegment) * 0.865,
};
br = { x: cx + r * Math.cos(segment), y: cy + r * Math.sin(segment) };
bl = {
  x: cx + r * Math.cos(hSegment + segment) * 0.865,
  y: cy + r * Math.sin(hSegment + segment) * 0.865,
};

function getRectangleCenter(c1, c2, c3, c4) {
  let centerX = (c1.x + c2.x + c3.x + c4.x) / 4;
  let centerY = (c1.y + c2.y + c3.y + c4.y) / 4;
  return {
    x: centerX,
    y: centerY,
  };
}

function getInt(p1, p2, t) {
  return { x: p1.x + (p2.x - p1.x) * t, y: p1.y + (p2.y - p1.y) * t };
}

function ToRadians(degrees) {
  return degrees * (Math.PI / 180);
}

var ctx = canvas.getContext("2d");

// Function to calculate cell label
function getCellLabel(row, col) {
  const letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
  return equivalent_cell[letters[row] + (col + 1)];
}

// Function to check if a point is inside a polygon
function isPointInPolygon(x, y, polygon) {
  var inside = false;
  for (var i = 0, j = polygon.length - 1; i < polygon.length; j = i++) {
    var xi = polygon[i].x,
      yi = polygon[i].y;
    var xj = polygon[j].x,
      yj = polygon[j].y;

    var intersect =
      yi > y != yj > y && x < ((xj - xi) * (y - yi)) / (yj - yi) + xi;
    if (intersect) inside = !inside;
  }
  return inside;
}

// Function to draw the board and labels
async function drawBoard() {
  var board = await getBoard();
  var rowIndex = 0;
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  cellPolygons = []; // Clear previous polygons
  for (i = 0; i < segments; i++) {
    toggle = !toggle;
    for (y = 0, yc = 0; y < 4; y++) {
      for (x = 0, xc = 0; x < 4; x++) {
        var l1a = getInt(ul, bl, yc),
          l1b = getInt(ur, br, yc),
          l2a = getInt(ul, bl, yc + check),
          l2b = getInt(ur, br, yc + check),
          c1 = getInt(l1a, l1b, xc),
          c2 = getInt(l1a, l1b, xc + check),
          c3 = getInt(l2a, l2b, xc + check),
          c4 = getInt(l2a, l2b, xc);
        center = getRectangleCenter(c1, c2, c3, c4);

        ctx.beginPath();
        ctx.moveTo(c1.x, c1.y);
        ctx.lineTo(c2.x, c2.y);
        ctx.lineTo(c3.x, c3.y);
        ctx.lineTo(c4.x, c4.y);
        ctx.fillStyle = toggle ? "#000" : "#fff";
        ctx.fill();

        const label = board[getCellLabel(rowIndex, x)];
        if (label) {
          ctx.beginPath();
          ctx.arc(center.x, center.y, 20, 0, Math.PI * 2);
          ctx.fillStyle = "blue";
          ctx.fill();
          ctx.font = "16px Arial";
          ctx.fillStyle = "#000";
          ctx.fillText(label, center.x - 10, center.y + 5);
        }

        toggle = !toggle;
        xc += check;

        // Save cell polygon and label with rotation
        var polygon = [c1, c2, c3, c4].map((p) =>
          rotatePoint(p, cx, cy, segment * i)
        );
        cellPolygons.push({
          polygon: polygon,
          label: getCellLabel(rowIndex, x),
        });
      }
      yc += check;
      toggle = !toggle;
      rowIndex++;
    }
    ctx.translate(cx, cy);
    ctx.rotate(segment);
    ctx.translate(-cx, -cy);
  }
}

// Function to get the board data from the server
async function getBoard() {
  try {
    let response = await fetch(`${URL}/getboard`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ key: KEY }),
    });
    board = await response.json();
    console.log(board);
    return board[0];
  } catch (error) {
    console.error("Fehler beim Laden des Boards:", error);
    debug.innerHTML = "Fehler beim Laden des Boards";
  }
}

// Function to create a new game
async function newgame() {
  try {
    let response = await fetch(`${URL}/creategame`);
    KEY = await response.json();
    newplayer();
    debug.innerHTML = `Game Key: ${KEY}`;
    drawBoard();
  } catch (error) {
    console.error("Fehler beim Erstellen des Spiels:", error);
    debug.innerHTML = "Fehler beim Erstellen des Spiels.";
  }
}

// Function to create a new player
async function newplayer() {
  try {
    let response = await fetch(`${URL}/newplayer`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ key: KEY }),
    });
    response = await response.json();
    PLAYER_KEY = await response[0];
    PLAYER = await response[1];
    console.log(PLAYER_KEY);
    console.log(PLAYER);
    if (PLAYER_KEY === "There is no free player") {
      debug.innerHTML = "There is no free player";
    }
  } catch (error) {
    console.error("Fehler beim Erstellen des Spielers:", error);
    debug.innerHTML = "Fehler beim Erstellen des Spielers.";
  }
}

// Function to join an existing game
function joingame() {
  KEY = key_input.value;
  newplayer();
  debug.innerHTML = `Game Key: ${KEY}`;
  drawBoard();
}

// Rotate point around the center
function rotatePoint(point, cx, cy, angle) {
  var s = Math.sin(angle);
  var c = Math.cos(angle);

  point.x -= cx;
  point.y -= cy;

  var xnew = point.x * c - point.y * s;
  var ynew = point.x * s + point.y * c;

  point.x = xnew + cx;
  point.y = ynew + cy;
  return point;
}

async function get_valid_pos(startpos) {
  try {
    let response = await fetch(`${URL}/validmoves`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ key: KEY, startpos: startpos }),
    });
    valid_pos = await response.json();
    return valid_pos;
  } catch (error) {
    console.error("Fehler beim Laden der Validen Felder:", error);
    debug.innerHTML = "Fehler beim Laden der Validen Felder.";
  }
}

var highlightedCell = [];
var currCell = undefined; // Store the currently highlighted cell

// Function to highlight a specific cell
async function highlightCell(labels, curr_cell) {
  highlightedCell = [];
  // Clear previous highlight
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  await drawBoard(); // Redraw the board
  for (label of labels) {
    // Find the cell polygon corresponding to the label
    let cell = cellPolygons.find((cell) => cell.label === label);
    // Draw highlight around the cell
    ctx.beginPath();
    ctx.lineWidth = 3;
    ctx.strokeStyle = "red";
    ctx.fillStyle = "rgba(255, 255, 0, 0.3)"; // Highlight color with transparency

    ctx.moveTo(cell.polygon[0].x, cell.polygon[0].y);
    cell.polygon.forEach((point) => ctx.lineTo(point.x, point.y));
    ctx.closePath();
    ctx.fill();
    ctx.stroke();

    highlightedCell.push(label);
  }
  currCell = curr_cell;
  // Find the cell polygon corresponding to the label
  cell = cellPolygons.find((cell) => cell.label === curr_cell);
  // Draw highlight around the cell
  ctx.beginPath();
  ctx.lineWidth = 3;
  ctx.strokeStyle = "red";
  ctx.fillStyle = "rgba(255, 255, 0, 0.3)"; // Highlight color with transparency

  ctx.moveTo(cell.polygon[0].x, cell.polygon[0].y);
  cell.polygon.forEach((point) => ctx.lineTo(point.x, point.y));
  ctx.closePath();
  ctx.fill();
  ctx.stroke();
}

async function setmove(startPos, endPos) {
  console.log(startPos, endPos);
  try {
    await fetch(`${URL}/setboard`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        key: KEY,
        startpos: startPos,
        endpos: endPos,
        playerkey: PLAYER_KEY,
        player: PLAYER,
      }),
    });
    await drawBoard();
  } catch (error) {
    console.error("Fehler beim Laden der Validen Felder:", error);
    debug.innerHTML = "Fehler beim Laden der Validen Felder.";
  }
}

// Event listener for canvas clicks
canvas.addEventListener("click", async function (event) {
  var rect = canvas.getBoundingClientRect();
  var x = event.clientX - rect.left;
  var y = event.clientY - rect.top;

  for (var i = 0; i < cellPolygons.length; i++) {
    if (isPointInPolygon(x, y, cellPolygons[i].polygon)) {
      console.log(cellPolygons[i].label);
      if (highlightedCell.some((item) => item === cellPolygons[i].label)) {
        setmove(currCell, cellPolygons[i].label);
      } else {
        console.log("Clicked cell label:", cellPolygons[i].label);
        valid_pos = await get_valid_pos(cellPolygons[i].label);
        console.log("Valid Positions. ", valid_pos);
        if (
          typeof valid_pos == String &&
          valid_pos.startsWith("No Figure at position")
        )
          break;
        highlightCell(valid_pos, cellPolygons[i].label);
        break;
      }
    }
  }
});

new_game_button.onclick = newgame;
join_game_button.onclick = joingame;
reloade_button.onclick = drawBoard;
