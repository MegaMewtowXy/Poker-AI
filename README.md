# ♠️ Texas Hold'em AI Engine

A desktop-based Texas Hold'em Poker Engine built in Python featuring a complete poker engine, intelligent AI opponents, Monte Carlo simulations, multiple game modes, and an interactive graphical interface using Pygame.

---

## Features

### Poker Engine
- Complete Texas Hold'em implementation
- Dealer button rotation
- Small Blind / Big Blind system
- Betting rounds
- Side Pot support
- All-In support
- Split pot handling
- Automatic showdown
- Hand evaluation
- Winner determination

---

## AI Engine

DeepBot includes multiple AI modules:

- Monte Carlo Equity Calculator
- Hand Strength Evaluation
- Position Analysis
- Pot Odds Calculation
- Bluff Engine
- Bet Sizing Engine
- Opponent Modeling
- Range Modeling
- Strategy Profiles
- Difficulty Levels
- Risk Management

Available AI Strategies:

- Tight Aggressive (TAG)
- Loose Aggressive (LAG)
- Tight Passive
- Loose Passive

Difficulty Levels:

- Easy
- Medium
- Hard

---

## Game Modes

- Human vs AI
- Human vs Human
- AI vs AI Simulation

---

## User Interface

Built using **Pygame**

Features include:

- Interactive poker table
- Community cards
- Player cards
- Betting controls
- Chip display
- Pot display
- AI Brain HUD
- Hand Rankings window
- Tutorial screen

---

## Project Structure

```
POKER/
│
├── ai/
│   ├── bet_sizing.py
│   ├── bluff_engine.py
│   ├── board_analysis.py
│   ├── decision.py
│   ├── equity.py
│   ├── hand_strength.py
│   ├── opponent_model.py
│   ├── position.py
│   ├── pot_odds.py
│   ├── range_model.py
│   ├── strategy.py
│   └── ...
│
├── engine/
│   ├── betting.py
│   ├── betting_round.py
│   ├── dealer.py
│   ├── evaluator.py
│   ├── game.py
│   └── ...
│
├── models/
├── simulation/
├── tests/
├── ui/
├── utils/
│
├── main.py
├── requirements.txt
└── README.md
```

---

## Installation

Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/Texas-Holdem-AI-Engine.git

cd Texas-Holdem-AI-Engine
```

Create a virtual environment

```bash
python -m venv venv
```

Activate the virtual environment

### Windows

```bash
venv\Scripts\activate
```

### Linux / macOS

```bash
source venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

## Running the Project

Start the application using:

```bash
python main.py
```

---

## Running Tests

Run all tests:

```bash
python -m pytest
```

Run Bot vs Bot simulation:

```bash
python -m tests.test_bot_vs_bot
```

---

## AI Decision Factors

The AI evaluates decisions using:

- Hand Strength
- Monte Carlo Equity
- Pot Odds
- Position
- Opponent Modeling
- Range Analysis
- Bluff Probability
- Strategy Profile
- Difficulty Level
- Stack Size
- Board Texture

---

## Technologies Used

- Python 3
- Pygame
- NumPy
- Object-Oriented Programming
- Monte Carlo Simulation
- Git
- GitHub

---

## Future Improvements

- Tournament Mode
- Multi-table Support
- Network Multiplayer
- Hand History Export
- AI Self-Learning
- Advanced Opponent Profiling
- Statistics Dashboard
- GTO-based Decision Engine

---

---

## Author

**Kshitij Kejriwal**

MCA Student – Veermata Jijabai Technological Institute (VJTI)

---

## License

This project is intended for educational and research purposes.