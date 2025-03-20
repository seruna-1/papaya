# build.py

Script that takes a directory as the source of a documentation and generates a directory with HTML files which use [kaki] framework.

# Command-line options

`--source=` is required, specifies a source directory.

`--source-format=` is required, specifies the format of the files in source directory. Can be [markdown] or [html].

If it is [markdown], the title of the generated HTML document will be the name of the file, excluding the extension [.md] and replacing [-] by [ ], that is, hifen by a blank space.

If the markdown had an embedded HTML element [title], it will be used instead of the file name.

`--destination=` is required, specifies a destination directory. Built files will be put under this location.

`--kaki=` is an optional relative path to a directory which will be used by the HTML files generated to acess the framework files. Is [kaki] by default, that is, files generated expect [kaki] to be directly inside the destination directory.

When building the documentation to put it in a orphan branch, in order to add this branch as a submodule of a repository that is a website, like the repository of [GitHub Pages], this option should be `[../kaki]`, so that the directory [kaki] will be expected to be 1 level up from the submodule directory.
