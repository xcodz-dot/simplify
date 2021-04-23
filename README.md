# Simplify
It is a simple set of utilities for python developers in specific.

It comes packed with the following tools:
* minifier
* show (to show file content in command line with syntax highlighting)

## Minifier

Minifier contains the support for the following languages and data formats
* Python
* JSON
* JavaScript
* HTML
* XML
* CSS

to use minifier using command line:

```commandline
simplify minify myfile.py output.py
```

to select a minifier explicitly:

```commandline
simplify minify myfile output.json --format json 
```

to overwrite input file

```commandline
simplify minify myfile.html -o
```

## Show

Show supports more that 400 formats (Thanks to Pygments!) but with the exceptional
ability to show using true color even in windows command prompt (Thanks to Prompt Toolkit!)

To use its command line abilities:

```commandline
simplify show index.html
```
