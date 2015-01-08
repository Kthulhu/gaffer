##########################################################################
#
#  Copyright (c) 2012, John Haddon. All rights reserved.
#  Copyright (c) 2013-2014, Image Engine Design Inc. All rights reserved.
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

import fnmatch

import IECore

import Gaffer
import GafferUI

import GafferScene
import GafferSceneUI

# SceneNode

Gaffer.Metadata.registerNodeDescription(

GafferScene.SceneNode,

"""The base type for all nodes which are capable of generating a hierarchical scene.""",

"out",
"""The output scene.""",

"enabled",
"""The on/off state of the node. When it is off, the node outputs an empty scene.""",

)

def __noduleCreator( plug ) :

	if isinstance( plug, GafferScene.ScenePlug ) :
		return GafferUI.StandardNodule( plug )

	return None

GafferUI.Nodule.registerNodule( GafferScene.SceneNode, fnmatch.translate( "*" ), __noduleCreator )
GafferUI.PlugValueWidget.registerType( GafferScene.ScenePlug, None )

Gaffer.Metadata.registerPlugValue( GafferScene.SceneNode, "enabled", "nodeUI:section", "Node" )

# Instancer

GafferUI.PlugValueWidget.registerCreator( GafferScene.Instancer, "instance", None )

# ObjectToScene

GafferUI.Nodule.registerNodule( GafferScene.ObjectToScene, "object", GafferUI.StandardNodule )

# AlembicSource

GafferUI.PlugValueWidget.registerCreator(
	GafferScene.AlembicSource,
	"fileName",
	lambda plug : GafferUI.PathPlugValueWidget( plug,
		path = Gaffer.FileSystemPath( "/", filter = Gaffer.FileSystemPath.createStandardFilter( extensions = [ "abc" ] ) ),
		pathChooserDialogueKeywords = {
			"bookmarks" : GafferUI.Bookmarks.acquire( plug, category = "sceneCache" ),
			"leaf" : True,
		},
	)
)

GafferUI.PlugValueWidget.registerCreator(
	GafferScene.AlembicSource,
	"refreshCount",
	GafferUI.IncrementingPlugValueWidget,
	label = "Refresh",
	undoable = False
)

# BranchCreator

GafferUI.PlugValueWidget.registerCreator(
	GafferScene.BranchCreator,
	"parent",
	lambda plug : GafferUI.PathPlugValueWidget(
		plug,
		path = GafferScene.ScenePath( plug.node()["in"], plug.node().scriptNode().context(), "/" ),
	),
)

# Group

GafferUI.PlugValueWidget.registerCreator( GafferScene.Group, "in[0-9]*", None )
GafferUI.PlugValueWidget.registerCreator( GafferScene.Group, "transform", GafferUI.TransformPlugValueWidget, collapsed=None )

# Filter

GafferUI.PlugValueWidget.registerCreator( GafferScene.Filter, "match", None )

# Constraint

GafferUI.PlugValueWidget.registerCreator(
	GafferScene.Constraint,
	"target",
	lambda plug : GafferUI.PathPlugValueWidget(
		plug,
		path = GafferScene.ScenePath( plug.node()["in"], plug.node().scriptNode().context(), "/" ),
	),
)

GafferUI.PlugValueWidget.registerCreator(
	GafferScene.Constraint,
	"targetMode",
	GafferUI.EnumPlugValueWidget,
	labelsAndValues = (
		( "Origin", GafferScene.Constraint.TargetMode.Origin ),
		( "BoundMin", GafferScene.Constraint.TargetMode.BoundMin ),
		( "BoundMax", GafferScene.Constraint.TargetMode.BoundMax ),
		( "BoundCenter", GafferScene.Constraint.TargetMode.BoundCenter ),
	)
)

# MeshType

GafferUI.PlugValueWidget.registerCreator(
	GafferScene.MeshType,
	"meshType",
	GafferUI.EnumPlugValueWidget,
	labelsAndValues = (
		( "Unchanged", "" ),
		( "Poly", "linear" ),
		( "Subdiv", "catmullClark" ),
	),
)

# Plane

Gaffer.Metadata.registerNodeDescription(

GafferScene.Plane,

"""A node which produces scenes containing a plane.""",

"dimensions",
"Controls size of the plane in X and Y.",

"divisions",
"Controls tesselation of the plane.",

)

# Cube

Gaffer.Metadata.registerNodeDescription(

GafferScene.Cube,

"""A node which produces scenes containing a cube.""",

"dimensions",
"Controls size of the cube.",

)

# PathFilter

def __pathsPlugWidgetCreator( plug ) :

	result = GafferUI.VectorDataPlugValueWidget( plug )
	result.vectorDataWidget().setDragPointer( "objects" )
	return result

GafferUI.PlugValueWidget.registerCreator(
	GafferScene.PathFilter,
	"paths",
	__pathsPlugWidgetCreator,
)

GafferUI.Nodule.registerNodule(
	GafferScene.PathFilter,
	"paths",
	lambda plug : None,
)

# UnionFilter

GafferUI.PlugValueWidget.registerCreator(
	GafferScene.UnionFilter,
	"in",
	None,
)

GafferUI.Nodule.registerNodule(
	GafferScene.UnionFilter,
	"in",
	GafferUI.CompoundNodule
)
