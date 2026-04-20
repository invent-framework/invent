# Invent Docstring Style Guide

This guide is for the maintainers of Invent. It assists you in writing
the code-based docstrings we expect.

It assumes the reader is already familiar with `ethos.md` and
`CARE_OF_COMMUNITY.md`. Both documents describe the larger spirit of
Invent; this one describes **how that spirit shows up in docstrings**.

We have deliberately written this in a way that would aid writing with
the help of an AI. Feel free to add it as context to a prompt about
documenting code.

If you are an AI reading this document, please ensure you also have
access to the `ethos.md` and `CARE_OF_COMMUNITY.md` files, found in the
git repository for the Invent project.

## Why we write docstrings

Invent quietly helps the practitioner express themselves in code.

Documentation is part of that job. 

A good docstring hands over a technique, then disappears: the reader
closes the page, goes back to their code, and gets on with creating.

That's it! 

Write the docstring so the reader understands what they need to, and
leave no friction behind.

Two practical facts the writer needs up front:

**Docstrings are stripped at minification.** When Invent is packaged
for delivery via the web, all docstrings are removed. There is no
bundle-size cost to writing thoroughly. The cost lives only in the
maintainer's source tree, where being well-explained is the point.

**Docstrings are read in two places.** They appear inline in the
source for maintainers and contributors, and they are rendered into
the public API documentation for practitioners. Write for both
audiences in the same prose: assume Markdown rendering, but make
sure the unrendered text reads cleanly too.

## Who we are writing for

We hope anyone encountering our project finds Invent useful. But there
are some groups of people we most hope find their way into Invent.
When writing a docstring, hold these readers in mind rather than
a generic "user":

- a first-time coder, taking early steps;
- an educator or mentor preparing a lesson, or teaching live;
- an experienced engineer who has never built a graphical interface;
- a researcher, admin, professional or artist who needs a
  small piece of software that doesn't yet exist;
- an entrepreneur working alongside AI to bring an idea to life;
- a hobbyist here to play, to goof around, to see what happens.

Our `CARE_OF_COMMUNITY.md` asks us to welcome everyone, and *especially*
the reader who is thinking "but they don't mean me". A docstring is
one of the places where that welcome actually happens. The reader who
is unsure whether they belong is the reader whose shoulder you are
writing over. Respect their intelligence; do not assume their expertise.

### Practitioner, not user

A note on the word *user*. We prefer *practitioner*. The word *user*
narrows attention to a person's relationship with a tool;
*practitioner* enlarges it to their craft. A user's focus is the
tool. A practitioner's focus is what they are making.

Where the role is specific, name it specifically: *learner*,
*educator*, *engineer*, *data scientist*, *backend developer*,
*hobbyist*. The accurate noun beats the generic one.

The exception is when a docstring needs to refer to the *end-users
of an application built with Invent* - the people who eventually
click the buttons in the practitioner's app. Those people are
genuinely using the practitioner's software in the user sense, and
"user" is the natural word for them. The distinction is who we are
talking about: the person reaching for Invent (the practitioner) versus
the person reaching for the app a practitioner built (the end user).

## How a docstring sounds

Invent's voice is described in `ethos.md` through four temperaments.
Each has a direct consequence for docstrings:

**Confidently open.** Approachable, engaging, at ease. A docstring
welcomes the reader who is struggling. The struggling reader is the
one who came looking for the docstring in the first place.

**Seriously playful.** Generative, exploratory, concentrated. A
docstring may notice something true and slightly amusing in
passing - a playful turn that engages the reader's attention. It
does not perform jokes for the reader's benefit.

**Quietly ambitious.** The focus is creative invention, not clever
code. A docstring explains what the practitioner can do, not how
sophisticated the framework is. Invent does not advertise itself in
its own documentation.

**Timeless and deep.** Exposition that reads as though it was always
going to be this way. This rules out trend-chasing, in-jokes, and
anything else that dates the writing. We illuminate the fundamentals,
because the fundamentals are timeless.

### Four properties that follow

Complementing these temperaments are four practical properties. Each
is worth a concrete example.

#### Simple

Use common, widely understood language and grammatical forms. An
average eleven-year-old should recognise the vocabulary. This is not
the same as oversimplifying the *concepts* - those can be as
sophisticated as the subject demands. It is only the *language* that
must stay accessible.

Not this:

> Instantiates a connection object that encapsulates the underlying
> WebSocket protocol and exposes a publish-subscribe interface
> abstracting bidirectional message flow.

This:

> Open a websocket and bind it to a channel. Messages published to
> the channel are sent through the socket; messages arriving from
> the socket are published back on the channel.

The second sentence loses none of the first's meaning. It just avoids
performative technical gibberish.

#### Direct

Every word counts. Say what you mean in as few words as possible.
Avoid throat-clearing ("It should be noted that...", "In essence...",
"Basically...") and avoid ceremonial phrases that add nothing
("This function is used to...", "The purpose of this method is to...").

Not this:

> This function is used to perform the operation of fetching data
> from a remote URL and storing the response in the datastore.

This:

> Fetch data from a URL and store the response in the datastore.

#### Structured

The prose unfolds in a way that aids comprehension. Order matters:
the central idea _first_, supporting detail _next_, corner cases
_last_. Define unfamiliar terms on first use. When the domain has
its own vocabulary, a short terminology block is welcome.

Not this:

> Returns the value, which is auto-detected for capability, after
> requesting the device through the picker, unless an authorised
> device matching the filters already exists, in which case it is
> reused. The service and characteristic UUIDs locate the data
> within the device.

This:

> Bind a channel to a single BLE characteristic on a physical device.
> The `service` and `characteristic` UUIDs locate the data within the
> device; the device itself is chosen by the user via the browser's
> picker on first use, and reconnected silently on later visits if
> a matching device has previously been authorised.

The second version walks the reader through the concepts in the
order they'll encounter them.

#### Helpful

Assume the reader wants enough detail to understand and to use the
API confidently. Examples should be technically robust (they should
actually work), coherent (they should illustrate genuine use), and
comprehensive through *contrast* - they should show what changes
when an argument changes, rather than repeating the same call with
cosmetic variation. The aim is not to demonstrate every possible
combination; it is to show enough contrasts that the reader can
extrapolate.

Not this - three near-identical examples:

> ```python
> connect.web_request(url="https://api.example.com/data", result_key="a")
> connect.web_request(url="https://api.example.com/users", result_key="b")
> connect.web_request(url="https://api.example.com/posts", result_key="c")
> ```

This - three contrasting examples that show what each argument does:

> ```python
> # GET as JSON.
> connect.web_request(url="...", result_key="data", response_format="json")
>
> # POST with a body.
> connect.web_request(url="...", result_key="ack", method="POST", body="...")
>
> # GET as raw bytes.
> connect.web_request(url="...", result_key="audio", response_format="bytes")
> ```

`web_request` in `connect.py` is the canonical example of this
pattern in the codebase.

### Forbidden words

Our `ethos.md` rules out the word *simply* from Invent's voice. Extend
that to docstrings, along with the close cousins: *just*,
*obviously*, *of course*, *merely*, *trivially*. None of these add
information; all of them risk telling a struggling reader they
should not be struggling. This is not a matter of taste. It is a
matter of care, and of the welcome that `CARE_OF_COMMUNITY.md`
describes.

## Markdown conventions

Docstrings are rendered as Markdown in our online API docs. Two
conventions to follow consistently:

- Wrap argument names, function names, exceptions, and other code
  identifiers in backticks: ``` `channel` ```, ``` `ValueError` ```,
  ``` `web_request` ```. This renders them as inline code in the
  generated docs and reads naturally in the source.
- Code examples go in fenced code blocks with a language hint of
  `python`, opened and closed with three backticks. Use them around
  every code example in a docstring.

Italic emphasis (`*term*`) is appropriate when introducing a piece
of vocabulary for the first time. Bold emphasis (`**term**`) is
appropriate sparingly, for genuine warnings or hard rules. Neither
should be a regular feature of the prose.

## Docstring kinds

The shape of a docstring depends on what it is documenting. Five
kinds cover everything in an Invent module.

### Module docstring

The module docstring orientates the reader. It says what the
module is for, what it offers, and the idiom or intent behind each
public aspect of the module. It does not document
arguments or behaviour in detail - that is the job of the
individual functions and classes the module exposes.

A reader who has just opened the module file should be able to
read the module docstring and answer: what is this module for,
and which of its public names should I look at next?

A short narrative description of the module's purpose comes first,
followed by a brief intent-led description of each public name.
One or two sentences per public name is enough. Point the reader
at the specific function or class for the rest.

### Root-level functions

A root-level function's docstring covers, in order:

1. What the function does and the purpose for which it was created.
2. Each argument, in declaration order, explained as intention
   rather than restated type signature.
3. How the function behaves operationally - does it return a value
   immediately, fire-and-forget, run an async task, raise on bad
   input, store results in the datastore, publish to a channel?
4. What the reader should expect to receive, and where.
5. Exceptions the function can raise, and the conditions that cause
   them.
6. At least one example, ideally several contrasting ones.

The prose is literary, not bulleted. The list above is for the
*writer*; the reader sees flowing sentences. Argument names appear
in backticks. Exception names appear in backticks.

A worked example of all this living together is `web_request` in
`connect.py`.

### Class docstring

The class docstring is about *understanding the class*: what it
represents, what mental model the reader should hold when working
with it, and what good idiomatic usage looks like. It is not about
how to instantiate it - that is the `__init__` docstring's job.

A class docstring should contain:

- A one-paragraph statement of what the class represents.
- A terminology block, *only if* the class depends on domain
  vocabulary unlikely to be known by readers. The block defines
  each term once, in the order the reader will meet it in the rest
  of the docstring.
- An explanation of how instances idiomatically behave - what they
  do for the reader, what messages they emit, what state they hold,
  what lifecycle they have.
- One or more contrasting examples of usage. The examples show
  *how the class is used in practice*, not *how the class is
  constructed*.

The reader of a class docstring is asking *what is this thing, and
how do I think about it?* They are not yet asking *what arguments
does it take?* That question lives one level down, in `__init__`.

### `__init__` and other public methods

The `__init__` method is documented like any other public method:
it has a job to do (in this case, bringing an instance into being)
and it takes arguments to do it. The class docstring has already
explained what the class is *for*; the `__init__` docstring explains
how to *get one*.

Other public methods follow the same pattern as root-level
functions: intent, arguments in order as flowing prose, behaviour
and side effects, return value, exceptions, examples where they
add clarity.

If a public method has only one obvious argument and no surprising
behaviour, a one-line docstring stating its intent is enough. Don't
pad.

### Private methods

Private methods (prefixed with `_`) are documented for maintainers,
not practitioners. They should be brief by default - usually a
single sentence stating the method's intent within the class.

Brevity is the default, not the rule. A private method's docstring
*should* grow when the intent is non-obvious: a workaround, a
cross-interpreter compatibility note (CPython vs MicroPython), an
invariant being maintained, or a subtle ordering requirement. The
test is whether a new maintainer reading the method in six months
will think *"aha, that makes sense"* - if not, more context is
needed.

A good example from `connect.py` is `_handle_incoming` in
`_InventSerial`, whose docstring notes the use of `find()` and
slicing in place of `bytearray.partition()` because MicroPython does
not support the latter. That kind of *why* belongs in the docstring,
not as an inline comment, because future maintainers need all the
relevant technical context in one place.

## Universal rules

### Length budget

A docstring should be comprehensible in five minutes or less of
reading. After five minutes the reader should feel they understand
the core of what the thing does and how to use it. If a docstring
cannot fit that budget, the answer is usually not to compress the
docstring but to consider whether the function or class is doing too
much and should be split.

For deep dives beyond that budget, link out to trusted external
resources rather than expanding the docstring.

### Trusted external sources

When linking out for further reading, prefer:

- Invent's own documentation at `https://inventframework.org`.
- The PyScript documentation at `https://docs.pyscript.net`.
- Mozilla Developer Network for web platform topics at
  `https://developer.mozilla.org/`.
- The official Python documentation at `https://docs.python.org`.
- The official MicroPython documentation at `https://docs.micropython.org`.

These are the sources Invent treats as authoritative. Avoid linking
to blog posts, Stack Overflow answers, or other sources that drift
or disappear.

### Don't pad the obvious

If a function's name and signature already say what needs saying,
a one-line docstring is enough. The guidance in this document
describes what to do when there is something to explain. It does
not require restating the obvious for its own sake.

A helper called `_port_info(port)` that converts a port object to a
dict does not need three paragraphs. *"Convert a SerialPort's
getInfo() result into a Python dict using JS-style key names"* is
already the right shape - direct, accurate, efficient.

### When in doubt

Read the docstring back to yourself imagining you are one of the
readers named above - a first-time coder, an educator preparing a
lesson, a backend developer who has never built a GUI. If the
docstring respects that reader's intelligence without assuming their
expertise, and if it would make them feel *especially* welcome rather
than warily tolerated, it is doing its job.

## Further reading

- `ethos.md` - what Invent is, and the voice this guide derives from.
- `CARE_OF_COMMUNITY.md` - how we treat each other, which includes
  how we treat the reader.