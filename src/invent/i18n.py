"""
A very simple gettext-ish internationalisation module for the Invent framework.
Language codes must conform to:

https://datatracker.ietf.org/doc/html/rfc5646

Based on original pre-COVID work by [Nicholas H.Tollervey.](https://ntoll.org/)

Copyright (c) 2024 Invent contributors.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import json
from pyscript import window


__all__ = [
    "load_translations",
    "set_language",
    "get_language",
    "_",
]


# The default language to use for translating strings. Initialise from the
# user's browser setting by default.
__language = window.navigator.language


# Will reference a dictionary of language/key translations used by _ to look
# up the replacement translations.
__translations = {}


def load_translations(translations="./invent/translations.json"):
    """
    Load the translations from the referenced JSON file.

    Checks the translations given the user's language preferences and sets the
    default language accordingly.

    The schema for the JSON file must be:

    {
      "fr-FR": {
        "hello": "bonjour",
        ...
      },
      "de": {
        "hello": "guten tag",
        ...
      },
      "zh": {
        "hello": "你好",
        ...
      },
      ...
    }
    """
    global __translations
    try:
        with open(translations, "r") as tr:
            __translations = json.load(tr)
    except Exception as ex:
        window.console.warn(str(ex))
    for language in window.navigator.languages:  # pragma: no cover
        if language in __translations:
            set_language(language)
            break


def set_language(to_language):
    """
    Sets the default language. This must be a valid RFC5646 language tag
    (e.g. "en-GB", "de" or "fr-FR"). Publishes a set_language message with
    details of the new language setting to the i18n channel.
    """
    # Avoid a circular import.
    from .channels import Message, publish

    global __language
    __language = to_language
    publish(
        Message(subject="set_language", to_language=to_language),
        to_channel="i18n",
    )


def get_language():
    """
    Get the current default language. The result should be a valid RFC5646
    language tag.
    """
    return __language


def _(text, language=None):
    """
    Look up the translation for the given text using either the given language
    code or the default language.
    """
    # No translations? Return the untranslated text.
    if not __translations:
        return text
    language = language if language else __language
    # If the translation for the text in the desired language exists, return
    # it. Otherwise, return the untranslated text.
    return __translations.get(language, {}).get(text, text)
