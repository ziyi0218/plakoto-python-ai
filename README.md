# plakoto-python-ai

A Python implementation of **Plakoto**, a strategic board game from the backgammon family, featuring a **text interface**, a **graphical interface with Pygame**, and a **Monte Carlo AI**.

This repository contains the source code, project documentation, and archived development history of a university software engineering project.

---

## Overview

**plakoto-python-ai** is a team project developed as part of a university programming/software engineering course.

The goal of the project is to provide a playable digital version of **Plakoto**, including:

- full implementation of the game rules
- legal move generation
- text-based gameplay
- graphical gameplay with Pygame
- Monte Carlo-based AI
- save/load support
- technical and project documentation

The project is organized in a modular way, separating the **game engine**, **AI**, **interfaces**, and **utility tools**.

---

## Features

### Game Engine

- 24-point board
- 15 checkers per player
- move validation
- bearing off support
- victory detection
- implementation of core Plakoto mechanics such as pinning/trapping

### Interfaces

- **Text interface** for terminal-based play
- **Graphical interface** built with **Pygame**

### Artificial Intelligence

- Monte Carlo-based move selection
- configurable AI difficulty
- simulation-based evaluation of legal moves
- caching and parallelization support for better performance

### Save System

- save current game state
- load and resume saved matches

---

## Project Structure

```text
plakoto-python-ai/
├── archive/                  # Archived development versions
├── docs/                     # Project documents and reports
├── src/
│   ├── data/
│   │   └── saves/            # Saved games
│   ├── docs/
│   │   └── rules.md          # Game rules
│   ├── plakoto/
│   │   ├── GUI/              # Graphical interface modules
│   │   ├── ai/               # AI modules
│   │   ├── core/             # Core game logic
│   │   ├── interfaces/       # Interface layer
│   │   ├── utils/            # Helper utilities
│   │   └── __init__.py
│   └── scripts/              # Launch scripts
├── .gitignore
├── CONTRIBUTING.md
├── LICENSE
├── README.md
└── requirements.txt
```

---

## Tech Stack

* **Python 3.11+**
* **Pygame**
* **concurrent.futures** for parallel simulation
* **pickle** for save/load functionality

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/ziyi0218/plakoto-python-ai.git
cd plakoto-python-ai
```

### 2. Create and activate a virtual environment

#### Windows

```bash
python -m venv .venv
.venv\Scripts\activate
```

#### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## Running the Project

### Text Interface

```bash
python src/scripts/play_text.py
```

### Graphical Interface

```bash
python src/scripts/play_gui.py
```

---

## Gameplay

Plakoto is a variant of backgammon with its own distinctive mechanics.

### Core Rules

* each player starts with **15 checkers**
* the board contains **24 points**
* players move in opposite directions
* checkers are **not captured** as in standard backgammon
* instead, a lone opposing checker can be **pinned/trapped**
* a pinned checker cannot move until it is released
* doubles can be played **four times**
* a player wins by bearing off all checkers

For more details, see:

```text
src/docs/rules.md
```

---

## AI System

The project includes a **Monte Carlo AI** that evaluates candidate moves through repeated simulations.

### AI characteristics

* generation of legal move sequences
* simulation-based move evaluation
* move selection based on estimated win rate
* support for caching to reduce repeated computation
* support for parallel computation to accelerate simulations

This makes the project both a playable game and an applied algorithmic/software engineering project.

---

## Architecture

### `plakoto/core/`

Core game logic:

* board representation
* move validation
* legal move generation
* win condition checking

### `plakoto/ai/`

Artificial intelligence logic:

* Monte Carlo simulations
* candidate move evaluation
* parallelized search support

### `plakoto/interfaces/`

Interface layer:

* text interface
* graphical interface abstraction / launch logic

### `plakoto/GUI/`

Graphical rendering and event handling with Pygame.

### `plakoto/utils/`

Helper functions such as save/load utilities.

---

## Performance Notes

The project includes several performance-oriented design choices:

* macro-move caching
* lightweight board copying for simulations
* parallel simulation with `ProcessPoolExecutor`
* modular code organization for future optimization

These techniques are especially useful for the Monte Carlo AI, where many game states must be explored efficiently.

---

## Documentation

This repository is accompanied by project documents such as:

* requirements/specification documents
* general and detailed design documents
* testing documents
* final report / mémoire

These documents reflect the full software engineering workflow behind the project.

---

## Archived Development History

The `archive/` directory preserves earlier development versions of the project, including work related to:

* AI
* text interface
* graphical interface

It provides insight into the evolution of the project during development.

---

## Possible Improvements

Potential future extensions include:

* stronger AI strategies
* GUI-based AI matches
* network multiplayer
* improved save management
* automated test suite expansion
* packaging and release distribution

---

## Authors

This project was developed as a team university project under the supervision of **Bruno Bouzy**.

### Student Team Members
* Ziyi Ren
* Hassrol Ya
* Ruby Ghanime
* Mahdi Bennamane

### Project Supervisor
* **Bruno Bouzy** - Project supervisor and advisor

---

## Contributing

Contributions, bug reports, and suggestions are welcome.

Please read [CONTRIBUTING.md](CONTRIBUTING.md) before opening an issue or submitting a pull request.

---

## License

This project is licensed under the **MIT License**.
See the [LICENSE](LICENSE) file for details.

---

## Acknowledgements

* university course staff and supervisors
* the Plakoto / backgammon family of games as inspiration
* the Python and Pygame communities



