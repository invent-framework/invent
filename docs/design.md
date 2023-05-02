# Design

PyperCard has a certain design outlook, way of paying attention to our users
and programming philosophy. This page explains and illustrates these things.

The summary is...

## PyperCard is for beginners

Who are beginners?

You're a beginner if creating typical UI based applications isn't your usual
focus.

PyperCard aims to be easy to learn, so you can get on with the fun of creating
interesting things. With a little experience, you'll be able to quickly build
all sorts of valuable stuff. PyperCard does the technical heavy lifting so you
can focus on with the important things.

We love feedback from users, so if you find a problem, please
[submit an issue](https://github.com/pyscript/pypercard/issues/new) while
remembering to follow our [contributing guidelines](contributing.md) and
[code of conduct](code_of_conduct.md).

If you're asking questions about technical features of PyperCard, such
as, why does PyperCard use the JavaScript `Audio` class like _this_ rather than
like _that_?, then you're probably not a beginner. However, we'd love to invite
you to contribute to PyperCard if you spot ways to _enhance the experience of
beginners_.

```{tip}
If you just want some deeply technical capability that PyperCard doesn't
provide, you should probably try another framework that supports that
capability rather than try to force it into PyperCard.
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
* **Flexible** - rather, we expect our core _pragmatic programming paradigms_
  to be _good enough most of the time_.
* **Opaque** - rather, you don't need to be a programmer with a degree in
computer science to _get started and building stuff in only minutes_.
* **Hard** - rather, we concede that some stuff is deeply challenging and you
  should _use something else if PyperCard doesn't work for you_.

## Personas

To help orientate folks contributing to PyperCard, we've created a small group
of personas to illustrate the diversity of "beginner" coders we hope to help
with our project.

Each persona has four sections:

1. an introduction that explains who they are,
2. a description of how they're using PyperCard,
3. any mitigating circumstances about their use of PyperCard, and,
4. a list of PyperCard related features/capabilities they need.

If there's a check (✅) next to the item in the list of related
features/capabilities, then this has been implemented and released.

The persona images were made via a stable diffusion based tool for generating
faces. _These people do not actually exist_!

### Alejando 🇲🇽
![](_static/persona_alejandro.png)

Alejandro is 12 years old, lives in Mexico and is learning how to code in his
after school computer club. He is also colour blind, so the colour pallette for
user interfaces sometimes poses a challenge for him.

His teacher, Miss.Perez, has asked him to create a simple game with PyperCard
in a choose-your-own-adventure style. Alejando is only too pleased with this
project since he has lots of story ideas based in the Star Wars / Marvel
universes.

Alejandro doesn't speak English, but Miss.Perez has created resources in
Spanish, based on the PyperCard documentation and tutorials. He builds and
hosts his PyperCard projects via [PyScript.com](https://pyscript.com/).

* A Spanish language version of PyScript.com.
* The availability of auto-didactic resources such as:
  - Beginner friendly example projects. ✅
  - Tutorials. ✅
  - A simple development environment that supports learning.
* Support for light, dark, high-contrast and custom themes in the UI layer.

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
PyperCard's use in an upcoming London Python Code Dojo community meetup.

* A technical cheat sheet for getting experienced developers up and running. ✅
* A simple and intuitive (yet powerful) means of making network calls via both
  HTTP and web-socket protocols.

### Mandisa 🇿🇦
![](_static/persona_mandisa.png)

Mandisa, 35, is a high school teacher in a girl's school in Claremont, Cape
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

* Good mobile performance so her students can run their work on their personal
  computing devices (MicroPython).
* Teacher friendly learning resources that can be freely adapted / adopted in
  the classroom.
* A classroom friendly configuration of pyscript.com (where teacher has admin
  control over student's workspaces / applications).

### Parminder 🇮🇳
![](_static/persona_parminder.png)

Parminder, 44, is a research scientist attached to the United Nations. Her
focus is the measurement and impact of long term environment change on
glaciers. She is also partially sighted, and often uses a screen reader and/or
magnification features while working across all her computing platforms
(Android mobile, Apple iPad and a Windows "work" Lenovo laptop).

She uses PyperCard to design data collection apps for both her scientific
colleagues and non-specialists in the field. These apps are often used in
relatively disconnected areas with only patchy 3G internet coverage, or
faster Starlink (satellite) based wifi at base-camps.

* Responsive: same app works on both mobile and laptop.
* Offline storage.
* Robust error handling for network based tasks.

### Janet 🇨🇦
![](_static/persona_janet.png)

Janet, 52, is COO at an established and flourishing aeronautical engineering 
company. Based in Vancouver, the company has several thousand employees in
offices in Canada, the US, UK, France and Italy. Much of her work depends on
her ability to communicate key facts in a timely manner. Janet, as someone with
a strong engineering background, has picked up a basic understanding of Python.

She uses PyperCard to create a stack of cards containing live data for the
purposes of sharing key insights with her colleagues. She likes to think of her
PyperCard apps as interactive dashboards quickly created for other C-level
executives in the company, and her reports who use it to monitor key status
indicators relating to all sorts of factors including financial, logistical,
manufacturing and sales based data.

She especially appreciates how PyperCard works with real-time data and behaves
like a multi-path presentation, depending upon what key insights the user wants
to learn. She also appreciates how easy it is to update the PyperCard app, as
business needs change, and the app just updates to the latest version when
refreshed ~ making the deployment story very easy, cross platform (including
mobile) and requiring little or no technical knowledge.

* Visual UI designer with access to code behind.
* A simple and intuitive (yet powerful) means of making network calls via both
  HTTP and web-socket protocols.
* Examples of cards to display common data patterns.

### Hasan 🇹🇷
![](_static/persona_hasan.png)

Hasan, 67, is an amateur tech enthusiast and restaurant owner from Selçuk,
Turkey. The historic ruins of the ancient city of Ephesus are only a few miles
away.

Never shy of embracing technology, he's decided to write a multi-lingual
PyperCard app that acts as the menu for tourists at his restaurant. He aims to
support Turkish, English, Arabic, Hebrew, French, German, Italian and Spanish
versions of his menu. He's famous among his friends for experimenting with new
technology. For instance, he's been using spreadsheets for managing stock and
accounting since Windows 3.1 and recently embraced a take-away food delivery
app to increase the reach of his restaurant (the inspiration and template for
his own menu app).

He started to learn Python as a personal project during the COVID
pandemic (his daughter-in-law is a Python programmer in Istanbul, and suggested
he look at PyperCard). Because of the tourist trade, he has relatively good
English and is working his way through the PyperCard tutorials while sketching 
out his ideas for the menu app for his restuarant. He likes using Python,
appreciates that PyperCard works on all his customer's devices (thanks to
MicroPython), and is pleased his rusty HTML skills can be used for generating
the user interface.

* Internationalization support.
* Ability to hand-craft HTML based cards.
