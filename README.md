# Peplum

![Peplum](https://raw.githubusercontent.com/davep/peplum/refs/heads/main/.images/peplum-social-banner.png)

## Introduction

Peplum is a terminal-based lookup manager for [Python Enhancement
Proposals](https://peps.python.org). It provides the ability to browse,
filter and search the metadata for all the PEPs available via the PEP API.

## Installing

### pipx

The package can be installed using [`pipx`](https://pypa.github.io/pipx/):

```sh
$ pipx install peplum
```

Once installed run the `peplum` command.

### Homebrew

The package is available via Homebrew. Use the following commands to install:

```sh
$ brew tap davep/homebrew
$ brew install peplum
```

Once installed run the `peplum` command.

## Using Peplum

The best way to get to know Peplum is to read the help screen, once in the
main application you can see this by pressing <kbd>F1</kbd>.

![Peplum help](https://raw.githubusercontent.com/davep/peplum/refs/heads/main/.images/peplum-help.png)

## File locations

Peplum stores files in a `peplum` directory within both
[`$XDG_DATA_HOME` and
`$XDG_CONFIG_HOME`](https://specifications.freedesktop.org/basedir-spec/latest/).
If you wish to fully remove anything to do with Peplum you will need to
remove those directories too.

Expanding for the common locations, the files normally created are:

- `~/.config/peplum/configuration.json` -- The configuration file.
- `~/.local/share/peplum/*.json` -- The locally-held PEP data.
- `~/.local/share/peplum/cache/*.rst` -- The locally-cached PEP source files.

## Getting help

If you need help, or have any ideas, please feel free to [raise an
issue](https://github.com/davep/peplum/issues) or [start a
discussion](https://github.com/davep/peplum/discussions).

## TODO

See [the TODO tag in
issues](https://github.com/davep/peplum/issues?q=is%3Aissue+is%3Aopen+label%3ATODO)
to see what I'm planning.

[//]: # (README.md ends here)
