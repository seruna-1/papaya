<title> Usage </title>

Takes a directory as the source of a documentation and generates a directory with HTML files which use [kaki] toolkit.

# Command-line options

[--source=] is required, specifies a source directory.

[--destination=] is required, specifies a destination directory. Built files will be put under this location.

[--kaki=] is an optional relative path to a directory which will be used by the HTML files generated to acess the framework files. Is [kaki] by default, that is, files generated expect [kaki] to be directly inside the destination directory. If it was [../kaki], they would expect it to be a sibling of the destination root.

When building the documentation to put it in a site, this option should could be [../kaki], so that the directory [kaki] will be expected to be 1 level up from the submodule directory. Then, there can be multiple built documentations from different projects that all use the same [kaki] CSS and javascript files.

[--build-only=] is an optional path to a json file that has a list of paths of selected source files to be built. Useful for debugging.

[--replace-spaces-by-dashes=]. If [true], spaces in source file name become dashes in built file name. This is the default.

# Title of generated document

The title of the generated HTML document will be the name of the source file, minus its suffix, unless the source file has a HTML element [title] specifying it. This apllies to markdown files, because there can be embedded HTML elements in it.
