# Design

PyperCard has a certain design outlook and philosophy. In many ways its aims
are not typical for a GUI framework, and we hope this page will both explain
and illustrate our objectives.

The summary is...

## PyperCard is for beginners

Who are beginners?

You're a beginner if you find yourself asking how to make stuff happen with
PyperCard. A classic example being, how do I play a sound in PyperCard? You may
even find missing features in PyperCard (I'd like to play a video in
PyperCard!), in which case, please
[submit an issue](https://github.com/pyscript/pypercard/issues/new) while
remembering to follow our [contributing guidelines](contributing.md) and
[code of conduct](code_of_conduct.md). But once you know how to make stuff
happen with PyperCard, you're able to build all sorts of interesting things
that reflect your interests and outlook.

However, if you're asking questions about technical features of PyperCard, such
as, why does PyperCard use the JavaScript `Audio` class
like _this_ rather than like _that_?, then you're probably not a beginner.
However, we'd love to invite you to contribute to PyperCard if you spot ways to
_enhance the experience of beginners_.

This is _inclusive coding for the 99%_.

```{tip}
If you just want some deeply technical capability that PyperCard doesn't
provide, you should probably try another framework that supports that
capability rather than try to force it into PyperCard.

Clearly, you're one of the programming 1%!

Nevertheless we do hope you consider helping us improve the experience of
beginners, by sharing your expertise with the project.
```

## What PyperCard is

* **Simple** - PyperCard doesn't need a lot to _make stuff happen_.
* **Expressive** - you can do _lots of different stuff_ with PyperCard.
* **Empowering** - PyperCard helps _assemble stuff_ so you get _what you want_.
* **Teachable** - it's easy to _explain and learn stuff_ with PyperCard. 
* **Fun** - it _feels good to make stuff_ with PyperCard.

## What PyperCard is NOT

* **Comprehensive** - rather, we try to implement _most_ of the features,
  _most_ beginners want, _most_ of the time.
* **Fast** - rather, we prefer to use Python because it is an _easy-to-learn
  and widely used_ programming language.
* **Flexible** - rather, we expect our pragmatic
  _stack-of-cards-with-transitions_ paradigm to be _good enough most of the
  time_.
* **Opaque** - rather, you don't need to be a programmer to _get started and
  building stuff in only minutes_.
* **Hard** - rather, we concede that some stuff is deeply challenging and you
  should _use something else if PyperCard doesn't work for you_.

## Personas

To help orientate folks contributing to PyperCard, we've created a quartet of
personas that illustrate the diversity of "beginner" coders we hope to help
with our project.

Each persona has three sections:

1. an introduction that explains who they are,
2. a description of how they're using PyperCard, and,
3. any mitigating circumstances about their use of PyperCard.

The persona images were made via a stable diffusion based tool for generating
faces.

_These people do not exist_!

### Alejando 🇲🇽
![](_static/persona_alejandro.png)

Alejandro is 12 years old, lives in Mexico and is learning how to code in his
after school computer club.

His teacher, Miss.Perez, has asked him to create a simple game with PyperCard
in a choose-your-own-adventure style. Alejando is only too pleased with this
project since he has lots of story ideas based in the Star Wars universe.

Alejandro doesn't speak English, but Miss.Perez has created resources in
Spanish, based on the PyperCard documentation and tutorials. He builds and
hosts his PyperCard projects via [PyScript.com](https://pyscript.com/).

### Ash 🇬🇧
![](_static/persona_ash.png)

Ash, 29, works as a back-end Python engineer at a hedge fund in the City of
London. They are part of a team responsible for ensuring the right information
and alerts get to the right colleagues as market conditions change throughout
the day. Most of their Python work is related to data science and the Python
tooling needed to create the bespoke and commercially sensitive information
used by their colleagues.

They often need to direct non-technical colleagues to specialist sources of
information, and to this end Ash has used PyperCard to create a simple wizard
like app to signpost and track the usage of internal services, depending on
user role and need. Ash hopes to follow this up with another PyperCard app that
allows traders to read financial alerts consumed from an internally developed
news API.

Ash, as an experienced developer who is already familiar with Python, was drawn
to the ease with which UI driven apps could be created by folks with little or
no frontend experience. They were up and running within an hour, after reading
the [cheatsheet](cheatsheet.md) and skimming the relevant sections of the
[tutorials](tutorials.md). It took just three days for them to produce the
wizard app for internal colleagues, and they presented their work to the wider
engineering teams in the company, as part of a lunchtime technical "brown bag"
session. They also suggested a couple of documentation changes as PRs to the
PyperCard repository and have been active on the project
[discord channel](https://discord.gg/TKyjvSynTP). They intend to suggest
PyperCard's use in an upcoming London Python Code Dojo session.

### Hasan 🇹🇷
![](_static/persona_hasan.png)

Hasan, 67, is an amateur tech enthusiast and restaurant owner from Selçuk,
Turkey.

Never shy of embracing technology, he's decided to write a multi-lingual
PyperCard app that acts as the menu for guests at his restaurant. He's famous
among his friends for experimenting with new technology. For instance, he's
been using spreadsheets for managing stock and accounting since Windows 3.1 and
recently embraced a take-away food delivery app to increase the reach
of his restaurant (the inspiration and template for his own menu
app).

He started to learn Python as a personal project during the COVID
pandemic (his daughter-in-law is a Python programmer in Istanbul, and suggested
he look at PyperCard). Because of the tourist trade, he has relatively good
English and is working his
way through the PyperCard tutorials while putting together his ideas for the
menu app for his restuarant. He likes using Python, appreciates that
PyperCard works on all his customer's devices (thanks to MicroPython), and is
pleased his rusty HTML skills can be used for generating the user interface.

### Mandisa 🇿🇦
![](_static/persona_mandisa.png)

Mandisa, 42, is a high school teacher in a girl's school in Claremont, Cape
Town, South Africa. She is a subject matter specialist for computing and is
responsible for developing and delivering the programming curriculum for
students aged between 11-16.

She first heard of PyperCard from a tutorial given at PyCon Africa in
Ghana, and has remained in touch with the mentor who ran the tutorial. She
understands the basics of Python but is often only a little bit more advanced
in her understanding than her most advanced 16 year old students. She enjoys
the fact that she can use PyperCard to create interactive presentations for her
students, doesn't need to persuade her school sysadmin to install anything (it
all works in the browser), and her students can easily take her example apps
as starting points for their own PyperCard projects.

She hopes to contribute a PyperCard talk at next year's education summit at
PyCon South Africa and all her learning resources, released under
[Creative Commons](https://creativecommons.org/) or
[Open Source](https://opensource.org/) licenses, can be found online via her
school's website and her [PyScript.com](https://pyscript.com/) account.
