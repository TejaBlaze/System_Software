# System_Software
A compilation of some system software components like Macro preprocessor, 2 pass assembler and Loaders

__Note__: Based on SIC architecture

Overview of Core modules implemented
------------------------------------
* ### 1PassMacroPreprocessor ###
Implements the 1 pass macro preprocessor to expand all macros in the source code.
* ### pass1 ###
Implements pass 1 of the 2 pass assembler
* ### pass2 ###
Implements pass 2 of the 2 pass assembler, with only absolute addresses.
* ### pass2_reloc ###
Implements pass 2 of the 2 pass assembler, with relocatable addresses.
* ### AbsoluteLoader ###
Simulates loading of object program into absolute locations in memory. (use with pass2)
* ### RelocationLoader ###
Simulates loading of object program into relocatable locations in memory. (use with pass2_reloc)

__Note__: Example SIC programs in Source_Codes/
