# 2026-SedDigital-Sisteminha

SedDigital Sisteminha — aplicação de linha de comando (CLI) em Python.

## Pré-requisitos

- [uv](https://docs.astral.sh/uv/) para gerenciamento de ambiente e dependências

## Instalação

```bash
uv sync
```

## Uso

```bash
uv run sisteminha --help
```

## Desenvolvimento

```bash
# Instalar dependências de desenvolvimento
uv sync

# Executar a aplicação
uv run sisteminha

# Adicionar uma dependência
uv add <pacote>

# Adicionar uma dependência de desenvolvimento
uv add --dev <pacote>
```