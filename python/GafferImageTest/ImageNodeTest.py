##########################################################################
#
#  Copyright (c) 2013, Image Engine Design Inc. All rights reserved.
#
#  Redistribution and use in source and binary forms, with or without
#  modification, are permitted provided that the following conditions are
#  met:
#
#      * Redistributions of source code must retain the above
#        copyright notice, this list of conditions and the following
#        disclaimer.
#
#      * Redistributions in binary form must reproduce the above
#        copyright notice, this list of conditions and the following
#        disclaimer in the documentation and/or other materials provided with
#        the distribution.
#
#      * Neither the name of John Haddon nor the names of
#        any other contributors to this software may be used to endorse or
#        promote products derived from this software without specific prior
#        written permission.
#
#  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS
#  IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
#  THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
#  PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR
#  CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
#  EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
#  PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
#  PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
#  LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
#  NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
#  SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
##########################################################################

import unittest
import threading

import IECore

import Gaffer
import GafferTest
import GafferImage

class ImageNodeTest( GafferTest.TestCase ) :

	def testCacheThreadSafety( self ) :

		c = GafferImage.Constant()
		c["format"].setValue( GafferImage.Format( 200, 200, 1.0 ) )
		g = GafferImage.Grade()
		g["in"].setInput( c["out"] )
		g["multiply"].setValue( IECore.Color3f( 0.4, 0.5, 0.6 ) )

		gradedImage = g["out"].image()

		# not enough for both images - will cause cache thrashing
		Gaffer.ValuePlug.setCacheMemoryLimit( 2 * g["out"].channelData( "R", IECore.V2i( 0 ) ).memoryUsage() )

		images = []
		exceptions = []
		def grader() :

			try :
				images.append( g["out"].image() )
			except Exception, e :
				exceptions.append( e )

		threads = []
		for i in range( 0, 10 ) :
			thread = threading.Thread( target = grader )
			threads.append( thread )
			thread.start()

		for thread in threads :
			thread.join()

		for image in images :
			self.assertEqual( image, gradedImage )

		for e in exceptions :
			raise e

	def setUp( self ) :

		self.__previousCacheMemoryLimit = Gaffer.ValuePlug.getCacheMemoryLimit()

	def tearDown( self ) :

		Gaffer.ValuePlug.setCacheMemoryLimit( self.__previousCacheMemoryLimit )

if __name__ == "__main__":
	unittest.main()

