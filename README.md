# LLM Negotiation

Behavioral economics games (ultimatum, dictator, etc.) simulated with LLM agents using [AutoGen](https://github.com/microsoft/autogen).

## Setup

Requires Python 3.11+ and [uv](https://docs.astral.sh/uv/).

```bash
uv sync
```

Create a `.env` file with your OpenAI API key:

```
OPENAI_API_KEY=sk-...
```

## Usage

```bash
# Run the ultimatum game (100 iterations by default)
uv run llm-negotiation ultimatum

# Run the dictator game with custom settings
uv run llm-negotiation dictator -n 50 -m gpt-4o -t 0.8

# Run with strategic thinking enabled
uv run llm-negotiation ultimatum --strategic

# Specify a run ID for the output file
uv run llm-negotiation dictator_anonymous -r 2

# Verbose logging
uv run llm-negotiation unfair_receiver -v
```

### Available games

| Game | Description |
|------|-------------|
| `ultimatum` | Proposer divides $100; responder can accept or reject |
| `dictator` | Proposer divides $100; responder has no rejection right |
| `dictator_anonymous` | Same as dictator, but the experimenter doesn't know who you are |
| `unfair_receiver` | Responder decides whether to accept an unfair (90/10) split |

### CLI options

```
usage: llm-negotiation [-h] [-n ITERATIONS] [-r RUN_ID] [-m MODEL]
                       [-t TEMPERATURE] [--strategic | --no-strategic] [-v]
                       {ultimatum,dictator,dictator_anonymous,unfair_receiver}

positional arguments:
  game                  Game type to run

options:
  -n, --iterations      Number of iterations (default: 100)
  -r, --run-id          Run identifier for the output filename (default: 1)
  -m, --model           OpenAI model to use (default: gpt-4o-mini-2024-07-18)
  -t, --temperature     Sampling temperature (default: 1.0)
  --strategic           Enable strategic thinking prompt
  --no-strategic        Disable strategic thinking prompt
  -v, --verbose         Enable verbose logging
```

## Project structure

```
├── src/llm_negotiation/
│   ├── cli.py          # CLI entry point
│   ├── config.py       # Game configuration & registry
│   ├── parsing.py      # LLM response parsing
│   ├── personality.py  # Random personality generation
│   ├── prompts.py      # Prompt constants for all game types
│   └── runner.py       # Experiment runner
├── results/            # Output CSV files (git-ignored)
├── pyproject.toml
└── README.md
```
