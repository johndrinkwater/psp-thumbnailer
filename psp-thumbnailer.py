#! /usr/bin/python
# -*- coding: utf-8 -*-
"""
	psp-thumbnailer, makes thumbnails for PSP files (EBOOT.PBP)

   	© 2010‐2011 John Drinkwater <john@nextraweb.com>
	http://johndrinkwater.name/code/psp-thumbnailer/

	This program is free software: you can redistribute it and/or modify
	it under the terms of the GNU Affero General Public License as
	published by the Free Software Foundation, either version 3 of the
	License, or (at your option) any later version.

	This program is distributed in the hope that it will be useful,
	but WITHOUT ANY WARRANTY; without even the implied warranty of
	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
	GNU Affero General Public License for more details.

	You should have received a copy of the GNU Affero General Public License
	along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
import os, sys, getopt, gconf, struct

__version__ = "0.01"

# TODO include --install option
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
		logging = open( os.path.expanduser( '~/.pspthumbnailerlog' ), 'a' )
		logging.write( str( sys.argv ) )
		logging.write( "\n" )

	# TODO move this into a function
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
		# TODO verify we’re a PBP file?

		thumbnaillocation = struct.unpack('<l', header[12:16])[0]
		thumbnailend = struct.unpack('<l', header[16:20])[0]
		
		pspfile.seek(thumbnaillocation)
		# TODO verify this is an image file
		thumbnaildata = pspfile.read( (thumbnailend - thumbnaillocation) )
		outfile = open( output, 'w' )
		outfile.write( thumbnaildata )
	except:
		sys.exit(-1)

	pspfile.close()
	outfile.close()

	if debugging is True:
		if logging:
			logging.close()

