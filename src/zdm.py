#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib2
import json
from xml.etree import ElementTree as ET


def get_items(uri):
    items = []
    request = urllib2.Request(uri)
    request.add_header("User-Agent", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.114 Safari/537.36")
    request.add_header("Host", "www.smzdm.com")
    entries = json.load(urllib2.urlopen(request))
    category_str = ""
    for it in entries:
        try:
            channel = it.get('article_channel', u'')
            price = it.get('article_price', u'无价格')
            category = it['article_category']
            if isinstance(category, dict):
                category_str = category.get('title', '')
            if isinstance(category, list):
                category_str = ",".join(category)

            tags = u', '.join([tag['name'] for tag in it['article_tese_tags'] if tag['name'] != category_str])
            items.append({
                'uid'           : it['article_id'],
                'title'         : u"%s: %s" % (channel, it['article_title']), 
                'subtitle'      : u"%s【%s, %s】" % (price, category_str, tags),
                'arg'           : it['article_url'], 
                'description'   : "test",
                'icon'          : 'icon.png',
            })
        except:
            pass

    xml = generate_xml(items)
    return xml


def generate_xml(items):
    xml_items = ET.Element('items')
    for item in items:
        xml_item = ET.SubElement(xml_items, 'item')
        for key in item.keys():
            if key in ('arg',):
                xml_item.set(key, item[key])
            else:
                child = ET.SubElement(xml_item, key)
                child.text = item[key]
    return ET.tostring(xml_items)

#if __name__ == '__main__':
#    print get_items("http://www.smzdm.com/json_more?timesort=120212735313")
