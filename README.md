[action_hero_logo]: ./art/logo.svg
![Action Hero Logo][action_hero_logo]


![PyPI - Python Version](https://img.shields.io/pypi/pyversions/action-hero?style=flat-square)
![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)
![PyPI - License](https://img.shields.io/pypi/l/action-hero?style=flat-square)
[![Build Status](https://travis-ci.org/kadimisetty/action-hero.svg?branch=master)](https://travis-ci.org/kadimisetty/action-hero)
[![PEP8](https://img.shields.io/badge/code%20style-pep8-green.svg)](https://www.python.org/dev/peps/pep-0008/)
[![codecov](https://codecov.io/gh/kadimisetty/action-hero/branch/master/graph/badge.svg)](https://codecov.io/gh/kadimisetty/action-hero)

####

`action_hero` is a python package that helps you  
__manage user arguments in command line applications using `argparse`__ 


[Introduction](#introduction) · [Quick Usage](#quick-usage) · [Help & FAQ](#help-and-faq) · [Catalog](#catalog) · [Development](#development)

## Introduction

<dl>

<dt><code>argparse</code></dt>
<dd><code>argparse</code> is a python standard library module used to make
command line applications.
<code>argparse</code> provides
<code>ArgumentParser</code> that parses user arguments and runs
<code>argparse.Action</code>s on them.
<a href="https://docs.python.org/3/library/argparse.html">⚓︎</a>
</dd>


<dt><code>action_hero</code> 🔥</dt>
<dd><code>action_hero</code> makes <code>argparse</code> more capable by
providing a large number of custom actions. For example, the
<strong><code>FileIsWritableAction</code> automatically verifies that file
path(s) accepted as arguments are writable, informing the user if they
aren't.</strong> This saves you the trouble of doing that check yourself. Nice,
no? <a href="#catalog">Browse the catalog</a> for many such actions.</dd>

</dl>




## Quick Usage

__1. Installation__:

```python 
pip install action_hero
```

__2. Quick Usage__: Import an action and specify it when adding an argument to your parser.

```python 
from action_hero import FileIsReadableAction
...
parser.add_argument("--file", action=FileIsReadableAction)
...
```

__3. Full Example__: CLI program that counts number of lines of a file. 

```python
# examples/line_counter.py
import argparse

from action_hero import FileIsReadableAction


if __name__ == "__main__":

    # Create parser
    parser = argparse.ArgumentParser()

    # Add user argument "--file" and assert that it will be readable
    parser.add_argument("--file", action=FileIsReadableAction)

    # Parse user arguments
    args = parser.parse_args()

    if args.file:
        # Print number of lines in file
        with open(args.file) as f:
            print("{} has {} lines".format(args.file, len(f.readlines())))
    else:
        # Print usage if no arguments were given
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

**Note**: _Supported Python Versions >= 3.5_

## Help and FAQ

### Accepting `action_values`
There are times your action requires an additional value. For instance, when your argument accepts only filenames with `md` or `markdown` extensions. You can use the `FileHasExtension` action for this and pass in the extensions to check for via `action_values`, like so — 

```python
parser.add_argument(
    "--file", 
    action=FileHasExtension, 
    action_values=["md", "markdown"]
)

```

Unless otherwise mentioned,  `action_values` should be provided as a non-empty
list of strings. e.g.
`action_values = ["md", "markdown"]`.


### Pipelining multiple actions

The `PipelineAction` allows you to run multiple actions as a pipeline. Pass in
your pipeline of actions as a list to `action_values`. If one of the actions
you're passing in has it's own `action_values`, put that one as a tuple, like
such: `(FileHasExtension, ["md", "markdown"])`. Here's an example of
pipelining actions for `--file` 

1. File has extensions `md` or `markdown`
2. File exists

```python
parser.add_argument(
    "--file", 
    action=PipelineAction, 
    action_values=[
        (FileHasExtension, ["md", "markdown"]),
        FileExistsAction
    ]
)
```

Another helpful feature, this action provides is the _order of error
reporting_.  In the above example, if the supplied argument file did not have
the markdown extensions, the error message would reflect that and exit.  After
the user redoes the entry with a valid filename the next action in the pipeline
applies `FileExistsAction` which checks for existence.  If the file does not
exist, an error message about file not existing will be shown and exits
allowing the user to try again.

This behavior can save you a lot of manual condition checks later on. For
example, here's how to check for an _existing, writable, non-empty_, markdown
file —

```python
parser.add_argument(
    "--file", 
    action=PipelineAction, 
    action_values=[
        FileExistsAction, 
        FileIsWritableAction,
        FileIsNotEmptyAction,
        (FileHasExtension, ["md", "markdown"])
]
```

### Exceptions in this module
You'll come across two different exceptions in `action_hero`.

1. __`ValueError`__: These are intended for you, the CLI developer. You'd want
   to fix any underlying issue that causes them before releasing your CLI.
   e.g. when `action_values` is an empty list.

2. __`argparse.ArgumentError`__: These are intended for your CLI's users, so
   they might use the messages as hints to provide corrent command line
   options.

### Not capturing user argument exceptions
`argparse.ArgumentParser` has a slightly unconventional approach to handling
`argparse.ArgumentError`s. Upon encountering one, it prints argument usage
information, error and exits. I mention this, so you don't setup a `try/except`
around `parser.parse_args()` to capture that exception. 

In order to maintain consistency with the rest of your `argparse` code,
exceptions in `action_hero` are also of type `argparse.ArgumentError` and
causes system exit as well. More information can be found in [PEP
389](https://www.python.org/dev/peps/pep-0389/#id46). Since this is
expected behavior, I recommend you allow this exception and let it display usage
information and exit.

### Arguments accepting multiple values
Just like any other `argparse.Action` each `action_hero.Action` handles
multiple values and provides relevant error messages.

### FAQ
<dl>
<dt>What do I need to know to use <code>action_hero</code> in my command line application?</dt>
<dd>Vanilla <code>argparse</code> knowledge should do it.</dd>

<dt>Where can I find information about <code>argparse</code>?</dt>
<dd><code>argparse</code> is part of the <a href="https://docs.python.org/3.7/library/argparse.html#module-argparse">Python standard library</a>.</dd>

<dt>Is <code>action_hero</code> tied to the <code>argparse</code> module?</dt>
<dd>Yes <em>(but technically no — any project that can use an <code>argpoarse.Action</code> should work as long as it handles the <code>argparse.ArgumentError</code> exception)</em></dd>

<dt>What type are the user argument exceptions?</dt>
<dd><code>argparse.ArgumentError{"helpful error message"}</code>, just like any other <code>argparse.Action</code></code></dd>

<dt>Why re-implement actions already provided by `argparse` like the `choices` action?</dt>
<dd>In order to include them in `PipelineAction`.</dd>

<dt>There was no mention of humans! Does this work for humans?</dt>
<dd>Yes, it works for humans :)</dd>
</dl>


## Catalog


1. __Special__ actions:

| Action | Description | `action_values` |
| --- | --- | --- |
| __`PipelineAction`__ | Run multiple actions as a pipeline | Actions to run as a pipeline. e.g. `[FileExistsAction, FileIsWritableAction]`. ([Read more](#pipelining-multiple-actions)) |
| __`DebugAction`__ | Print debug information. There can be multiple of these in a pipeline | |

2. __Path, Directory and File__ related actions:

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
| __`EnsureDirectoryAction`__<sup>*</sup> | Ensure directory exists and create it if it doesnt | |
| __`EnsureFileAction`__<sup>*</sup> | Ensure file exists and create it if it doesnt | |
| __`FileDoesNotExistAction`__ | Check if file doesnt exist | |
| __`FileExistsAction`__ | Check if file exists | |
| __`FileIsEmptyAction`__ | Check if file is empty | |
| __`FileIsExecutableAction`__ | Check if file is executable | |
| __`FileIsNotEmptyAction`__ | Check if file is not empty | |
| __`FileIsNotExecutableAction`__ | Check if file is not executable | |
| __`FileIsNotReadableAction`__ | Check if file is not readable | |
| __`FileIsNotWritableAction`__ | Check if file is not writable | |
| __`FileIsReadableAction`__ | Check if file is readable | |
| __`FileIsValidAction`__ | Check file is valid | |
| __`FileIsWritableAction`__ | Check if file is writable | |
| __`FileHasExtension`__ | Check if file has specified extension | Extensions to check against. e.g. `["md", "markdown"]` |
| __`PathDoesNotExistsAction`__ | Check if path does not exist | |
| __`PathExistsAction`__ | Check if path exists | |
| __`PathIsExecutableAction`__ | Check if path is executable | |
| __`PathIsNotExecutableAction`__ | Check if path is not executable | |
| __`PathIsNotReadableAction`__ | Check if path is not writable | |
| __`PathIsNotWritableAction`__ | Check if path is not writable | |
| __`PathIsReadableAction`__ | Check if path is readable | |
| __`PathIsValidAction`__ | Check if path is valid | |
| __`PathIsWritableAction`__ | Check if path is writable | |
| __`ResolvePathAction`__<sup>†</sup> | Resolves path to canonical path removing symbolic links if present | |


3. __Net & Email__ related actions:

| Action | Description | `action_values` |
| --- | --- | --- |
| __`IPIsValidIPAddressAction`__ | Check if ip is valid ipv4 or ipv6 address | |
| __`IPIsValidIPv4AddressAction`__ | Check if ip address is valid ipv4 address | |
| __`IPIsValidIPv6AddressAction`__ | Check if ip address is valid ipv6 address | |
| __`URLIsNotReachableAction`__ | Check if URL is not reachable | |
| __`URLIsReachableAction`__ | Check if URL is reachable | |
| __`URLWithHTTPResponseStatusCodeAction`__ | Check if upplied URL responds with expected HTTP response status code | [Status codes](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status) to check against. e.g. `["200", "201", "202", "204"]`  |
| __`EmailIsValidAction`__ | Checks if email address is valid | |


4. __Type__ related actions:

| Action | Description | `action_values` |
| --- | --- | --- |
| __`IsConvertibleToFloatAction`__ | Check if value is convertible to float | |
| __`IsConvertibleToIntAction`__ | Check if value is convertible to int | |
| __`IsConvertibleToUUIDAction`__ | Checks if value is convertible to UUID | |
| __`IsFalsyAction`__ | Checks if value is falsy | |
| __`IsTruthyAction`__ | Checks if value is truthy | |

5. __Range__ related actions:

| Action | Description | `action_values` |
| --- | --- | --- |

6. __Miscellaneous__ actions:

| Action | Description | `action_values` |
| --- | --- | --- |
| __`ChoicesAction`__ | Argument can only have values from provided choice(s)  | Choices e.g. `["red", "blue", "green"]` |
| __`NotifyAndContinueAction`__ | Print provided notification message(s) | Message(s) e.g. `["This command will be deprecated in the next version."]` |
| __`NotifyAndExitAction`__ | Print provided notification message(s) and Exit | Message(s) e.g. `["This command has been deprecated", "Try --new-command"]` |
| __`ConfirmAction`__ | Print provided message and proceed with user confirmation _yes or no_. | Message(s) e.g. `["Proceed to Installation? (Y/n)"]` |
| __`GetInputAction`__<sup>†</sup> | Get user input and save to `self.dest`  | Message(s) e.g. `["Favorite color"]` |
| __`GetSecretInputAction`__<sup>†</sup> | Get user input without displaying characters and save to the `self.dest`  | Message(s) e.g. `["Enter your Password"]` |
| __`LoadJSONFromFileAction`__<sup>†</sup> | Return loaded JSON file(s) |  |
| __`LoadYAMLFromFileAction`__<sup>†</sup> | Return loaded YAML file(s) |  |
| __`LoadPickleFromFileAction`__<sup>†</sup> | Return unpickled file(s) |  |
| __`CollectIntoDictAction`__<sup>†</sup> | Collect values into a dict | Delimiter(s) to split value(s) into key:value pair(s) e.g. `[":", "="]` (If multiple delimiters exist inside a value, only the first match is used) |
| __`CollectIntoListAction`__<sup>†</sup> | Collect values into a list |  |
| __`CollectIntoTupleAction`__<sup>†</sup> | Collect values into a tuple |  |


<strong><sup>*</sup></strong> Actions that can make changes to disk  
<strong><sup>†</sup></strong> Actions that can make changes to `self.dest`


## Development

### Notes
- __Formatting__-: _PEP8 only. Please format with black using `black_linelength=79`_
- __License__: _The MIT License_
- __Image Attributions__: _Karate by Alex Auda Samora from the Noun Project_

Thank you for using `action_hero` — [@kadimisetty](https://github.com/kadimisetty) ⭐️✨
