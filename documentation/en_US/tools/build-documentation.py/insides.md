<title> Insides </title>

# Class Builder

Responsible for building the documentation. As input, constructor takes a namespace and recreate supported names in [self]. Supported names are:

 - [source_root], path to the directory that acomodates source files.

 - [source-format], that specifies the format of the source files.

 - [destination_root], path to the directory that will acomodate generated files.

 - [kaki_expected_path_from_destination_root], the expected path to [kaki] from [destination_root]. That will be used as base to insert paths to kaki files in each destination HTML file. This consists in prefixing as many [../] to [kaki_expected_path_from_destination_root] as needed to reach [kaki]. The deeper a destination file is inside destination root, the more [../] will be prefixed. The resulting path, with needed corrections to be valid, if any, is stored as property [kaki_expected_path_from_destination_file], updated for each file being built.

Properties [source_root] and [destination_root] are resolved.

Property [model_path]

From each source file, will be generated a destination file at the same relative path from [source_root], except that the file type extension may change, like from ".md" suffix in the source file to ".html" suffix in generated file.

Property [source_file_path] is an object [pathlib.Path], the path to the current source file being built. Its relative to [source_root].

# Method Builder.build

A model HTML file is read and its text is stored.

[Path.walk()] is used to select each directory inside source root directory. If there is at least one relevant source file directly inside the current source directory, the relative path to that directory from the source root directory is replicated in destination root directory.

The relevant source files are read, built and written to destination.

If a relevant file is an HTML file, its text is passed directly to method [Builder.build_from_html], resulting in a text ready to be writed.

If a relevant file is not an HTML file, its text is transformed to HTML format before proceding to pass it to method [Builder.build_from_html].

The model HTML text is parsed and BeautifulSoup object is passed to [Builder.build_from_html]. This includes a slightly overhead, as the object is recreated from model text for each time [Builder.build_from_html] is called.

# Method Builder.build_from_html



A parsed format of it is created and replaces the element [main] in template. If there is a element [title] inside a element [meta] inside a element [head], it is ripped and replaces the title of the template.

# Method FileBuilder.set_source

Variable [documentation_destination_from_file_destination] can be interpreted as a sequence of [../] that leads to the directory of property [destination] inside the object [DocumentationBuilder]. That means, for a file inside that directory, the expected path to [kaki] is a path that leads to the root of destination plus the path of the root destination to [kaki].
