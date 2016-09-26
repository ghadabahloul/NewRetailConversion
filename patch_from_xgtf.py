#!/usr/bin/env python

import sys # Required for reading command line arguments

from xml.etree import ElementTree as ET # Required for manipulating  XML files (XGTF files are also XML in nature)

from xml.etree.ElementTree  import QName # Required for handling namespaces in XGTF files

import os # Required for path manipulations

from os import listdir # Required for making a list of all the images in the directory

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

import json

with open('config.json') as f:
		data = json.load(f)
		for location_name in data["location_name"]:
			print(location_name)
			location_name=list()
		for image_type in data["image_type"]:
			print(image_type)			
			
def classify_patches(xgtf_name,frames_path,frame_ext,new_location,new_prefix):
	'''
	xgtf_name : Full path + name of the XGTF File.

	frames_path : Root path in which the patches are stored 

	frame_ext : Extension of the frame image files. If you store frames as *.jpg files, then frame_ext = jpg (please note that it is not .jpg or *.jpg)

	new_location : Root location in which positive and negative patches are to be stored along with their corresponsing annotations.

    new_prefix : new_prefix is a prefix that is prefixpended to all the frames when they are stored in new_location. Can be provided with an empty argument '' as well, if needed.	
	'''
		
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
	frame_list=list() 
	j=list()
	temp_list=list()
	root=doc.getroot()
	for x in data.iter():
		print(x.tag)
		location = ["Location","info2D"]
		if (x.get('name')in location): #This is to be used for extracting the 'Location' tag from the .xgtf file. Modify this according to the .xgtf file being used.
			f= [gt.get('framespan') for gt in x] 
			j=list()
			for frame in f:				#Iterate through the list f which contains information of the frames in '34:34' format.
				g=frame.split(':',1)	#Used to strip the entry 
				g= map(int,g)			#Convert the string into an integer
				if g[0]==g[1]:			# For handling entries of the form '34:34'
					j.append(g[0])		#Append either one of the entry to the temporary list
				if g[0]!=g[1]:			# For handling entries of the form '34:36'
					for i in range(g[0],g[1]+1): #Append the list of numbers from the starting to the finishing frame
						j.append(i)
		frame_list=list(set(frame_list+j)) 
	for frame in f:  #Delete the original f list which has entries of the form '12:12' & '13:14'
		del frame
	list_of_files=[name for name in listdir(frames_path) if name[-3:] in image_type ] #Generate a list of the files from the dataset. #to extract the files with .jpeg extension. Modify it to get .jpg if need be.
	#print(list_of_files)
	list_of_files.sort() #Sort the list of files from the ground truth 
	for idx in frame_list:  #Loop to check the correspondence of positive frames from the list of files and append them to a new list 
		if idx not in temp_list:
			temp_list.append(list_of_files[idx-1])	
	[frame_list]=[temp_list] # It takes the list of images for positive patches(obtained from the Ground Truth file)
	neg_patches= list(set(list_of_files)-set(frame_list)) #To find the negative patches
	if not(os.path.exists(new_location) and os.path.isdir(new_location)):
		os.makedirs(new_location)
	if not(os.path.exists(os.path.join(new_location,'positive'))):
		os.makedirs(os.path.join(new_location,'positive'))
	if not(os.path.exists(os.path.join(new_location,'negative'))):
		os.makedirs(os.path.join(new_location,'negative'))
	time_init = time.time()
	print "\nCopying positive patches.\n"   
	for frame in frame_list:
		shutil.copyfile(os.path.join(path_folder,frame),os.path.join(new_location,'positive',new_prefix+'_'+frame))
	print ("Time taken to copy positive patches: %s seconds" %(time.time()-time_init))
	time_init=time.time()
	print ('positive patches are: ' ,frame_list)
	print "\nCopying negative patches.\n"
	for f in neg_patches:
		shutil.copyfile(os.path.join(path_folder,f),os.path.join(new_location,'negative',new_prefix+'_'+f))
	print("Time taken to copy negative patches %s seconds" %(time.time() - time_init))
	write_voc_format(os.path.join(root_path,fname),frames_path,os.path.join(new_location,'positive'),new_prefix,frame_ext,'positive',neg_patches)
	print('Time taken to write the positive annotation files was %s seconds'%(time.time()-time_init))
	time_init = time.time()
	write_voc_format(os.path.join(root_path,fname),frames_path,os.path.join(new_location,'negative'),new_prefix,frame_ext,'negative',neg_patches)
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
	print ('negative patches are : ' ,neg_patches)
	print('Time taken to write the negative label file was %s seconds'%(time.time()-time_init))
	#print frame_list
	print('Some preprocessing is required for the XML files. Doing that...\n')
	for f in frame_list:
		Popen(['sh remove_xml_declaration.sh %s'%(os.path.join(new_location,'positive','annotations',new_prefix+'_'+os.path.splitext(f)[0]+'.xml'))],shell=True)
	for f in neg_patches:
	 	Popen(['sh remove_xml_declaration.sh %s'%(os.path.join(new_location,'negative','annotations',new_prefix+'_'+os.path.splitext(f)[0]+'.xml'))],shell=True)
	print('The Preprocessing is finished.\n')

def write_voc_format(xgtf_path,frames_path, patch_folder, patch_prefix, patch_ext, patch_type,negative_list):
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
		j=list()
		temp_list=list()
		if not(os.path.exists(os.path.join(path_folder,'annotations'))):
			os.makedirs(os.path.join(path_folder,'annotations'))
		for x in data.iter():
			location = ["Location","info2D"]
			if (x.get('name') in location):
				f=[[gt.get('framespan'),gt.get('height'),gt.get('width'),gt.get('x'),gt.get('y')] for gt in x]
				for frame in f:
					g=frame[0].split(':',1)
					g= map(int,g)
					if g[0]==g[1]:
						j.append(g[0])
						height_list.append(int(frame[1]))
						width_list.append(int(frame[2]))
						x_list.append(int(frame[3]))
						y_list.append(int(frame[4]))
					if g[0]!=g[1]:
						for i in range(g[0],g[1]+1):
							j.append(i)
							height_list.append(int(frame[1]))
							width_list.append(int(frame[2]))
							x_list.append(int(frame[3]))
							y_list.append(int(frame[4]))
			frame_list=list(set(frame_list+j))

		for frame in f: #Delete the original f list which has entries of the form '12:12' & '13:14'
			del frame
		
		
		list_of_files=[name for name in listdir(frames_path) if name[-3:] in image_type ] #to extract the files with .jpeg extension. Modify it to get .jpg if need be.
		list_of_files.sort() #Sort the list of files from the ground truth 
				#frame_list=map(int, frame_list)
		
		for idx in frame_list:
			temp_list.append(list_of_files[idx-1])
		[frame_list]=[temp_list]
		neg_patches= list(set(list_of_files)-set(frame_list))
		frame_list = [os.path.splitext(each)[0] for each in frame_list]
		occour = Counter(frame_list) # This counts the number of people in each frame depending on number of occourances of that frame with GT information
	#	print "Negative patches from the second function",neg_patches
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
		#patch_files = glob.glob(os.path.join(path_folder,'*.'+patch_ext))
		#print 'The Patch files here are', negative_list
		patch_files=list()
		for key in negative_list:
			patch_files.append('_'+key)
		#patch_files = [os.path.basename(f) for f in patch_files]
#		patch_files = [os.path.splitext(f)[0] for f in patch_files]
		annotate_folder = os.path.basename(os.path.normpath(patch_folder))
		if not(os.path.exists(os.path.join(path_folder,'annotations'))):
			os.makedirs(os.path.join(path_folder,'annotations'))
		#print 'Reaches here',patch_files
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
	


	

			
			

	
	






