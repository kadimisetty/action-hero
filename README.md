[action_heroes_logo]: ./art/logo.svg
![Action Heroes Logo][action_heroes_logo]


[![codecov](https://codecov.io/gh/kadimisetty/action-heroes/branch/master/graph/badge.svg?token=7myLPPQe8k)](https://codecov.io/gh/kadimisetty/action-heroes)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/action_heroes)
![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)
![PyPI - License](https://img.shields.io/pypi/l/action_heroes)
[![Build Status](https://travis-ci.org/kadimisetty/action-heroes.svg?branch=master)](https://travis-ci.org/kadimisetty/action-heroes)


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

<dd>For example, the <strong><code>FileIsWritableAction</code> automatically verifies that all file paths accepted as arguments are indeed writable, informing the user if they aren't.</strong> This saves you the trouble of doing that check yourself. Nice, no? <a href="#catalog">Browse the catalog</a> for more custom actions.</dd>

</dl>

Therefore __`argparse`__ + __`action_heroes`__ = 🧨


## Quick Usage
> [Introduction](#introduction) · __Quick Usage__ · [Help & FAQ](#help-and-faq) · [Catalog](#catalog) · [Development](#development)

__1. Installation__: Use `pip` for installation

```python 
pip install action_heroes
```

__2. Quick Usage__: Import an action and specify it when adding an argument to your parser.

```python 
from action_heroes import FileIsReadableAction
...
parser.add_argument("--file", action=FileIsReadableAction)
...
```

__3. Full Example__: CLI program that counts number of lines of a file. 

```python
# examples/line_counter.py
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
            # print(f"{args.file} has {len(f.readlines())} lines")
            print("{} has {} lines".format(args.file, len(f.readlines())))
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

**Note**: _Supported Python versions 3.6 upwards._

## Help and FAQ
> [Introduction](#introduction) · [Quick Usage](#quick-usage) · __Help & FAQ__ · [Catalog](#catalog) · [Development](#development)

### On accepting `action_values`
There are times your action requires an additional value. For instance, when your argument accepts only filenames with `md` or `markdown` extensions. You can use the `FileHasExtension` action for this and pass in the extensions to check for via `action_values`, like so — 

```python
parser.add_argument("--filename", action=FileHasExtension, action_values=["md", "markdown"])

```

### On not capturing user argument exceptions
`argparse.ArgumentParser` has a slightly unconventional approach to handling `argparse.ArgumentError`s. Upon encountering one, it prints argument usage information, error and exits. I mention this, so you don't setup a `try/except` around `parser.parse_args()` to capture the exception. 

In order to maintain consistency with the rest of your `argparse` code, exceptions in `action_heroes` are also of type `argparse.ArgumentError`. More information can be found in [PEP 389](https://www.python.org/dev/peps/pep-0389/#id46). Since this is the expected behavior, I recommend you allow the exception to display usage information and exit as well.

### On arguments accepting multiple values
Just like any other `argparse.Action` each `action_hero.Action` handles both singular and plural values with error messages customized for that as well.

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

__Note__: `action_values` should be provided as a non-empty list of strings. e.g.
`action_values = ["md", "markdown"]`. See [help section on action_values](#accepting-action_values) for more


1. __Path, Directory and File__ related actions:

| Action | Description | `action_values` |
| --- | --- | --- |
| __`DirectoryDoesNotExistAction`__ | Check if directory does not exist | |
| __`DirectoryExistsAction`__ | Check if directory exists | |
| __`DirectoryIsExecutableAction`__ | Check if directory is executable | |
| __`DirectoryIsNotExecutableAction`__ | Check if directory is not executable | |
| __`DirectoryIsNotReadableAction`__ | Check if directory is not readable | |
| __`DirectoryIsNotWritableAction`__ | Check if directory is not writable | |
| __`DirectoryIsReadableAction`__ | Check if directory is readable | |
| __`DirectoryIsValidAction`__ | Check directory is valid | |
| __`DirectoryIsWritableAction`__ | Check if directory is writable | |
| __`EnsureDirectoryAction`__ | Ensure directory exists and create it if it doesnt | |
| __`EnsureFileAction`__ | Ensure file exists and create it if it doesnt | |
| __`FileDoesNotExistAction`__ | Check if file doesnt exist | |
| __`FileExistsAction`__ | Check if file exists | |
| __`FileHasExtension`__ | Check if file has specified extension | Extensions to check against. e.g. `["md", "markdown"]` |
| __`FileIsEmptyAction`__ | Check if file is empty | |
| __`FileIsExecutableAction`__ | Check if file is executable | |
| __`FileIsNotEmptyAction`__ | Check if file is not empty | |
| __`FileIsNotExecutableAction`__ | Check if file is not executable | |
| __`FileIsNotReadableAction`__ | Check if file is not readable | |
| __`FileIsNotWritableAction`__ | Check if file is not writable | |
| __`FileIsReadableAction`__ | Check if file is readable | |
| __`FileIsValidAction`__ | Check file is valid | |
| __`FileIsWritableAction`__ | Check if file is writable | |
| __`PathDoesNotExistsAction`__ | Check if path does not exist | |
| __`PathExistsAction`__ | Check if path exists | |
| __`PathIsExecutableAction`__ | Check if path is executable | |
| __`PathIsNotExecutableAction`__ | Check if path is not executable | |
| __`PathIsNotReadableAction`__ | Check if path is not writable | |
| __`PathIsNotWritableAction`__ | Check if path is not writable | |
| __`PathIsReadableAction`__ | Check if path is readable | |
| __`PathIsValidAction`__ | Check if path is valid | |
| __`PathIsWritableAction`__ | Check if path is writable | |
| __`ResolvePathAction`__ | Resolves path to canonical path removing symbolic links if present | |


2. __Network__ related actions:

| Action | Description | `action_values` |
| --- | --- | --- |
| __`IPIsValidIPAddressAction`__ | Check if ip is valid ipv4 or ipv6 address | |
| __`IPIsValidIPv4AddressAction`__ | Check if ip address is valid ipv4 address | |
| __`IPIsValidIPv6AddressAction`__ | Check if ip address is valid ipv6 address | |
| __`URLIsNotReachableAction`__ | Check if URL is not reachable | |
| __`URLIsReachableAction`__ | Check if URL is reachable | |
| __`URLWithHTTPResponseStatusCodeAction`__ | Check if upplied URL responds with expected HTTP response status code | [Status codes](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status) to check against. e.g. `["200", "201", "202", "204"]`  |



3. __Type__ related actions:

| Action | Description | `action_values` |
| --- | --- | --- |
| __`IsConvertibleToFloatAction`__ | Check if value is convertible to float | |
| __`IsConvertibleToIntAction`__ | Check if value is convertible to int | |
| __`IsConvertibleToUUIDAction`__ | Checks if value is convertible to UUID | |
| __`IsFalsyAction`__ | Checks if value is falsy | |
| __`IsTruthyAction`__ | Checks if value is truthy | |


4. __Range__ related actions:

| Action | Description | `action_values` |
| --- | --- | --- |


5. __Email__ related actions:

| Action | Description | `action_values` |
| --- | --- | --- |
| __`EmailIsValidAction`__ | Checks if email address is valid | |


## Development
> [Introduction](#introduction) · [Quick Usage](#quick-usage) · [Help & FAQ](#help-and-faq) · [Catalog](#catalog) · __Development__

### Notes
- __Formatting__-: _PEP8 only. Please format with  black using `black_linelength=79`_
- __License__: _The MIT License_
- __Image Attributions__: _Karate by Alex Auda Samora from the Noun Project_

### Roadmap
1. Configurable exception type. e.g. ValueError/ArgumentError etc.
2. More Actions.
3. Reference with Sphinx docs + github pages on a seperate branch.
4. More examples.
5. Proper repo things.

> Thank you for using `action_heroes`.  
> If you like action heroes do give it a quick __star__ ⭐️ Will be much appreciated!
