# -*- coding: utf-8 -*-
from zipfile import ZipFile
import biplist
import shutil
import sys
import time
import warnings
warnings.filterwarnings("ignore")

def log(msg):
	print '[%s]%s'%(time.strftime('%H:%M:%S'),msg)

def main(infile):
	with ZipFile(infile.replace('.ipa','_patched.ipa'),'w') as zipObjo:
		with ZipFile(infile, 'a') as zipObj:
			for item in zipObj.infolist():
				buffer = zipObj.read(item.filename)
				if '.plist' not in item.filename or 'Info' not in item.filename.split('/')[-1][0:4]:
					zipObjo.writestr(item, buffer)
				else:
					zipObj.extract(item.filename,'.')
					pl=biplist.readPlist(item.filename)
					if 'CFBundleIdentifier' in pl:
						if 'mila.' not in pl['CFBundleIdentifier']:
							log('[+] found CFBundleIdentifier:%s'%(pl['CFBundleIdentifier']))
							pl['CFBundleIdentifier']='mila.'+pl['CFBundleIdentifier']
							biplist.writePlist(pl,item.filename)
							zipObjo.write(item.filename)
	log('[+] cleaning')
	shutil.rmtree('Payload')
	log('[+] %s is finished'%infile)

if __name__ == "__main__":
	main(sys.argv[1])