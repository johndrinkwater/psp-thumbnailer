#!/usr/bin/python
# coding=UTF-8
#
# psp-thumbnailer makes thumbnails for PSP files (EBOOT.PBP)
#
# Author: John Drinkwater, john@nextraweb.com
# Licence: GPL v3
# Licence URL: http://www.gnu.org/licenses/gpl-3.0.html
#
import os, sys, getopt, gconf, struct

__version__ = "0.01"

def printusage():
	print "psp-thumbnailer %s" % __version__
	print "Usage: %s <EBOOT.PBP> <OUTPUT>" % os.path.basename( __file__ )

def install():
	# find out if I need to do anything more here
	# XXX generate schema?
	gnomethumb = gconf.client_get_default()
	gnomethumb.set_string('/desktop/gnome/thumbnailers/application@x-extension-pbp/command',
		"%s %%i %%o" % os.path.realpath( __file__ ) )
	gnomethumb.set_bool('/desktop/gnome/thumbnailers/application@x-extension-pbp/enable', 1)
	print "Set GConf keys for thumbnailing."
	sys.exit()

if __name__ == '__main__':

	debugging = False
	if debugging is True:
		export = open( os.path.expanduser( '~/.pspthumbnailerlog' ), 'a' )
		export.write( str( sys.argv ) )
		export.write( "\n" )

	try:
		opts, args = getopt.getopt(sys.argv[1:], 'h', ["help", "install"])
	except getopt.GetoptError, err:
		printusage()
		sys.exit(2)

	for o, a in opts:
		if o in ("-h", "--help"):
			printusage()
			sys.exit()
		if o == "--install":
			install()
			sys.exit()
	
	if len(args) > 1:
		pbpfile = args[0]
		output  = args[1]
	else:
		printusage()
		sys.exit(-1)

	try:
		pspfile = open( pbpfile, 'rb' )
		header = pspfile.read(40)
		# verify we’re a PBP file?

		thumbnaillocation = struct.unpack('<l', header[12:16])[0]
		thumbnailend = struct.unpack('<l', header[16:20])[0]
		print thumbnailend, thumbnaillocation
		pspfile.seek(thumbnaillocation)
		thumbnaildata = pspfile.read( (thumbnailend - thumbnaillocation) )
		outfile = open( output, 'w' )
		outfile.write( thumbnaildata )
	except:
		sys.exit(-1)

	pspfile.close()
	outfile.close()

	if debugging is True:
		if export:
			export.close()

