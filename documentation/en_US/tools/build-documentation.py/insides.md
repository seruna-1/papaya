<title> Insides </title>

# Class DocumentationBuilder

Responsible for building the documentation. The building process of each individual file is carried by another class: [FileBuilder].

An instance of [FileBuilder] is created at the end of method [DocumentationBuilder.__init__], as [self.file_builder].

As input, [DocumentationBuilder.__init__] takes a [argparse.Namespace] named [options] and treats it as a dictionary. Supported keys in it are recreated in [self], as properties. They are:

 - [source], path to the directory that acomodates source files.

 - [destination], path to the directory that will acomodate generated files.

 - [kaki_from_destination], the expected path to [kaki] from [self.destination]. That will be used by instance of [FileBuilder], when method [FileBuilder.set_source] is called, to define the path from the source to [kaki]. This involves prefixing as many [../] to [kaki_from_destination] as needed for the current file to reach the root, and then reach [kaki].

 - [selection_to_build]. A path to a json file consisting of a list of files to be built. Can be [None]. If not [None], the file will be parsed into an pythonic list. If this list is empty, an error will be throwed. Otherwise, only the files specified by the paths in that list will be built. The list is stored in property [self.selection_to_build].

Properties [self.source] and [self.destination] are resolved.

From each source file, will be generated a destination file at the same relative path from [self.source], except that the file type extension may change, like from [.md] suffix in the source file to [.html] suffix in generated file.

## Method DocumentationBuilder.build

A model HTML file is read and its text is stored.

[Path.walk()] is used to select each directory inside source root directory. If there is at least one relevant source file directly inside the current source directory, the relative path to that directory from the source root directory is replicated in destination root directory.

The relevant source files are read, built and written to destination.

If a relevant file is an HTML file, its text is passed directly to method [Builder.build_from_html], resulting in a text ready to be writed.

If a relevant file is not an HTML file, its text is transformed to HTML format before proceding to pass it to method [Builder.build_from_html].

The model HTML text is parsed and BeautifulSoup object is passed to [Builder.build_from_html]. This includes a slightly overhead, as the object is recreated from model text for each time [Builder.build_from_html] is called.

## Method DocumentationBuilder.build_specific

## Method DocumentationBuilder.build_all

# Class FileBuilder

Responsible for building a single source file, defined by method [FileBuilder.set_source]. An object of this class can be reused to build many files by repeatdly calling this method for each one of them.

## Method FileBuilder.set_source

Takes the path to the source file to build as input named [path], and stores it as property [self.source].

From [self.source], the path to the destination file is inferred and stored as [self.destination].

[self.idiom] is the idiom of the source file. It is defined as:

```
self.idiom = source_from_root.parents[-2]
```

The variable [source_from_root] is the path of source file relative to the source root. The last parent of this path is [./], which is irrelevant, and the second is something like [pt_BR] or [en_US], which tells the idiom of the file, thus the [-2] index.

Property [self.root_from_file] is a path that consists in a sequence of [../] that can lead to root from a file. It works for both reaching source root by source file and reaching destination root from destination file.

## Method FileBuilder.build

Builds the source file.

## Method FileBuilder.build_title

## Method FileBuilder.build_references_to_kaki

## Method FileBuilder.build_language_information

# Class SectionBuilder

Groups methods that form sections in an object [BeautifulSoup.Tag], named root, that does not have any sections and where each heading is a direct child of it.

## Method SectionBuilder.build

No inputs.

Performs the main task that this class is suposed to perform.

A section includes a title, denoted by an header element, and all the posterior sibling elements until the next header.

The first section may not include title.

The parent of a section should be a section.

It performs an loop over the elements siblings of the first element in element [main]. Whenever a heading is found, a element [section] is created and inserted before it. The heading, as well as any element after it, are extracted and inserted into that section.

If another heading with same relevance as previous is found, it inaugurates another section, sibling to the previous. If the heading found has lower relevance, it inaugurates a subsection.

The current open sections are tracked by the list named [sections]

