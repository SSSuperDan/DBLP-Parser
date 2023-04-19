#! /usr/bin/env python3

import argparse
import os
import csv
from lxml import etree
from xml.sax import make_parser
from xml.sax.handler import ContentHandler, feature_namespaces


def tree_recursive(tree, names):
    tl = tree.left
    tr = tree.right
    if tl is not None:
        if tl.name is not None:
            names.add(tl.name)
        tree_recursive(tl, names)
    if tr is not None:
        if tr.name is not None:
            names.add(tr.name)
        tree_recursive(tr, names)


def get_elements(dtd_file) -> [set, set]:
    dtd = etree.DTD(dtd_file)
    elements = set()
    attributes = set()
    for el in dtd.iterelements():
        if el.name == 'dblp':
            tree_recursive(el.content, elements)
            break

    for en in dtd.iterentities():
        if en.name == 'field':
            attributes = set(en.orig.split('|'))
            break
    return elements, attributes


def get_attributes(xml_file, elements, attributes) -> dict:
    parser = make_parser()
    parser.setFeature(feature_namespaces, 0)

    handler = AttributeHandler(elements, attributes)
    parser.setContentHandler(handler)
    parser.parse(xml_file)
    attributes_dict = handler.getattribute_dict()

    for element in elements:
        if len(attributes_dict[element]) == 0:
            attributes_dict.pop(element)

    print(attributes_dict)
    return attributes_dict


def parse_xml(xml_file, elements, attributes_dict, output_files):
    parser = make_parser()
    parser.setFeature(feature_namespaces, 0)

    handler = DataHandler(elements, attributes_dict, output_files)
    parser.setContentHandler(handler)
    parser.parse(xml_file)


def open_outputfiles(elements: set, element_attributes: dict, output_filename: str) -> dict:
    (path, ext) = os.path.splitext(output_filename)
    output_files = dict()
    for element in elements:
        fieldnames = element_attributes.get(element, None)
        if fieldnames is not None and len(fieldnames) > 0:
            fieldnames = sorted(list(fieldnames))
            fieldnames.insert(0, 'id')
            output_path = '%s_%s%s' % (path, element, ext)
            output_file = open(output_path, mode='w', encoding='UTF-8')
            output_writer = csv.DictWriter(output_file, fieldnames=fieldnames, delimiter=' ',
                                           quoting=csv.QUOTE_MINIMAL, quotechar='"', doublequote=True,
                                           restval='', extrasaction='raise')
            output_writer.writeheader()
            output_files[element] = output_writer
    return output_files


def existing_file(filename: str) -> str:
    if os.path.isfile(filename):
        return filename
    else:
        raise argparse.ArgumentTypeError('%s is not a valid input file!' % filename)


def parse_args():
    parser = argparse.ArgumentParser(description='Parse the DBLP XML file and convert it to CSV')
    parser.add_argument('xml_filename', action='store', type=existing_file, help='The XML file that will be parsed',
                        metavar='xml_filename')
    parser.add_argument('dtd_filename', action='store', type=existing_file,
                        help='The DTD file used to parse the XML file', metavar='dtd_filename')
    parser.add_argument('outputfile', action='store', type=str, help='The output CSV file', metavar='outputfile')

    parsed_args = parser.parse_args()

    return parsed_args


class AttributeHandler(ContentHandler):
    def __init__(self, elements: set, attributes: set):
        ContentHandler.__init__(self)
        self.CurrentTag = ""
        self.CurrentAttr = list()
        self.PreTag = ""
        self.Elements = elements
        self.BasicAttrs = attributes
        self.AttributesDict = dict()
        for element in elements:
            self.AttributesDict[element] = set()

    def getattribute_dict(self):
        return self.AttributesDict

    def startElement(self, tag, attributes):
        if self.PreTag == "" and tag in self.Elements:
            self.PreTag = tag
            keys = attributes.keys()
            if len(keys) > 0:
                self.AttributesDict[tag].update(keys)
        elif self.PreTag != "" and self.CurrentTag == "" and tag in self.BasicAttrs:
            self.CurrentTag = tag
            self.CurrentAttr = attributes.keys()

    def endElement(self, tag):
        if tag == self.CurrentTag:
            self.CurrentTag = ""
        elif tag == self.PreTag:
            self.PreTag = ""

    def characters(self, content):
        if self.PreTag != "" and self.CurrentTag != "" and content is not None:
            attr = self.AttributesDict[self.PreTag]
            attr.add(self.CurrentTag)
            if len(self.CurrentAttr) > 0:
                for at in self.CurrentAttr:
                    attr.add('%s-%s' % (self.CurrentTag, at))


class DataHandler(ContentHandler):
    def __init__(self, elements: set, attributes_dict: dict, output_files: dict):
        ContentHandler.__init__(self)
        self.index = 0
        self.PersistringTag = False
        self.CurrentTag = ""
        self.CurrentAttr = dict()
        self.PreTag = ""
        self.data = dict()
        self.Elements = elements
        self.AttributesDict = attributes_dict
        self.Output_files = output_files
        self.multiple_valued_cells = set()

    def startElement(self, tag, attributes):
        if self.PreTag == "" and tag in self.Elements:
            self.PreTag = tag
            self.data.clear()
            self.multiple_valued_cells.clear()
            keys = attributes.keys()
            if len(keys) > 0:
                self.data.update(attributes)
        elif self.PreTag != "" and self.CurrentTag == "" and tag in self.AttributesDict[self.PreTag]:
            self.CurrentTag = tag
            self.PersistringTag = False
            self.CurrentAttr = attributes

    def endElement(self, tag):
        if tag == self.CurrentTag:
            self.CurrentTag = ""
        elif tag == self.PreTag:
            for cell in self.multiple_valued_cells:
                self.data[cell] = '|||'.join(sorted(self.data[cell]))
            self.data['id'] = self.index
            self.Output_files[self.PreTag].writerow(self.data)
            self.index += 1
            self.PreTag = ""

    def set_cell_value(self, column_name: str, value: str):
        entry = self.data.get(column_name)
        if entry is None:
            self.data[column_name] = value
        else:
            if isinstance(entry, list):
                entry.append(value)
            else:
                self.data[column_name] = [entry, value]
                self.multiple_valued_cells.add(column_name)

    def append_cell_value(self, column_name: str, value: str):
        entry = self.data.get(column_name)
        if isinstance(entry, list):
            entry[-1] += value
        else:
            self.data[column_name] = entry + value

    def characters(self, content):
        if self.PreTag != "" and self.CurrentTag != "" and content is not None:
            if not self.PersistringTag:
                self.PersistringTag = True
                self.set_cell_value(self.CurrentTag, content)
            else:
                self.append_cell_value(self.CurrentTag, content)

            for k, v in self.CurrentAttr.items():
                column_name = '%s-%s' % (self.CurrentTag, k)
                self.set_cell_value(column_name, v)


def main():
    args = parse_args()
    if args.xml_filename is not None and args.dtd_filename is not None and args.outputfile is not None:
        with open(args.dtd_filename, mode='rb') as dtd_file:
            print('Reading elements from DTD file...')
            elements, attributes = get_elements(dtd_file)
        with open(args.xml_filename, mode='rb') as xml_file:
            print('Finding unique attributes for all elements...')
            attributes_dict = get_attributes(xml_file, elements, attributes)
        print('Opening output files...')
        outputfile = "output.csv"
        output_files = open_outputfiles(elements, attributes_dict, outputfile)

        with open(args.xml_filename, mode='rb') as xml_file:
            print('Parsing XML and writing to CSV files...')
            parse_xml(xml_file, elements, attributes_dict, output_files)


if __name__ == '__main__':
    main()
