<title> Usage </title>

A script that builds a release of [kaki]. The release contains only the essential parts required to render pages, the license and the file [version.json]

# Command-line options

[--repository=] is optional, specifies the repository. If not present, the repository is considered to be the one that contains the script.

[--destination=] is required, specifies the location to where kaki will be built.

# File [version.json]

The release contains a file named [version.json] at its top diretory, with a string named [commit-id], containing the id of the commit from which it was built.

If the reference [HEAD] in the repository has a versioning tag, the variable [tag] will also be present in the file, indicating the name of such tag.
