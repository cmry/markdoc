# MarkDoc

This piece of code can be used to convert
[NumPy-styled](https://sphinxcontrib-napoleon.readthedocs.org/en/latest/example_numpy.html) Python docstrings ([example](https://github.com/scikit-learn/scikit-learn/blob/master/sklearn/neural_network/multilayer_perceptron.py#L134)),
such as those used in [scikit-learn](https://www.scikit-learn.org/), to
Markdown with minimum dependencies. In this way, only the code-contained
documentation needs to be editted, and your documentation on for example
[readthedocs](http://www.readthedocs.org/) can be automatically updated
thereafter with some configuration.

## Example

The converted documentation for this particular code can be found
[here](https://github.com/cmry/markdoc/blob/master/markdoc.md).

## Before Use

The format assumes that your code (or at least your docstring documentation) is
in line with the styleguides of *both* PEP8 and PEP257. There are two ways to
go about making sure this is the case:

#### Fast

Just check the example
[here](https://github.com/cmry/markdoc/blob/master/markdoc.py#L304) to get a
quick overview of how the docstrings would have to look in order for them
to parse correctly.

#### Better

The styleguides are incorporated into two libraries that can be used to check
the Python files for style errors in terminal, like so:

``` shell
pip install pep8
pip install pep257

pep8 yourpythonfile.py
pep257 yourpythonfile.py
```

These are more conveniently implemented in linter plugins such as `linter-pep8`
and `linter-pep257` for the [linter](https://atom.io/users/AtomLinter/packages)
package in [Atom](http://www.atom.io/), and
[Flake8Lint](https://github.com/dreadatour/Flake8Lint) for
[Sublime Text](https://www.sublimetext.com/) (and pretty much every other IDE).


## Usage

First clone from GitHub:

``` shell
git clone https://www.github.com/cmry/markdoc
```

To use the script within terminal, simply type:

``` shell
python3 markdoc.py /dir/to/somefile.py /dir/to/somedoc.md
```

If you want to automatically generate a bunch of documentation and are not
comfortable with writing `.sh` scripts, you can use the code in Python as well:

``` python
from markdoc import MarkDoc
md = MarkDoc('/dir/to/somefile.py', '/dir/to/somedoc.md')
```

You can access the converted markdown string in:

``` python
# print markdown from class attribute
print(md.markdown)
```

The class runs itself on initialization (calls `self.read`). If you do not
want this, you can add `cold=True` to the class initialization, like so:

``` python
md = MarkDoc('file.py', 'doc.md', cold=True)
```

## Planned Fixes

- Handle consecutive classes within the same file.
- Fix inherrited classes being handled correctly (no `__init__`, no `object`).
- Link class methods from table to their documentation.
- Might not handle decorators neatly.

## Docstring Issues

Some caveats:

- Do not use `"""` for anything other than docstrings.
- First line of any docstring has to contain the first short title
  ([example](https://github.com/cmry/markdoc/blob/master/markdoc.py#L162)).
- Classes have to be structured new-style: `class SomeClass(object):`.
- Codeblocks in examples have to be vanilla Python (`>>>` and `...`).
- Please do not use `class` as a parameter name!

## Notes

Script has only been tested with Python 3.4 on Ubuntu.
