#!/usr/bin/env python
#coding=utf-8

import os
import traceback
import sys
import re

# Returns True of callback indicates to stop iteration
def deep_iterate_dir(rootDir, callback, to_iter=True):
    for lists in os.listdir(rootDir):
        path = os.path.join(rootDir, lists)
        if os.path.isdir(path):
            if not to_iter:
                print("*** Skip sub directory: " + path)
                continue
            if callback(path, True):
                return True
            else:
                if deep_iterate_dir(path, callback, to_iter):
                    return True
        elif os.path.isfile(path):
            if callback(path, False):
                return True
    return False

exe_name = None

def decrypt_binary_file(execute_file_path):
	command = "DYLD_INSERT_LIBRARIES=dumpdecrypted_6.dylib \"" + execute_file_path + "\" mach-o decryption dumper"
	ret = os.system(command)
	if 0 == ret:
		raise Exception("dumpdecrypted failed!")

def main():

	def callback(path, is_dir):
		global exe_name

		if is_dir:
			r = re.search("[^/]*\.app", path)
			if r:
				exe_name = r.group(0)
				# remove .app
				exe_name = exe_name.split('.')[0]
		else:
			file_name = os.path.split(path)[1]
			if exe_name == file_name:
				print("==> find: " + path)
				decrypt_binary_file(path)

		return False

	deep_iterate_dir("/var/mobile/Applications", callback)

if __name__ == '__main__':
	try:
		main()
	except Exception,e:
		traceback.print_exc()
		sys.exit(1)