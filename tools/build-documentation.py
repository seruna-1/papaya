import markdown

import argparse

import json

from pathlib import Path

from bs4 import BeautifulSoup

import shutil

import csv

class SectionBuilder :

	def __init__ ( self, root ) :

		self.heading_names = [ 'h1', 'h2', 'h3', 'h4', 'h5' ]

		self.root = root

		self.section = None

		self.element = None

		self.heading_level = None

		return

	def build ( self ) :

		self.section = None

		self.element = self.root.contents[0]

		next_element = None

		while ( self.element != None ) :

			assert ( self.element.name != 'section' ), "Document should either have no sections or have proper sections."

			if ( self.element.name in self.heading_names ) : self.handle_heading()

			next_element = self.element.next_sibling

			if ( self.section != None ) : self.section.append( self.element.extract() )

			self.element = next_element

		return

	def handle_heading ( self ) :

		found_heading = self.element

		found_heading_level = SectionBuilder.get_heading_level( found_heading.name )

		if ( self.heading_level == None ) :

			first_heading = found_heading

			assert ( found_heading_level == 1 ) , "First heading found is not [h1]"

			first_section = self.root.new_tag( 'section' )

			first_heading.insert_before( first_section )

			self.section = first_section

			self.heading_level = 1

		elif ( found_heading_level == self.heading_level ) :

			new_section = self.root.new_tag( 'section' )

			self.section.insert_after( new_section )

			self.section = new_section

		elif ( found_heading_level == ( self.heading_level + 1 ) ) :

			new_section = self.root.new_tag( 'section' )

			self.section.append( new_section )

			self.section = new_section

			self.heading_level = found_heading_level

		elif ( found_heading_level == ( self.heading_level - 1 ) ) :

			assert ( self.section.parent.name == 'section' )

			self.section = self.section.parent

			self.heading_level = found_heading_level

		else : raise Exception( "What???" )

		return


	def get_heading_level ( heading_name ) :

		return int( heading_name.replace( 'h', '' ) )

class FileBuilder :

	def __init__ ( self, documentation_builder ) :

		self.documentation_builder = documentation_builder

		self.source = None

		self.valid_source_suffixes = [ '.md', '.html' ]

		self.destination = None

		self.papaya_from_file = None

		self.idiom_tags = []

		language_tags_csv_path = Path(__file__).parent / 'ietf-language-tags.csv'

		assert language_tags_csv_path.exists()

		with open( language_tags_csv_path ) as csvfile:

			reader = csv.DictReader(csvfile)

			for row in reader: self.idiom_tags.append( row['lang'] )

		self.idiom = None

		self.translations = None

		return

	def set_source ( self, path ) :

		self.source = path.resolve()

		if not self.source.suffix in self.valid_source_suffixes : raise Exception( "Invalid source suffix." )

		if self.documentation_builder.source.is_file() :

			self.destination = self.documentation_builder.destination / self.source.with_suffix( ".html" ).name

		else :

			source_from_root = self.source.relative_to( self.documentation_builder.source )

			self.destination = self.documentation_builder.destination / source_from_root.with_suffix( ".html" )

		if self.documentation_builder.replace_spaces_by_dashes : self.destination = Path( str( self.destination ).replace( ' ', '-' ) )

		self.find_idiom()

		self.root_from_file = self.documentation_builder.destination.relative_to( self.destination.parent, walk_up=True )

		self.papaya_from_file = self.root_from_file / self.documentation_builder.papaya_from_destination

		if ( self.documentation_builder.translations != None ) : self.find_translation_group()

	def find_idiom ( self ) :

		for suffix in self.source.suffixes :

			if suffix[1:] in self.idiom_tags : self.idiom = suffix[1:] ; return

		for parent in self.source.parents :

			if parent.name in self.idiom_tags : self.idiom = parent.name ; return

		self.idiom = None

		return

	def find_translation_group ( self ) :

		translation_groups = self.documentation_builder.translations

		assert ( translation_groups != None )

		self.translations = None

		for group in translation_groups :

			if ( self.translations != None ) : break

			for file_path in group :

				if ( source_from_root.with_suffix('') == Path( file_path ) ) :

					self.translations = group.copy()

					self.translations.remove( file_path )

					break

		return

	def build ( self ) :

		document = BeautifulSoup( self.documentation_builder.model_text, 'html.parser' )

		part = self.source.read_text()

		if self.source.suffix == '.md' : part = markdown.markdown( part )

		part = BeautifulSoup( part, 'html.parser' )

		if self.source.suffix == '.md' :

			section_builder = SectionBuilder( part )

			section_builder.build()

		insert_point = document.find( 'main' )

		insert_point.append(part)

		self.build_title( document )

		self.build_language_information( document )

		self.build_references_to_papaya( document )

		self.destination.write_text( document.prettify() )

		return

	def build_title ( self, document ) :

		given_titles = document.select( 'main title' )

		title = None

		if ( given_titles != [] ) :

			assert ( len( given_titles ) == 1 ) , 'More than one title in part.'

			title = given_titles[0].string

			given_titles[0].decompose()

		else : title = str( self.source.stem )

		document.html.head.title.append( title )

		return

	def build_references_to_papaya ( self, document ) :

		papaya_css_path = self.papaya_from_file / 'main.css'

		papaya_javascript_path = self.papaya_from_file / 'main.js'

		elements_link_stylesheet = document.head.find_all( 'link', rel='stylesheet' )

		assert ( elements_link_stylesheet != None ) , "Could not find any element [link] with attribute [rel] set to [stylesheet]."

		for element in elements_link_stylesheet :

			refers_to_papaya = 'papaya' in element['href']

			if refers_to_papaya : element['href'] = str( papaya_css_path ) ; break

		elements_script = document.find_all( 'script' )

		assert ( elements_script != None ) , "Could not find any element [script]."

		for element_script in elements_script :

			refers_to_papaya = ( 'src' in element_script.attrs ) and ( 'papaya' in element_script['src'] )

			if refers_to_papaya : element_script['src'] = str( papaya_javascript_path ) ; break

		return

	def build_language_information ( self, document ) :

		metas = document.head.select( "meta[lang]" )

		meta = None

		if ( len( metas ) > 1 ) : raise Exception( "More than one [meta] containing idiom information." )

		elif ( len( metas ) == 1 ) and ( self.idiom == None ) :

			metas[0].decompose()

		elif ( len( metas ) == 1 ) and ( self.idiom != None ) :

			meta = metas[0]

		elif ( len( metas ) == 0 ) and ( self.idiom != None ) :

			meta = document.new_tag( "meta" )

			document.head.append( meta )

		if ( meta != None ) : meta['lang'] = str( self.idiom )

		dialog = document.find_all( 'dialog' )[0]

		div = document.new_tag( "div" )

		dialog.append( div )

		paragraph = document.new_tag( "p" ) ; div.append( paragraph )

		if ( self.idiom == None ) : paragraph.string = "Unknown idiom." ; return

		else : paragraph.string = f"This page is in {self.idiom}."

		if self.translations != None :

			for translation_path in self.translations :

				translation_idiom = str( Path( translation_path ).parents[-2] )

				translation_path = self.root_from_file / translation_path

				paragraph = document.new_tag( 'p', href=str( translation_path ) )

				div.append( paragraph )

				anchor = document.new_tag( 'a', href=str( translation_path.with_suffix( '.html' ) ) )

				anchor.string = str( translation_idiom )

				paragraph.append( anchor )

		else :

			paragraph = document.new_tag( "p" ) ; paragraph.string = "No translations for this page."

			div.append( paragraph )

		return

class DocumentationBuilder :

	def __init__ ( self, options ) :

		options = options.__dict__

		valid_options = [
			'source',
			'destination',
			'papaya_from_destination',
			'selection_to_build',
			'replace_spaces_by_dashes',
		]

		for name in options :

			if name in valid_options : setattr( self, name, options[name] )

		self.source = self.source.resolve()

		self.destination = self.destination.resolve()

		model_path = Path( __file__ ).parent / 'model.html'

		self.model_text = model_path.read_text()

		self.get_translations()

		if self.selection_to_build != None : self.selection_to_build = json.loads( self.selection_to_build.read_text() )

		self.file_builder = FileBuilder( **{ 'documentation_builder' : self } )

		return

	def get_translations ( self ) :

		translations_path = self.source / 'translations.json'

		if (
			self.source.is_dir()
			and translations_path.is_file()
		) :
			self.translations = json.loads( translations_path.read_text() )

		else : self.translations = None

		return

	def build_selected ( self ) :

		assert ( len( self.selection_to_build ) > 0 ) , 'Nothing specified to build.'

		for source_file_path in self.selection_to_build :

			source_file_path = self.source / source_file_path

			self.file_builder.set_source( source_file_path )

			self.file_builder.destination.parent.mkdir( parents=True, exist_ok=True )

			self.file_builder.build()

		return

	def build_all ( self ) :

		for source_directory_path, source_directory_names, source_file_names in self.source.walk() :

			parent_was_relocated = False

			for source_file_name in source_file_names :

				source_file_path = source_directory_path / source_file_name

				try : self.file_builder.set_source( source_file_path )

				except : continue

				if not parent_was_relocated : self.file_builder.destination.parent.mkdir( parents=True, exist_ok=True ) ; parent_was_relocated = True

				self.file_builder.build()

		return

	def build ( self ) :

		if self.destination.exists() : shutil.rmtree( str( self.destination ) )

		self.destination.mkdir()

		if ( self.source.is_file() ) :

			self.file_builder.set_source( self.source )

			self.file_builder.build()

			print( f"\"{self.file_builder.destination}\"" )

			return

		else : assert ( self.source.is_dir() )

		if (
			self.selection_to_build != None
			and self.selection_to_build != []
		) :
			self.build_selected()

		else : self.build_all()

		return

if __name__ == '__main__':

	option_parser = argparse.ArgumentParser()

	option_parser.add_argument( "--source", dest='source', required=True, type=Path )

	option_parser.add_argument( "--destination", dest='destination', default=Path( '/tmp/papaya' ), type=Path )

	option_parser.add_argument( "--papaya", dest='papaya_from_destination', default=Path(__file__).parents[1].resolve(), type=Path )

	option_parser.add_argument( "--build-only", dest='selection_to_build', type=Path )

	option_parser.add_argument( "--replace-spaces-by-dashes", dest='replace_spaces_by_dashes', default=True, action=argparse.BooleanOptionalAction )

	options = option_parser.parse_args()

	builder = DocumentationBuilder( options )

	builder.build()
