//////////////////////////////////////////////////////////////////////////
//  
//  Copyright (c) 2012, John Haddon. All rights reserved.
//  
//  Redistribution and use in source and binary forms, with or without
//  modification, are permitted provided that the following conditions are
//  met:
//  
//      * Redistributions of source code must retain the above
//        copyright notice, this list of conditions and the following
//        disclaimer.
//  
//      * Redistributions in binary form must reproduce the above
//        copyright notice, this list of conditions and the following
//        disclaimer in the documentation and/or other materials provided with
//        the distribution.
//  
//      * Neither the name of John Haddon nor the names of
//        any other contributors to this software may be used to endorse or
//        promote products derived from this software without specific prior
//        written permission.
//  
//  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS
//  IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
//  THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
//  PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR
//  CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
//  EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
//  PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
//  PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
//  LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
//  NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
//  SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
//  
//////////////////////////////////////////////////////////////////////////

#ifndef GAFFERSCENE_SHADER_H
#define GAFFERSCENE_SHADER_H

#include "IECore/ObjectVector.h"
#include "IECore/Shader.h"

#include "Gaffer/Node.h"

#include "GafferScene/TypeIds.h"

namespace GafferScene
{

class Shader : public Gaffer::Node
{

	public :

		Shader( const std::string &name=staticTypeName() );
		virtual ~Shader();

		IE_CORE_DECLARERUNTIMETYPEDEXTENSION( Shader, ShaderTypeId, Gaffer::Node );
		
		IECore::MurmurHash stateHash() const;
		void stateHash( IECore::MurmurHash &h ) const;
		/// Returns a series of IECore::StateRenderables suitable for specifying this
		/// shader (and it's inputs) to an IECore::Renderer.
		IECore::ObjectVectorPtr state() const;
				
	protected :
		
		virtual void shaderHash( IECore::MurmurHash &h ) const = 0;
		virtual IECore::ShaderPtr shader() const = 0;
			
		virtual void compute( Gaffer::ValuePlug *output, const Gaffer::Context *context ) const;
		
};

} // namespace GafferScene

#endif // GAFFERSCENE_SHADER_H
