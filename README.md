# kaki

Kaki is a minimalistic CSS and Javascript framework for use with static HTML pages. It can be used, for example, in a personal website.

It can also be used to document a project.

Documentation source is avaiable in 2 formats: HTML, inside [documentation/html]; and markdown, inside [documentation/markdown]. Any of them can be built using the script [tools/build]. From inside the repository directory:

```
./tools/build --format=html --source=./documentation/HTML
```

or

```
./tools/build --format=markdown --source=./documentation/markdown
```

respectively.

The documentation will be built to directory [built/documentation/html-kaki].

This script depends on. also uses pandoc when building from markdown files.

The source code is open and avaiable at [Github](https://codeberg.org/kalamado/kaki) and [Codeberg](https://codeberg.org/kalamado/kaki).

Here is a screenshot of the page [built/documentation/html-kaki/pt-BR/index.html]:

![](screenshot.png)