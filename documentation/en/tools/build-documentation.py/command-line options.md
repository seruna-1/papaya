# [--source=]

Required, the path to a source directory or a source file.

# [--destination=]

The path where will be created a destination directory, grouping built files, or a built file.

If not present, built file or directory will be put into a temporary location, in [/tmp/papaya].

# [--papaya=]

Path to a directory which will be used by the HTML files generated to acess the framework files. This is relative to the destination root.

If not present, the built files will refer to the absolute path of the local papaya, retrieved from the location of the script.

When building the documentation to put it in a site, this option should could be [../papaya], so that the directory [papaya] will be expected to be 1 level up from the built directory. This way, multiple built documentations from different projects can use the same [papaya] CSS and javascript files.

# [--build-only=]

Optional path to a json file that has a list of paths of selected source files to be built. Useful for debugging.

# [--no-replace-spaces-by-dashes]

Do not replace spaces in source file name by dashes in built file name.

# [--pack]

To put local files referenced in source files into destination directory.

An condition to this is that the local file must be inside the source directory. If it is outside, it wont be packed. The ideal solution to this is: a file is outside the source directory but it has a link (either symbolical or hard) in there and the source file references the link, so that the actual file will be copied to the destination directory.

The link is only dereferenced when it points to a file outside the source root. If a link inside the root points to a file also inside the root, the link will be recreated in the destination root. This allows a file having many names, depending on the idiom, without massive content duplication.
