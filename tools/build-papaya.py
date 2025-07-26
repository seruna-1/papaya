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

		if not self.destination_root_path : self.destination_root_path = self.repository_root_path / 'built'

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

		files_to_copy = [ 'main.css', 'main.js', 'LICENSE', 'tools/ietf-language-tags.csv', 'tools/model.html', 'tools/model-redirector.html', 'inconsolata/Inconsolata-Regular.woff2' ]

		for file_path_relative in files_to_copy :

			destination_path = self.destination_root_path / file_path_relative

			destination_path.parent.mkdir( parents=True, exist_ok=True )

			repository_path = self.repository_root_path / file_path_relative

			shutil.copy( repository_path, destination_path )

		scripts_to_binaries = [ 'tools/build-documentation.py', 'tools/build-papaya.py' ]

		for path_relative in scripts_to_binaries :

			path_relative = pathlib.Path( path_relative )

			source_path = self.repository_root_path / path_relative

			content_to_write = f'#! /bin/python\n\n{source_path.read_text()}\n'

			destination_path = self.destination_root_path / path_relative.with_suffix('')

			destination_path.write_text( content_to_write )

			destination_path.chmod(0o755)

		return

if __name__ == '__main__':

	option_parser = argparse.ArgumentParser()

	option_parser.add_argument( "--repository", type=pathlib.Path )

	option_parser.add_argument( "--destination", type=pathlib.Path )

	options = option_parser.parse_args()

	builder = Builder( options )

	builder.build()
