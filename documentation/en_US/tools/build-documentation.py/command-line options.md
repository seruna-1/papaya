# [--source=]

Required, the path to a source directory or a source file.

# [--destination=]

The path where will be created a destination directory, grouping built files, or a built file.

If not present, built file or directory will be put into a temporary location, in [/tmp/kaki].

# [--kaki=]

Path to a directory which will be used by the HTML files generated to acess the framework files. This is relative to the destination root.

If not present, the built files will refer to the absolute path of the local kaki, retrieved from the location of the script.

When building the documentation to put it in a site, this option should could be [../kaki], so that the directory [kaki] will be expected to be 1 level up from the built directory. This way, multiple built documentations from different projects can use the same [kaki] CSS and javascript files.

# [--build-only=]

Optional path to a json file that has a list of paths of selected source files to be built. Useful for debugging.

# [--no-replace-spaces-by-dashes]

Boolean.

Do not replace spaces in source file name by dashes in built file name.

