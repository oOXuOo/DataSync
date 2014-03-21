#! /usr/bin/env python
# -*- coding:utf-8 -*-

import sys
import os
import shutil
import filecmp

def getDirTree(rootpath):
	'''
	返回以rootpath为根的相对目录树
	完整的目录树是srcroot:/T
	'''
	T = [os.path.sep]
	rootpath = delTail(rootpath)
	#开始遍历
	for dirpath, dirnames, filenames in  os.walk(rootpath):
		for dir_name in dirnames:
			subdirname = os.path.join(dirpath,dir_name)  
			T.append(subdirname.replace(rootpath,''))
	return T

def syncDir(srcpath,dstpath):
	#确保目录存在
	try:
		srcEnv = os.listdir(srcpath)
	except:
		print('error path:' + srcpath)
		return -1
	if not os.path.exists(dstpath):
		os.mkdir(dstpath)
	dstEnv = os.listdir(dstpath)
	#删除多余
	for anything in dstEnv:
		if not anything in srcEnv:
			try:
				os.remove(  os.path.join(dstpath,anything)  )
			except:
				try:
					shutil.rmtree(os.path.join(dstpath,anything))
				except:
					print('Delete Error:'+anything+' Pass it')
	#填补不足
	for anything in srcEnv:
		copy_src = os.path.join(srcpath,anything)
		copy_dst = os.path.join(dstpath,anything)
		#不存在的情况
		if  not anything in dstEnv:
			if os.path.isfile(copy_src):
				shutil.copy(copy_src,copy_dst)
			else:
				os.mkdir(copy_dst)
		#存在的情况(因为可能不一致)		
		else:
			#Is a file 
			if os.path.isfile(copy_src):
				if filecmp.cmp(copy_src,copy_dst):
					pass
				else:
					os.remove(  copy_dst )
					shutil.copy(copy_src,copy_dst)
			#Is a dir 
			else:
				pass

def delTail(raw_path):
	if os.path.sep == '/':
		if raw_path[-1]=='/':
			raw_path = raw_path[:-1]
		return raw_path
	elif os.path.sep == '\\':
		if raw_path[-1]=='\\':
			raw_path = raw_path[:-1]
		return raw_path
	else:
		print('该系统的文件分割符号未知')
		print(os.path.sep)


if __name__ == '__main__':
	#获取用户输入
	if len(sys.argv)==1:
		srcROOT = input('请输入源路径:')
		dstROOT = input('请输入目标路径:')
	elif len(sys.argv)==3:
		srcROOT = sys.argv[1]
		dstROOT = sys.argv[2]
	else:
		print('参数错误！')
		exit(1)
	#去掉尾巴
	srcROOT = delTail(srcROOT)
	dstROOT = delTail(dstROOT)

	#验证源目录存在
	if not os.path.exists(srcROOT):
		print('源路径错误')
		exit(1)
	else:			#验证目标目录存在
		if os.path.exists(dstROOT) :
			pass
		else:
			try:
				os.mkdir(dstROOT)
			except:
				print('目标路径无法创建')
				exit(1)


	#Syncing.........
	DT = getDirTree(srcROOT) 
	print('目录树构建成功，开始同步......')
	for short_path in DT:
		src_long_path = srcROOT+short_path
		dst_long_path = dstROOT+short_path

		syncDir(src_long_path,dst_long_path)



