"""Template tags for translations."""
from django import template
from django.urls import resolve, reverse
from django.utils.translation import activate, get_language

register = template.Library()

@register.simple_tag(takes_context=True)
def change_lang_url(context, lang):
    """Change the language in the URL."""
    path = context['request'].path
    url_parts = resolve(path)

    url = path
    if 'i18n_patterns' in context.template.engine.builtins:
        # If using i18n_patterns, build the URL with the new language
        cur_language = get_language()
        try:
            activate(lang)
            url = reverse(url_parts.view_name, kwargs=url_parts.kwargs, current_app=url_parts.app_name)
        finally:
            activate(cur_language)

    return url