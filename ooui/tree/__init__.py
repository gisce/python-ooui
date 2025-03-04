from __future__ import absolute_import, unicode_literals
from .base import Tree


def parse_tree(xml):
    """
    Parse a tree from an XML string.
    :param xml:
    :return:
    :rtype ooui.tree.Tree
    """
    from lxml import etree

    tree = etree.fromstring(xml)
    tree = tree.xpath('//tree')[0]
    return Tree(tree)