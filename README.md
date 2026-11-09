# HordesOfHell

## Introduction

HordesOfHell explores machine learning for predicting "Aether" from Infernal Hordes run data in "Diablo 4".

For example, see the [Simple Model](./docs/simple.md) documentation.

## Project layout

```text
HordesOfHell/
├── src/
│   ├── hordesofhell/
│   │   └── ...
│   └── data/
│       └── ...
├── notebooks/
│   └── ...
├── tests/
├── simple_output.csv
├── pyproject.toml
└── README.md
```

## How to use 

### Setup

#### Dev Container (VS Code)

Using a popular IDE like VSCode, you can use a [devcontainer exstension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers). In VSCode, you press `CTRL+SHIFT+P` and write and select `Dev Containers: Rebuild and reopen in container`, after which you should have a fully set up dev environment.

#### Local environment

This project uses Python 3.14+.

Install dependencies with `uv`:

```bash
uv sync --extra dev
```

If you want notebook tooling as well:

```bash
uv sync --extra dev --extra notebook
```

### Usefull Terminal Commands

```bash
data                           Convert data files
format                         Format the code
help                           Display this help
lint                           Run linters
pipeline                       Run the full pipeline
tests                          Run tests
validate                       Run data validation rules
```

## License

[LICENSE](./LICENSE)

## Authors

- [Uplink036](https://github.com/Uplink036)
- [s02blom](https://github.com/s02blom)