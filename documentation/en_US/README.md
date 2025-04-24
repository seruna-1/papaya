[Kaki] is a small toolkit to build and render static HTML pages. It can be 
used, for example, in a personal website or a documentation of a project.

Source files can be partial [HTML] or [markdown]. The documentation of [kaki], itself, uses both.

It can be built using the script [tools/build-documentation.py]. From inside the repository directory:

```
python ./tools/build-documentation.py --source=./documentation --destination=./built/documentation/html-kaki --kaki=./
```

The documentation will be built to directory [built/documentation/html-kaki]. A release of [kaki] will be expected to be there. To generate it, use [tools/build-kaki.py]:

```
python ./tools/build-kaki.py --repository=./ --destination=./built/documentation/html-kaki/kaki
```

To build a single file, use:

```
python ./tools/build-documentation.py --source=./documentation/en_US/README.md
```

This will build the file specified by [--source]. The ommission of [--destination] will make it to be put in a temporary location, under the directory [/tmp/kaki], and make the program return the location to the built file. The ommission of [--kaki] makes the location of css and javascript files be inferred using the location of the script (these files are siblings of the directory  that contains the scripts).

So, to view a file in a browser:

```
chromium $(python ./tools/build-documentation.py --source=./documentation/en_US/README.md)
```

# Idiom

The idiom of a page is retrieved from its path when it includes an idiom iso abbreviation, like [en_US] or [pt_BR].

The idiom evidence must appear only one time in the path of a source file, either as a directory name:

```
[en_US/readme.md]
```

Or as an extension of the file name:

```
[readme.en_US.md]
```

Putting the evidence in the file name is convenient when the file will not have many translations and the name of the directories parents of this file do not, necessarialy, match its idiom.

Putting the evidence as a directory implies that not only the files in it, but also any subdirectory, will match this idiom. It can be used, for example, in a website.

When the path of a file does not includes this, its idiom is left undefined.

# Translations

Files with an defined idiom can be part of a translation group.

A translation group is formed by different versions of a file, each being in a different language.

Each built file whose source file was in a translation group will include links to the other files in the translation group. 

Translation groups are defined in a file [translations.json]. For a given source directory, this file may appear at different points in its depths. This file consists of a single list of translation groups, each translation group being a list of paths to source files. Paths may or not include the file extension, like [.html] or [.md]. An example of the contents of this file would be:

```
[
	[ "pt_BR/leia-me", "en_US/read me" ]

	[ "pt_BR/importante", "en_US/important" ]
]
```
# Refernces to files

Files that are referenced in source files will be copied to built destination upon building. The tool [build-file]

# Title of generated document

The title of the generated HTML document will be the name of the source file, minus its suffix, unless the source file has a HTML element [title] specifying it. This apllies to markdown files, because there can be embedded HTML elements in it.
