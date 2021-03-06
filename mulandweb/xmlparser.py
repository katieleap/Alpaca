# coding: utf-8
'''Provides an XML parser for MulandWeb interface'''

from xml.etree.ElementTree import Element, SubElement, ParseError
from xml.etree.ElementTree import ElementTree as ElementWrapper
from io import BytesIO
from defusedxml import ElementTree

__all__ = ['load', 'loads', 'dump', 'dumps']

def dump(datain, file):
    '''Build and return XML file from data generated by Muland'''
    ElementWrapper(_build(datain)).write(file, encoding='utf-8',
                                         xml_declaration=True)

def dumps(datain):
    '''Build and return XML string from data generated by Muland'''
    buffer = BytesIO()
    dump(datain, buffer)
    return buffer.getvalue().decode('utf-8')

def _build(datain):
    '''Build and return XML Element from Muland Output dict'''
    datatag = Element('data')
    for file_key, file_value in datain.items():
        filetag = SubElement(datatag, file_key)
        for record in file_value:
            recordtag = SubElement(filetag, 'record')
            for recdata in record:
                SubElement(recordtag, 'rd').text = str(recdata)
    return datatag

def load(file):
    '''Load XML from file-like object and returns location list'''
    try:
        tree = ElementTree.parse(file)
        root = tree.getroot()
    except ParseError:
        return
    return _parse_root(root)

def loads(string):
    '''Load XML from string and returns location list'''
    try:
        tree = ElementTree.fromstring(string)
        root = tree.getroot()
    except ParseError:
        return
    return _parse_root(root)

def _parse_root(root):
    '''Parse Tree's root returning location list'''
    ret = []
    for element in root:
        if element.tag == 'location':
            location = _parse_location(element)
            if location is not None:
                ret.append(location)
    return ret

def _parse_location(location):
    '''Parse location tag returning dict of it.'''
    if 'lat' not in location.attrib:
        return
    if 'lng' not in location.attrib:
        return
    try:
        lnglat = [float(location.attrib['lng']),
                  float(location.attrib['lat'])]
    except ValueError:
        return
    ret = {'units': [], 'lnglat': lnglat}
    for element in location:
        if element.tag == 'unit':
            unit = _parse_unit(element)
            if unit is not None:
                ret['units'].append(unit)
        else:
            override = _parse_override(element)
            if override is not None:
                ret[element.tag] = override
    return ret

def _parse_unit(unit):
    '''Parse unit tag returning dict of it.'''
    if 'type' not in unit.attrib:
        return
    try:
        unit_type = int(unit.attrib['type'])
    except ValueError:
        return
    ret = {'type': unit_type}
    for element in unit:
        override = _parse_override(element)
        if override is not None:
            ret[element.tag] = override
    return ret

def _parse_override(override):
    '''Parse override tags returning value of override.'''
    try:
        value = float(override.text)
    except ValueError:
        return
    return value
