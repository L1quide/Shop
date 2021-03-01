from django import template
from django.utils.safestring import mark_safe
from ..models import Smartphone

register = template.Library()

TABLE_HEAD = """
    <table>
        <tbody>
"""

TABLE_TAIL = """
        </tbody>
    </table>
"""

TABLE_CONTENT = """
        <tr>
        <td>{name}</td>
        <td>{value}</td>
    </tr>
"""

PRODUCT_SPEC = {
    'notebook': {
        'Диагональ': 'diagonal'
    },
    'smartphone': {
            'Диагональ': 'diagonal',
            'Наличие SD карты': 'sd_cart',
            'Объем памяти': 'sd_cart_max_volume'
        }
}

def get_product_spec(product, model_name):
    table_content = ''
    for name, value in PRODUCT_SPEC[model_name].items():
        table_content += TABLE_CONTENT.format(name=name, value=getattr(product, value))
    return table_content

@register.filter
def product_spec(product):
    model_name = product.__class__._meta.model_name
    if isinstance(product, Smartphone):
        if not product.sd_cart:
            PRODUCT_SPEC['smartphone'].pop('Объем памяти')
        else:
            PRODUCT_SPEC['smartphone']['Объем памяти'] = 'd_cart_max_volume'
    return mark_safe(TABLE_HEAD + get_product_spec(product, model_name) + TABLE_TAIL)