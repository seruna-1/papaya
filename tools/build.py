from pathlib import Path

import argparse

from bs4 import BeautifulSoup

class Builder:

	def __init__ ( self, source_root, source_format, destination_root, kaki_relative_path ) :

		self.source_root = Path( source_root )

		self.destination_root = Path( destination_root )

		self.source_format = source_format

		match self.source_format:

			case 'html' : self.relevant_file_extension = '.html'

			case 'markdown' : self.relevant_file_extension = '.md'

		return

	def build ( self ) :

		for source_directory_path, source_directory_names, source_file_names in Path( self.source_root ).walk() :

			is_parent_relocated = False

			for source_file_name in source_file_names :

				if source_file_name.endswith( self.relevant_file_extension ) :

					source_file_path = source_directory_path / source_file_name

					destination_file_path = Path(
						str( source_file_path ).replace( self.source_root, self.destination_root )
					)

					if is_parent_relocated == False : destination_file_path.parent.mkdir() ; is_parent_relocated = True

					if self.source_format != 'html' : print( "Error. Not html." ) ; return

					html_text = source_file_path.read_text()

					html_text = self.build_from_html( html_text )

					destination_file_path.write_text( html_text )

		return

	def read_from_html ( text ) :

		result = "This is just a text.\n"

		return result

if __name__ == '__main__':

	option_parser = argparse.ArgumentParser()

	option_parser.add_argument( "--source", required=True )

	option_parser.add_argument( "--source-format", dest='source_format', required=True )

	option_parser.add_argument( "--destination" )

	option_parser.add_argument( "--kaki" )

	options = option_parser.parse_args()

	builder = Builder( source=options.source, source_format=options.source_format, destination=options.destination, kaki=options.kaki )

	builder.build()
