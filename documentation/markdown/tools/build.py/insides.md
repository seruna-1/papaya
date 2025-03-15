# Insides

One class: [Builder], responsible for building the documentation. As input, constructor takes:

- [source_root], a path to the directory that acomodates source files.

- [source-format], that specifies the format of the source files, according to commandline option `[--source-format]`.

- [destination_root], a path to the directory that will acomodate generated files.

- [kaki-relative-path], a relative path that will be used for the topmost generated files to reference the framework.

From each source file, will be generated a destination file at the same relative path from their relative topmost directories, except that the file type extension may change, like from ".md" suffix in the source file to ".html" suffix in generated file.

# Method Builder.build

[Path.walk()] is used to select each directory inside source root directory. If there is at least one relevant source file directly inside the current source directory, the relative path to that directory from the source root directory is replicated in destination root directory.

The relevant source files are read, built and writed to destination.

