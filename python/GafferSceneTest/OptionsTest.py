##########################################################################
#  
#  Copyright (c) 2012, John Haddon. All rights reserved.
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

import IECore

import Gaffer
import GafferScene
import GafferSceneTest

class OptionsTest( GafferSceneTest.SceneTestCase ) :

	def test( self ) :
	
		p = GafferScene.Plane()
		options = GafferScene.Options( inputs = { "in" : p["out"] } )
	
		# check that the scene hierarchy is passed through
	
		self.assertEqual( options["out"].object( "/" ), None )
		self.assertEqual( options["out"].transform( "/" ), IECore.M44f() )
		self.assertEqual( options["out"].bound( "/" ), IECore.Box3f( IECore.V3f( -0.5, -0.5, 0 ), IECore.V3f( 0.5, 0.5, 0 ) ) )
		self.assertEqual( options["out"].childNames( "/" ), IECore.StringVectorData( [ "plane" ] ) )
		
		self.assertEqual( options["out"].object( "/plane" ), IECore.MeshPrimitive.createPlane( IECore.Box2f( IECore.V2f( -0.5 ), IECore.V2f( 0.5 ) ) ) )
		self.assertEqual( options["out"].transform( "/plane" ), IECore.M44f() )
		self.assertEqual( options["out"].bound( "/plane" ), IECore.Box3f( IECore.V3f( -0.5, -0.5, 0 ), IECore.V3f( 0.5, 0.5, 0 ) ) )
		self.assertEqual( options["out"].childNames( "/plane" ), None )
		
		# check that we have some displays
		
		options["options"].addParameter( "test", IECore.IntData( 10 ) )
		options["options"].addParameter( "test2", IECore.StringData( "10" ) )
		
		g = options["out"]["globals"].getValue()
		self.assertEqual( len( g ), 1 )
		self.assertEqual( g[0], IECore.Options( { "test" : 10, "test2" : "10" } ) )
	
	def testSerialisation( self ) :
	
		s = Gaffer.ScriptNode()
		s["optionsNode"] = GafferScene.Options()
		s["optionsNode"]["options"].addParameter( "test", IECore.IntData( 10 ) )
		s["optionsNode"]["options"].addParameter( "test2", IECore.StringData( "10" ) )
		
		ss = s.serialise()
		
		s2 = Gaffer.ScriptNode()		
		s2.execute( ss )
		
		g = s2["optionsNode"]["out"]["globals"].getValue()
		self.assertEqual( len( g ), 1 )
		self.assertEqual( g[0], IECore.Options( { "test" : 10, "test2" : "10" } ) )
	
	def testHashPassThrough( self ) :
	
		# the hash of the per-object part of the output should be
		# identical to the input, so that they share cache entries.
	
		p = GafferScene.Plane()
		options = GafferScene.Options( inputs = { "in" : p["out"] } )
		
		self.assertSceneHashesEqual( p["out"], options["out"], childPlugNames = ( "transform", "bound", "attributes", "object", "childNames" ) )
	
if __name__ == "__main__":
	unittest.main()
