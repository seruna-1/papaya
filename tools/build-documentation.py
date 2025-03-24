import markdown

import argparse

from pathlib import Path

from bs4 import BeautifulSoup

class FileBuilder :

	def __init__ ( self, documentation_builder ) :

		self.documentation_builder = documentation_builder

		print( self.documentation_builder.source )

		self.source = None

		self.valid_source_suffixes = [ '.md', '.html' ]

		self.destination = None

		self.kaki_expected_path = None

		return

	def set_source ( self, path ) :

		self.source = path

		source_from_root = self.source.relative_to( self.documentation_builder.source )

		self.destination = self.documentation_builder.destination / source_from_root.with_suffix( ".html" )

		self.idiom = source_from_root.parents[-2]

		documentation_destination_from_file_destination = self.documentation_builder.destination.relative_to( self.destination.parent, walk_up=True )

		self.kaki_expected_path = documentation_destination_from_file_destination / self.documentation_builder.kaki_expected_path_from_destination

		return

	def build ( self ) :

		document = BeautifulSoup( self.documentation_builder.model_text, 'html.parser' )

		part = self.source.read_text()

		if self.source.suffix == '.md' : part = markdown.markdown( part )

		part = BeautifulSoup( part, 'html.parser' )

		insert_point = document.find( 'main' )

		for child in part.children : insert_point.append( child.extract() )

		given_titles = document.select( 'main title' )

		if ( given_titles != [] ) :

			assert ( len( given_titles ) == 1 ) , 'More than one title in part.'

			document.html.head.title.replace_with( given_titles[0] )

		self.build_language_information( document )

		self.build_references_to_kaki( document )

		self.destination.write_text( document.prettify() )

		return

	def build_references_to_kaki ( self, document ) :

		kaki_css_path = self.kaki_expected_path / 'main.css'

		kaki_javascript_path = self.kaki_expected_path / 'main.js'

		elements_link_stylesheet = document.head.find_all( 'link', rel='stylesheet' )

		assert ( elements_link_stylesheet != None ) , "Could not find any element [link] with attribute [rel] set to [stylesheet]."

		for element in elements_link_stylesheet :

			refers_to_kaki = 'kaki' in element['href']

			if refers_to_kaki : element['href'] = str( kaki_css_path ) ; break

		elements_script = document.find_all( 'script' )

		assert ( elements_script != None ) , "Could not find any element [script]."

		for element_script in elements_script :

			refers_to_kaki = ( 'src' in element_script.attrs ) and ( 'kaki' in element_script['src'] )

			if refers_to_kaki : element_script['src'] = str( kaki_javascript_path ) ; break

		return

	def build_language_information ( self, document ) :

		for element in document.head.find_all( 'meta' ) :

			if 'lang' in element.attrs : element['lang'] = str( self.idiom ) ; break

		return

class DocumentationBuilder :

	def __init__ ( self, options ) :

		options = options.__dict__

		valid_options = [
			'source',
			'destination',
			'kaki_expected_path_from_destination'
		]

		for name in options :

			if name in valid_options : setattr( self, name, options[name] )

		paths_to_resolve = [ self.source, self.destination ]

		for path in paths_to_resolve : path = path.resolve()

		self.model_path = Path( __file__ ).parent / 'model.html'

		self.model_text = self.model_path.read_text()

		self.file_builder = FileBuilder( **{ 'documentation_builder' : self } )

		return

	def build ( self ) :

		for source_directory_path, source_directory_names, source_file_names in self.source.walk() :

			parent_was_relocated = False

			for source_file_name in source_file_names :

				source_file_path = source_directory_path / source_file_name

				if not source_file_path.suffix in self.file_builder.valid_source_suffixes : next

				self.file_builder.set_source( **{
					'path' : source_file_path
				} )

				if not parent_was_relocated : self.file_builder.destination.parent.mkdir( parents=True, exist_ok=True ) ; parent_was_relocated = True

				self.file_builder.build()

		return

if __name__ == '__main__':

	option_parser = argparse.ArgumentParser()

	option_parser.add_argument( "--source", dest='source', required=True, type=Path )

	option_parser.add_argument( "--destination", dest='destination', required=True, type=Path )

	option_parser.add_argument( "--kaki", dest='kaki_expected_path_from_destination', default="kaki", type=Path )

	options = option_parser.parse_args()

	builder = DocumentationBuilder( options )

	builder.build()
