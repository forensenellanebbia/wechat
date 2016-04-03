#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author: Gabriele Zambelli (Twitter: @gazambelli)
# Blog  : http://forensenellanebbia.blogspot.it
#
# WARNING: This program is provided "as-is"
# See http://forensenellanebbia.blogspot.it/2015/12/wechat-script-to-convert-and-play-aud.html for further details.

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
# 2016-04-03 Added Silk v3 decoder
# 2015-12-01 First public release
#
# Prerequisites:
# - Python v2.7
# - libav for Microsoft Windows (Open source audio and video processing tools - https://www.libav.org/)
#   Tested version: http://builds.libav.org/windows/nightly-gpl/libav-x86_64-w64-mingw32-20151130.7z
# - Silk v3 decoder (decoder.exe from https://github.com/netcharm/wechatvoice)
# - FFMpeg (https://ffmpeg.org/download.html)
#
# What you have to do first:
# - export WeChat chats in HTML format using the UFED Physical Analyzer software ("Export to HTML" option) 
# - put libav, decoder.exe and ffmpeg in c:\tools
#
# What the script does:
# - this script converts WeChat audio messages to WAV files
# - it then modifies each HTML report by replacing the strings ".aud" and ".amr" with ".wav"

# Script based on these blog posts/scripts:
# http://ppwwyyxx.com/2014/Classify-WeChat-Audio-Messages/
# http://www.giacomovacca.com/2013/06/voip-calls-encoded-with-silk-from-rtp.html
# https://github.com/netcharm/wechatvoice (https://github.com/netcharm/wechatvoice/blob/master/amr2ogg.py)

from datetime import datetime
import os
import subprocess
import sys

path_to_tools = "c:\\tools"

def check_prequesites():
    try:
        subprocess.Popen([path_to_tools + '\\decoder.exe'], stderr=subprocess.STDOUT, stdout=subprocess.PIPE).communicate()
        subprocess.Popen([path_to_tools + '\\ffmpeg.exe'], stderr=subprocess.STDOUT, stdout=subprocess.PIPE).communicate()
        subprocess.Popen([path_to_tools + '\\avconv.exe', '-version'], stderr=subprocess.STDOUT, stdout=subprocess.PIPE).communicate()
    except:
        print "\n!! Error: SILKv3 decoder or ffmpeg or avconv missing !!\n"
        sys.exit()

def check():
    os.system('cls')
    if len(sys.argv) == 1:
        print "\n**** WeChat audio file converter + UFED Physical Analyzer HTML Report fix ****"
        print "\n(The script will search recursively)\n\n"
        print "How to use:\n==> %s absolute_path_to_your_folder\n" % os.path.basename(sys.argv[0])
        check_prequesites()
    elif len(sys.argv) == 2:
        if os.path.exists(sys.argv[1]) == True:
            check_prequesites()
            pass
        else:
            print "\n!! Error: %s not found !!\n\n" % sys.argv[1]
            check_prequesites()
            sys.exit()


# function to convert aud files into wav files by using avconv
# avconv options:
# -y overwrites existing wav files
# -i input file

def amr2wav(filename, path):
    f_wav = '"' + path + '\\' + filename[:filename.find('.amr')] + '.wav' + '"'
    f_source = '"' + path + '\\' + filename + '"'
    cmd = path_to_tools + '\\avconv.exe -y -i ' + f_source + ' ' + f_wav
    subprocess.Popen(cmd, stderr=subprocess.STDOUT, stdout=subprocess.PIPE).communicate()

def silk2pcm(filename, path):
    f_source = '"' + path + '\\' + filename + '"'
    f_pcm = '"' + path + '\\' + filename[:filename.find('.amr')] + '.pcm'+ '"'
    cmd = path_to_tools + '\\decoder.exe ' + f_source + " " + f_pcm
    subprocess.Popen(cmd, stderr=subprocess.STDOUT, stdout=subprocess.PIPE).communicate()
    
def pcm2wav(filename,path):
    f_source = '"' + path + '\\' + filename + '"'
    f_wav = '"' + path + '\\' + filename[:filename.find('.pcm')] + '.wav' + '"'
    cmd = path_to_tools + '\\ffmpeg.exe -y -f s16le -ar 24000 -i ' + f_source + ' ' + f_wav
    subprocess.Popen(cmd, stderr=subprocess.STDOUT, stdout=subprocess.PIPE).communicate()

check()

path = sys.argv[1]
os.chdir(path)

f_aud_counter  = 0   #number of audio files converted
report_counter = 0   #number of reports checked

start_time = datetime.now()

print "\nPlease wait...\n"

for root, dirs, files in os.walk(path):
    for f_audio in files:
        if f_audio.endswith(".aud") or f_audio.endswith(".amr"):
            f_audio_pfn = os.path.join(root, f_audio) #pfn = path + filename
            with open(f_audio_pfn, 'rb') as fb_audio: #fb  = file binary
                data = fb_audio.read()
                base = os.path.basename(f_audio_pfn)
                f_amr = os.path.splitext(base)[0] + ".amr"
                fb_audio.seek(0)
                magic_silk = fb_audio.read(10)
                magic_amr  = fb_audio.read(6)
                if magic_silk == "\x02\x23\x21\x53\x49\x4C\x4B\x5F\x56\x33": # #!SILK_V3
                    with open(os.path.join(root, f_amr), 'wb') as fb_amr:
                        fb_amr.write(data[1:])  #prepend amr header to amr files
                        fb_amr.close()
                        silk2pcm(f_amr,root)
                        f_aud_counter += 1
                elif magic_silk == "\x23\x21\x53\x49\x4C\x4B\x5F\x56\x33\x0C": # #!SILK_V3
                    silk2pcm(f_amr,root)
                    f_aud_counter += 1
                elif magic_amr == "\x23\x21\x41\x4D\x52": # #!AMR 
                    amr2wav(f_amr,root)
                    f_aud_counter += 1
                else:
                    with open(os.path.join(root, f_amr), 'wb') as fb_amr:
                        fb_amr.write('#!AMR\n'+data)  #prepend amr header to amr files
                        fb_amr.close()
                        amr2wav(f_amr,root) #from amr to wav
                        f_aud_counter += 1

for root, dirs, files in os.walk(path):
    for f_audio in files:
        if f_audio.endswith(".pcm"):
            pcm2wav(f_audio,root)
            os.remove(os.path.join(root, f_audio))
        elif f_audio.endswith(".html"):
            report_counter += 1
            path_to_report = os.path.join(root,f_audio)
            report_source = open(path_to_report, 'r')
            report_tmp = open(path_to_report+".tmp", 'w') #temporary report file
            for line in report_source:
                line = line.replace('.aud','.wav').replace('.amr','.wav')
                report_tmp.write(line)
            report_source.close()
            report_tmp.close()
            os.remove(root + "\\" + f_audio)
            os.rename(root + "\\" + f_audio + ".tmp", root + "\\" + f_audio)
        elif f_audio.endswith(".amr"):
            os.remove(os.path.join(root, f_audio))
        elif f_audio.endswith(".aud"):
            os.remove(os.path.join(root, f_audio))


os.system('cls')

print "\n**** WeChat audio file converter + UFED Physical Analyzer HTML Report fix ****"
print "\nHTML report(s) checked ................  %d"   % report_counter
print "Audio files converted to WAV files ....  %d\n" % f_aud_counter
print "\nDone !!!\n"                    

end_time = datetime.now()
print "\n\nScript started : " + str(start_time)
print "Script finished: " + str(end_time)
print('Duration       : {}'.format(end_time - start_time))

subprocess.Popen('explorer %s' % path)
