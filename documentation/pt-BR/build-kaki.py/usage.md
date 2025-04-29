<title> Usage </title>

A script that build a release of [kaki] from a commit of its git repository.

# Command-line options

[--repository=] is optional, specifies the repository. If not present, the repository is considered to be the one that contains the script.

[--destination=] is required, specifies the location to where kaki will be built.

# File [version.txt]

The release contains a file named [version.json] at its top diretory, with a string named [commit-id], containing the id of the commit from which it was built.

If it was built using the [--tag] option, a variable [tag] will also be present, indicating the name of the tag.
