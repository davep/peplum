# Peplum ChangeLog

## v1.0.1

**Released: 2025-05-15**

- Fixed a crash if "superseded by" is a list of PEPs rather than just a
  single PEP. ([#65](https://github.com/davep/peplum/pull/65))

## v1.0.0

**Released: 2025-05-03**

- Made Textual v3.1.1 the minimum required version.
  (#62[](https://github.com/davep/peplum/pull/62))
- Fixed the colour of the `All` key reminder not being updated when the
  theme is changed. ([#59](https://github.com/davep/peplum/issues/59))

## v0.6.1

**Released: 2025-04-12**

- Make Textual v3.1.0 the minimum required version, to take advantage of the
  fix for [#58](https://github.com/davep/peplum/issues/58).
  ([#60](https://github.com/davep/peplum/pull/60))
- Add a workaround for
  [textual#5742](https://github.com/Textualize/textual/issues/5742).
  ([#60](https://github.com/davep/peplum/pull/60))

## v0.6.0

**Released: 2025-04-09**

- Added the ability to configure the keyboard bindings for the system
  commands. ([#52](https://github.com/davep/peplum/pull/52))
- Added `--bindings` as a command line switch.
  ([#52](https://github.com/davep/peplum/pull/52))

## v0.5.0

**Released: 2025-04-08**

- Added a system command for reversing the current sort order.
  ([#46](https://github.com/davep/peplum/pull/46))
- Added `--theme` as a command line switch.
  ([#48](https://github.com/davep/peplum/pull/48))
- Added `--sort-by` as a command line switch.
  ([#48](https://github.com/davep/peplum/pull/48))
- Added support for taking a PEP number on the command line and jumping to
  it on startup. ([#48](https://github.com/davep/peplum/pull/48))

## v0.4.2

**Released: 2025-03-17**

- Bumped minimum Python version to 3.1.0.
  ([#40](https://github.com/davep/peplum/pull/40))
- Ensured the code works with *all* stable Python versions from 3.10 and
  above. ([#40](https://github.com/davep/peplum/pull/40))

## v0.4.1

**Released: 2025-02-16**

- Pinned Textual to v1.0.0 for now; v2.0.x introduced some unstable
  behaviour.

## v0.4.0

**Released: 2025-02-04**

- When saving a PEP's source a default filename is provided.
  ([#24](https://github.com/davep/peplum/pull/24))
- Updated the PEP loading code to use the [newly-added `author_names`
  property in the API](https://github.com/python/peps/issues/4211).
  ([#30](https://github.com/davep/peplum/pull/30))

## v0.3.0

**Released: 2025-01-29**

- Added the ability to view the source of a PEP.
  ([#17](https://github.com/davep/peplum/pull/17))
- Made some cosmetic changes to the notes editor dialog so that it better
  matches the rest of the application.
  ([#18](https://github.com/davep/peplum/pull/18))
- Dropped Python 3.8 as a supported Python version.
  ([#19](https://github.com/davep/peplum/pull/19))
- Added support for saving the source of a PEP to a file.
  (#20[](https://github.com/davep/peplum/pull/20))

## v0.2.0

**Released: 2025-01-27**

- Worked around a likely Textual bug that caused an occasional cosmetic
  problem with the main PEPs list.
  ([#6](https://github.com/davep/peplum/pull/6))
- Added the created date of a PEP to the list of things searched when doing
  a free text search. ([#7](https://github.com/davep/peplum/pull/7))
- Commands in the Python version filtering palette are now sorted by proper
  version order. ([#12](https://github.com/davep/peplum/pull/12))
- Added the ability to attach notes to a PEP.
  ([#13](https://github.com/davep/peplum/pull/13))

## v0.1.0

**Released: 2025-01-25**

- Initial release.

## v0.0.1

**Released: 2025-01-14**

- Initial placeholder package to test that the name is available in PyPI.

[//]: # (ChangeLog.md ends here)
