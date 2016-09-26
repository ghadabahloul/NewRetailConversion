#!/usr/bin/python

import sys # Required for reading command line arguments
import os # Required for path manipulations
from os.path import expanduser # Required for expanding '~', which stands for home folder. Used just in case the command line arguments contain "~". Without this, python won't parse "~"
import glob # Filename pattern matching
import shutil # offers a number of high-level operations on files. Support file copying, moving and removal.


def copy_dataset(arg1,arg2,arg3,arg4):
	
		'''
	arg1 : Root location in which positive and negative patches are stored with their corresponsing annotations

	arg2 : Root location of pascal VOC2007 folder to copy al images and annotation

	arg3 : File extension of the patches. If you store frames as *.jpg files, then frame_ext = jpg (please note that it is not .jpg or *.jpg)

    arg4 : is a prefix that is prefixpended to _trainval.txt and train.txt.	
	'''
	
    path1 = os.path.expanduser(arg1) # Root location in which positive and negative patches are stored with their corresponsing annotations
    path2 = os.path.expanduser(arg2)  # Root location of pascal VOC2007 folder to copy al images and annotation
    frame_ext = arg3 # File extension of the patches  
    pos_files = glob.glob(os.path.join(path1,'positive/'+'*.'+frame_ext))
    neg_files = glob.glob(os.path.join(path1,'negative/'+'*.'+frame_ext))
    pos_annotation = glob.glob(os.path.join(path1,'positive/annotations/'+'*.'+'xml'))
    neg_annotation = glob.glob(os.path.join(path1,'negative/annotations/'+'*.'+'xml'))

    #mv $1/positive/*.$3 $2/JPEGImages
    print "\n moving positive patches in VOCDEVKIT.\n"
    for x in pos_files:
        shutil.copy(x, os.path.join(path2,'JPEGImages/'))
    

    #mv $1/negative/*.$3 $2/JPEGImages
    print "\n moving negative patches in VOCDEVKIT.\n"
    for y in neg_files:
        shutil.copy(y, os.path.join(path2,'JPEGImages/'))

    #mv $1/positive/annotations/*.xml $2/Annotations
    print "\n moving positive annotation in VOCDEVKIT.\n"
    for w in pos_annotation:
        shutil.copy(w, os.path.join(path2,'Annotations/'))

    #mv $1/negative/annotations/*.xml $2/Annotations
    print "\n moving negative annotation in VOCDEVKIT.\n"
    for z in neg_annotation:
        shutil.copy(z, os.path.join(path2,'Annotations/'))

    #cut -d' ' -f1 $1/positive_label.txt > $4_trainval.txt
    file1 = open(path1+'/positive_label.txt')
    file2 = open(path1+'/'+arg4+'_trainval.txt','w+')
    for line in file1:
        newline = line.split(' ')[0]
        file2.write(newline+'\n')
        
	#cut -d' ' -f1 $1/negative_label.txt > $4_train.txt
	file3 = open(path1+'/negative_label.txt')
    file4 = open(path1+'/'+arg4+'_train.txt','w+')
    for line2 in file3:
		newline2 = line2.split(' ')[0]
		file4.write(newline2+'\n')
		





