<title> Insides </title>

# Class Builder

Inputs:

 - [repository], a string or a pathlib.Path of the repository. Can be [None]

Object [pygit2.repository] got from input [repository] becomes class property [repository]. If input [repository] is [None], it is set to be the repository at wich the script is located. If script is not located in a repository, constructor raises an error.


# Method Builder.get_tag_name

Returns the name of a versioning tag

# Method Builder.build

If instance property [commit] is [None], maybe it was not set through methods [Builder.set_commit_from_id_text] and [Builder.set_commit_from_tag]. In that case, the commit is defined based on reference [HEAD].
