# Introduction

```{.textual path="docs/screenshots/basic_app.py" title="Peplum" lines=50 columns=120}
```

Peplum is a terminal-based lookup manager for [Python Enhancement
Proposals](https://peps.python.org). It provides the ability to browse,
filter and search the metadata for all the PEPs available via the [PEP
API](https://peps.python.org/api/).

## Installation

### pipx

The application can be installed using [`pipx`](https://pypa.github.io/pipx/):

```sh
pipx install peplum
```

### uv

If you are a [`uv`](https://docs.astral.sh/uv/) user you can:

```sh
uv tool install peplum
```

Also, if you do have uv installed, you can simply use
[`uvx`](https://docs.astral.sh/uv/guides/tools/):

```sh
uvx peplum
```

to run `peplum`.

### Homebrew

The package is available via [Homebrew](https://brew.sh). Use the following
commands to install:

```sh
brew tap davep/homebrew
brew install peplum
```

## Running Peplum

Once you've installed Peplum using one of the [above
methods](#installation), you can run the application using the `peplum`
command.

### Command line options

Peplum has a number of command line options; they include:

#### `-b`, `--bindings`

Prints the application commands whose keyboard bindings can be modified,
giving the defaults too.

```sh
peplum --bindings
```
```bash exec="on" result="text"
peplum --bindings
```

#### `-h`, `--help`

Prints the help for the `peplum` command.

```sh
peplum --help
```
```bash exec="on" result="text"
peplum --help
```

#### `--license`, `--licence`

Prints a summary of [Peplum's license](license.md).

```sh
peplum --license
```
```bash exec="on" result="text"
peplum --license
```

#### `-t`, `--theme`

Sets Peplum's theme; this overrides and changes any previous theme choice made
[via the user interface](configuration.md#theme).

To see a list of available themes use `?` as the theme name:

```sh
peplum --theme=?
```
```bash exec="on" result="text"
peplum --theme=?
```

#### `-v`, `--version`

Prints the version number of Peplum.

```sh
peplum --version
```
```bash exec="on" result="text"
peplum --version
```

## Getting help

A great way to get to know Peplum is to read the help screen. Once in the
application you can see this by pressing <kbd>F1</kbd>.

```{.textual path="docs/screenshots/basic_app.py" title="The Peplum Help Screen" press="f1" lines=50 columns=120}
```

### The command palette

Another way of discovering commands and keys in Peplum is to use the command
palette (by default you can call it with <kbd>ctrl</kbd>+<kbd>p</kbd> or
<kbd>meta</kbd>+<kbd>x</kbd>).

```{.textual path="docs/screenshots/basic_app.py" title="The Peplum Command Palette" press="ctrl+p" lines=50 columns=120}
```

## Questions and feedback

If you have any questions about Peplum, or you have ideas for how it might be
improved, do please feel free to [visit the discussion
area](https://github.com/davep/peplum/discussions) and [ask your
question](https://github.com/davep/peplum/discussions/categories/q-a) or
[suggest an
improvement](https://github.com/davep/peplum/discussions/categories/ideas).

When doing so, please do search past discussions and also [issues current
and previous](https://github.com/davep/peplum/issues) to make sure I've not
already dealt with this, or don't have your proposed change already flagged
as something to do.

[//]: # (index.md ends here)
