<title> Insides </title>

One class: [Builder], responsible for building the documentation. As input, constructor takes:

- [source_root], a path to the directory that acomodates source files.

- [source-format], that specifies the format of the source files, according to commandline option `[--source-format]`.

- [destination_root], a path to the directory that will acomodate generated files.

- [kaki-relative-path], a relative path that will be used for the topmost generated files to reference the framework.

From each source file, will be generated a destination file at the same relative path from their relative topmost directories, except that the file type extension may change, like from ".md" suffix in the source file to ".html" suffix in generated file.

# Method Builder.build

A model HTML file is read and its text is stored.

[Path.walk()] is used to select each directory inside source root directory. If there is at least one relevant source file directly inside the current source directory, the relative path to that directory from the source root directory is replicated in destination root directory.

The relevant source files are read, built and writed to destination.

If a relevant file is an HTML file, its text is passed directly to method [Builder.build_from_html], resulting in a text ready to be writed.

If a relevant file is not an HTML file, its text is transformed to HTML format before proceding to pass it to method [Builder.build_from_html].

The model HTML text is parsed and BeautifulSoup object is passed to [Builder.build_from_html]. This includes a slightly overhead, as the object is recreated from model text for each time [Builder.build_from_html] is called.

# Method Builder.build_from_html

The HTML text received as input is prefixed with

`<main>`

And suffixed with

`</main>`

A parsed format of it is created and replaces the element [main] in template. If there is a element [title] inside a element [meta] inside a element [head], it is ripped and replaces the title of the template.
