# MarkDoc

This piece of code can be used to convert
[sklearn](https://www.scikit-learn.org/)-styled python docstrings (example) to
markdown. In this way, only the code-contained documentation needs to be
editted, and your documentation on for example [
readthedocs]('http://www.readthedocs.org/') can be automatically updated
thereafter with some configuration.

## Usage

To use the script within terminal, simply type:

``` shell
python3 doc2md.py /dir/to/somefile.py /dir/to/somedoc.md
```

If you want to automatically generate a bunch of documentation and are not
comfortable with writing `.sh` scripts, you can use the code in python as well:

``` python
from doc2md import Doc2Markdown
d2m = Doc2Markdown('/dir/to/somefile.py', '/dir/to/somedoc.md')
```

You can access the converted markdown string in:

``` python
d2m.markdown
```

The class runs itself on initialization (calls `self.read`). If you do not
want this, you can add `cold=True` to the class initialization, like so:

``` python
d2m = Doc2Markdown('file.py', 'doc.md', cold=True)
```

## Docstring Requirements

Docstrings are assumed to be styled according to **both** PEP8 and PEP257. If
you need examples on how to structure these, just check the docstrings of
`doc2md.py`. Some other caveats:

- Do not use `"""` for anything other than docstrings.
- First line of a any docstring has to contain the first short title ([example]()).
- Classes have to be structured new-style: `class SomeClass(object):`.
- Codeblocks in examples have to be vanilla python (`>>>` and `...`).
- Please do not use `class` as a parameter name!
