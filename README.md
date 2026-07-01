# Warships v2.0

Warships is a thrilling turn-based naval strategy game where two players face off to locate and destroy each other's entire fleet.

Featuring a radar system to assist in target scanning and a robust UDP server architecture for fast move synchronization, the game delivers a smooth and thrilling experience. Each shot demands careful prediction and strategy, turning every match into an intense battle of wits on the open seas.

## 🎯 Gameplay

In Warships, each player commands a hidden fleet arranged on a grid map. Your task is to use strategy and deduction to locate and destroy all of your opponent's ships.

The game is played in turns:
- Each turn, you choose a coordinate to attack.
- **Hit:** If you hit an opponent's ship, the marker will turn orange and you get an extra attack on the next turn.
- **Miss:** If you miss, your turn ends and passes to the opponent.
- **Radar Hit:** If you hit an opponent's radar, the marker will turn blue and you will gain more radar usages.

**Radar System:** When using the radar, it scans a 3x3 area (around your target) and returns the number of ship tiles within that area. 

Victory goes to the player who destroys the entire opponent's fleet first.

## 🎮 Controls
- **Left mouse click:** Fire
- **Right mouse click:** Rotate ship
- **Left mouse hold and move:** Move ship
- **Click Torpedo/Radar labels:** Switch attack mode

## 🚀 How to Run

### Project Structure
The source code is organized clearly in the `src/` folder. Assets and fonts remain in the root directory.

### Running the Server
One player must act as the host by running the server:
```bash
python server.py
```
*Note: Make sure to check the terminal for the server IP address. Players must be on the same local network (or use virtual LAN tools like Radmin VPN/Hamachi).*

### Running the Game Client
To start the game, simply run:
```bash
python client.py
```
When playing an online match, you will be prompted to enter the Host's IP address.

## 🛠 Technical Architecture & Methods

This project implements several interesting software engineering and algorithmic approaches:

### 1. Networking & State Synchronization (UDP)
- **Protocol:** The multiplayer mode uses **UDP sockets** (`socket.AF_INET`, `socket.SOCK_DGRAM`) to ensure fast and low-latency communication between the client and server.
- **Serialization:** Custom signal objects (`SignalSended`, `SignalRecieved`) encapsulate the game state (turns, phases, hit coordinates) and are serialized using Python's `pickle` module before transmission.
- **Concurrency:** The central server manages multiple connections using Python's `threading` module, handling incoming packets simultaneously while avoiding race conditions via Thread Locks (`threading.Lock`).

### 2. Probabilistic Bot Logic (AI)
The single-player offline mode features an intelligent bot (`botLogic.py`) that operates on a probabilistic **Hunt and Target** algorithm rather than pure randomness:
- **Heatmap Generation (`secondBoard`):** The bot dynamically calculates a probability density map (heatmap) based on the remaining unhit tiles and the lengths of surviving enemy ships. It prioritizes firing at cells with the highest combinatorial overlap.
- **State Machine Strategy:** The bot switches between **Random Mode** (firing based on highest probability) and **Hunt Mode** (when a hit occurs, the bot systematically targets adjacent cells in `forward` or `backward` directions to sink the rest of the ship).

### 3. Game Engine & UI
- **Pygame:** The game loop, rendering, event handling, and audio are powered entirely by Pygame.
- **Custom UI System:** The project avoids external GUI libraries by implementing its own custom UI layer (`widget.py`, `screen.py`), providing custom buttons, text rendering, hover effects, and screen state management (Menu, Prepare, Playing, End).

## 👨‍💻 Authors
- Nguyễn Văn Vinh (Vinhnub)
- Quốc Huy
