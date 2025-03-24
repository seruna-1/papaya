<title> Usage </title>

Takes a directory as the source of a documentation and generates a directory with HTML files which use [kaki] toolkit.

# Command-line options

[--source=] is required, specifies a source directory.

[--source-format=] is required, specifies the format of the files in source directory. Can be [markdown] or [html].

If it is [markdown], the title of the generated HTML document will be the name of the file, excluding the extension [.md] and replacing [-] by [ ], that is, hifen by a blank space.

If the markdown had an embedded HTML element [title], it will be used instead of the file name.

[--destination=] is required, specifies a destination directory. Built files will be put under this location.

[--kaki=] is an optional relative path to a directory which will be used by the HTML files generated to acess the framework files. Is [kaki] by default, that is, files generated expect [kaki] to be directly inside the destination directory. If it is [../kaki], they would expect it to be a sibling of the destination root.

When building the documentation to put it in a site, this option should could be [../kaki], so that the directory [kaki] will be expected to be 1 level up from the submodule directory. Then, there can be multiple built documentations from different projects that all use the same [kaki] CSS and javascript files.
