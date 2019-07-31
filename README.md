[action_heroes_logo]: ./logo.svg
![Action Heroes Logo][action_heroes_logo]


 <!--SHIELD:  COVERAGE --> [![Build Status](https://camo.githubusercontent.com/550782da80dba216452e4f747237c0fee66e8510/68747470733a2f2f696d672e736869656c64732e696f2f636f766572616c6c732f636f766572616c6c732d636c69656e74732f636f766572616c6c732d707974686f6e2f6d61737465722e7376673f7374796c653d666c61742d737175617265)]()
<!--SHIELD:  CODESTYLE -->[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/python/black) 
<!--SHIELD:  LICENSE [![Code style: black](https://img.shields.io/github/license/kadimisetty/vuri)](https://github.com/python/black) -->
<!--SHIELD:  PYTHONv --> [![Python Version Support](https://camo.githubusercontent.com/718b0c250361d97af792b64d7499ea616a637acd/68747470733a2f2f696d672e736869656c64732e696f2f707970692f707976657273696f6e732f7079746573742d636f762e737667)]() 
<!--SHIELD:  BUILD STATUS -->[![Build Status](https://camo.githubusercontent.com/2dcdb388c206e4e3776ba9c61bbb1086160c3413/68747470733a2f2f7472617669732d63692e6f72672f736561746765656b2f66757a7a7977757a7a792e7376673f6272616e63683d6d6173746572)]()




####

`action_heroes` is a python package that provides a bunch of   
__custom argparse _Actions_ to help you write command line interfaces.__


>  Contents — [Introduction](#introduction) · __[Quick Usage](#quick-usage)__ · [Help](#help) · [FAQ](#faq) · [Catalog](#catalog) · [Development](#development)



## Introduction

🤷‍♂️ _Argparse, Parsers, Actions ? What now ??_

<dl>

<dt>1. argparse</dt>
<dd><code>argparse</code> is a python module, in the python standard library, used to build command line interfaces that accept user arguments.
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

<dd>For example, the <code>action_hero.FileIsWritableAction</code> <strong>automatically verifies that all file paths accepted as arguments are indeed writable.</strong> This saves you the trouble of coding that check yourself. Nice, no? <a href="#catalog">Browse the catalog</a> for more custom actions.</dd>

</dl>

> Hey! If you like action heroes could you give it a quick __star__ ⭐️   
> I put a lot of effort into this and each lil' star makes my day — @kadimisetty


## Quick Usage

- Use `pip` to install `action_heroes` 


```python
pip install action_heroes
```

## Help and Usage
## Catalopg
## Screencast

