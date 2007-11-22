#!/usr/bin/python -u
# Copyright or Copr. INRIA/Scilab - Sylvestre LEDRU
#
# Sylvestre LEDRU - <sylvestre.ledru@inria.fr> <sylvestre@ledru.info>
# 
# This software is a computer program whose purpose is to generate C++ wrapper 
# for Java objects/methods.
# 
# This software is governed by the CeCILL  license under French law and
# abiding by the rules of distribution of free software.  You can  use, 
# modify and/ or redistribute the software under the terms of the CeCILL
# license as circulated by CEA, CNRS and INRIA at the following URL
# "http://www.cecill.info". 
# 
# As a counterpart to the access to the source code and  rights to copy,
# modify and redistribute granted by the license, users are provided only
# with a limited warranty  and the software's author,  the holder of the
# economic rights,  and the successive licensors  have only  limited
# liability. 
# 
# In this respect, the user's attention is drawn to the risks associated
# with loading,  using,  modifying and/or developing or reproducing the
# software by the user in light of its specific status of free software,
# that may mean  that it is complicated to manipulate,  and  that  also
# therefore means  that it is reserved for developers  and  experienced
# professionals having in-depth computer knowledge. Users are therefore
# encouraged to load and test the software's suitability as regards their
# requirements in conditions enabling the security of their systems and/or 
# data to be ensured and,  more generally, to use and operate it in the 
# same conditions as regards security. 
# 
# The fact that you are presently reading this means that you have had
# knowledge of the CeCILL license and that you accept its terms.
# 
# For more information, see the file COPYING

from types import MethodType

class JNIFrameWork:
	"""
	This class provides the JNI code
	"""
	
	JavaVMVariable="jvm"
	JavaVMVariableType="JavaVM"
	
	def getHeader(self,namespaceName):
		return """
		#ifndef __%s__
		#define __%s__
		#include <string>
		#include <iostream>
		#include <stdlib.h>
		#include <jni.h>
		"""%(namespaceName.upper(), namespaceName.upper())

	def getJavaVMVariable(self):
		return self.JavaVMVariable
	
	def getJavaVMVariableType(self):
		return self.JavaVMVariableType

	def getMethodGetCurrentEnv(self,objectName):
		return """
		JNIEnv * %s::getCurrentEnv() {
		JNIEnv * curEnv = NULL;
		this->jvm->AttachCurrentThread((void **) &curEnv, NULL);
		return curEnv;
		}"""%(objectName)

	
	def getObjectDestuctor(self,objectName):
		return ("""
		%s::~%s() {
		JNIEnv * curEnv = NULL;
		this->jvm->AttachCurrentThread((void **) &curEnv, NULL);
		
		curEnv->DeleteGlobalRef(this->instance);
		curEnv->DeleteGlobalRef(this->instanceClass);
		}
		""")%(objectName, objectName)
	

	def getSynchronizeMethod(self,objectName):
		return ("""
		
		void %s::synchronize() {
		if (getCurrentEnv()->MonitorEnter(instance) != JNI_OK) {
		std::cerr << "Fail to enter monitor." << std::endl;
		exit(EXIT_FAILURE);
		}
		}
		""")%(objectName)
	
	def getEndSynchronizeMethod(self,objectName):
		return ("""
		void %s::endSynchronize() {
		if ( getCurrentEnv()->MonitorExit(instance) != JNI_OK) {
		std::cerr << "Fail to exit monitor." << std::endl;
		exit(EXIT_FAILURE);
		}
		}
		""")%(objectName)
	
        # For static methods, we can not call getCurrentEnv() because it is not static
	def getStaticProfile(self):
		return """
		JNIEnv * curEnv = NULL;
                jvm_->AttachCurrentThread((void **) &curEnv, NULL);
                jclass cls = curEnv->FindClass( className().c_str() );
		""" 

	def getObjectInstanceProfile(self):
		return """
		JNIEnv * curEnv = getCurrentEnv();
                jclass cls = curEnv->FindClass( className().c_str() );
		""" 
	def getExceptionCheckProfile(self):
		return """
		if (curEnv->ExceptionOccurred()) {
		curEnv->ExceptionDescribe() ;
		}
		"""

	def getMethodIdProfile(self,method):
		params=""
		for parameter in method.getParameters():
			if parameter.getType().isArray(): # It is an array
				params+="["
			params+=parameter.getType().getTypeSignature()

		methodIdName=method.getUniqueNameOfTheMethod()
		
		signatureReturn=method.getReturn().getTypeSignature()
		if method.getReturn().isArray(): # Returns an array ... 
			signatureReturn="["+signatureReturn
		
                if method.getModifier()=="static":
                        getMethod = "GetStaticMethodID"
                        firstParam = "cls"
                else:
                        getMethod = "GetMethodID"
                        firstParam = "this->instanceClass"

		return ("""
		jmethodID %s = curEnv->%s(%s, "%s", "(%s)%s" ) ;
		if (%s == NULL) {
		std::cerr << "Could not access to the method " << "%s" << std::endl;
		exit(EXIT_FAILURE);
		}
		""")%(methodIdName, getMethod, firstParam, method.getName(), params,signatureReturn , methodIdName, method.getName())


	def getCallObjectMethodProfile(self, method):
		parametersTypes=method.getParameters()
		returnType=method.getReturn()
		i=1
		params=""
		
		for parameter in parametersTypes:
			if i==1:
				params+="," # in order to manage call without param
			params+=parameter.getName()
			if parameter.getType().specificPreProcessing(parameter)!=None:
				params+="_" # There is a pre-processing, then, we add the _ 
			if len(parametersTypes)!=i: 
				params+=", "
			i=i+1
			
		if returnType.getNativeType()=="void": # Dealing with a void ... 
			returns=""
		else:
			typeOfReturn=returnType.getJavaTypeSyntax()
			returns="""%s res =  (%s)"""%(typeOfReturn, typeOfReturn)

                if method.getModifier()=="static":
                        return """
                        %s curEnv->%s(cls, methodID %s);
                        %s
                        """ % (returns, returnType.getCallStaticMethod(), params,self.getExceptionCheckProfile())
                else:
                        return """
                        %s curEnv->%s( this->instance, %s %s);
                        %s
                        """ % (returns, returnType.getCallMethod(), method.getUniqueNameOfTheMethod(), params,self.getExceptionCheckProfile())


	def getReturnProfile(self, returnType):
		return returnType.getReturnSyntax()
		

