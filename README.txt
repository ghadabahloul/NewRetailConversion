This document describes the following points :-

 Given frames of a Video + XGTF file, how to :-
 a) Segregate the positive and negative patches.
 b) Create the corresponding annotation files.
 c) Create the corresponding label files.
 d) Run Girshik's code with these patches.

Assumptions
---------------


a) All frame images are named as 0.jpg, 1.jpg , 2.jpg and so on....
b) The Pascal VOCDevKit and Images have been downloaded and saved as follows :-
    i) Download PASCAL VOC-2007  VOCDevkit from http://host.robots.ox.ac.uk/pascal/VOC/voc2007/VOCdevkit_08-Jun-2007.tar 
   ii) Extract the devkit in a location such as ~/temp. This will create ~/temp/VOC2007/VOCdevkit.
  iii) Download PASCAL VOC-2007 training and validation data from http://host.robots.ox.ac.uk/pascal/VOC/voc2007/VOCtrainval_06-Nov-2007.tar
   iv) Extract the images in ~/temp/VOC2007/VOCdevkit. This will create a folder ~/temp/VOC2007/VOCdevkit/VOC2007 and within it all the images. 
       
      PLEASE REMEMBER THAT THE ABOVE DIRECTORY STRUCTURE IS PERTINENT FOR PROPER FUNCTIONING OF GIRSHIK's CODE WITHOUT ANY CHANGES. FOR ANY OTHER DIRECTORY STRUCTURE YOU HAVE TO MODIFY voc_config.m

Description of code 
------------------------


STEP 1 : CREATE YOUR DATASET 
-------------------------------------
   
The basic code is in patches_from_xgtf.py

You have to call this function from another file.

An example is in abc.py

The patches_from_xgtf.py has the following format:-

classify_patches(xgtf_name,frames_path,frame_ext,new_location,new_prefix)

Here,

xgtf_name : Full path + name of the XGTF File.

frames_path : Root path in which the patches are stored (if you store xgtf file and frames in the same folder, then it is the same as xgtf_name (minus the xgtf file name)

frame_ext : Extension of the frame image files. If  you store frames as *.jpg files, then frame_ext = jpg (please note that it is not .jpg or *.jpg)

new_location : Root location in which positive and negative patches are stored.

new_prefix : You might have a number of videos with frames extracted as (0.jpg, 1.jpg and so on). new_prefix is a prefix that is prpended to all the frames when they are stored in new_location.

Example
--------


If you call the function as 

classify_patches('./1.Testvid1_rachid/testvid1_720x405/testvid1.xgtf','./1.Testvid1_rachid/testvid1_720x405/','jpg','./video1','video1')

Then at the end following is the output:-

./video1/positive :- Stores frames which contain a person.

./video1/negative :- Stores frames which do not contain a person.

./video1/positive/annotations :- Stores XML annotation files in PASCAL VOC Format.

./videos1/negative/annotations :- Stores XML annotation files in PASCAL VOC Format.

If your patches in ./1.Testvid1_rachid/testvid1_720x405/ are numbered as 0.jpg , 1.jpg and so on, they are stored as 

./videos1/positive/video1_0.jpg , ./1.Testvid1_rachid/testvid1_720x405/video1_1.jpg and so on

Following files are also created:-

./videos1/positive_labels.txt and ./videos1/negative_labels.txt . These contain labels for positive and negative frames. Positive frames are labeled as 1 and negative frames are labeled as -1.


STEP 2 : COPY YOUR DATASET TO PASCAL VOC Folder 
-------------------------------------------------

i) Run copy_dataset.sh as follows 

sh copy_dataset ./videos1 ~/temp/VOC2007/VOCdevkit/VOC2007 jpg videos1

This will do the following 

 a) Copy all images and annotations to the destined folders JPEGImages and Annotations respectively.
 b) Create two file videos1_trainval.txt and videos1_train.txt in your pwd.

These two files have to be put in ~/temp/VOC2007/VOCdevkit/VOC2007/ImageSets/Main 

These files are not directly copied because you might want to mix two or more datasets together.

STEP 3 : Download Girshik's code and in voc_config.m  in LINE 36 change BASE_DIR to ~/temp and project to some folder name.

STEP 4 : Now run pascal('person',<Num_components>/2)


