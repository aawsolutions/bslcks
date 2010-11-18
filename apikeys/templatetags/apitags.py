from django import template

register = template.Library()

@register.filter(name='fetchkey')
def fetchkey(keys, target):
    if keys != 'ERROR':
        return keys.filter(vendor__name=target)[0].key 
    return keys
