#!/usr/bin/env python

import sys

from xml.etree import ElementTree

from xml.etree.ElementTree import Element, SubElement

from xml.dom import minidom

from lxml import etree

#from ElementTree_pretty import prettify

def prettify(elem):
    """Return a pretty-printed XML string for the Element.
    """
    rough_string = ElementTree.tostring(elem,'utf8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="\t")




def get_voc_header(fname, img_size,annotate_folder):
	top = Element('annotation')
	
	folder = SubElement(top,'folder')
	folder.text = 'VOC2007'
	
	filename = SubElement(top,'filename')

	filename.text = fname


	source = SubElement(top,'source')
	database = SubElement(source,'database')
	database.text = 'SuperMarket Video Frame Database'
	annotation_source = SubElement(source,'annotation')
	annotation_source.text = 'SuperMarket Video Annotation by Mani'
	image_source = SubElement(source,'image')
	image_source.text = "STARS Camera"
	imageid_source = SubElement(source,'flickerid')
	imageid_source.text = "STARS ID"

	owner = SubElement(top,'owner')
	id_owner = SubElement(owner,'flickerid')
	id_owner.text= "STARS ID"
	id_name = SubElement(owner,'name')
	id_name.text = "STARS INRIA Sophia"

	size_part = SubElement(top,'size')
	width = SubElement(size_part,'width')
	height = SubElement(size_part,'height')
	depth = SubElement(size_part,'depth')

	width.text = str(img_size[1])
	height.text = str(img_size[0])
	if len(img_size)==3:
		depth.text = str(img_size[2])
	else:
		depth.text = '1'

	segmented = SubElement(top,'segmented')
	segmented.text ='0'
	return top




