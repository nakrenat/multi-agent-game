# Multi-Agent Game

A modern, interactive game where you navigate through a grid while being chased by AI agents with different strategies. Built with Python and Pygame.

![Game Screenshot](screenshot.png)

## Features

- **Multiple AI Agents**: Each with unique behaviors and strategies
  - Random Agent: Moves unpredictably
  - Greedy Agent: Chases the player
  - Defensive Agent: Avoids other agents
  - Patrol Agent: Follows a predefined path

- **Three Difficulty Levels**
  - Easy: 3 agents, slower speed, lower score multiplier
  - Medium: 4 agents, moderate speed, medium score multiplier
  - Hard: 5 agents, faster speed, higher score multiplier

- **Modern UI Elements**
  - Glassmorphism effects
  - Smooth animations
  - Particle effects
  - Glowing text
  - Modern color scheme

- **Game Features**
  - Personalized high scores
  - Score multiplier based on difficulty
  - Floating score indicators
  - Victory and Game Over screens with confetti effects
  - Custom agent images

## Requirements

- Python 3.x
- Pygame 2.x

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/multi-agent-game.git
cd multi-agent-game
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

## How to Play

1. Run the game:
```bash
python main.py
```

2. Enter your name at the welcome screen
3. Select difficulty level
4. Use arrow keys to move your character
5. Collect green dots to score points
6. Avoid other agents to stay alive
7. Reach the target score to win

## Controls

- **Arrow Keys**: Move your character
- **ESC**: Exit game
- **SPACE**: Restart game (after game over/victory)
- **ENTER**: Confirm name entry
- **BACKSPACE**: Delete character in name input

## Game Rules

- Collect green dots to earn points
- Points are multiplied based on difficulty level
- Colliding with defensive agents reduces your score
- Colliding with other agents ends the game
- Reach the target score to win:
  - Easy: 50 points
  - Medium: 100 points
  - Hard: 150 points

## Project Structure

```
multi-agent-game/
├── main.py           # Main game file
├── agent.py          # Agent class and strategies
├── grid.py           # Grid system
├── requirements.txt  # Python dependencies
├── README.md         # This file
└── assets/          # Game assets
    ├── me.jpg       # Player character image
    └── raz.jpeg     # Agent image
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Pygame community for the excellent game development library
- All contributors who have helped improve the game 