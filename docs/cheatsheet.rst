PyperCard CheatSheet
====================

PyperCard is an easy and simple GUI framework with a focus on beginner Python
programmers. This page contains all the technical information you need in one
place. You should use it for reference purposes. If you'd like to learn about
PyperCard you should consult the :doc:`tutorials`.

.. contents::
    :depth: 2

Installation
++++++++++++

PyperCard only works with Python 3.6 or above. It is built on the
`Kivy framework <https://kivy.org/>`_ and should work anywhere Kivy does
(Windows, OSX, Linux, Android and iOS).

PyperCard is on PyPI and can be installed thus::

    pip3 install pypercard

Check the installation works with the following "Hello World!" test app::

    from pypercard import CardApp, Card

    app = CardApp(stack=[Card("hello", text="Hello, World!"), ])
    app.run()

Save this somewhere (e.g. as ``test.py``) and run it with::

    python3 test.py 

If all goes to plan you should see a Window containing the words
"Hello, World" appear.

If you require help or support please
`use our chat channel <https://gitter.im/pypercard/community>`_. If you think
you've found a bug in PyperCard or would like to suggest a new feature or
improvement, please do so by raising a new issue via
`our GitHub page for the project <https://github.com/ntoll/pypercard/issues>`_.
We expect everyone to abide by our :doc:`code_of_conduct` -- we're a friendly
and welcoming project, but we won't tolerate rudeness, prejudice or other forms
of anti-social behaviour via our communication channels.

Core Concepts
+++++++++++++

PyperCard is inspired by `HyperCard <https://en.wikipedia.org/wiki/HyperCard>`_
and means you should be familiar with the following core concepts:

* An application is made from a **stack** of cards.
* Each **card** in the stack represents a screen in the application. At the
  very least, a card must have a **unique title** attribute (but will often
  have further attributes that define its content and behaviour).
* Users move between cards via **transitions**, usually activated by pressing a
  button.
* Transitions can be as simple as **a string identifying the title of the next
  card to display**. However, **a transition can also be a function** that
  returns a string identifying the next card to display. Business logic for the
  application happens in these transition functions.
* Simple **form inputs** can be used to capture input from the user.
* An application has a **data store** Python dictionary to be used to set and
  get arbitrary application state.
* Transition funtions always **take two arguments**, a reference to the
  application's ``data_store`` (containing application state) and the value of
  the ``form_input`` found on the preceeding card from which the user is
  transitioning.
* Future versions of PyperCard will **automate the packaging of your app** for
  Windows, OSX, Linux, Android and iOS.

The following diagram may help you visualise these concepts. There are three
cards in the application stack: ``blue``, ``white`` and ``yellow``. The
``blue`` card can transition to the ``white`` and ``yellow`` cards (as
demonstrated by the arrows).

.. raw:: html

    <img alt="Splash image" src="_static/splash.png" style="border: none;">

Colours
+++++++

It is possible to set the colour of various aspects of the user interface (for
example, the text colour, background colour, button colour and button
background).

To make this as easy as possible for beginners, colours can be specified by
their English names. A full list of recognized colour names (and an example of
the colour) can be found in the palette shown below.

Alternatively, instead of naming the colour of choice, you can provide the
hex RGB value as a string in two common forms: ``0xRRGGBB`` (raw hex) and
``#RRGGBB`` (web hex).

.. raw:: html

  <table>
    <tr>
      <td><span style="background: #000000; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>black</td>
      <td><span style="background: #696969; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>dimgrey</td>
      <td><span style="background: #A9A9A9; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>darkgrey</td>
      <td><span style="background: #BEBEBE; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>grey</td>
    </tr>
    <tr>
      <td><span style="background: #000000; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>grey0</td>
      <td><span style="background: #030303; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>grey1</td>
      <td><span style="background: #050505; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>grey2</td>
      <td><span style="background: #080808; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>grey3</td>
    </tr>
    <tr>
      <td><span style="background: #0A0A0A; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>grey4</td>
      <td><span style="background: #0D0D0D; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>grey5</td>
      <td><span style="background: #0F0F0F; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>grey6</td>
      <td><span style="background: #121212; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>grey7</td>
    </tr>
    <tr>
      <td><span style="background: #141414; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>grey8</td>
      <td><span style="background: #171717; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>grey9</td>
      <td><span style="background: #1A1A1A; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>grey10</td>
      <td><span style="background: #1C1C1C; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>grey11</td>
    </tr>
    <tr>
      <td><span style="background: #1F1F1F; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>grey12</td>
      <td><span style="background: #212121; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>grey13</td>
      <td><span style="background: #242424; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>grey14</td>
      <td><span style="background: #262626; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>grey15</td>
    </tr>
    <tr>
      <td><span style="background: #292929; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>grey16</td>
      <td><span style="background: #2B2B2B; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>grey17</td>
      <td><span style="background: #2E2E2E; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>grey18</td>
      <td><span style="background: #303030; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>grey19</td>
    </tr>
    <tr>
      <td><span style="background: #333333; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>grey20</td>
      <td><span style="background: #363636; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>grey21</td>
      <td><span style="background: #383838; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>grey22</td>
      <td><span style="background: #3B3B3B; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>grey23</td>
    </tr>
    <tr>
      <td><span style="background: #3D3D3D; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>grey24</td>
      <td><span style="background: #404040; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>grey25</td>
      <td><span style="background: #424242; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>grey26</td>
      <td><span style="background: #454545; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>grey27</td>
    </tr>
    <tr>
      <td><span style="background: #474747; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>grey28</td>
      <td><span style="background: #4A4A4A; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>grey29</td>
      <td><span style="background: #4D4D4D; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>grey30</td>
      <td><span style="background: #4F4F4F; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>grey31</td>
    </tr>
    <tr>
      <td><span style="background: #525252; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>grey32</td>
      <td><span style="background: #545454; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>grey33</td>
      <td><span style="background: #575757; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>grey34</td>
      <td><span style="background: #595959; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>grey35</td>
    </tr>
    <tr>
      <td><span style="background: #5C5C5C; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>grey36</td>
      <td><span style="background: #5E5E5E; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>grey37</td>
      <td><span style="background: #616161; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>grey38</td>
      <td><span style="background: #636363; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>grey39</td>
    </tr>
    <tr>
      <td><span style="background: #666666; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>grey40</td>
      <td><span style="background: #696969; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>grey41</td>
      <td><span style="background: #6B6B6B; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>grey42</td>
      <td><span style="background: #6E6E6E; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>grey43</td>
    </tr>
    <tr>
      <td><span style="background: #707070; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>grey44</td>
      <td><span style="background: #737373; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>grey45</td>
      <td><span style="background: #757575; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>grey46</td>
      <td><span style="background: #787878; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>grey47</td>
    </tr>
    <tr>
      <td><span style="background: #7A7A7A; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>grey48</td>
      <td><span style="background: #7D7D7D; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>grey49</td>
      <td><span style="background: #7F7F7F; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>grey50</td>
      <td><span style="background: #828282; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>grey51</td>
    </tr>
    <tr>
      <td><span style="background: #858585; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>grey52</td>
      <td><span style="background: #878787; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>grey53</td>
      <td><span style="background: #8A8A8A; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>grey54</td>
      <td><span style="background: #8C8C8C; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>grey55</td>
    </tr>
    <tr>
      <td><span style="background: #8F8F8F; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>grey56</td>
      <td><span style="background: #919191; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>grey57</td>
      <td><span style="background: #949494; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>grey58</td>
      <td><span style="background: #969696; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>grey59</td>
    </tr>
    <tr>
      <td><span style="background: #999999; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>grey60</td>
      <td><span style="background: #9C9C9C; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>grey61</td>
      <td><span style="background: #9E9E9E; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>grey62</td>
      <td><span style="background: #A1A1A1; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>grey63</td>
    </tr>
    <tr>
      <td><span style="background: #A3A3A3; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>grey64</td>
      <td><span style="background: #A6A6A6; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>grey65</td>
      <td><span style="background: #A8A8A8; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>grey66</td>
      <td><span style="background: #ABABAB; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>grey67</td>
    </tr>
    <tr>
      <td><span style="background: #ADADAD; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>grey68</td>
      <td><span style="background: #B0B0B0; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>grey69</td>
      <td><span style="background: #B3B3B3; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>grey70</td>
      <td><span style="background: #B5B5B5; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>grey71</td>
    </tr>
    <tr>
      <td><span style="background: #B8B8B8; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>grey72</td>
      <td><span style="background: #BABABA; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>grey73</td>
      <td><span style="background: #BDBDBD; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>grey74</td>
      <td><span style="background: #BFBFBF; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>grey75</td>
    </tr>
    <tr>
      <td><span style="background: #C2C2C2; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>grey76</td>
      <td><span style="background: #C4C4C4; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>grey77</td>
      <td><span style="background: #C7C7C7; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>grey78</td>
      <td><span style="background: #C9C9C9; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>grey79</td>
    </tr>
    <tr>
      <td><span style="background: #CCCCCC; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>grey80</td>
      <td><span style="background: #CFCFCF; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>grey81</td>
      <td><span style="background: #D1D1D1; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>grey82</td>
      <td><span style="background: #D4D4D4; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>grey83</td>
    </tr>
    <tr>
      <td><span style="background: #D6D6D6; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>grey84</td>
      <td><span style="background: #D9D9D9; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>grey85</td>
      <td><span style="background: #DBDBDB; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>grey86</td>
      <td><span style="background: #DEDEDE; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>grey87</td>
    </tr>
    <tr>
      <td><span style="background: #E0E0E0; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>grey88</td>
      <td><span style="background: #E3E3E3; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>grey89</td>
      <td><span style="background: #E5E5E5; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>grey90</td>
      <td><span style="background: #E8E8E8; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>grey91</td>
    </tr>
    <tr>
      <td><span style="background: #EBEBEB; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>grey92</td>
      <td><span style="background: #EDEDED; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>grey93</td>
      <td><span style="background: #F0F0F0; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>grey94</td>
      <td><span style="background: #F2F2F2; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>grey95</td>
    </tr>
    <tr>
      <td><span style="background: #F5F5F5; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>grey96</td>
      <td><span style="background: #F7F7F7; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>grey97</td>
      <td><span style="background: #FAFAFA; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>grey98</td>
      <td><span style="background: #FCFCFC; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>grey99</td>
    </tr>
    <tr>
      <td><span style="background: #D3D3D3; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>lightgrey</td>
      <td><span style="background: #DCDCDC; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>gainsboro</td>
      <td><span style="background: #F5F5F5; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>whitesmoke</td>
      <td><span style="background: #FFFFFF; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>white</td>
    </tr>
    <tr>
      <td><span style="background: #8B0000; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>darkred</td>
      <td><span style="background: #8B4513; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>saddlebrown</td>
      <td><span style="background: #A0522D; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>sienna</td>
      <td><span style="background: #FF8247; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>sienna1</td>
    </tr>
    <tr>
      <td><span style="background: #EE7942; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>sienna2</td>
      <td><span style="background: #CD6839; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>sienna3</td>
      <td><span style="background: #8B4726; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>sienna4</td>
      <td><span style="background: #A52A2A; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>brown</td>
    </tr>
    <tr>
      <td><span style="background: #FF4040; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>brown1</td>
      <td><span style="background: #EE3B3B; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>brown2</td>
      <td><span style="background: #CD3333; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>brown3</td>
      <td><span style="background: #8B2323; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>brown4</td>
    </tr>
    <tr>
      <td><span style="background: #B03060; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>maroon</td>
      <td><span style="background: #FF34B3; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>maroon1</td>
      <td><span style="background: #EE30A7; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>maroon2</td>
      <td><span style="background: #CD2990; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>maroon3</td>
    </tr>
    <tr>
      <td><span style="background: #8B1C62; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>maroon4</td>
      <td><span style="background: #B22222; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>firebrick</td>
      <td><span style="background: #FF3030; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>firebrick1</td>
      <td><span style="background: #EE2C2C; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>firebrick2</td>
    </tr>
    <tr>
      <td><span style="background: #CD2626; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>firebrick3</td>
      <td><span style="background: #8B1A1A; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>firebrick4</td>
      <td><span style="background: #B8860B; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>darkgoldenrod</td>
      <td><span style="background: #FFB90F; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>darkgoldenrod1</td>
    </tr>
    <tr>
      <td><span style="background: #EEAD0E; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>darkgoldenrod2</td>
      <td><span style="background: #CD950C; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>darkgoldenrod3</td>
      <td><span style="background: #8B6508; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>darkgoldenrod4</td>
      <td><span style="background: #BC8F8F; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>rosybrown</td>
    </tr>
    <tr>
      <td><span style="background: #FFC1C1; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>rosybrown1</td>
      <td><span style="background: #EEB4B4; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>rosybrown2</td>
      <td><span style="background: #CD9B9B; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>rosybrown3</td>
      <td><span style="background: #8B6969; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>rosybrown4</td>
    </tr>
    <tr>
      <td><span style="background: #BDB76B; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>darkkhaki</td>
      <td><span style="background: #C71585; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>mediumvioletred</td>
      <td><span style="background: #CD5C5C; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>indianred</td>
      <td><span style="background: #FF6A6A; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>indianred1</td>
    </tr>
    <tr>
      <td><span style="background: #EE6363; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>indianred2</td>
      <td><span style="background: #CD5555; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>indianred3</td>
      <td><span style="background: #8B3A3A; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>indianred4</td>
      <td><span style="background: #CD853F; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>peru</td>
    </tr>
    <tr>
      <td><span style="background: #D02090; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>violetred</td>
      <td><span style="background: #FF3E96; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>violetred1</td>
      <td><span style="background: #EE3A8C; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>violetred2</td>
      <td><span style="background: #CD3278; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>violetred3</td>
    </tr>
    <tr>
      <td><span style="background: #8B2252; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>violetred4</td>
      <td><span style="background: #D2691E; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>chocolate</td>
      <td><span style="background: #FF7F24; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>chocolate1</td>
      <td><span style="background: #EE7621; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>chocolate2</td>
    </tr>
    <tr>
      <td><span style="background: #CD661D; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>chocolate3</td>
      <td><span style="background: #8B4513; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>chocolate4</td>
      <td><span style="background: #D2B48C; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>tan</td>
      <td><span style="background: #FFA54F; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>tan1</td>
    </tr>
    <tr>
      <td><span style="background: #EE9A49; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>tan2</td>
      <td><span style="background: #CD853F; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>tan3</td>
      <td><span style="background: #8B5A2B; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>tan4</td>
      <td><span style="background: #DA70D6; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>orchid</td>
    </tr>
    <tr>
      <td><span style="background: #FF83FA; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>orchid1</td>
      <td><span style="background: #EE7AE9; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>orchid2</td>
      <td><span style="background: #CD69C9; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>orchid3</td>
      <td><span style="background: #8B4789; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>orchid4</td>
    </tr>
    <tr>
      <td><span style="background: #DAA520; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>goldenrod</td>
      <td><span style="background: #FFC125; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>goldenrod1</td>
      <td><span style="background: #EEB422; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>goldenrod2</td>
      <td><span style="background: #CD9B1D; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>goldenrod3</td>
    </tr>
    <tr>
      <td><span style="background: #8B6914; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>goldenrod4</td>
      <td><span style="background: #DB7093; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>palevioletred</td>
      <td><span style="background: #FF82AB; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>palevioletred1</td>
      <td><span style="background: #EE799F; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>palevioletred2</td>
    </tr>
    <tr>
      <td><span style="background: #CD6889; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>palevioletred3</td>
      <td><span style="background: #8B475D; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>palevioletred4</td>
      <td><span style="background: #DEB887; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>burlywood</td>
      <td><span style="background: #FFD39B; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>burlywood1</td>
    </tr>
    <tr>
      <td><span style="background: #EEC591; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>burlywood2</td>
      <td><span style="background: #CDAA7D; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>burlywood3</td>
      <td><span style="background: #8B7355; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>burlywood4</td>
      <td><span style="background: #E9967A; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>darksalmon</td>
    </tr>
    <tr>
      <td><span style="background: #EEDD82; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>lightgoldenrod</td>
      <td><span style="background: #FFEC8B; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>lightgoldenrod1</td>
      <td><span style="background: #EEDC82; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>lightgoldenrod2</td>
      <td><span style="background: #CDBE70; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>lightgoldenrod3</td>
    </tr>
    <tr>
      <td><span style="background: #8B814C; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>lightgoldenrod4</td>
      <td><span style="background: #EEE8AA; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>palegoldenrod</td>
      <td><span style="background: #F08080; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>lightcoral</td>
      <td><span style="background: #F0E68C; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>khaki</td>
    </tr>
    <tr>
      <td><span style="background: #FFF68F; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>khaki1</td>
      <td><span style="background: #EEE685; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>khaki2</td>
      <td><span style="background: #CDC673; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>khaki3</td>
      <td><span style="background: #8B864E; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>khaki4</td>
    </tr>
    <tr>
      <td><span style="background: #F4A460; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>sandybrown</td>
      <td><span style="background: #F5DEB3; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>wheat</td>
      <td><span style="background: #FFE7BA; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>wheat1</td>
      <td><span style="background: #EED8AE; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>wheat2</td>
    </tr>
    <tr>
      <td><span style="background: #CDBA96; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>wheat3</td>
      <td><span style="background: #8B7E66; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>wheat4</td>
      <td><span style="background: #FA8072; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>salmon</td>
      <td><span style="background: #FF8C69; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>salmon1</td>
    </tr>
    <tr>
      <td><span style="background: #EE8262; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>salmon2</td>
      <td><span style="background: #CD7054; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>salmon3</td>
      <td><span style="background: #8B4C39; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>salmon4</td>
      <td><span style="background: #FAEBD7; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>antiquewhite</td>
    </tr>
    <tr>
      <td><span style="background: #FFEFDB; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>antiquewhite1</td>
      <td><span style="background: #EEDFCC; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>antiquewhite2</td>
      <td><span style="background: #CDC0B0; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>antiquewhite3</td>
      <td><span style="background: #8B8378; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>antiquewhite4</td>
    </tr>
    <tr>
      <td><span style="background: #FAF0E6; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>linen</td>
      <td><span style="background: #FDF5E6; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>oldlace</td>
      <td><span style="background: #FF0000; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>red</td>
      <td><span style="background: #FF0000; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>red1</td>
    </tr>
    <tr>
      <td><span style="background: #EE0000; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>red2</td>
      <td><span style="background: #CD0000; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>red3</td>
      <td><span style="background: #8B0000; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>red4</td>
      <td><span style="background: #FF1493; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>deeppink</td>
    </tr>
    <tr>
      <td><span style="background: #FF1493; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>deeppink1</td>
      <td><span style="background: #EE1289; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>deeppink2</td>
      <td><span style="background: #CD1076; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>deeppink3</td>
      <td><span style="background: #8B0A50; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>deeppink4</td>
    </tr>
    <tr>
      <td><span style="background: #FF4500; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>orangered</td>
      <td><span style="background: #FF4500; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>orangered1</td>
      <td><span style="background: #EE4000; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>orangered2</td>
      <td><span style="background: #CD3700; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>orangered3</td>
    </tr>
    <tr>
      <td><span style="background: #8B2500; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>orangered4</td>
      <td><span style="background: #FF6347; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>tomato</td>
      <td><span style="background: #FF6347; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>tomato1</td>
      <td><span style="background: #EE5C42; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>tomato2</td>
    </tr>
    <tr>
      <td><span style="background: #CD4F39; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>tomato3</td>
      <td><span style="background: #8B3626; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>tomato4</td>
      <td><span style="background: #FF69B4; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>hotpink</td>
      <td><span style="background: #FF6EB4; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>hotpink1</td>
    </tr>
    <tr>
      <td><span style="background: #EE6AA7; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>hotpink2</td>
      <td><span style="background: #CD6090; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>hotpink3</td>
      <td><span style="background: #8B3A62; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>hotpink4</td>
      <td><span style="background: #FF7F50; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>coral</td>
    </tr>
    <tr>
      <td><span style="background: #FF7256; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>coral1</td>
      <td><span style="background: #EE6A50; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>coral2</td>
      <td><span style="background: #CD5B45; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>coral3</td>
      <td><span style="background: #8B3E2F; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>coral4</td>
    </tr>
    <tr>
      <td><span style="background: #FF8C00; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>darkorange</td>
      <td><span style="background: #FF7F00; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>darkorange1</td>
      <td><span style="background: #EE7600; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>darkorange2</td>
      <td><span style="background: #CD6600; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>darkorange3</td>
    </tr>
    <tr>
      <td><span style="background: #8B4500; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>darkorange4</td>
      <td><span style="background: #FFA07A; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>lightsalmon</td>
      <td><span style="background: #FFA07A; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>lightsalmon1</td>
      <td><span style="background: #EE9572; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>lightsalmon2</td>
    </tr>
    <tr>
      <td><span style="background: #CD8162; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>lightsalmon3</td>
      <td><span style="background: #8B5742; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>lightsalmon4</td>
      <td><span style="background: #FFA500; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>orange</td>
      <td><span style="background: #FFA500; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>orange1</td>
    </tr>
    <tr>
      <td><span style="background: #EE9A00; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>orange2</td>
      <td><span style="background: #CD8500; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>orange3</td>
      <td><span style="background: #8B5A00; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>orange4</td>
      <td><span style="background: #FFB6C1; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>lightpink</td>
    </tr>
    <tr>
      <td><span style="background: #FFAEB9; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>lightpink1</td>
      <td><span style="background: #EEA2AD; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>lightpink2</td>
      <td><span style="background: #CD8C95; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>lightpink3</td>
      <td><span style="background: #8B5F65; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>lightpink4</td>
    </tr>
    <tr>
      <td><span style="background: #FFC0CB; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>pink</td>
      <td><span style="background: #FFB5C5; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>pink1</td>
      <td><span style="background: #EEA9B8; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>pink2</td>
      <td><span style="background: #CD919E; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>pink3</td>
    </tr>
    <tr>
      <td><span style="background: #8B636C; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>pink4</td>
      <td><span style="background: #FFD700; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>gold</td>
      <td><span style="background: #FFD700; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>gold1</td>
      <td><span style="background: #EEC900; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>gold2</td>
    </tr>
    <tr>
      <td><span style="background: #CDAD00; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>gold3</td>
      <td><span style="background: #8B7500; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>gold4</td>
      <td><span style="background: #FFDAB9; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>peachpuff</td>
      <td><span style="background: #FFDAB9; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>peachpuff1</td>
    </tr>
    <tr>
      <td><span style="background: #EECBAD; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>peachpuff2</td>
      <td><span style="background: #CDAF95; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>peachpuff3</td>
      <td><span style="background: #8B7765; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>peachpuff4</td>
      <td><span style="background: #FFDEAD; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>navajowhite</td>
    </tr>
    <tr>
      <td><span style="background: #FFDEAD; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>navajowhite1</td>
      <td><span style="background: #EECFA1; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>navajowhite2</td>
      <td><span style="background: #CDB38B; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>navajowhite3</td>
      <td><span style="background: #8B795E; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>navajowhite4</td>
    </tr>
    <tr>
      <td><span style="background: #FFE4B5; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>moccasin</td>
      <td><span style="background: #FFE4C4; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>bisque</td>
      <td><span style="background: #FFE4C4; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>bisque1</td>
      <td><span style="background: #EED5B7; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>bisque2</td>
    </tr>
    <tr>
      <td><span style="background: #CDB79E; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>bisque3</td>
      <td><span style="background: #8B7D6B; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>bisque4</td>
      <td><span style="background: #FFE4E1; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>mistyrose</td>
      <td><span style="background: #FFE4E1; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>mistyrose1</td>
    </tr>
    <tr>
      <td><span style="background: #EED5D2; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>mistyrose2</td>
      <td><span style="background: #CDB7B5; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>mistyrose3</td>
      <td><span style="background: #8B7D7B; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>mistyrose4</td>
      <td><span style="background: #FFEBCD; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>blanchedalmond</td>
    </tr>
    <tr>
      <td><span style="background: #FFEFD5; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>papayawhip</td>
      <td><span style="background: #FFF0F5; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>lavenderblush</td>
      <td><span style="background: #FFF0F5; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>lavenderblush1</td>
      <td><span style="background: #EEE0E5; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>lavenderblush2</td>
    </tr>
    <tr>
      <td><span style="background: #CDC1C5; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>lavenderblush3</td>
      <td><span style="background: #8B8386; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>lavenderblush4</td>
      <td><span style="background: #FFF5EE; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>seashell</td>
      <td><span style="background: #FFF5EE; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>seashell1</td>
    </tr>
    <tr>
      <td><span style="background: #EEE5DE; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>seashell2</td>
      <td><span style="background: #CDC5BF; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>seashell3</td>
      <td><span style="background: #8B8682; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>seashell4</td>
      <td><span style="background: #FFF8DC; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>cornsilk</td>
    </tr>
    <tr>
      <td><span style="background: #FFF8DC; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>cornsilk1</td>
      <td><span style="background: #EEE8CD; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>cornsilk2</td>
      <td><span style="background: #CDC8B1; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>cornsilk3</td>
      <td><span style="background: #8B8878; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>cornsilk4</td>
    </tr>
    <tr>
      <td><span style="background: #FFFACD; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>lemonchiffon</td>
      <td><span style="background: #FFFACD; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>lemonchiffon1</td>
      <td><span style="background: #EEE9BF; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>lemonchiffon2</td>
      <td><span style="background: #CDC9A5; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>lemonchiffon3</td>
    </tr>
    <tr>
      <td><span style="background: #8B8970; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>lemonchiffon4</td>
      <td><span style="background: #FFFAF0; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>floralwhite</td>
      <td><span style="background: #FFFAFA; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>snow</td>
      <td><span style="background: #FFFAFA; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>snow1</td>
    </tr>
    <tr>
      <td><span style="background: #EEE9E9; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>snow2</td>
      <td><span style="background: #CDC9C9; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>snow3</td>
      <td><span style="background: #8B8989; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>snow4</td>
      <td><span style="background: #556B2F; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>darkolivegreen</td>
    </tr>
    <tr>
      <td><span style="background: #CAFF70; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>darkolivegreen1</td>
      <td><span style="background: #BCEE68; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>darkolivegreen2</td>
      <td><span style="background: #A2CD5A; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>darkolivegreen3</td>
      <td><span style="background: #6E8B3D; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>darkolivegreen4</td>
    </tr>
    <tr>
      <td><span style="background: #6B8E23; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>olivedrab</td>
      <td><span style="background: #C0FF3E; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>olivedrab1</td>
      <td><span style="background: #B3EE3A; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>olivedrab2</td>
      <td><span style="background: #9ACD32; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>olivedrab3</td>
    </tr>
    <tr>
      <td><span style="background: #698B22; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>olivedrab4</td>
      <td><span style="background: #7CFC00; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>lawngreen</td>
      <td><span style="background: #7FFF00; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>chartreuse</td>
      <td><span style="background: #7FFF00; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>chartreuse1</td>
    </tr>
    <tr>
      <td><span style="background: #76EE00; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>chartreuse2</td>
      <td><span style="background: #66CD00; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>chartreuse3</td>
      <td><span style="background: #458B00; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>chartreuse4</td>
      <td><span style="background: #9ACD32; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>yellowgreen</td>
    </tr>
    <tr>
      <td><span style="background: #ADFF2F; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>greenyellow</td>
      <td><span style="background: #F5F5DC; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>beige</td>
      <td><span style="background: #FAFAD2; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>lightgoldenrodyellow</td>
      <td><span style="background: #FFFF00; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>yellow</td>
    </tr>
    <tr>
      <td><span style="background: #FFFF00; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>yellow1</td>
      <td><span style="background: #EEEE00; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>yellow2</td>
      <td><span style="background: #CDCD00; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>yellow3</td>
      <td><span style="background: #8B8B00; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>yellow4</td>
    </tr>
    <tr>
      <td><span style="background: #FFFFE0; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>lightyellow</td>
      <td><span style="background: #FFFFE0; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>lightyellow1</td>
      <td><span style="background: #EEEED1; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>lightyellow2</td>
      <td><span style="background: #CDCDB4; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>lightyellow3</td>
    </tr>
    <tr>
      <td><span style="background: #8B8B7A; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>lightyellow4</td>
      <td><span style="background: #FFFFF0; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>ivory</td>
      <td><span style="background: #FFFFF0; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>ivory1</td>
      <td><span style="background: #EEEEE0; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>ivory2</td>
    </tr>
    <tr>
      <td><span style="background: #CDCDC1; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>ivory3</td>
      <td><span style="background: #8B8B83; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>ivory4</td>
      <td><span style="background: #006400; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>darkgreen</td>
      <td><span style="background: #00FA9A; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>mediumspringgreen</td>
    </tr>
    <tr>
      <td><span style="background: #00FF00; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>green</td>
      <td><span style="background: #00FF00; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>green1</td>
      <td><span style="background: #00EE00; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>green2</td>
      <td><span style="background: #00CD00; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>green3</td>
    </tr>
    <tr>
      <td><span style="background: #008B00; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>green4</td>
      <td><span style="background: #00FF7F; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>springgreen</td>
      <td><span style="background: #00FF7F; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>springgreen1</td>
      <td><span style="background: #00EE76; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>springgreen2</td>
    </tr>
    <tr>
      <td><span style="background: #00CD66; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>springgreen3</td>
      <td><span style="background: #008B45; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>springgreen4</td>
      <td><span style="background: #20B2AA; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>lightseagreen</td>
      <td><span style="background: #228B22; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>forestgreen</td>
    </tr>
    <tr>
      <td><span style="background: #2E8B57; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>seagreen</td>
      <td><span style="background: #54FF9F; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>seagreen1</td>
      <td><span style="background: #4EEE94; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>seagreen2</td>
      <td><span style="background: #43CD80; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>seagreen3</td>
    </tr>
    <tr>
      <td><span style="background: #2E8B57; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>seagreen4</td>
      <td><span style="background: #32CD32; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>limegreen</td>
      <td><span style="background: #3CB371; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>mediumseagreen</td>
      <td><span style="background: #40E0D0; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>turquoise</td>
    </tr>
    <tr>
      <td><span style="background: #00F5FF; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>turquoise1</td>
      <td><span style="background: #00E5EE; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>turquoise2</td>
      <td><span style="background: #00C5CD; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>turquoise3</td>
      <td><span style="background: #00868B; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>turquoise4</td>
    </tr>
    <tr>
      <td><span style="background: #48D1CC; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>mediumturquoise</td>
      <td><span style="background: #66CDAA; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>mediumaquamarine</td>
      <td><span style="background: #7FFFD4; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>aquamarine</td>
      <td><span style="background: #7FFFD4; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>aquamarine1</td>
    </tr>
    <tr>
      <td><span style="background: #76EEC6; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>aquamarine2</td>
      <td><span style="background: #66CDAA; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>aquamarine3</td>
      <td><span style="background: #458B74; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>aquamarine4</td>
      <td><span style="background: #8FBC8F; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>darkseagreen</td>
    </tr>
    <tr>
      <td><span style="background: #C1FFC1; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>darkseagreen1</td>
      <td><span style="background: #B4EEB4; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>darkseagreen2</td>
      <td><span style="background: #9BCD9B; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>darkseagreen3</td>
      <td><span style="background: #698B69; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>darkseagreen4</td>
    </tr>
    <tr>
      <td><span style="background: #90EE90; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>lightgreen</td>
      <td><span style="background: #98FB98; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>palegreen</td>
      <td><span style="background: #9AFF9A; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>palegreen1</td>
      <td><span style="background: #90EE90; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>palegreen2</td>
    </tr>
    <tr>
      <td><span style="background: #7CCD7C; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>palegreen3</td>
      <td><span style="background: #548B54; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>palegreen4</td>
      <td><span style="background: #F0FFF0; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>honeydew</td>
      <td><span style="background: #F0FFF0; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>honeydew1</td>
    </tr>
    <tr>
      <td><span style="background: #E0EEE0; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>honeydew2</td>
      <td><span style="background: #C1CDC1; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>honeydew3</td>
      <td><span style="background: #838B83; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>honeydew4</td>
      <td><span style="background: #F5FFFA; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>mintcream</td>
    </tr>
    <tr>
      <td><span style="background: #008B8B; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>darkcyan</td>
      <td><span style="background: #00BFFF; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>deepskyblue</td>
      <td><span style="background: #00BFFF; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>deepskyblue1</td>
      <td><span style="background: #00B2EE; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>deepskyblue2</td>
    </tr>
    <tr>
      <td><span style="background: #009ACD; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>deepskyblue3</td>
      <td><span style="background: #00688B; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>deepskyblue4</td>
      <td><span style="background: #00CED1; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>darkturquoise</td>
      <td><span style="background: #00FFFF; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>cyan</td>
    </tr>
    <tr>
      <td><span style="background: #00FFFF; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>cyan1</td>
      <td><span style="background: #00EEEE; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>cyan2</td>
      <td><span style="background: #00CDCD; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>cyan3</td>
      <td><span style="background: #008B8B; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>cyan4</td>
    </tr>
    <tr>
      <td><span style="background: #1E90FF; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>dodgerblue</td>
      <td><span style="background: #1E90FF; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>dodgerblue1</td>
      <td><span style="background: #1C86EE; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>dodgerblue2</td>
      <td><span style="background: #1874CD; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>dodgerblue3</td>
    </tr>
    <tr>
      <td><span style="background: #104E8B; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>dodgerblue4</td>
      <td><span style="background: #2F4F4F; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>darkslategrey</td>
      <td><span style="background: #2F4F4F; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>darkslategray</td>
      <td><span style="background: #97FFFF; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>darkslategray1</td>
    </tr>
    <tr>
      <td><span style="background: #8DEEEE; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>darkslategray2</td>
      <td><span style="background: #79CDCD; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>darkslategray3</td>
      <td><span style="background: #528B8B; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>darkslategray4</td>
      <td><span style="background: #4169E1; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>royalblue</td>
    </tr>
    <tr>
      <td><span style="background: #4876FF; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>royalblue1</td>
      <td><span style="background: #436EEE; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>royalblue2</td>
      <td><span style="background: #3A5FCD; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>royalblue3</td>
      <td><span style="background: #27408B; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>royalblue4</td>
    </tr>
    <tr>
      <td><span style="background: #4682B4; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>steelblue</td>
      <td><span style="background: #63B8FF; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>steelblue1</td>
      <td><span style="background: #5CACEE; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>steelblue2</td>
      <td><span style="background: #4F94CD; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>steelblue3</td>
    </tr>
    <tr>
      <td><span style="background: #36648B; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>steelblue4</td>
      <td><span style="background: #5F9EA0; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>cadetblue</td>
      <td><span style="background: #98F5FF; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>cadetblue1</td>
      <td><span style="background: #8EE5EE; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>cadetblue2</td>
    </tr>
    <tr>
      <td><span style="background: #7AC5CD; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>cadetblue3</td>
      <td><span style="background: #53868B; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>cadetblue4</td>
      <td><span style="background: #6495ED; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>cornflowerblue</td>
      <td><span style="background: #708090; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>slategrey</td>
    </tr>
    <tr>
      <td><span style="background: #708090; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>slategray</td>
      <td><span style="background: #C6E2FF; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>slategray1</td>
      <td><span style="background: #B9D3EE; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>slategray2</td>
      <td><span style="background: #9FB6CD; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>slategray3</td>
    </tr>
    <tr>
      <td><span style="background: #6C7B8B; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>slategray4</td>
      <td><span style="background: #778899; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>lightslategray</td>
      <td><span style="background: #778899; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>lightslategrey</td>
      <td><span style="background: #87CEEB; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>skyblue</td>
    </tr>
    <tr>
      <td><span style="background: #87CEFF; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>skyblue1</td>
      <td><span style="background: #7EC0EE; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>skyblue2</td>
      <td><span style="background: #6CA6CD; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>skyblue3</td>
      <td><span style="background: #4A708B; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>skyblue4</td>
    </tr>
    <tr>
      <td><span style="background: #87CEFA; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>lightskyblue</td>
      <td><span style="background: #B0E2FF; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>lightskyblue1</td>
      <td><span style="background: #A4D3EE; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>lightskyblue2</td>
      <td><span style="background: #8DB6CD; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>lightskyblue3</td>
    </tr>
    <tr>
      <td><span style="background: #607B8B; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>lightskyblue4</td>
      <td><span style="background: #ADD8E6; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>lightblue</td>
      <td><span style="background: #BFEFFF; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>lightblue1</td>
      <td><span style="background: #B2DFEE; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>lightblue2</td>
    </tr>
    <tr>
      <td><span style="background: #9AC0CD; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>lightblue3</td>
      <td><span style="background: #68838B; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>lightblue4</td>
      <td><span style="background: #AFEEEE; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>paleturquoise</td>
      <td><span style="background: #BBFFFF; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>paleturquoise1</td>
    </tr>
    <tr>
      <td><span style="background: #AEEEEE; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>paleturquoise2</td>
      <td><span style="background: #96CDCD; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>paleturquoise3</td>
      <td><span style="background: #668B8B; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>paleturquoise4</td>
      <td><span style="background: #B0C4DE; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>lightsteelblue</td>
    </tr>
    <tr>
      <td><span style="background: #CAE1FF; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>lightsteelblue1</td>
      <td><span style="background: #BCD2EE; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>lightsteelblue2</td>
      <td><span style="background: #A2B5CD; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>lightsteelblue3</td>
      <td><span style="background: #6E7B8B; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>lightsteelblue4</td>
    </tr>
    <tr>
      <td><span style="background: #B0E0E6; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>powderblue</td>
      <td><span style="background: #E0FFFF; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>lightcyan</td>
      <td><span style="background: #E0FFFF; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>lightcyan1</td>
      <td><span style="background: #D1EEEE; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>lightcyan2</td>
    </tr>
    <tr>
      <td><span style="background: #B4CDCD; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>lightcyan3</td>
      <td><span style="background: #7A8B8B; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>lightcyan4</td>
      <td><span style="background: #F0F8FF; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>aliceblue</td>
      <td><span style="background: #F0FFFF; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>azure</td>
    </tr>
    <tr>
      <td><span style="background: #F0FFFF; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>azure1</td>
      <td><span style="background: #E0EEEE; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>azure2</td>
      <td><span style="background: #C1CDCD; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>azure3</td>
      <td><span style="background: #838B8B; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>azure4</td>
    </tr>
    <tr>
      <td><span style="background: #000080; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>navy</td>
      <td><span style="background: #000080; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>navyblue</td>
      <td><span style="background: #00008B; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>darkblue</td>
      <td><span style="background: #0000CD; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>mediumblue</td>
    </tr>
    <tr>
      <td><span style="background: #0000FF; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>blue</td>
      <td><span style="background: #0000FF; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>blue1</td>
      <td><span style="background: #0000EE; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>blue2</td>
      <td><span style="background: #0000CD; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>blue3</td>
    </tr>
    <tr>
      <td><span style="background: #00008B; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>blue4</td>
      <td><span style="background: #191970; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>midnightblue</td>
      <td><span style="background: #483D8B; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>darkslateblue</td>
      <td><span style="background: #6A5ACD; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>slateblue</td>
    </tr>
    <tr>
      <td><span style="background: #836FFF; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>slateblue1</td>
      <td><span style="background: #7A67EE; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>slateblue2</td>
      <td><span style="background: #6959CD; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>slateblue3</td>
      <td><span style="background: #473C8B; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>slateblue4</td>
    </tr>
    <tr>
      <td><span style="background: #7B68EE; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>mediumslateblue</td>
      <td><span style="background: #8470FF; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>lightslateblue</td>
      <td><span style="background: #8A2BE2; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>blueviolet</td>
      <td><span style="background: #9370DB; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>mediumpurple</td>
    </tr>
    <tr>
      <td><span style="background: #AB82FF; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>mediumpurple1</td>
      <td><span style="background: #9F79EE; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>mediumpurple2</td>
      <td><span style="background: #8968CD; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>mediumpurple3</td>
      <td><span style="background: #5D478B; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>mediumpurple4</td>
    </tr>
    <tr>
      <td><span style="background: #9400D3; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>darkviolet</td>
      <td><span style="background: #9932CC; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>darkorchid</td>
      <td><span style="background: #BF3EFF; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>darkorchid1</td>
      <td><span style="background: #B23AEE; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>darkorchid2</td>
    </tr>
    <tr>
      <td><span style="background: #9A32CD; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>darkorchid3</td>
      <td><span style="background: #68228B; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>darkorchid4</td>
      <td><span style="background: #A020F0; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>purple</td>
      <td><span style="background: #9B30FF; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>purple1</td>
    </tr>
    <tr>
      <td><span style="background: #912CEE; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>purple2</td>
      <td><span style="background: #7D26CD; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>purple3</td>
      <td><span style="background: #551A8B; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>purple4</td>
      <td><span style="background: #BA55D3; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>mediumorchid</td>
    </tr>
    <tr>
      <td><span style="background: #E066FF; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>mediumorchid1</td>
      <td><span style="background: #D15FEE; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>mediumorchid2</td>
      <td><span style="background: #B452CD; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>mediumorchid3</td>
      <td><span style="background: #7A378B; border: 1px #000 solid;">&nbsp&nbsp;&nbsp;&nbsp;</span></td><td>mediumorchid4</td>
    </tr>
  </table>


The CardApp
+++++++++++

The ``CardApp`` class is used to instantiate an application. Depending on your
level of skill and / or need for refinement, there are several approaches to
this.

If you have defined a stack in a JSON file (see below), all that is required
is::

    from pypercard import CardApp

    app = CardApp()
    app.load("my_stack.json")
    app.run()

If you're declaring your stack of cards with Python (something you'll need to
do for more complicated applications), then you can pass the stack as an
argument when instantiating the ``CardApp`` class. The ``stack`` argument must
be a list of ``Card`` instances::

    from pypercard import CardApp, Card

    app = CardApp(stack=[Card("hello", text="Hello, World!"), ])
    app.run()

Finally, you could use the ``CardApp`` class's ``add_card`` method to add
individual ``Card`` instances. However, the ``stack`` argument is far more
convenient and is a simple convenience wrapper around the ``add_card`` to save
you time.

Obviously, as demonstrated in the examples above, to make the application run
you call the ``run`` method.

The ``CardApp`` can take the following arguments when instantiated:

* ``name`` - what your operating system will display as the name of the
  application. Defaults to ``"A PyperCard Application :-)"``.
* ``data_store`` - a dictionary the application should use for storing
  application state. Pass in your own dictionary if you need to pre-load it
  with default state, depending on the needs of your application. If you don't
  supply a ``data_store`` argument, then PyperCard will use an empty
  dictionary. The ``data_store`` instance is one of the arguments passed into
  transition functions (see below).
* ``stack`` - a list of ``Card`` instances which defines the application's
  stack (see description above).

For more information about the ``CardApp`` class, please see :doc:`api`.

Cards
+++++

Instances of the ``Card`` class represent different screens in the application
stack. Users transition between cards in one of two ways: by pressing a button
to activate a transition (see below) or by automatically advancing to a target
card after a pre-determined period of time.

All cards must have a unique (and preferably meaningful) ``title`` attribute,
supplied as an argument when the object is instantiated. All the other
attributes for a card are optional and define how the card looks and behaves.
Such attributes are usually assigned when the card is instantiated. Once the
card is associated with an application its attributes cannot be changed.

The available attributes are (see the :doc:`api` for more details):

* ``title`` - a unique (within the stack) and preferably meaningful string
  identifier for the card.
* ``text`` - the (string) textual content of the card. It's possible to change
  the look of the text using
  `BBCode style markup <https://kivy.org/doc/stable/api-kivy.core.text.markup.html>`_.
  If there is a form, the ``text`` will be displayed in the form of a label for
  the form input, otherwise the text will take up the full screen.
* ``text_color`` - a string containing the default colour of the text. Defaults
  to ``"white"``. See the section on colour (above) for valid colour names and
  values.
* ``text_size`` - an integer representing the default size of the text.
  Defaults to 48 (px).
* ``form`` - the type of form input (see below) associated with the card. Must
  be one of the attributes of the ``Inputs`` enum class: ``TEXTBOX``,
  ``TEXTAREA``, ``MULTICHOICE``, ``SELECT`` or ``SLIDER``.
* ``options`` - a list or tuple containing configuration options needed by the
  form input. See the description of each form input (below) for more
  information.
* ``sound`` - a string containing the path to a sound file to play when the
  card is displayed. Only sound formats supported by the platform upon which
  the application is running can be played.
* ``sound_repeat`` - a boolean flag to indicate if the sound associated with
  the card should continue to loop.
* ``background`` - a string containing either the colour (see above) of the
  card's background, or a path to an image to display as the background. The
  default value is ``"black"``.
* ``buttons`` - a list or tuple containing dictionary definitions of the
  buttons to display on the card which will be used to activate a transition
  to other cards in the stack. Each button dictionary must have at least two
  attributes: ``label`` (associated with a string containing the text to
  display on the button) and ``target`` (associated with either a string
  containing the ``title`` of the target card to transition to, or a function
  [see below] containing business logic which will return the ``title`` of
  the target card for transition). Button dictionaries may also contain three
  options attributes: ``text_size`` (an integer indication of the size of the
  button's label text), ``text_color`` (a string containing the colour of the
  button's label text), and ``background_color`` (a string containing the
  colour of the button's background).
* ``auto_advance`` - a floating point value to indicate the number of seconds
  to wait until the card automatically transitions to the card indicated by the
  ``auto_target`` attribute. It is possible to mix buttons and ``auto_advance``
  as a means to transition from a card. If a button is clicked before the
  scheduled automatic transition then the scheduled transition will not take
  place.
* ``auto_target`` - a string containing the ``title`` of the card to transition
  to after the number of seconds indicated by the ``auto_advance`` attribute.

Here's an example of a card with textual content and a single button which will
transition the application to another card called ``another_card``. Notice how
the first argument is the card's mandatory and unique ``title`` attribute::

    from pypercard import Card, CardApp

    card = Card("example_card", text="Hello, World!", text_color="red")
    app = CardApp(stack=[card, ])
    app.run()

It's important to understand the life-cycle of a card.

When the ``Card`` class is instantiated with the various attributes needed to
describe the new card object's content and behaviour, the various constraints
required for the card to behave properly are validated. If there's a problem
(for example, you specify a ``form`` input which requires ``options`` to work
properly, but you fail to supply any ``options``) then a ``ValueError``
exception will be raised.

When the card is added to the application (usually as a member of a stack list
when the application is instantiated), then it is drawn as a
``Kivy.uix.screenmanager.Screen`` instance and added to a screen manager object
that belongs to the application.

If a card is indicated as the next target to display, before it is shown to the
user all the textual content of the card is re-formatted against the contents
of the application's ``data_store``. This means Python's built-in simple
string templating language can be used to make the content of the card
dynamic. For instance if the ``text`` attribute of the card was the string,
``"Hello, {name}."``, and the application's ``data_store`` dictionary was,
``{"name": "Nicholas"}``, then the textual content displayed to the user would
be updated to, ``"Hello, Nicholas"``. The textual content, form label and
button labels can all be updated in this way.

When a card is first displayed to the user two things happen: if a ``sound``
should be played (and repeated) then this is started, and if the card can
automatically advance after a certain period of time, this event is scheduled.

Finally, when the card is removed from the screen (and before the next card
is displayed), then if there is any sound playing, this is stopped.

JSON Stacks
+++++++++++

PyperCard is designed to be easy to use and understand with special attention
paid to the needs of beginner developers.

Writing Python code can be intimidating for beginner developers. In order to
declare the UI stack of cards in Python a developers needs to instantiate
several classes, create a Python list and even write their own functions when
all they want to do is describe a very simple stack of cards.

As a result, it's possible to declare a simple stack of cards that require no
business logic using the JSON data format. This was the approach taken by
Adafruit who
`provided the inspiration for this project <https://learn.adafruit.com/circuit-python-your-own-adventure>`_.

The JSON file must contain an array of JSON objects. Each object represents a
card in the application's stack.

Attributes of the JSON objects must match the names of the arguments used when
instantiating the Python ``Card`` class (see above).

Use the ``CardApp`` class's ``load`` convenience function with the path to the
JSON file to load the stack::

    from pypercard import CardApp

    app = CardApp()
    app.load("my_stack.json")
    app.run()

The JSON data format is a lightweight and easy to read solution which has the
advantage of being a ubiquitous form of data exchange. Following simple naming
conventions for defining JSON objects means little effort is needed to define
a working stack for a simple app::

    [
        {
            "title": "hello",
            "text": "Hello there!",
            "text_color": "green",
            "buttons": [
                {
                    "label": "OK",
                    "target": "goodbye"
                }
            ]
        },
        {
            "title": "goodbye",
            "text": "Goodbye!",
            "text_color": "red",
            "buttons": [
                {
                    "label": "OK",
                    "target": "hello"
                }
            ]
        }
    ]

This also has the advantage that, at some later date, a graphical beginner
friendly tool, could be created to emit valid JSON files to make this process
even less intimidating. Nevertheless, writing JSON in a text editor is not an
onerous task and goes some way to demonstrating how simple it is to use a text
based medium for programming.

Forms
+++++

As has been pointed out in the section on the ``Card`` class (see above), a
card can contain a form input field. Only one form input field can be displayed
on each card. The input field is specified as one of the attributes of the
``Inputs`` enumeration class::

    from pypercard import Card, Inputs, CardApp

    card = Card("form_example", form=Inputs.TEXTBOX, text="A text box")
    app = CardApp(stack=[card, ])
    app.run()

In the example above, a text box with the label ``"A text box"`` will be
displayed by the card.

The value of the form input field is used as an argument into the transition
function called when the user moves away from the card.

Sometimes, the form input field needs extra information to designate
``options`` needed to display the input field properly. These options are
explained below as each form field is described.

TEXTBOX
~~~~~~~

A text box is a single line text entry field which needs no special options:

.. image:: textbox.png

TEXTAREA
~~~~~~~~

A text area is a multi line text entry field which needs no special options:

.. image:: textarea.png

MULTICHOICE
~~~~~~~~~~~

A multiple choice field allows users to select none, any or all of a range of
options. These options should be expressed as a tuple of string values.

.. image:: multichoice.png

SELECT
~~~~~~

A selector field allows users to select either a single value or no value from
a range of options. The options should be expressed as a tuple of string
values.

.. image:: select.png

SLIDER
~~~~~~

A slider is for providing numeric input. It must have a minimum (min),
maximum (max) and optional step value provided in a tuple of numeric values.

.. image:: slider.png

The code for creating each of the illustrated form elements, including examples
of the options for multiple choice, selector and slider fields is copied
below::

    from pypercard import Inputs, Card, CardApp


    stack = [
        Card(
            "TextBox",
            form=Inputs.TEXTBOX,
            text="A single line textbox",
            buttons=[{"label": "Next", "target": "TextArea"}],
        ),
        Card(
            "TextArea",
            form=Inputs.TEXTAREA,
            text="A multi line text area",
            buttons=[{"label": "Next", "target": "MultiChoice"}],
        ),
        Card(
            "MultiChoice",
            form=Inputs.MULTICHOICE,
            options=["Ham", "Eggs", "Bacon", "Sausage"],
            text="A multiple choice selection",
            buttons=[{"label": "Next", "target": "Select"}],
        ),
        Card(
            "Select",
            form=Inputs.SELECT,
            options=["Red", "Green", "Yellow", "Blue"],
            text="A single choice collection",
            buttons=[{"label": "Next", "target": "Slider"}],
        ),
        Card(
            "Slider",
            form=Inputs.SLIDER,
            options=(-100, 100, 10),
            text="A slider with min/max/step",
            buttons=[{"label": "Next", "target": "TextBox"}],
        ),
    ]
    app = CardApp(name="Examples of form elements...", stack=stack)
    app.run()

Transitions
+++++++++++

Transitions are how the user moves between cards. Transitions can be of two
types:

* A string value referencing the unique ``title`` attribute of the target card.
* A function, containing business logic, which returns a string value
  referencing the unique ``title`` attribute of the target card.

Transitions are declared in two places:

* As the value associated with the ``"target"`` attribute of a button, or;
* As the value of a card's ``auto_target`` attribute.

If you're using transition functions, you should declare them first, before
creating the ``Card`` objects which may reference them.

Transition functions always take two arguments and must always return a string
containing a valid card ``title``. The two arguments are:

* ``data_store`` - a reference to the application's ``data_store`` instance
  which is used to set and get application state.
* ``form_value`` - the current value of the form input field in the card from
  which the user is transitioning. This will be ``None`` if the card didn't
  contain a form input field, or false-y if the user didn't enter anything.

As a result, your transition function should look something like this::

    def my_transition(data_store, form_value):
        # Arbitrary Python code here.
        return "a_card_title"

.. warning::

    The code within the transition function can be any arbitrary Python, but it
    is important to note that these are **blocking functions** so do not do
    anything which will cause the application to pause.

Please note that the text associated with labels and buttons is formatted for
template names with the values found in the ``data_store`` (see the example
below). In this way, values stored in the ``data_store`` can safely be
shown to the user.

The following simple example demonstrates how transition functions work::

    from pypercard import Inputs, Card, CardApp


    def get_name(data_store, form_value):
        """
        Gets the name of the user from the form field and stores it in the
        data_store. If no name is given, causes an error to be displayed.
        """
        if form_value:
            data_store["name"] = form_value
            return "hello"
        else:
            return "error"


    stack = [
        Card(
            "get_value",
            form=Inputs.TEXTBOX,
            text="What is your name..?",
            buttons=[
                {"label": "OK", "target": get_name}  # Use the function!
            ]
        ),
        Card(
            "hello",
            text="Hello {name}!",
            buttons=[
                {"label": "OK", "target": "get_value"}
            ]
        ),
        Card(
            "error",
            text="ERROR\n\nPlease enter a name!",
            text_color="white",
            background="red",
            auto_advance=3,
            auto_target="get_value"
        ),
    ]

    app = CardApp(stack=stack)
    app.run()

The end result looks like this:

.. image:: name_app.gif

Packaging
+++++++++

Coming in a future version.
