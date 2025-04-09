# Introduction

The way that Peplum works can be configured using a configuration file. This
section will describe what can be configured and how.

The location of the configuration file will depend on how your operating
system and its settings; but by default it is looked for in
[`$XDG_CONFIG_HOME`](https://specifications.freedesktop.org/basedir-spec/latest/),
in a `peplum` subdirectory. Mostly this will translate to the file being
called `~/.config/peplum/configuration.json`.

## Keyboard bindings

Peplum allows for a degree of configuration of its keyboard bindings;
providing a method for setting up replacement bindings for the commands that
appear in the [command palette](index.md#the-command-palette).

### Bindable commands

The following commands can have their keyboard bindings set:

```bash exec="on"
peplum --bindings | sed -e 's/^\([A-Z].*\) - \(.*\)$/- `\1` - *\2*/' -e 's/^    \(Default:\) \(.*\)$/    - *\1* `\2`/'
```

### Changing a binding

If you wish to change the binding for a command, edit the configuration file
and add the binding to the `bindings` value. For example, if you wanted to
change the binding used to View the text of a PEP, changing it from
<kbd>F4</kbd> to <kbd>ctrl</kbd>+<kbd>v</kbd>, and you also wanted to use
<kbd>F5</kbd> to redownload the PEP data, you would set `bindings` to this:

```json
"bindings": {
    "ViewPEP": "ctrl+v",
    "RedownloadPEPs": "f5"
}
```

The designations used for keys is based on the internal system used by
[Textual](https://textual.textualize.io); as such [its caveats about what
works where
apply](https://textual.textualize.io/FAQ/#why-do-some-key-combinations-never-make-it-to-my-app).
The main modifier keys to know are `shift`, `ctrl`, `alt`, `meta`, `super`
and `hyper`; letter keys are their own letters; shifted letter keys are
their upper-case versions; function keys are simply <kbd>f1</kbd>,
<kbd>f2</kbd>, etc; symbol keys (the likes of `#`, `@`, `*`, etc...)
generally use a name (`number_sign`, `at`, `asterisk`, etc...).

!!! tip

    If you want to test and discover all of the key names and combinations
    that will work, you may want to install
    [`textual-dev`](https://github.com/Textualize/textual-dev) and use the
    `textual keys` command.

    If you need help with keyboard bindings [please feel free to
    ask](index.md#questions-and-feedback).

## Theme

Peplum has a number of themes available. You can select a theme using the
`Change Theme` ([`ChangeTheme`](#bindable-commands), bound to <kbd>F9</kbd>
by default) command. The available themes include:

```bash exec="on"
peplum --theme=? | sed 's/^/- /'
```

!!! tip

    You can also [set the theme via the command line](index.md#-t-theme). This can
    be useful if you want to ensure that Peplum runs up with a specific theme.
    Note that this *also* configures the theme for future runs of Peplum.

Here's a sample of some of the themes:

```{.textual path="docs/screenshots/basic_app.py" title="textual-light" lines=40 columns=120 press="f9,t,e,x,t,u,a,l,-,l,i,g,h,t,enter"}
```

```{.textual path="docs/screenshots/basic_app.py" title="nord" lines=40 columns=120 press="f9,n,o,r,d,enter"}
```

```{.textual path="docs/screenshots/basic_app.py" title="catppuccin-latte" lines=40 columns=120 press="f9,c,a,t,p,p,u,c,c,i,n,-,l,a,t,t,e,enter"}
```

```{.textual path="docs/screenshots/basic_app.py" title="dracula" lines=40 columns=120 press="f9,d,r,a,c,u,l,a,enter"}
```

[//]: # (configuration.md ends here)
