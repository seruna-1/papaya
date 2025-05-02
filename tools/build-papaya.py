import argparse

import pygit2

import pathlib

import shutil

import json

class Builder :

	def __init__ ( self, arguments ) :

		if arguments.repository != None : self.repository_root_path = arguments.repository

		else : self.repository_root_path = pathlib.Path(__file__).parent / '..' ; self.repository_root_path.resolve()

		self.repository = pygit2.Repository( str( self.repository_root_path ) )

		self.destination_root_path = arguments.destination

		return

	def get_tag_name ( self ) :

		for reference in self.repository.references.iterator() :

			if ( reference.target != self.repository.head.target ) : return None

			maybe_tag = self.repository[ reference.target ]

			if (
				isinstance( maybe_tag, pygit2.Tag )
				and maybe_tag.name.startswith( 'version' )
			) : return maybe_tag.name

		return None

	def build ( self ) :

		self.destination_root_path.mkdir( parents=True, exist_ok=True )

		version_file_path = self.destination_root_path / 'version.json'

		version_file_content = { 'commit' : str( self.repository.head.target ) }

		tag_name = self.get_tag_name()

		if tag_name != None : version_file_content['tag'] = tag_name

		version_file_path.write_text( json.dumps( version_file_content ) + '\n' )

		for repository_directory_path, directory_names, file_names in self.repository_root_path.walk() :

			directory_path_relative = repository_directory_path.relative_to( self.repository_root_path )

			destination_directory_path = self.destination_root_path / directory_path_relative

			for file_name in file_names :

				file_path_relative = directory_path_relative / file_name

				if str( file_path_relative ) in [ 'main.css', 'main.js', 'LICENSE' ] :

					destination_directory_path.mkdir( parents=True, exist_ok=True )

					repository_file_path = self.repository_root_path / file_path_relative

					destination_file_path = self.destination_root_path / file_path_relative

					shutil.copy( repository_file_path, destination_file_path )

		return

if __name__ == '__main__':

	option_parser = argparse.ArgumentParser()

	option_parser.add_argument( "--repository", type=pathlib.Path )

	option_parser.add_argument( "--destination", required=True, type=pathlib.Path )

	option_parser.add_argument( "--include-tools", default='no' )

	options = option_parser.parse_args()

	builder = Builder( options )

	builder.build()
