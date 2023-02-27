from typing import Any

from django import template

register = template.Library()


@register.filter(name='get')
def get(value: dict[str, Any], arg: str) -> Any:
    return value.get(arg, [])
