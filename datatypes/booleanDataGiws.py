#!/usr/bin/python -u

from dataGiws import dataGiws

class booleanDataGiws(dataGiws):
	
	def getTypeSignature(self):
		return "Z"

	def getJavaTypeSyntax(self):
		return "jboolean"

	def getRealJavaType(self):
		return "boolean"
	
	def getDescription(self):
		return "unsigned 8 bits"

	def getNativeType(self):
		return "bool"
	
	def CallMethod(self):
		return "CallBooleanMethod"

if __name__ == '__main__':
	print booleanDataGiws().getReturnTypeSyntax()
