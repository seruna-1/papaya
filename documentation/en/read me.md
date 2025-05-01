[papaya] is a small framework for static HTML pages and a toolkit to build them from simplified HTML or markdown versions.

# Motivation

This is a personal project that I developed to help me to create:

 - My site, which was static, because I had no conditions to host a public http server and, at the same time, wanted simplicity.

 - Documentation for other projects.

I could simply use one of many frameworks avaiable to stylize the pages in my site, but encountered some problems:

 - Verbosity of HTML, mainly by the need to actually include repetitive tags like [meta] or [title] in each page. I wanted each page to focus only in the differential content content.

 - Idiomatic acessibility, something that would be a lot easier with an server-side framework, but, in my case, would be mainly achieavable by putting references to other versions of each page by hand, something unpractical even for two idioms.

 - Many small style and scripting details that I had in mind and thout that would be conveninent (mainly focusing on ease of use and navigation in both mobile and PC).

# Name idea

Project had many names. In chronological order:

 - Hanabi, japanese word for fireworks (I dont remember why I chose this, to be honest).

 - Kaki, an orange fruit.

 - Papaya, also the name of a fruit that includes the main colors used for highliting: orange and green.

# Some usage cases

The documentation of the project is in directory [documentation] and serves as an example. It can be built using the script [tools/build-documentation.py]. From inside the repository directory:

	python ./tools/build-documentation.py --source=./documentation --destination=./built/documentation/html-papaya --papaya=./

The documentation will be built to directory [built/documentation/html-papaya]. A release of [papaya], containing CSS and JavaScript files, will be expected to be there. To generate it, use [tools/build-papaya.py]:

	python ./tools/build-papaya.py --repository=./ --destination=./built/documentation/html-papaya/papaya

To build a single file, use:

	python ./tools/build-documentation.py --source="./documentation/en/read me.md"

This will build the file specified by [--source]. The ommission of [--destination] will make it to be put in a temporary location, under the directory [/tmp/papaya], and make the program return the location to the built file. The ommission of [--papaya] makes the location of css and javascript files be inferred using the location of the script (these files are siblings of the directory  that contains the scripts).

So, to view a file in a browser:

	chromium $(python ./tools/build-documentation.py --source="./documentation/en/read me.md")

# Idiom

The idiom of a page is retrieved from its path when it includes an idiom ISO abbreviation, like [en] or [pt-BR].

The idiom evidence must appear only one time in the path of a source file, either as a directory name:

	[en-US/readme.md]

Or as an extension of the file name:

	[readme.en-US.md]

Putting the evidence in the file name is convenient when the file will not have many translations and the name of the directories parents of this file do not, necessarialy, match its idiom.

Putting the evidence as a directory implies that not only the files in it, but also any subdirectory, will match this idiom.

When the path of a file does not includes this, its idiom is left undefined.

# Translations

Files with an defined idiom can be part of a translation group.

A translation group is formed by different versions of a file, each being in a different language.

Each built file whose source file was in a translation group will include links to the other files in the translation group. 

Translation groups are defined in a file [translations.json]. For a given source directory, this file may appear at different points in its depths. This file consists of a single list of translation groups, each translation group being a list of paths to source files. Paths may or not include the file extension, like [.html] or [.md]. An example of the contents of this file would be:

	[
		[ "pt-BR/leia-me", "en/read me" ]

		[ "pt-BR/importante", "en/important" ]
	]

# Packing

Files that are referenced in source files will be copied to built destination upon building.

An condition to this is that the local file must be inside the source directory. If it is outside, it wont be packed. The ideal solution is: a file is outside the source directory but it has a link (either symbolical or hard) in there and the source file references the link, so that the actual file will be copied to the destination directory.

The link is only dereferenced when it points to a file outside the source root. If a link inside the root points to a file also inside the root, the link will be recreated in the destination root. This allows a file having many names, depending on the idiom, without massive content duplication.

# Title of generated document

The title of the generated HTML document will be the name of the source file, minus its suffix, unless the source file has a HTML element [title] specifying it. This apllies to markdown files, because there can be embedded HTML elements in it.
