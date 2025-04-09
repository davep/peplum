# Peplum

[![Peplum](https://raw.githubusercontent.com/davep/peplum/refs/heads/main/.images/peplum-social-banner.png)](https://peplum.davep.dev/)

[![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/davep/peplum/style-lint-and-test.yaml)](https://github.com/davep/peplum/actions)
[![GitHub commits since latest release](https://img.shields.io/github/commits-since/davep/peplum/latest)](https://github.com/davep/peplum/commits/main/)
[![GitHub Issues or Pull Requests](https://img.shields.io/github/issues/davep/peplum)](https://github.com/davep/peplum/issues)
[![GitHub Release Date](https://img.shields.io/github/release-date/davep/peplum)](https://github.com/davep/peplum/releases)
[![PyPI - License](https://img.shields.io/pypi/l/peplum)](https://github.com/davep/peplum/blob/main/LICENSE)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/peplum)](https://github.com/davep/peplum/blob/main/pyproject.toml)
[![PyPI - Version](https://img.shields.io/pypi/v/peplum)](https://pypi.org/project/peplum/)

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

### Homebrew

The package is available via Homebrew. Use the following commands to install:

```sh
$ brew tap davep/homebrew
$ brew install peplum
```

## Using Peplum

Once you've installed Peplum using one of the above methods, you can run the
application using the `peplum` command.

The best way to get to know Peplum is to read the help screen, once in the
main application you can see this by pressing <kbd>F1</kbd>.

![Peplum help](https://raw.githubusercontent.com/davep/peplum/refs/heads/main/.images/peplum-help.png)

For more information and details on configuring Peplum, see [the online
documentation](https://peplum.davep.dev/).

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
