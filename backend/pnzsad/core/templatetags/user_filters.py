from django import template

register = template.Library()


@register.filter
def addclass(field, css):
    return field.as_widget(attrs={'class': css})


@register.filter
def add_multiple_tags(field, tags):
    tags = iter(tags.split('~'))
    attrs = {}

    while True:
        try:
            key = next(tags)
            value = next(tags)
        except StopIteration:
            break
        attrs[key] = value

    return field.as_widget(attrs=attrs)


@register.filter
def add_max_tag(field, max):
    return field.as_widget(attrs={'class': 'cart__input', 'max': max})


@register.filter
def int_view(value):
    try:
        return int(value)
    except BaseException as err:
        return err
