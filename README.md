# Ping Pong Game

A simple **Ping Pong** game built using **Python** and **Pygame**, featuring score tracking using **JSON**.

## Features 🚀

- **Classic 2-player Ping Pong gameplay**
- **Score persistence** using a JSON file (`scores.json`)
- **Winning system** (First to 10 points wins)
- **Collision handling** for realistic ball movement
- **Paddle controls for both players**

## Installation 📥

### Prerequisites

- Python 3 installed
- Pygame library installed

### Steps

1. **Clone the repository**
   ```sh
   git clone https://github.com/gabrielkinyua/ping_pong
   cd ping_pong
   ```
2. **Install Pygame**
   ```sh
   pip install pygame
   ```
3. **Run the game**
   ```sh
   python solution.py
   ```

## How to Play 🎮

- **Left Player Controls:**
  - `W` - Move paddle up
  - `S` - Move paddle down
- **Right Player Controls:**
  - `Up Arrow` - Move paddle up
  - `Down Arrow` - Move paddle down

## Score Management 🏆

The game keeps track of scores using `scores.json`.

- **Scores are saved automatically** after each point.
- **Scores reset** when a player wins.
- **To manually reset scores**, delete `scores.json` or modify it.

## Contributing 🤝

Feel free to fork this repository and submit pull requests with improvements!

## License 📝

This project is licensed under the MIT License.
