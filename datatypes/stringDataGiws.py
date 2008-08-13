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

from dataGiws import dataGiws
from configGiws import configGiws

class stringDataGiws(dataGiws):

	nativeType="char *"
	callMethod="CallObjectMethod"
	callStaticMethod="CallStaticObjectMethod"
	
	def getTypeSignature(self):
		return "Ljava/lang/String;"

	def getJavaTypeSyntax(self):
		if self.isArray():
			return "jobjectArray"
		else:			
			return "jstring"

	def getRealJavaType(self):
		return "java.lang.String"

	def getDescription(self):
		return "Java String"

	def getNativeType(self):
		if self.isArray():
			return "char **"
		else:
			return "char *"

	def specificPreProcessing(self, parameter):
		""" Overrides the preprocessing of the array """
		name=parameter.getName()
		# Management of the error when not enought memory to create the string
		if configGiws().getThrowsException():
			errorMgntMem="""throw %s::JniBadAllocException(curEnv);"""%(configGiws().getExceptionFileName())
		else:
			errorMgntMem="""std::cerr << "Could not allocate Java string array, memory full." << std::endl;
			exit(EXIT_FAILURE);"""

		# Management of the error when not enought memory to create the string
		if configGiws().getThrowsException():
			errorMgntMemBis="""throw %s::JniBadAllocException(curEnv);"""%(configGiws().getExceptionFileName())
		else:
			errorMgntMemBis="""std::cerr << "Could not convert C string to Java UTF string, memory full." << std::endl;
			exit(EXIT_FAILURE);"""

		if self.isArray():
			return """			
			
			// create java array of strings.
			jobjectArray %s_ = curEnv->NewObjectArray( %sSize, stringArrayClass, NULL);
			if (%s_ == NULL)
			{
			%s
			}

			// convert each char * to java strings and fill the java array.
			for ( int i = 0; i < %sSize; i++)
			{
			jstring TempString = curEnv->NewStringUTF( %s[i] );
			if (TempString == NULL)
			{
			%s
			}
			
			curEnv->SetObjectArrayElement( %s_, i, TempString);
			
			// avoid keeping reference on to many strings
			curEnv->DeleteLocalRef(TempString);
			}"""%(name,name,name,errorMgntMem,name,name,errorMgntMemBis,name)
		else:
			# Need to store is for the post processing (delete)
			self.parameterName=name
			return """
			jstring %s = curEnv->NewStringUTF( %s );
			"""%(name+"_",name)
	
	def specificPostProcessing(self):
		""" Called when we are returning a string or an array of string """
		if self.isArray():
			return """
			jsize len = curEnv->GetArrayLength(res);
			char **arrayOfString;
                        arrayOfString= (char**)malloc ((len+1)*sizeof(char*));
			for (jsize i = 0; i < len; i++){
			jstring resString = (jstring)curEnv->GetObjectArrayElement(res, i);
			const char *tempString = curEnv->GetStringUTFChars(resString, 0);
			arrayOfString[i] = new char[strlen(tempString) + 1];

			strcpy(arrayOfString[i], tempString);
			curEnv->ReleaseStringUTFChars(resString, tempString);
			curEnv->DeleteLocalRef(resString);
			}
			"""
		else:
			str=""
			if hasattr(self,"parameterName"):
				str="""curEnv->DeleteLocalRef(%s);"""%(self.parameterName+"_")
			return str+"""

			const char *tempString = curEnv->GetStringUTFChars(res, 0);
			char * myStringBuffer = new char[strlen(tempString) + 1];
			strcpy(myStringBuffer, tempString);
			curEnv->ReleaseStringUTFChars(res, tempString);
			curEnv->DeleteLocalRef(res);
			"""

	def getReturnSyntax(self):
		if self.isArray():
			return """
			return arrayOfString;
			"""
		else:
			return """
			return myStringBuffer;
			"""
	
