from django import template  
import socket
import struct
from iptocountry.models import IpToCountry
from django.conf import settings
import os

register = template.Library()

def ip2long(ip):
    ip_array = ip.split('.')
    ip_long = int(ip_array[0]) * 16777216 + int(ip_array[1]) * 65536 + int(ip_array[2]) * 256 + int(ip_array[3])
    return ip_long

def long2ip(long):
    return socket.inet_ntoa(struct.pack("!I", long))

class FlagObject(template.Node):  
    def __init__(self, ip, varname):
        self.ip = ip
        self.varname = varname
   
    def render(self, context):  
        ip = ip2long(template.resolve_variable(self.ip, context))
        try:
            iptc = IpToCountry.objects.get(IP_FROM__lte=ip, IP_TO__gte=ip)
            iptc.flag_url = os.path.join(os.path.join(settings.MEDIA_URL, 'iptocountry/flags'), iptc.COUNTRY_CODE2.lower()+'.gif')
            context.update({self.varname: iptc,})
        except IpToCountry.DoesNotExist:
            pass
        return ''

def get_flag(parser, token):  
    """
    Retrieves a IpToCountry object given ip.

    Usage::

       {% get_flag [ip] as [varname] %}

    Example::

        {% get_flag object.ip_address as flag %}
    """
    bits = token.contents.split()
    if len(bits) != 4:
        raise template.TemplateSyntaxError(_('%s tag requires exactly three arguments') % bits[0])
    if bits[2] != 'as':
        raise template.TemplateSyntaxError(_("second argument to %s tag must be 'as'") % bits[0])
    return FlagObject(bits[1], bits[3])
   
register.tag('get_flag', get_flag) 