pynae
=====

pynae is a **Python 2** string encoder. It is possible to create
Python 2 strings using only non-alphanumeric characters. This is a
quick implementation I've hacked together after finding a way to
create arbitrary strings with this. Creating such strings manually
will give you shorter results most of the time, but this script
should do well enough to save you some time.  
  
So why would you want to encode your Python strings with nonalpha
characters? I really don't have a clue yet, but it might help you
obfuscating your script or do something else stupid ;-).  
  
Finally some words on nonalpha code in Python: After investigating
this topic a little bit I think I'm pretty sure that it is not
possible to execute arbitrary code with nonalpha characters (like
it has been done in JavaScript or PHP). There is just no way of
executing \_\_builtins\_\_.eval or something like that with only 
nonalpha characters at your hand. If you proove me wrong please
contact me ;-).  
  
## Usage ##
You can either import the encoder.py as a module or call it directly
from the command line. If you do the latter you have to pass your
string as the first command line argument. This script should work
with Python 3.x and 2.x.  
  
The created nonalpha code will only work under Python 2.x (because
of the backticks).
