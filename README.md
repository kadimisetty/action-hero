[action_heroes_logo]: ./logo.svg
![Action Heroes Logo][action_heroes_logo]


![Build Status](https://camo.githubusercontent.com/550782da80dba216452e4f747237c0fee66e8510/68747470733a2f2f696d672e736869656c64732e696f2f636f766572616c6c732f636f766572616c6c732d636c69656e74732f636f766572616c6c732d707974686f6e2f6d61737465722e7376673f7374796c653d666c61742d737175617265)
![Python Version Support](https://camo.githubusercontent.com/718b0c250361d97af792b64d7499ea616a637acd/68747470733a2f2f696d672e736869656c64732e696f2f707970692f707976657273696f6e732f7079746573742d636f762e737667)
![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)
![LICENSE MIT](https://img.shields.io/github/license/kadimisetty/vuri)
![Build Status](https://camo.githubusercontent.com/2dcdb388c206e4e3776ba9c61bbb1086160c3413/68747470733a2f2f7472617669732d63692e6f72672f736561746765656b2f66757a7a7977757a7a792e7376673f6272616e63683d6d6173746572)


####

`action_heroes` is a python package that provides 
__custom argparse _Actions_ to help you write command line interfaces.__


## Introduction
> __[Introduction](#introduction)__ · [Quick Usage](#quick-usage) · [Help & FAQ](#help-and-faq) · [Catalog](#catalog) · [Development](#development)

##### 🤷‍♂️ Argparse, Parsers, Actions ? What now ??

<dl>

<dt>1. argparse</dt>
<dd><code>argparse</code> is a python standard library module used to build command line interfaces that accept user arguments.
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

<dd>For example, the <strong><code>FileIsWritableAction</code> automatically verifies that all file paths accepted as arguments are indeed writable.</strong> This saves you the trouble of coding that check yourself. Nice, no? <a href="#catalog">Browse the catalog</a> for more custom actions.</dd>

</dl>

> Hey! If you like action heroes could you give it a quick __star__ ⭐️   
> I put a lot of effort into this and each lil' star brightens my day


## Quick Usage
> [Introduction](#introduction) · __[Quick Usage](#quick-usage)__ · [Help & FAQ](#help-and-faq) · [Catalog](#catalog) · [Development](#development)

- Use `pip` to install `action_heroes` 


```python
pip install action_heroes
```


## Help and FAQ
> [Introduction](#introduction) · [Quick Usage](#quick-usage) · __[Help & FAQ](#help-and-faq)__ · [Catalog](#catalog) · [Development](#development)

### FAQ
<dl>
<dt>There was no mention of humans! Does this work for humans™?</dt>
<dd>Yeah, yeah it works for humans :)</dd>

<dt>What do I need to know to use <code>action_heroes</code> in my command line application?</dt>
<dd>Vanilla <code>argparse</code> knowledge should do it.</dd>

<dt>What type are user argument exceptions going to bubble up as?</dt>
<dd><code>argparse.ArgumentError{"helpful error message"}</code></dd>

<dt>Is <code>action_heroes</code> tied to the <code>argparse</code> module?</dt>
<dd>Technically no. Any project that can use an <code>argpoarse.Action</code> should work.Do have a way to hadle the exception type <code>argparse.ArgumentError</code> though.</dd>

<dt>I don't want to learn another library. I already know <code>argparse.ArgumentParser</code>!</dt>
<dd>Great! You know the concepts then. <code>action_heroes</code> can pretty much just be used like any other `argparse.Action`.</dd>
</dl>


## Catalog
> [Introduction](#introduction) · [Quick Usage](#quick-usage) · [Help & FAQ](#help-and-faq) · __[Catalog](#catalog)__ · [Development](#development)


## Development
> [Introduction](#introduction) · [Quick Usage](#quick-usage) · [Help & FAQ](#help-and-faq) · [Catalog](#catalog) · __[Development](#development)__
