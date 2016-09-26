#!/usr/bin/env python

import sys # Required for reading command line arguments

from xml.etree import ElementTree as ET # Required for manipulating  XML files (XGTF files are also XML in nature)

from xml.etree.ElementTree  import QName # Required for handling namespaces in XGTF files

import os # Required for path manipulations

from os.path import expanduser # Required for expanding '~', which stands for home folder. Used just in case the command line arguments contain "~". Without this, python won't parse "~"

import glob

import shutil

import time

from xml.etree.ElementTree import Element, SubElement

from xml.etree.ElementTree  import QName # Required for handling namespaces in XGTF files

import os # Required for path manipulations

from skimage.data import imread # Required for reading images

from skimage.io import imsave # Required for writing image patches

from collections import Counter # Required for counting occourances of each element in a list

from os.path import expanduser # Required for expanding '~', which stands for home folder. Used just in case the command line arguments contain "~". Without this, python won't parse "~"

from subprocess import Popen

from voc_headers import *

def classify_patches(xgtf_name,frames_path,frame_ext,new_location,new_prefix):
	fname = os.path.expanduser(xgtf_name) # Full path of the Ground Truth XGTF File
	root_path, fname = os.path.split(fname)
	path_folder = os.path.expanduser(frames_path) # Full path of the folder where frames have been stored.
	frame_ext  = frame_ext  # File extension of the patches
	new_location  = os.path.expanduser(new_location)
	# The next three lines find out all the frame numbers present in the video
	patch_files = glob.glob(os.path.join(path_folder,'*.'+frame_ext))
	patch_files = [os.path.basename(f) for f in patch_files]
	patch_files = [os.path.splitext(f)[0] for f in patch_files]
	namespace = 'http://lamp.cfar.umd.edu/viper#' # All XGTF files from SUP use this namespace. DO NOT EDIT or REMOVE this line 
	doc = ET.parse(os.path.join(root_path,fname)) # This line reads the XGTF file from the disk
	data_tag = str(QName(namespace,'data')) # This helps Python to parse each tag by stripping it off its namespace part. So it is essential. DO NOT CHANGE OR COMMENT
	data = doc.find(data_tag) # All relevant data for creating patches is present with a "data" tag. Hence we find all nodes which have a "data" tag
	# The next 5 lines create empty lists for storing ground truth annotation information (frame number, height, width, x (column) and y (row)	
	frame_list = list()
	for x in data.iter():
		if (x.get('name')=='info2D'): # Those elements which have "data" tags  and  have "info2D" attribute  have annotation information. We now look beneath each such node
			f = [gt.get('framespan') for gt in x]
		        f =[ frame.rsplit(':',1)[0] for frame in f] # This line converts an entry like "432:432" to "432"
			frame_list = frame_list + f # We concatenate information into the lists created outside the loops. This helps us in counting number of people in each frame and writing files accordingly
	neg_patches =  list(set(patch_files)-set(frame_list)) # We find the negative patches in here
	neg_patches = [f+'.'+frame_ext for f in neg_patches] # In this and next line we reconstruct the filenames for positive and negative patches
	frame_list = [f +'.'+frame_ext for f in frame_list]
	if not(os.path.exists(new_location) and os.path.isdir(new_location)):
		os.makedirs(new_location)
	if not(os.path.exists(os.path.join(new_location,'positive'))):
		os.makedirs(os.path.join(new_location,'positive'))
	if not(os.path.exists(os.path.join(new_location,'negative'))):
		os.makedirs(os.path.join(new_location,'negative'))
	time_init = time.time()
	print "Copying positive patches.\n"
	for f in frame_list:
		shutil.copyfile(os.path.join(path_folder,f),os.path.join(new_location,'positive',new_prefix+'_'+f))
	print("Time taken to positive patches %s seconds" %(time.time()-time_init))
	time_init = time.time()
	print "Copying negative patches.\n"
	for f in neg_patches:
		shutil.copyfile(os.path.join(path_folder,f),os.path.join(new_location,'negative',new_prefix+'_'+f))	
	print("Time taken to copy negative patches %s seconds" %(time.time() - time_init))
	time_init = time.time()
	write_voc_format(os.path.join(root_path,fname),os.path.join(new_location,'positive'),new_prefix,frame_ext,'positive')
	print('Time taken to write the positive annotation files was %s seconds'%(time.time()-time_init))
	time_init = time.time()
	write_voc_format(os.path.join(root_path,fname),os.path.join(new_location,'negative'),new_prefix,frame_ext,'negative')
	print('Time taken to write the negative  annotation files was %s seconds'%(time.time()-time_init))
	time_init = time.time()
	frame_list = list(set(frame_list))
	label_file = open(os.path.join(new_location,'positive_label.txt'),'w')
	for f in frame_list:
		label_file.write(new_prefix+'_'+os.path.splitext(f)[0]+' 1\n')
	label_file.close()
	print('Time taken to write the positive label file  was %s seconds'%(time.time()-time_init))
	time_init = time.time()
	neg_patches = list(set(neg_patches))
	label_file = open(os.path.join(new_location,'negative_label.txt'),'w')
	for f in neg_patches:
		label_file.write(new_prefix+'_'+os.path.splitext(f)[0]+' -1\n')
	label_file.close()
	print('Time taken to write the negative label file was %s seconds'%(time.time()-time_init))
	print frame_list
	print('Some preprocessing is required for the XML files. Doing that...\n')
	for f in frame_list:
		Popen(['sh remove_xml_declaration.sh %s'%(os.path.join(new_location,'positive','annotations',new_prefix+'_'+os.path.splitext(f)[0]+'.xml'))],shell=True)
	for f in neg_patches:
		Popen(['sh remove_xml_declaration.sh %s'%(os.path.join(new_location,'negative','annotations',new_prefix+'_'+os.path.splitext(f)[0]+'.xml'))],shell=True)
	print('The Preprocessing is finished.\n')




def write_voc_format(xgtf_path,patch_folder,patch_prefix,patch_ext,patch_type):
	if patch_type=='positive':
		fname = os.path.expanduser(xgtf_path) # Full path of the Ground Truth XGTF File
		root_path, fname = os.path.split(fname)
		path_folder = os.path.expanduser(patch_folder) # Full path of the folder where image patches have to be stored
		annotate_folder = os.path.basename(os.path.normpath(patch_folder))
		namespace = 'http://lamp.cfar.umd.edu/viper#' # All XGTF files from SUP use this namespace. DO NOT EDIT or REMOVE this line 
		doc = ET.parse(os.path.join(root_path,fname)) # This line reads the XGTF file from the disk
		data_tag = str(QName(namespace,'data')) # This helps Python to parse each tag by stripping it off its namespace part. So it is essential. DO NOT CHANGE OR COMMENT
		data = doc.find(data_tag) # All relevant data for creating patches is present with a "data" tag. Hence we find all nodes which have a "data" tag
		# The next 5 lines create empty lists for storing ground truth annotation information (frame number, height, width, x (column) and y (row)
		frame_list = list()
		height_list = list()
		width_list = list()
		x_list = list()
		y_list = list()
		if not(os.path.exists(os.path.join(path_folder,'annotations'))):
			os.makedirs(os.path.join(path_folder,'annotations'))
		for x in data.iter():
			if (x.get('name')=='info2D'): # Those elements which have "data" tags  and  have "info2D" attribute  have annotation information. We now look beneath each such node
				f = [gt.get('framespan') for gt in x]
				height = [int(gt.get('height')) for gt in x]
				width = [int(gt.get('width')) for gt in x]
				x_col = [int(gt.get('x')) for gt in x]
				y_row = [int(gt.get('y')) for gt in x]
			        f =[ frame.rsplit(':',1)[0] for frame in f] # This line converts an entry like "432:432" to "432"
				frame_list = frame_list + f # We concatenate information into the lists created outside the loops. This helps us in counting number of people in each frame and writing files accordingly
				height_list = height_list + height
				width_list = width_list + width
				x_list = x_list + x_col
				y_list = y_list + y_row

		occour = Counter(frame_list) # This counts the number of people in each frame depending on number of occourances of that frame with GT information
		for key in occour:
			counter=1
		#	img = imread(os.path.join(root_path,input_name)) # Read the image. This uses scikit-image and not OpenCV
			indices = [i for i, x  in enumerate(frame_list) if x==key] # Find indices containing information about a certain frame 
			for ind in indices: 
				if counter==1:
					input_name = patch_prefix+'_'+key+'.'+patch_ext
					img = imread(os.path.join(path_folder,input_name))
					root = get_voc_header(input_name,img.shape,annotate_folder)
				else:
					root_doc = ET.parse(os.path.join(path_folder,'annotations',patch_prefix+'_'+key+'.xml'))
					root = root_doc.getroot()	
				counter = counter + 1
				obj = SubElement(root,'object')
				obj_name = SubElement(obj,'name')
				obj_name.text = 'person'
				obj_pose = SubElement(obj,'pose')
				obj_pose.text = 'Unspecified'
				obj_truncated = SubElement(obj,'truncated')
				obj_truncated.text = '0'
				obj_difficult = SubElement(obj,'difficult')
				obj_difficult.text= '0'
				obj_bndbox = SubElement(obj,'bndbox')
				bnd_xmin = SubElement(obj_bndbox,'xmin')
				bnd_xmin.text = str(x_list[ind])
				bnd_ymin = SubElement(obj_bndbox,'ymin')
				bnd_ymin.text = str(y_list[ind])
				bnd_xmax = SubElement(obj_bndbox,'xmax')
				bnd_xmax.text = str(x_list[ind] + width_list[ind])
				bnd_ymax = SubElement(obj_bndbox,'ymax')
				bnd_ymax.text = str(y_list[ind] + height_list[ind])
				out_file = open(os.path.join(path_folder,'annotations',patch_prefix+'_'+key+'.xml'),'w')
				out_file.write(prettify(root))
				out_file.close()
	else:
		path_folder = os.path.expanduser(patch_folder) # Full path of the folder where image patches have to be stored
		patch_files = glob.glob(os.path.join(path_folder,'*.'+patch_ext))
		patch_files = [os.path.basename(f) for f in patch_files]
#		patch_files = [os.path.splitext(f)[0] for f in patch_files]
		annotate_folder = os.path.basename(os.path.normpath(patch_folder))
		if not(os.path.exists(os.path.join(path_folder,'annotations'))):
			os.makedirs(os.path.join(path_folder,'annotations'))
		for f in patch_files:
			img = imread(os.path.join(path_folder,f))
			root = get_voc_header(f,img.shape,annotate_folder)
			obj = SubElement(root,'object')
			obj_name = SubElement(obj,'name')
			obj_name.text = 'Non-person'
			obj_pose = SubElement(obj,'pose')
			obj_pose.text = 'Unspecified'
			obj_truncated = SubElement(obj,'truncated')
			obj_truncated.text = '0'
			obj_difficult = SubElement(obj,'difficult')
			obj_difficult.text= '0'
			obj_bndbox = SubElement(obj,'bndbox')
			bnd_xmin = SubElement(obj_bndbox,'xmin')
			bnd_xmin.text = '120'
			bnd_ymin = SubElement(obj_bndbox,'ymin')
			bnd_ymin.text = '120'
			bnd_xmax = SubElement(obj_bndbox,'xmax')
			bnd_xmax.text = '160'
			bnd_ymax = SubElement(obj_bndbox,'ymax')
			bnd_ymax.text = '200'
			out_file = open(os.path.join(path_folder,'annotations',os.path.splitext(f)[0]+'.xml'),'w')
			out_file.write(prettify(root))
			out_file.close()
#		if len(img.shape)==3: # This If condition allows us to support grayscale images as well
#			img = img[y_list[ind]:y_list[ind]+height_list[ind],x_list[ind]:x_list[ind]+width_list[ind]] 
#		else:
#			img = img[y_list[ind]:y_list[ind]+height_list[ind],x_list[ind]:x_list[ind]+width_list[ind],3]

		


