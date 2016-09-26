#!/usr/bin/python
# -*- coding: utf-8 -*-

# from patch_from_xgtf import *
from patch_from_xml import *
import argparse


classify_patches('./test-files/videoOriginalcut/Animaux-v2.xml','./test-files/videoOriginalcut/images/','jpg','./test-files/resultat','')

#classify_patches('/user/gbahloul/home/WORK_2016/Retail-Conversion-master/videoOriginalcut/Animaux-v2.xml','/user/gbahloul/home/WORK_2016/Retail-Conversion-master/videoOriginalcut/images/','jpg','./originalcut','originalcut')

#def main():
#	parser = argparse.ArgumentParser()
#	parser.add_argument("GTfile", help="Full location of the Ground Truth file(.xgtf file)")
#	parser.add_argument("images", help="Location of the images of the dataset")
#	parser.add_argument("imageformat", help="Give 'jpeg' for .jpeg files and 'jpg' for .jpg files")
#	parser.add_argument("patcheslocation", help="The folder where you want to store the generated patches")
#	parser.add_argument("prefix",help="The new_prefix to be added to the images")
#	args = parser.parse_args()
#	xgtf_name=args.GTfile
#	frames_path=args.images
#	frame_ext=args.imageformat
#	new_location=args.patcheslocation
#	new_prefix=args.prefix
#	print xgtf_name
#	print frames_path
#	print frame_ext
#	print new_location
#	print new_prefix
#	classify_patches(xgtf_name,frames_path,frame_ext,new_location,new_prefix)


#if __name__ == "__main__":
# main()
