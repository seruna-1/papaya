# kaki

[Kaki] is a small toolkit to build and render static HTML pages. It can be used, for example, in a personal website or a documentation of a project.

Documentation source of [kaki] is avaiable in 2 formats: HTML, inside [documentation/html]; and markdown, inside [documentation/markdown]. Any of them can be built using the script [tools/build-documentation]. From inside the repository directory:

```
python ./tools/build-documentation.py --source=./documentation/html --source-format=html --destination=./built/documentation/html-kaki
```

or

```
python ./tools/build-documentation.py --source-format=markdown --source=./documentation/markdown --destination=./built/documentation/html-kaki
```

respectively.

The documentation will be built to directory [built/documentation/html-kaki]. A release of [kaki] will be expected to be there. To generate it, the script [tools/build-documentation] is used:

```
python ./tools/build-kaki.py --repository=./ --destination=./built/documentation/html-kaki/kaki
```

Here is a screenshot of a built page that uses [kaki] [built/documentation/html-kaki/pt-BR/index.html]:

![](screenshot.png)

# General directory tree layout

The framework expects the root source directory to contain:

 - one or more directories with a name consisting of a language abbreviation, like [en_US] or [pt_BR]. A directory with a language abbreviation groups the source files that use that language.

 - the file [translations.json].

 - the directory [media].

Two or more files may have the same content, but be written in different languages and have different names. In each built file, [kaki] inserts links to other files with same content, but in a different language, using the information in [translations.json].

[translations.json] contains a list where each element is a list of translated files. When building a source file, [kaki] searches for its location in these inner lists. If any contains it, a link to each other file in this list is included in the generated file, allowing users to choose the idiom of a page.

The directory [media] contains everything that is not a relevant source file, but is referenced by a relevant source file, like a video or an image.
