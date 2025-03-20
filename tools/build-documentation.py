import markdown

import argparse

from pathlib import Path

from bs4 import BeautifulSoup

class Builder:

	def __init__ ( self, source_root, source_format, destination_root, kaki_relative_path ) :

		self.source_root = Path( source_root )

		self.destination_root = Path( destination_root )

		self.source_format = source_format

		self.kaki_relative_path_from_top = Path( kaki_relative_path )

		match self.source_format:

			case 'html' : self.relevant_file_extension = '.html'

			case 'markdown' : self.relevant_file_extension = '.md'

			case _ : raise Exception( "Not a valid source format." )

		return

	def build ( self ) :

		model_path = Path( __file__ ).parent / 'model.html'

		model_text = model_path.read_text()

		for source_directory_path, source_directory_names, source_file_names in self.source_root.walk() :

			parent_was_relocated = False

			for source_file_name in source_file_names :

				if source_file_name.endswith( self.relevant_file_extension ) :

					source_file_path = source_directory_path / source_file_name

					destination_file_path = self.destination_root / source_file_path.relative_to( self.source_root ).with_suffix( ".html" )

					self.kaki_relative_path = self.destination_root.relative_to( destination_file_path.parent, walk_up=True ) / self.kaki_relative_path_from_top

					if parent_was_relocated == False : destination_file_path.parent.mkdir( parents=True, exist_ok=True ) ; parent_was_relocated = True

					text = source_file_path.read_text()

					if self.source_format == 'markdown' :

						text = markdown.markdown( text )

					model = BeautifulSoup( model_text, 'html.parser' )

					built = self.build_from_html( text, model )

					destination_file_path.write_text( built )

		return

	def build_from_html ( self, text, model ) :

		text = '<main>' + text + '</main>'

		model.find( 'main' ).replace_with( BeautifulSoup( text, 'html.parser' ).main )

		result = model

		given_titles = result.select( 'main title' )

		if given_titles != [] : result.html.head.title.replace_with( given_titles[0] )

		result = self.generate_references_to_kaki( result )

		return result.prettify()

	def generate_references_to_kaki ( self, soup ) :

		kaki_css_path = self.kaki_relative_path / 'main.css'

		kaki_javascript_path = self.kaki_relative_path / 'main.js'

		elements_link_stylesheet = soup.head.find_all( 'link', rel='stylesheet' )

		assert ( elements_link_stylesheet != None ) , "Could not find any element [link] with attribute [rel] set to [stylesheet]."

		for element in elements_link_stylesheet :

			refers_to_kaki = 'kaki' in element['href']

			if refers_to_kaki == True : element['href'] = str( kaki_css_path ) ; break

		elements_script = soup.find_all( 'script' )

		assert ( elements_script != None ) , "Could not find any element [script]."

		for element_script in elements_script :

			refers_to_kaki = ( 'src' in element_script.attrs ) and ( 'kaki' in element_script['src'] )

			if  refers_to_kaki == True : element_script['src'] = str( kaki_javascript_path ) ; break

		return soup

if __name__ == '__main__':

	option_parser = argparse.ArgumentParser()

	option_parser.add_argument( "--source", required=True )

	option_parser.add_argument( "--source-format", dest='source_format', required=True )

	option_parser.add_argument( "--destination", required=True )

	option_parser.add_argument( "--kaki", default="./kaki" )

	options = option_parser.parse_args()

	builder = Builder(
		source_root=options.source,
		source_format=options.source_format,
		destination_root=options.destination,
		kaki_relative_path=options.kaki
	)

	builder.build()
