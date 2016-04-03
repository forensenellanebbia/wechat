# WeChat audio file converter + UFED Physical Analyzer HTML Report fix

Blog post: http://forensenellanebbia.blogspot.it/2015/12/wechat-script-to-convert-and-play-aud.html

Prerequisites:
 - Python v2.7
 - libav for Microsoft Windows (Open source audio and video processing tools - https://www.libav.org/)
   Tested version: http://builds.libav.org/windows/nightly-gpl/libav-x86_64-w64-mingw32-20151130.7z
 - Silk v3 decoder (decoder.exe from https://github.com/netcharm/wechatvoice)
 - FFMpeg (https://ffmpeg.org/download.html)

What you have to do first:
 - export WeChat chats in HTML format using the UFED Physical Analyzer software ("Export to HTML" option) 
 - put libav, decoder.exe and ffmpeg in c:\tools

What the script does:
 - this script converts WeChat audio messages to WAV files
 - it then modifies each HTML report by replacing the strings ".aud" and ".amr" with ".wav"

 
Script based on these blog posts/scripts:
http://ppwwyyxx.com/2014/Classify-WeChat-Audio-Messages/
http://www.giacomovacca.com/2013/06/voip-calls-encoded-with-silk-from-rtp.html
https://github.com/netcharm/wechatvoice (https://github.com/netcharm/wechatvoice/blob/master/amr2ogg.py)