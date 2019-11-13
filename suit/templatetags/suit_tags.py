import itertools
from django import template
from django.contrib.admin.utils import lookup_field
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import ForeignKey
from django.template.defaulttags import NowNode
from django.urls import NoReverseMatch, reverse
from django.utils.safestring import mark_safe
from suit import utils
from suit.config import get_config

register = template.Library()
simple_tag = register.simple_tag


@register.filter(name='suit_conf')
def suit_conf(name):
    value = get_config(name)
    return mark_safe(value) if isinstance(value, str) else value


@register.tag
def suit_date(parser, token):
    return NowNode(get_config('HEADER_DATE_FORMAT'))


@register.tag
def suit_time(parser, token):
    return NowNode(get_config('HEADER_TIME_FORMAT'))


@register.filter
def field_contents_foreign_linked(admin_field):
    """Return the .contents attribute of the admin_field, and if it
    is a foreign key, wrap it in a link to the admin page for that
    object.

    Use by replacing '{{ field.contents }}' in an admin template (e.g.
    fieldset.html) with '{{ field|field_contents_foreign_linked }}'.
    """
    fieldname = admin_field.field['field']
    displayed = admin_field.contents()
    obj = admin_field.form.instance

    if not hasattr(admin_field.model_admin, 'linked_readonly_fields') or fieldname not in admin_field .model_admin .linked_readonly_fields:
        return displayed

    try:
        fieldtype, attr, value = lookup_field(fieldname, obj, admin_field.model_admin)
    except ObjectDoesNotExist:
        fieldtype = None

    if isinstance(fieldtype, ForeignKey):
        try:
            url = admin_url(value)
        except NoReverseMatch:
            url = None
        if url:
            displayed = "<a href='%s'>%s</a>" % (url, displayed)
    return mark_safe(displayed)


@register.filter
def admin_url(obj):
    info = (obj._meta.app_label, obj._meta.object_name.lower())
    return reverse("admin:%s_%s_change" % info, args=[obj.pk])


@register.simple_tag
def suit_bc(*args):
    return utils.value_by_version(args)


@simple_tag
def suit_bc_value(*args):
    return utils.value_by_version(args)


@simple_tag
def admin_extra_filters(cl):
    """ Return the dict of used filters which is not included
    in list_filters form """
    used_parameters = list(itertools.chain(*(s.used_parameters.keys() for s in cl.filter_specs)))
    return dict((k, v) for k, v in cl.params.items() if k not in used_parameters)


def str_to_version(string):
    return tuple([int(s) for s in string.split('.')])

@register.filter
def get_menu_tree(path):
    array_path = path.split('/')
    return ('/'.join(array_path[0:4]) + "/").replace("//", "/")

@register.filter
def get_for_one_string(fields_list):
    return ' | '.join(x.capitalize().replace("_", " ") for x in fields_list)


@register.filter
def get_for_two_string(lista):
    result = []
    for fildset_type, fildset in lista:
        for field in fildset['fields']:
            result.append(field)
    return ' | '.join(x.capitalize().replace("_", " ") for x in result)


@register.filter
def get_for_two_count(lista):
    result = 0
    for lista_int in lista:
        for _int in lista_int:
            result += 1
    return result

@register.filter
def concatene(value1,value2):
    return str(value1) + " " + str(value2)

@register.filter
def get_menu_tree(path):
    array_path = path.split('/')
    return ('/'.join(array_path[0:4]) + "/").replace("//", "/")

@register.filter
def get_for_one_noespace(name):
    return name.replace(" ", "_")