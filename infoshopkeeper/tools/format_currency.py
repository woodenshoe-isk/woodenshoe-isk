import locale


def format_currency(currency_string="0", currency_float=0.0):
    locale.setlocale(locale.LC_ALL, locale.getdefaultlocale())
    if currency_string:
        currency_string = currency_string.strip(locale.localeconv()["currency_symbol"])
        currency_float = locale.atof(currency_string)
    return locale.currency(currency_float)
