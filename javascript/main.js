const baseUrl = "http://localhost:4242";

async function initializeBoard() {
  try {
    const response = await fetch(`${baseUrl}/initialize`, { method: "POST" });
    if (response.ok) {
      alert("Board initialized successfully");
      getBoard(); // Optional: Refresh the board after initialization
    } else {
      alert("Failed to initialize board");
    }
  } catch (error) {
    console.error("Error:", error);
  }
}

async function getBoard() {
  try {
    const response = await fetch(`${baseUrl}/board`);
    if (response.ok) {
      const board = await response.json();
      console.log(board);
    } else {
      alert("Failed to fetch board");
    }
  } catch (error) {
    console.error("Error:", error);
  }
}

async function updateBoard() {
  const newBoard = {
    player: 2,
    a1: "QB",
    a2: "QW",
  };
  try {
    const response = await fetch(`${baseUrl}/board`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(newBoard),
    });
    if (response.ok) {
      alert("Board updated successfully");
      getBoard(); // Optional: Refresh the board after update
    } else {
      alert("Failed to update board");
    }
  } catch (error) {
    console.error("Error:", error);
  }
}

console.log(getBoard());
