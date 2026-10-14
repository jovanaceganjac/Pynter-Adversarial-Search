# Pynter — Adversarial Search Agents

AI agents for **Pynter**, a multiplayer grid game where players paint tiles to
gain territory. Built for the *Intelligent Systems* course at ETF Belgrade.

## Agents

| Agent | Approach |
|---|---|
| `RandomAgent` | random legal move (baseline) |
| `GreedyAgent` | best immediate score |
| `MinimaxAgent` | depth-limited minimax for two players |
| `MinimaxABAgent` | minimax with alpha-beta pruning |
| `MaxNAgent` | Max^n search for more than two players |

## Run

```bash
pip install pygame
python main.py MinimaxABAgent,GreedyAgent example_map.txt 5 0 5
#              agents                     map           rounds time-limit depth
```

## Tech

Python 3, Pygame
