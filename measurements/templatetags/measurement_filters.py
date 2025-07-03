# D:\blood_pressure\blood_pressure_python_2\measurements\templatetags\measurement_filters.py

from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """
    Returns the value from a dictionary for a given key.
    Allows access to dictionary items dynamically in Django templates.
    Usage: {{ my_dict|get_item:my_key }}
    """
    return dictionary.get(key)