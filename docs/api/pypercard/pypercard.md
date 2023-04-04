# {py:mod}`pypercard`

```{py:module} pypercard
:noindex:
```

```{autodoc2-docstring} pypercard
:allowtitles:
```

## Module Contents

### Classes

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`DataStore <pypercard.DataStore>`
  - ```{autodoc2-docstring} pypercard.DataStore
    :summary:
    ```
* - {py:obj}`Card <pypercard.Card>`
  - ```{autodoc2-docstring} pypercard.Card
    :summary:
    ```
* - {py:obj}`App <pypercard.App>`
  - ```{autodoc2-docstring} pypercard.App
    :summary:
    ```
````

### API

`````{py:class} DataStore(**kwargs)
:canonical: pypercard.DataStore
:noindex:

```{autodoc2-docstring} pypercard.DataStore
```

```{rubric} Initialization
```

```{autodoc2-docstring} pypercard.DataStore.__init__
```

````{py:method} clear()
:canonical: pypercard.DataStore.clear
:noindex:

```{autodoc2-docstring} pypercard.DataStore.clear
```

````

````{py:method} copy()
:canonical: pypercard.DataStore.copy
:noindex:

```{autodoc2-docstring} pypercard.DataStore.copy
```

````

````{py:method} get(key, default=None)
:canonical: pypercard.DataStore.get
:noindex:

```{autodoc2-docstring} pypercard.DataStore.get
```

````

````{py:method} items()
:canonical: pypercard.DataStore.items
:noindex:

```{autodoc2-docstring} pypercard.DataStore.items
```

````

````{py:method} keys()
:canonical: pypercard.DataStore.keys
:noindex:

```{autodoc2-docstring} pypercard.DataStore.keys
```

````

````{py:method} pop(key, default=None)
:canonical: pypercard.DataStore.pop
:noindex:

```{autodoc2-docstring} pypercard.DataStore.pop
```

````

````{py:method} popitem()
:canonical: pypercard.DataStore.popitem
:noindex:
:abstractmethod:

```{autodoc2-docstring} pypercard.DataStore.popitem
```

````

````{py:method} setdefault(key, value=None)
:canonical: pypercard.DataStore.setdefault
:noindex:

```{autodoc2-docstring} pypercard.DataStore.setdefault
```

````

````{py:method} update(iterable)
:canonical: pypercard.DataStore.update
:noindex:

```{autodoc2-docstring} pypercard.DataStore.update
```

````

````{py:method} values()
:canonical: pypercard.DataStore.values
:noindex:

```{autodoc2-docstring} pypercard.DataStore.values
```

````

````{py:method} __len__()
:canonical: pypercard.DataStore.__len__
:noindex:

```{autodoc2-docstring} pypercard.DataStore.__len__
```

````

````{py:method} __getitem__(key)
:canonical: pypercard.DataStore.__getitem__
:noindex:

```{autodoc2-docstring} pypercard.DataStore.__getitem__
```

````

````{py:method} __setitem__(key, value)
:canonical: pypercard.DataStore.__setitem__
:noindex:

```{autodoc2-docstring} pypercard.DataStore.__setitem__
```

````

````{py:method} __delitem__(key)
:canonical: pypercard.DataStore.__delitem__
:noindex:

```{autodoc2-docstring} pypercard.DataStore.__delitem__
```

````

````{py:method} __iter__()
:canonical: pypercard.DataStore.__iter__
:noindex:

```{autodoc2-docstring} pypercard.DataStore.__iter__
```

````

````{py:method} __contains__(key)
:canonical: pypercard.DataStore.__contains__
:noindex:

```{autodoc2-docstring} pypercard.DataStore.__contains__
```

````

`````

`````{py:class} Card(name, template=None, on_render=None, auto_advance=None, auto_advance_after=None)
:canonical: pypercard.Card
:noindex:

```{autodoc2-docstring} pypercard.Card
```

```{rubric} Initialization
```

```{autodoc2-docstring} pypercard.Card.__init__
```

````{py:method} register_app(app)
:canonical: pypercard.Card.register_app
:noindex:

```{autodoc2-docstring} pypercard.Card.register_app
```

````

````{py:method} render(datastore)
:canonical: pypercard.Card.render
:noindex:

```{autodoc2-docstring} pypercard.Card.render
```

````

````{py:method} hide()
:canonical: pypercard.Card.hide
:noindex:

```{autodoc2-docstring} pypercard.Card.hide
```

````

````{py:method} register_transition(element_id, event_name, handler)
:canonical: pypercard.Card.register_transition
:noindex:

```{autodoc2-docstring} pypercard.Card.register_transition
```

````

````{py:method} get_by_id(element_id)
:canonical: pypercard.Card.get_by_id
:noindex:

```{autodoc2-docstring} pypercard.Card.get_by_id
```

````

````{py:method} get_element(selector)
:canonical: pypercard.Card.get_element
:noindex:

```{autodoc2-docstring} pypercard.Card.get_element
```

````

````{py:method} get_elements(selector)
:canonical: pypercard.Card.get_elements
:noindex:

```{autodoc2-docstring} pypercard.Card.get_elements
```

````

````{py:method} play_sound(name, loop=False)
:canonical: pypercard.Card.play_sound
:noindex:

```{autodoc2-docstring} pypercard.Card.play_sound
```

````

````{py:method} pause_sound(name, keep_place=False)
:canonical: pypercard.Card.pause_sound
:noindex:

```{autodoc2-docstring} pypercard.Card.pause_sound
```

````

`````

`````{py:class} App(name='My PyperCard App', datastore=None, card_list=None, sounds=None)
:canonical: pypercard.App
:noindex:

```{autodoc2-docstring} pypercard.App
```

```{rubric} Initialization
```

```{autodoc2-docstring} pypercard.App.__init__
```

````{py:method} _resolve_card(card_reference)
:canonical: pypercard.App._resolve_card
:noindex:

```{autodoc2-docstring} pypercard.App._resolve_card
```

````

````{py:method} render_card(card)
:canonical: pypercard.App.render_card
:noindex:

```{autodoc2-docstring} pypercard.App.render_card
```

````

````{py:method} add_card(card)
:canonical: pypercard.App.add_card
:noindex:

```{autodoc2-docstring} pypercard.App.add_card
```

````

````{py:method} remove_card(card_reference)
:canonical: pypercard.App.remove_card
:noindex:

```{autodoc2-docstring} pypercard.App.remove_card
```

````

````{py:method} add_sound(name, url)
:canonical: pypercard.App.add_sound
:noindex:

```{autodoc2-docstring} pypercard.App.add_sound
```

````

````{py:method} get_sound(name)
:canonical: pypercard.App.get_sound
:noindex:

```{autodoc2-docstring} pypercard.App.get_sound
```

````

````{py:method} remove_sound(name)
:canonical: pypercard.App.remove_sound
:noindex:

```{autodoc2-docstring} pypercard.App.remove_sound
```

````

````{py:method} transition(from_card, element, event)
:canonical: pypercard.App.transition
:noindex:

```{autodoc2-docstring} pypercard.App.transition
```

````

````{py:method} start(card_reference)
:canonical: pypercard.App.start
:noindex:

```{autodoc2-docstring} pypercard.App.start
```

````

````{py:method} dump()
:canonical: pypercard.App.dump
:noindex:

```{autodoc2-docstring} pypercard.App.dump
```

````

````{py:method} load(tree)
:canonical: pypercard.App.load
:noindex:

```{autodoc2-docstring} pypercard.App.load
```

````

`````
