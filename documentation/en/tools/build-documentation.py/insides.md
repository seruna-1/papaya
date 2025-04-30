# Class DocumentationBuilder

Responsible for building the documentation, as a hole. The building process of each individual file is carried by an object of class [FileBuilder], created at the end of method [DocumentationBuilder.__init__], as [self.file_builder].

## Method DocumentationBuilder.__init__

Input:

 - Instance of [argparse.Namespace] named [options] treated as a dictionary containing command-line options and their values. Its upported keys are recreated in [self], as properties.

[self.source] is the root directory for all source files, as [self.destination] is for all built files. Both are absolute paths.

If provided [self.source] is a source file, it becomes the parent directory of that file and the file becomes the selection to be built.

From each source file, will be generated a destination file at the same relative path from [self.source], except that the file type extension may change, like from [.md] suffix in the source file to [.html] suffix in generated file.

[self.model_text] is a HTML text that will be used as base when building a file. Since source files are or provide partial HTML, only regarding the content, the generic content is stored in this model. A built file is the combination of these parts.

Calls method [get_translations] to load translation groups from json file.

If the command-line option [selection_to_build] is present, the specified json file will be loaded.

The instance of [FileBuilder] is created.

If [self.pack] is true, there will be a list, called [self.external_packed], that will store paths of packed files. This will be checked by the instance of FileBuilder.

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

Responsible for building a single source file, which is defined by method [FileBuilder.set_source]. This method must be recalled before each building. The building process is performed by [FileBuilder.build].

## Method FileBuilder.__init__

Receives an instance of [DocumentationBuilder] as only input, which is the parent object.

[self.valid_source_suffixes] is a list of suffixes that must appear in source file names.

[self.source] is the path of the source file being built, initially set to [None].

[self.destination] is the path of the destination file, initially set to [None].

Note that destination and source are present in instances of both DocumentationBuilder and Filebuilder,  with different meanings:

 - In DocumentationBuilder, they refer to the root directories, that contain source files and built files.

 - In FileBuilder, they refere to single files.

[self.papaya_from_file] is the relative path to a directory containing papaya rendering files (CSS and Javascript).

[self.idiom_tags] is a list of IETF idiom tags (the ones that appear in meta HTMl elements), taken from a csv file.

[self.idiom] is the idiom of current source file.

[self.translations] is also present in DocumentationBuilder. There, it is a list of translations groups. Here, it is a single translation group that contains the current file.

[self.document] is an instance of BeautifulSoup representing the current file.

## Method FileBuilder.set_source

Takes the path to the source file to build as input named [path], and stores it as property [self.source].

From [self.source], the path to the destination file is inferred and stored as [self.destination].

[self.idiom] is the idiom of the source file. It is defined as:

	self.idiom = source_from_root.parents[-2]

The variable [source_from_root] is the path of source file relative to the source root. The last parent of this path is [./], which is irrelevant, and the second is something like [pt_BR] or [en_US], which tells the idiom of the file, thus the [-2] index.

Property [self.root_from_file] is a path that consists in a sequence of [../] that can lead to root from a file. It works for both reaching source root by source file and reaching destination root from destination file.

## Method FileBuilder.build

Builds the source file.

## Method FileBuilder.build_title

## Method FileBuilder.build_references_to_papaya

## Method FileBuilder.build_language_information

## Method FileBuilder.pack_external

Packs local files referenced by the current source file into destination root.

References are selected by the HTML attributes [href] amd [src].

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

