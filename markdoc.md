# Docstring to Markdown


This piece of code is used within Shed (https://www.github.com/cmry/shed) to
convert sklearn-styled python docstrings to markdown. In this way, only the
code documentation needs to be editted, and the readthedocs is automatically
updated thereafter. To use it, simply type `python3 markdoc.py
somefile.py somedoc.md`. Check class help for python usage. Don't forget to
also check the class notes (they are important for docstring format
guidelines).


# MarkDoc 

``` python 
 class MarkDoc(file_in, file_out, cold=False) 
```

Documentation to Markdown.

This class converts a python file with properly formed sklearn-style
docstrings to a markdown file that can be used in for example Readthedocs
or jekyll.

| Parameters    | Type             | Doc             |
|:-------|:-----------------|:----------------|
|     file_in | str |         Python (.py) file from where the docstrings should be taken. | 
|     file_out | str |         Markdown (.md) file where the documentation should be written. | 
|     cold | boolean, optional, default False |         If you want to start the class without starting the reader, set True. | 


| Attributes    | Type             | Doc             |
|:-------|:-----------------|:----------------|
|     markdown | str |         The entire markdown file that will be appended to and written out. | 


------- 

##Examples

Use of the package should just be from commandline with `python3 markdoc.py
in.py out.md`. However, if for some reason it is required to load it as a
class, you can just do:


``` python 
 >>> from markdoc import MarkDoc
>>> d2m = MarkDoc('some/dir/file.py', '/some/otherdir/doc.md')
 
```


The string of the markdown can be accessed by:


``` python 
 >>> print(d2m.markdown)
 
```



------- 

##Notes

List of common errors and styleguide conflicts:

#### list index out of range?

- """ used for non-docstring strings.


- First Class or method Documentation line has newline after """.


Fix with: """This is the first line.


Here comes the rest.


"""
#### Class parameters not showing in code blocks?

- Class is not structed new-style (object after class).


#### Code blocks not showing?

- Code is ipython style rather than vanilla (i.e. In [1]: instead of >>>).


#### tuple index out of range?

- Mistake in var : type lists (for example var: type).


- Description also contains a :.


#### some table parts are not showing?

- Probably included some seperators in there such as : or -----.


#### methods are garbled?

- Did you name a parameter 'class' or any other matches?



--------- 

## Methods 

 
| method    | Doc             |
|:-------|:----------------|
| read | Open python code file, spit out markdown file. | 
| handle_classes | Given class docs only, write out their docs and methods. | 
| find_declaration | Find `class Bla(object):` or `def method(params):` across lines. | 
| structure_doc | Produce a structured dictionary from docstring. | 
| md_title | Handle title and text parts for main and class-specific. | 
| md_table | Place parameters and attributes in a table overview. | 
| md_code_text | Section text and/or code in the example part of the doc. | 
| md_class_method | Replace `class ...(object)` with `__init__` arguments. | 
| md_methods_doc | Merge all method elements in one string. | 
| md_class_doc | Merge all class section elements in one string. | 
 
 

### read

``` python 
    read(file_in, file_out) 
```


Open python code file, spit out markdown file.

### handle_classes

``` python 
    handle_classes(classes) 
```


Given class docs only, write out their docs and methods.

### find_declaration

``` python 
    find_declaration(lines) 
```


Find `class Bla(object):` or `def method(params):` across lines.

### structure_doc

``` python 
    structure_doc(doc) 
```


Produce a structured dictionary from docstring.

The key is the part of the documentation (name, title, params,
attributes, etc.), and value is a list of lines that make up this part.
Is used to handle the order and different parses of different sections.

| Parameters    | Type             | Doc             |
|:-------|:-----------------|:----------------|
|         doc | str |             Flat string structure of a docstring block. | 


| Returns    | Type             | Doc             |
|:-------|:-----------------|:----------------|
|         X_doc | dict |             Class or method doc, a structure dict with section; lines. | 


### md_title

``` python 
    md_title(title_part, class_line=False) 
```


Handle title and text parts for main and class-specific.

Pretty convoluted but delicate method that seperates the top part
that should not be part of the title docstring off the document,
handles correct punctuation of titles, for both classes and methods.
Also detects if there's a description under the first line.

| Parameters    | Type             | Doc             |
|:-------|:-----------------|:----------------|
|         title_part | str |             Part of the document that starts with triple qutoes and is below            any line seperators. | 
|         class_line | bool, optional, default False |             The first line of the docstring by default servers as a title            header. However, for classes it should be formed into a normal            description. Thefefore, the # marker is removed and a . is added. | 


| Returns    | Type             | Doc             |
|:-------|:-----------------|:----------------|
|         line_buffer | str |             Correctly formated markdown from the buffer. | 


### md_table

``` python 
    md_table(doc, name) 
```


Place parameters and attributes in a table overview.

The documentation parts that are typed by 'var : type \n description'
can be splitted into a table. The same holds true for a list of class
methods. These are handled by this method. Table structures are on
the top of this python file.

| Parameters    | Type             | Doc             |
|:-------|:-----------------|:----------------|
|         doc | str |             Flat string structure of a docstring block. | 
|         name | str |             Indicator for the table, can be for example Parameters or            Attributes. | 


| Returns    | Type             | Doc             |
|:-------|:-----------------|:----------------|
|         table | str |             Markdown-type table with filled rows and formatted name. | 


### md_code_text

``` python 
    md_code_text(doc, name, flat=False) 
```


Section text and/or code in the example part of the doc.

If some code related beginnings (>>>, ...) is founds buffer to code,
else we regard it as text. Record order so that multiple consecutive
blocks of text and code are possible.

| Parameters    | Type             | Doc             |
|:-------|:-----------------|:----------------|
|         doc | str |             Flat string structure of a docstring block. | 
|         name | str |             Name of the section (Examples, Notes). | 
|         flat | bool, optional, default False |             If there are no code blocks, flat can be used to stop parsing them. | 


| Returns    | Type             | Doc             |
|:-------|:-----------------|:----------------|
|         code | str |             Formatted block of fenced markdown code-snippets and flat text. | 


------- 

#### Notes

Please note that this method assumes markdown is uses so-called
fenced codeblocks that are commonly accepted by Readthedocs, Github,
Bitbucket, and Jekyll (for example with Redcarpet).


This current implementation does NOT allow for ipython styled code
examples. (In [1]: Out[1]: etc.)


### md_class_method

``` python 
    md_class_method(doc, class_parts) 
```


Replace `class ...(object)` with `__init__` arguments.

In sklearn-style, each class is represented as it's name, along with
the parameters accepted in `__init__` as its parameters, as you would
call the method in python. The markdown therefore needs to fill the
(object) tag that is assigned to classes with the `__init__` params.

| Parameters    | Type             | Doc             |
|:-------|:-----------------|:----------------|
|         doc | str |             Flat string structure of a docstring block. | 
|         class_parts | list |             List with parts that the docstring constituted of. First line            should be the class name and can therefore be replaced. | 


| Returns    | Type             | Doc             |
|:-------|:-----------------|:----------------|
|         doc | str |             Same as doc, only now (object) has been replaced with `__init__`            parameters. | 


------- 

#### Notes

Please note that this implementation assumes you're using new-style
class declarations where for example `class SomeClass:` should be
written as `class SomeClass(object):`.




### md_methods_doc

``` python 
    md_methods_doc(method_doc) 
```


Merge all method elements in one string.

This method will scan each method docstring and extract parameters,
returns and descriptions. It will append them to the method table
and link them in the doc (TODO).

| Parameters    | Type             | Doc             |
|:-------|:-----------------|:----------------|
|         method_doc | list |             Lower part of the class docstrings that holds a method docstring            per entry. | 


| Returns    | Type             | Doc             |
|:-------|:-----------------|:----------------|
|         methods | str |             Formatted markdown string with all method information. | 


------- 

#### Notes

On the bottom, dict calls are being done to order several parts of
the docstring. If you use more than Parameters and Returns, please make
sure they are added in the code there.




### md_class_doc

``` python 
    md_class_doc(class_doc) 
```


Merge all class section elements in one string.

This will piece together the descriptions contained in the docstring
of the class. Currently, they are written *below* the top of the
python file, and not put into any subfiles per class.

| Parameters    | Type             | Doc             |
|:-------|:-----------------|:----------------|
|         class_doc | str |             Flat text containing the class docstring part. | 


| Returns    | Type             | Doc             |
|:-------|:-----------------|:----------------|
|         mark_doc | str |             Markdown formatted class docstring, including all subsections. | 


------- 

#### Notes

On the bottom, dict calls are being done to order several parts of
the docstring. If you use more than Parameters, Attributes, Examples,
and Notes, please make sure they are added in the code there.


