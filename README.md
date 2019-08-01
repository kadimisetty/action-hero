[action_heroes_logo]: ./logo.svg
![Action Heroes Logo][action_heroes_logo]


![Build Status](https://camo.githubusercontent.com/550782da80dba216452e4f747237c0fee66e8510/68747470733a2f2f696d672e736869656c64732e696f2f636f766572616c6c732f636f766572616c6c732d636c69656e74732f636f766572616c6c732d707974686f6e2f6d61737465722e7376673f7374796c653d666c61742d737175617265)
![Python Version Support](https://camo.githubusercontent.com/718b0c250361d97af792b64d7499ea616a637acd/68747470733a2f2f696d672e736869656c64732e696f2f707970692f707976657273696f6e732f7079746573742d636f762e737667)
![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)
![LICENSE MIT](https://img.shields.io/github/license/kadimisetty/vuri)
![Build Status](https://camo.githubusercontent.com/2dcdb388c206e4e3776ba9c61bbb1086160c3413/68747470733a2f2f7472617669732d63692e6f72672f736561746765656b2f66757a7a7977757a7a792e7376673f6272616e63683d6d6173746572)


####

`action_heroes` is a python package that provides  
__custom argparse _Actions_ to help you manage user arguments in command line interfaces.__


## Introduction
> __Introduction__ · [Quick Usage](#quick-usage) · [Help & FAQ](#help-and-faq) · [Catalog](#catalog) · [Development](#development)

##### _Argparse, Parsers, Actions? What now??_ 🤷‍♂️

<dl>

<dt>1. argparse</dt>
<dd><code>argparse</code> is a python standard library module used to build command line interfaces.
<a href="https://docs.python.org/3/library/argparse.html">⚓︎</a>
</dd>

<dt>2. ArgumentParser</dt>
<dd><code>argparse.ArgumentParser</code> parses user arguments by inspecting the command line, converting each argument to an appropriate type and finally invoking an appropriate <code>argparse.Action</code>
<a href="https://docs.python.org/3/library/argparse.html#argparse.ArgumentParser">⚓︎</a>
</dd>


<dt>3. Action</dt>
<dd><code>argparse.Action</code> objects are used by <code>ArgumentParser</code> to represent information needed to parse arguments from the command line.
<a href="https://docs.python.org/3/library/argparse.html#action">⚓︎</a>
</dd>


<dt>4. action_heroes 💥</dt>
<dd><code>argparse.Action</code> objects are subclassable, to allow custom actions. This library, <code>action_heroes</code>, include many such custom actions that will prove their worth when dealing with accepting user arguments in your command line application.</dd>

<dd>For example, the <strong><code>FileIsWritableAction</code> automatically verifies that all file paths accepted as arguments are indeed writable.</strong> This saves you the trouble of doing that check yourself. Nice, no? <a href="#catalog">Browse the catalog</a> for more custom actions.</dd>

</dl>

Therefore __`argparse`__ + __`action_heroes`__ = 🧨

> Hey! If you like action heroes could you give it a quick __star__ ⭐️   
> I put a lot of effort into this and each lil' star brightens my day


## Quick Usage
> [Introduction](#introduction) · __Quick Usage__ · [Help & FAQ](#help-and-faq) · [Catalog](#catalog) · [Development](#development)

**1. Installation**: Use `pip` for installation

```python 
pip install action_heroes
```

**2. Quick Usage**: CLI program that counts number of lines of a file. 

```python
#line_counter.py
import argparse

from action_heroes import FileIsReadableAction


if __name__ == "__main__":
    # Create parser
    parser = argparse.ArgumentParser()

    # Add user argument "file"
    parser.add_argument("--file", action=FileIsReadableAction)

    # Parse user arguments
    args = parser.parse_args()

    if args.file:
        # Count lines in file
        with open(args.file) as f:
            print(f"{args.file} has {len(f.readlines())} lines")
    else:
        # Print usage when no arguments were supplied
        parser.print_usage()
```

Run `line_counter.py` on the command line

```bash
$ ls
line_counter.py mary.md

$ python line_counter.py --file mary.md
mary.md has 39 lines

$ python line_counter.py
usage: line_counter.py [-h] [--file FILE]

$ python line_counter.py --file nofile.md
usage: line_counter.py [-h] [--file FILE]
line_counter.py: error: argument --file: File is not readable
```

**Note**: _Supported Python versions 3.4 upwards._

## Help and FAQ
> [Introduction](#introduction) · [Quick Usage](#quick-usage) · __Help & FAQ__ · [Catalog](#catalog) · [Development](#development)

### On not capturing user argument exceptions
`ArgumentParser` has a slightly unconventional approach to handling `ArgumentError`s. Upon encountering one, it prints argument usage information, error and exits. 

I mention this, so you don't setup a `try/except` around `parser.parse_args()` to capture the exception. In order to maintain consistency with the rest of your `argparse` code, exceptions in `action_heroes` are also of type `argparse.ArgumentError`. More information can be found in [PEP 389](https://www.python.org/dev/peps/pep-0389/#id46). Since this is the expected behavior, I recommend you allow the exception to display usage information and exit.

### FAQ
<dl>
<dt>What do I need to know to use <code>action_heroes</code> in my command line application?</dt>
<dd>Vanilla <code>argparse</code> knowledge should do it.</dd>

<dt>Where can I find information about <code>argparse</code>?</dt>
<dd><code>argparse</code> is part of the <a href="https://docs.python.org/3.7/library/argparse.html#module-argparse">Python standard library</a>.</dd>

<dt>What type are the user argument exceptions?</dt>
<dd><code>argparse.ArgumentError{"helpful error message"}</code>, just like any other <code>argparse.Action</code></code></dd>

<dt>Is <code>action_heroes</code> tied to the <code>argparse</code> module?</dt>
<dd>Yes <em>(but technically no — any project that can use an <code>argpoarse.Action</code> should work as long as it handles the <code>argparse.ArgumentError</code> exception)</em></dd>

<dt>I don't want to learn another library. I already know <code>argparse</code>!</dt>
<dd><code>action_heroes</code> can be used just like any other <code>argparse.Action</code>, so feel free to take advantage.</dd>

<dt>There was no mention of humans! Does this work for humans?</dt>
<dd>Yes, yes it works for humans :)</dd>
</dl>


## Catalog
> [Introduction](#introduction) · [Quick Usage](#quick-usage) · [Help & FAQ](#help-and-faq) · __Catalog__ · [Development](#development)

Example of importing an action  
`from action_heroes import FileIsReadableAction `


### Path
Contains Actions related to _paths, directories and files_

| Action | Description | Arguments |
| --- | --- | --- |
| DirectoryDoesNotExistAction | | |
| DirectoryExistsAction | | |
| DirectoryIsExecutableAction | | |
| DirectoryIsNotExecutableAction | | |
| DirectoryIsNotReadableAction | | |
| DirectoryIsNotWritableAction | | |
| DirectoryIsReadableAction | | |
| DirectoryIsValidAction | | |
| DirectoryIsWritableAction | | |
| EnsureDirectoryAction | | |
| EnsureFileAction | | |
| FileDoesNotExistAction | | |
| FileExistsAction | | |
| FileHasExtension | | |
| FileIsEmptyAction | | |
| FileIsExecutableAction | | |
| FileIsNotEmptyAction | | |
| FileIsNotExecutableAction | | |
| FileIsNotReadableAction | | |
| FileIsNotWritableAction | | |
| FileIsReadableAction | | |
| FileIsValidAction | | |
| FileIsWritableAction | | |
| PathDoesNotExistsAction | | |
| PathExistsAction | | |
| PathIsExecutableAction | | |
| PathIsNotExecutableAction | | |
| PathIsNotReadableAction | | |
| PathIsNotWritableAction | | |
| PathIsReadableAction | | |
| PathIsValidAction | | |
| PathIsWritableAction | | |
| ResolvePathAction | | |


### Net
Contains Actions related to networks

| Action | Description | Arguments |
| --- | --- | --- |
| IPIsValidIPAddressAction | | |
| IPIsValidIPAddressAction | | |
| IPIsValidIPv4AddressAction | | |
| IPIsValidIPv6AddressAction | | |
| URLIsNotReachableAction | | |
| URLIsReachableAction | | |
| URLWithHTTPResponseStatusCodeAction | | |


### Types
Contains Actions related to types

| Action | Description | Arguments |
| --- | --- | --- |
| IsConvertibleToFloatAction | | |
| IsConvertibleToIntAction | | |
| IsConvertibleToUUIDAction | | |
| IsFalsyAction | | |
| IsTruthyAction | | |


### Range
Contains Actions related to ranges

| Action | Description | Arguments |
| --- | --- | --- |


### Email
Contains Actions related to emails

| Action | Description | Arguments |
| --- | --- | --- |
| EmailIsValidAction | | |


## Development
> [Introduction](#introduction) · [Quick Usage](#quick-usage) · [Help & FAQ](#help-and-faq) · [Catalog](#catalog) · __Development__

### Notes
- __Formatting__-: _PEP8 only. Please format with  black using `black_linelength=79`_
- __License__: _The MIT License_
- __Image Attributions__: _Karate by Alex Auda Samora from the Noun Project_

### Roadmap
1. Configurable exception type. eg. ValueError/ArgumentError etc.
2 More Actions.
3 Reference with Sphinx docs + github pages on a seperate branch.
4 More examples.
5 Proper repo things.

> Thank you for using `action_heroes`.  
> If you have any ideas for more actions, please leave a github issue. 💥  
> And if you like what you see, a ⭐️ would be much appreciated!
