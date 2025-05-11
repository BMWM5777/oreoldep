from django import template

register = template.Library()

@register.filter
def censor_username(username):
    """
    Фильтр, который оставляет первые 2 и последние 2 символа имени, заменяя всё между ними звездочками.
    Если имя короче 5 символов, заменяет центральную часть на одну звездочку.
    """
    username = str(username)
    n = len(username)
    if n <= 2:
        return username
    if n <= 4:
        return username[0] + '*' + username[-1]
    stars = '*' * (n - 4)
    return username[:2] + stars + username[-2:]
