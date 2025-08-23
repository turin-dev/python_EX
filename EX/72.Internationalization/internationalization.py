"""Internationalization examples using gettext and locale."""

from __future__ import annotations

import gettext
import locale
import calendar


def demonstrate_gettext() -> None:
    # load a translation catalog if available, fallback to default language
    lang = gettext.translation('messages', localedir='locale', languages=['fr'], fallback=True)
    lang.install()
    # translate a message
    print(_('Hello, world!'))


def demonstrate_locale_formatting() -> None:
    # set locale to user default
    locale.setlocale(locale.LC_ALL, '')
    value = 123456.789
    formatted = locale.format_string("%.2f", value, grouping=True)
    print("Localized number:", formatted)
    # print month name in German locale if available
    try:
        locale.setlocale(locale.LC_TIME, 'de_DE.utf8')
        print("March in German:", calendar.month_name[3])
    except locale.Error:
        print("German locale not installed")


if __name__ == "__main__":
    demonstrate_gettext()
    demonstrate_locale_formatting()