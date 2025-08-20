
from django import template
register = template.Library()

@register.filter
def as_widget(field, attrs):
    attrs = attrs or {}
    return field.as_widget(attrs={'class': 'form-select' if field.field.widget.__class__.__name__ == 'Select' else 'form-control', **attrs})
