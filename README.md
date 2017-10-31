* Description *

Bredogenerator ("rave generator" in English) is a small program which learns on books, articles and any other written text sources and generates the specified amount of coherent text.

* Requirements *
* Python 3.4+
* Pickle


* Launch *
Manual for launch: `./main.py --help`
Example of launching: `./main.py generate data.pickle`

* Usage *

There are two modes:
* Learn - take the list of files to process and learn on them. It is also possible to give the text through stdin.
* Generate - create several sentences (10 by default), with given number of punctuation marks and words (from 3 to 10 by default).

* Algorithm *

The left-context trie is built using given texts and something similar to PPM compression algorithm is performed.

* Author *
Khanova Anna, FT-101, 2017.
