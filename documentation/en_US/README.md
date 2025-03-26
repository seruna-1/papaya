# kaki

[Kaki] is a small toolkit to build and render static HTML pages. It can be 
used, for example, in a personal website or a documentation of a project.

Source files can be [HTML] or [markdown]. The documentation of [kaki] uses both. It can be built using the script [tools/build-documentation.py]. But, before executing it, markdown files in the root of the repository, including this one, as well as their media, shall be included in documentation. From inside the repository directory:

```
python ./tools/include-missing-documentation.py
```

Now, to build the documentation:

```
python ./tools/build-documentation.py --source=./documentation --destination=./built/documentation/html-kaki
```

The documentation will be built to directory [built/documentation/html-kaki]. A release of [kaki] will be expected to be there. To generate it, the script [tools/build-kaki.py] is used:

```
python ./tools/build-kaki.py --repository=./ --destination=./built/documentation/html-kaki/kaki
```

# General directory tree layout

The framework expects the root source directory to contain:

 - one or more directories with a name consisting of a language abbreviation, like [en_US] or [pt_BR]. A directory with a language abbreviation groups the source files that use that language.

 - the file [translations.json].

 - the directory [media].

Two or more files may have the same content, but be written in different languages and have different names. In each built file, [kaki] inserts links to other files with same content, but in a different language, using the information in [translations.json].

[translations.json] contains a list where each element is a list of translated files. When building a source file, [kaki] searches for its location in these inner lists. If any contains it, a link to each other file in this list is included in the generated file, allowing users to choose the idiom of a page.

The directory [media] contains everything that is not a relevant source file, but is referenced by a relevant source file, like a video or an image.
