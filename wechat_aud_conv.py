#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author: Gabriele Zambelli (Twitter: @gazambelli)
# Blog  : http://forensenellanebbia.blogspot.it
#
# WARNING: This program is provided "as-is"
# See http://forensenellanebbia.blogspot.it/ for further details.

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You can view the GNU General Public License at <http://www.gnu.org/licenses/>
#
#
# Change history
# 2015-12-01 First public release (v 0.1)
#
#
# Script based on this blog post:
# http://ppwwyyxx.com/2014/Classify-WeChat-Audio-Messages/
#
# Prerequisites:
# - tested on Python v2.7.8
# - libav for Microsoft Windows (Open source audio and video processing tools - https://www.libav.org/)
#   Tested version: http://builds.libav.org/windows/nightly-gpl/libav-x86_64-w64-mingw32-20151130.7z
#
# What you have to do first:
# - export WeChat chats in HTML format using the UFED Physical Analyzer software ("Export to HTML" option) 
#
# What the script does:
# - this script converts AUD audio files to WAV files so that they can be played
# - it then modifies each HTML report by replacing the string ".aud" with ".wav"


import os
import subprocess
import sys

path_to_libav = "c:\\tools"

def check():
    os.system('cls')
    if len(sys.argv) == 1:
        print "\n**** WeChat audio file converter + UFED Physical Analyzer HTML Report fix ****"
        print "\n(The script will search recursively - AUD files won't be deleted)\n\n"
        print "How to use: python %s absolute_path_to_your_folder\n" % sys.argv[0]
    else:
        pass
    if sys.version_info > (2,7,0) and sys.version_info < (3,0,0):
        pass
    else:
        print "Python version should be at least 2.7.\nNot tested on Python 3"
        sys.exit()
    
    try:
        subprocess.Popen([path_to_libav + '\\avconv', '-version'], stderr=subprocess.STDOUT, stdout=subprocess.PIPE).communicate()
    except:
        print "\n!! Error: Libav not found in %s      !!\n\nPlease check the path in the script or download libav from:\nhttps://www.libav.org\n" % path_to_libav
        if len(sys.argv) == 2:
            if os.path.exists(sys.argv[1]) == True:
                pass
            else:
                print "\n!! Error: %s not found !!\n\n" % sys.argv[1]
        sys.exit()
    if len(sys.argv) == 2:
        if os.path.exists(sys.argv[1]) == True:
            pass
        else:
            print "\n!! Error: %s not found !!" % sys.argv[1]
            sys.exit()
    else:
        sys.exit()



# function to convert aud files into wav files by using avconv
# avconv options:
# -y overwrites existing wav files
# -i input file

def convert(var1, var2):
    f_wav = var2 + '\\' + var1[:var1.find('.amr')] + '.wav'
    f_source = var2 + '\\' + var1
    #os.system('avconv -y -i "%s" "%s"' % (f_source, f_wav))
    subprocess.Popen([path_to_libav + '\\avconv', '-y', '-i',f_source, f_wav], stderr=subprocess.STDOUT, stdout=subprocess.PIPE).communicate()
    os.remove(f_source) #remove AMR files (original AUD files won't be removed)

check()

path = sys.argv[1]
os.chdir(path)

f_aud_counter  = 0   #number of aud files converted
report_counter = 0   #number of reports checked

print "\nPlease wait...\n"

for root, dirs, files in os.walk(path):
	for file in files:
		if file.endswith(".aud"):
			f_aud_filename = os.path.join(root, file)
			with open(f_aud_filename, 'rb') as f_aud:
				data = f_aud.read()
				base = os.path.basename(f_aud_filename)
				f_amr_filename = os.path.splitext(base)[0] + ".amr"
				with open(os.path.join(root, f_amr_filename), 'wb') as f_amr:
					f_amr.write('#!AMR\n'+data)  #prepend amr header to amr files
					f_amr.close()
					convert(f_amr_filename,root) #from amr to wav
					f_aud_counter += 1

for root, dirs, files in os.walk(path):
	for file in files:
		if file.endswith(".html"):
			report_counter += 1
			path_to_report = os.path.join(root,file)
			report_source = open(path_to_report, 'r')
			report_tmp = open(path_to_report+".tmp", 'w') #temporary report file
			for line in report_source:
				report_tmp.write(line.replace('.aud','.wav'))
			report_source.close()
			report_tmp.close()
			os.remove(root + "\\" + file)
			os.rename(root + "\\" + file + ".tmp", root + "\\" + file)

os.system('cls')

print "\n**** WeChat audio file converter + UFED Physical Analyzer HTML Report fix ****"
print "\nHTML report(s) checked ..............  %d"   % report_counter
print "AUD files converted to WAV files ....  %d\n" % f_aud_counter
print "\nDone !!!\n"                    

subprocess.Popen('explorer %s' % path)
