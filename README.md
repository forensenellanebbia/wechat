# WeChat audio file converter + UFED Physical Analyzer HTML Report fix

Prerequisites:
 - tested on Python v2.7.8
 - libav for Microsoft Windows (Open source audio and video processing tools - https://www.libav.org/)
   Tested version: http://builds.libav.org/windows/nightly-gpl/libav-x86_64-w64-mingw32-20151130.7z

What you have to do first:
 - export WeChat chats in HTML format using the UFED Physical Analyzer software ("Export to HTML" option) 

What the script does:
 - this script converts AUD audio files to WAV files
 - it then modifies each HTML report by replacing the string ".aud" with ".wav"
