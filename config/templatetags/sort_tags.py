from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag
def sort_link(request, field_name, display_name):
    """
    Vytvoří odkaz na řazení pro dané pole a zobrazený text.
    """
    # Aktuální parametry GET
    curr_sort_by = request.GET.get('sort_by', '')
    curr_sort_order = request.GET.get('sort_order', 'asc')

    # Přepnutí pořadí řazení
    new_sort_order = 'desc' if curr_sort_by == field_name and curr_sort_order == 'asc' else 'asc'

    # Kopírování aktuálních parametrů dotazu
    new_query_params = request.GET.copy()
    new_query_params['sort_by'] = field_name
    new_query_params['sort_order'] = new_sort_order

    # Sestavení nové URL
    base_url = request.path
    full_url = f"{base_url}?{new_query_params.urlencode()}"

    # Kontrola, zda je pole aktuálně tříděno a v jakém směru
    sort_icon = ''
    if curr_sort_by == field_name:
        sort_icon = ' ↑' if curr_sort_order == 'asc' else ' ↓'

    # Vrací odkaz na řazení s ikonou pro vizualizaci směru řazení
    return mark_safe(f'<a href="{full_url}">{display_name}{sort_icon}</a>')


@register.simple_tag
def sort_links(request, table_id, field_name, display_name):
    """ Vytvoří odkaz na řazení pro dané pole v zadané tabulce.
     v pohledu s vice tabulkamy"""
    sort_by_param = f'{table_id}_sort_by'
    sort_order_param = f'{table_id}_sort_order'

    # Aktuální parametry GET
    curr_sort_by = request.GET.get(sort_by_param, '')
    curr_sort_order = request.GET.get(sort_order_param, 'asc')

    # Přepnutí pořadí řazení
    new_sort_order = 'desc' if curr_sort_by == field_name and curr_sort_order == 'asc' else 'asc'

    # Kopírování aktuálních parametrů dotazu
    new_query_params = request.GET.copy()
    new_query_params[sort_by_param] = field_name
    new_query_params[sort_order_param] = new_sort_order

    # Sestavení nové URL
    base_url = request.path
    full_url = f"{base_url}?{new_query_params.urlencode()}"

    # Kontrola, zda je pole aktuálně tříděno a v jakém směru
    sort_icon = ''
    if curr_sort_by == field_name:
        sort_icon = ' ↑' if curr_sort_order == 'asc' else ' ↓'

    # Vrací odkaz na řazení s ikonou pro vizualizaci směru řazení
    return mark_safe(f'<a href="{full_url}">{display_name}{sort_icon}</a>')