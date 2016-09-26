
from copyFunc import *
import argparse

copy_dataset('./resultat2','/user/gbahloul/home/WORK_2016/DPMTraining/temp/VOC2007/VOCdevkit/VOC2007','jpeg','resultat2')

#def main():
#	parser = argparse.ArgumentParser()
#	parser.add_argument("path1", help="Root location in which positive and negative patches are stored with their corresponsing annotations")
#	parser.add_argument("path2", help="Root location of pascal VOC2007 folder to copy al images and annotation")
#	parser.add_argument("frame_ext", help="File extension of the patches, Give 'jpeg' for .jpeg files and 'jpg' for .jpg files...")
#	parser.add_argument("prefix",help="prefix to be added to train.txt/trainval.txt")
#	args = parser.parse_args()
#	arg1=args.path1
#	arg2=args.path2
#	arg3=args.frame_ext
#	arg4=args.prefix
#	print arg1
#	print arg2
#	print arg3
#	print arg4
#	copy_dataset(arg1,arg2,arg3,arg4)


#if __name__ == "__main__":
# main()
