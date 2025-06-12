from lxml import etree


def preprocess_feature_tags(xml_str, feature_checker):
    doc = etree.fromstring(xml_str)

    for node in doc.xpath('//feature'):
        key = node.get('key')
        status = node.get('status', 'enabled')
        active = feature_checker(key)

        if status == 'enabled':
            condition_met = active
        elif status == 'disabled':
            condition_met = not active
        else:
            condition_met = True

        parent = node.getparent()
        if condition_met:
            for child in list(node):
                parent.insert(parent.index(node), child)
            parent.remove(node)
        else:
            parent.remove(node)

    return etree.tostring(doc)
