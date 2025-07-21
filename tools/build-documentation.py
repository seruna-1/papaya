import markdown

import argparse

import json

from pathlib import Path

from bs4 import BeautifulSoup

import shutil

import csv

import os

class Debugger :

	def __init__ ( self, instance ) :

		self.activated = True

		self.name = type(instance).__name__

		return

	def post ( self, message ) :

		print( f"Instance of {self.name}:\n{message}\n\n" )

		return

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

		self.debug = self.documentation_builder.debug

		if self.debug : self.debugger = Debugger( self )

		self.source = None

		self.valid_source_suffixes = [ '.md', '.html' ]

		self.destination = None

		self.papaya_from_file = None

		self.idiom_tags = []

		language_tags_csv_path = Path(__file__).parent / 'ietf-language-tags.csv'

		with open( language_tags_csv_path ) as csvfile:

			reader = csv.DictReader(csvfile)

			for row in reader: self.idiom_tags.append( row['lang'] )

		self.idiom = None

		self.translations = None

		self.document = None

		return

	def set_source ( self, path ) :

		self.source = path.resolve()

		if not self.source.suffix in self.valid_source_suffixes : raise Exception( f"File {self.source} has invalid source suffix {self.source.suffix}." )

		if self.debug : self.debugger.post( f"Set file {self.source} as source." )

		self.source_from_root = self.source.relative_to( self.documentation_builder.source )

		self.destination = self.documentation_builder.destination / self.source_from_root.with_suffix( ".html" )

		if self.debug : self.debugger.post( f"Building as file {self.source}." )

		if self.documentation_builder.replace_spaces_by_dashes :

			self.destination = Path( str( self.destination ).replace( ' ', '-' ) )

			if self.debug : self.debugger.post( f"Replaced spaces by dashes. Destination became {self.destination}." )

		self.idiom = self.find_idiom( self.source )

		if self.debug : self.debugger.post( f"Idiom: {self.idiom}" )

		self.root_from_file = self.documentation_builder.destination.relative_to( self.destination.parent, walk_up=True )

		self.papaya_from_file = self.root_from_file / self.documentation_builder.papaya_from_destination

		if ( self.documentation_builder.translations != None ) : self.find_translation_group()

		if self.debug : self.debugger.post( f"Current file translations: {self.translations}." )

		return

	def find_idiom ( self, file_path ) :

		file_path = Path( file_path )

		idiom = None

		parts = []

		for parent in file_path.parents : parts.append( parent.name )

		for suffix in file_path.suffixes : parts.append( suffix[1:] )

		for part in parts :

			is_tag = part in self.idiom_tags

			if is_tag and ( idiom == None ) : idiom = part

			elif is_tag and ( idiom != part ) : raise Exception()

		return idiom

	def find_translation_group ( self ) :

		translation_groups = self.documentation_builder.translations

		assert ( translation_groups != None )

		self.translations = None

		for group in translation_groups :

			if ( self.translations != None ) : print("group"); break

			for file_path in group :

				if str( self.source_from_root ).startswith( file_path ) :

					self.translations = group.copy()

					self.translations.remove( file_path )

					break

		return

	def build ( self ) :

		self.document = BeautifulSoup( self.documentation_builder.model_text, 'html.parser' )

		part = self.source.read_text()

		if self.source.suffix == '.md' : part = markdown.markdown( part )

		part = BeautifulSoup( part, 'html.parser' )

		if self.source.suffix == '.md' :

			section_builder = SectionBuilder( part )

			section_builder.build()

		insert_point = self.document.find( 'main' )

		insert_point.append(part)

		self.build_title( self.document )

		self.build_language_information( self.document )

		self.build_references_to_papaya( self.document )

		self.destination.write_text( self.document.prettify() )

		self.update_references()

		return

	def build_title ( self, document ) :

		given_titles = document.select( 'main title' )

		title = None

		if ( given_titles != [] ) :

			assert ( len( given_titles ) == 1 ) , 'More than one title in part.'

			title = given_titles[0].string

			given_titles[0].decompose()

		else :

			title = str( self.source.stem ).replace( f".{self.idiom}", '' )

			if self.debug : self.debugger.post( f"Generated title {title} from filename {self.source.name}." )

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

				if not translation_path.endswith( '.html' ) : translation_path = translation_path + '.html'

				if self.documentation_builder.replace_spaces_by_dashes : translation_path = translation_path.replace( ' ', '-' )

				translation_idiom = self.find_idiom( translation_path )

				translation_path = self.root_from_file / translation_path

				paragraph = document.new_tag( 'p' )

				div.append( paragraph )

				anchor = document.new_tag( 'a', href=str( translation_path ) )

				anchor.string = str( translation_idiom )

				paragraph.append( anchor )

		else :

			paragraph = document.new_tag( "p" )

			paragraph.string = "No translations for this page."

			div.append( paragraph )

		return

	def update_references ( self ) :

		if self.documentation_builder.pack : packed = self.documentation_builder.packed
		else : packed = None

		attributes = [ 'href', 'src' ]

		references = []

		for element in self.document.main.find_all() :

			for attribute in attributes :

				if attribute in element.attrs : references.append( Path( element[attribute] ) )

		for reference in references :

			current_location = self.source.parent / reference

			current_location = current_location.absolute()

			destination = self.documentation_builder.destination / current_location.relative_to( self.documentation_builder.source )

			if ( packed == None ) :
				destination.parent.mkdir( parents=True, exist_ok=True )

				os.symlink( current_location, destination )

			elif \
			(
				current_location.exists()
				and current_location not in packed
			) :
				if not current_location.is_symlink() :

					destination.parent.mkdir( parents=True, exist_ok=True )

					shutil.copyfile( current_location, destination, follow_symlinks=False )

					packed.append( current_location )

				else :

					link = current_location

					link_destination = destination

					linked = link.resolve()

					linked_destination = self.documentation_builder.destination / linked.relative_to( self.documentation_builder.source )

					link_target = linked_destination.relative_to( link_destination.parent, walk_up=True )

					if \
					(
						not linked.is_relative_to( self.documentation_builder.source )
						or linked not in packed
					) :
						linked_destination.parent.mkdir( parents=True, exist_ok=True )

						shutil.copyfile( linked, linked_destination )

						packed.append( linked_destination )

					link_destination.parent.mkdir( parents=True, exist_ok=True )

					os.symlink( link_target, link_destination )

					packed.append( link )

		return

class DocumentationBuilder :

	def __init__ ( self, options ) :

		options = options.__dict__

		valid_options = [
			'source',
			'destination',
			'overwrite',
			'papaya_from_destination',
			'replace_spaces_by_dashes',
			'build_selection',
			'pack',
			'redirector_destination',
			'debug',
			'debug_for_file'
		]

		for name in options :

			if name in valid_options : setattr( self, name, options[name] )

		if self.debug : self.debugger = Debugger( self )

		self.source = self.source.resolve()

		self.destination = self.destination.resolve()

		if ( self.redirector_destination == None ) : self.redirector_destination = self.destination / 'index.html'

		model_path = Path( __file__ ).parent / 'model.html'

		self.model_text = model_path.read_text()

		translations_path = self.source / 'translations.json'

		if translations_path.is_file() : self.translations = json.loads( translations_path.read_text() )

		else : self.translations = None

		self.selection_to_build = []

		if self.source.is_file():

			self.selection_to_build.append( self.source )

			self.source = self.source.parent

		file_selection_json = self.source / "selection.json"

		if \
		(
			self.build_selection
			and file_selection_json.is_file()
		):
			self.selection_to_build.append( json.loads( file_selection_json.read_text() ) )

		self.file_builder = FileBuilder( **{ 'documentation_builder' : self } )

		if self.pack : self.packed = []

		return

	def build_redirector ( self ) :

		entry_points_json = self.source / "entry-points.json"

		if ( entry_points_json.is_file() ) : entry_points = json.loads( entry_points_json.read_text() )
		else : return

		if self.debug : self.debugger.post( f"Entry points: {entry_points}." )

		model_redirector = Path(__file__).parent / 'model-redirector.html'

		redirector = BeautifulSoup( model_redirector.read_text(), 'html.parser' )

		main = redirector.find( "main" )

		for entry_point in entry_points :

			#path = self.source / ( entry_point )

			#if not path.is_file() : raise Exception( f"Entry point {entry_point} not file." )

			redirector_to_destinaiton_root = self.destination.relative_to( self.redirector_destination.parent.absolute() )

			destinaiton_root_to_redirected = entry_point + '.html'

			if self.replace_spaces_by_dashes : destinaiton_root_to_redirected = destinaiton_root_to_redirected.replace( " ", "-" )

			redirector_to_redirected = redirector_to_destinaiton_root / destinaiton_root_to_redirected

			paragraph = redirector.new_tag( "p" )

			paragraph.string = str( redirector_to_redirected )

			main.append( paragraph )

		self.redirector_destination.write_text( redirector.prettify() )

		return

	def build_selected ( self ) :

		for source_file_path in self.selection_to_build :

			source_file_path = self.source / source_file_path

			self.file_builder.set_source( source_file_path )

			self.file_builder.destination.parent.mkdir( parents=True, exist_ok=True )

			self.file_builder.build()

			print( self.file_builder.destination )

		return

	def build_all ( self ) :

		for source_directory_path, source_directory_names, source_file_names in self.source.walk() :

			parent_was_relocated = False

			for source_file_name in source_file_names :

				source_file_path = source_directory_path / source_file_name

				try :
					self.file_builder.set_source( source_file_path )

				except : continue

				if not parent_was_relocated : self.file_builder.destination.parent.mkdir( parents=True, exist_ok=True ) ; parent_was_relocated = True ; #print(f"{self.file_builder.destination.parent}")

				self.file_builder.build()

		return

	def build ( self ) :

		if \
		(
			self.destination.exists()
			and len( os.listdir( self.destination ) ) > 0
		) :
			if self.overwrite : shutil.rmtree( str( self.destination ) )
			else : raise Exception( "Destination directory exists.")

		if not self.destination.exists() : self.destination.mkdir()

		if len( self.selection_to_build ) > 0 : self.build_selected()
		else : self.build_all()

		self.build_redirector()

		return

if __name__ == '__main__':

	option_parser = argparse.ArgumentParser()

	option_parser.add_argument( "--source", dest='source', required=True, type=Path )

	option_parser.add_argument( "--destination", dest='destination', default=Path( '/tmp/papaya' ), type=Path )

	option_parser.add_argument( "--overwrite", default=False, action=argparse.BooleanOptionalAction )

	option_parser.add_argument( "--papaya", dest='papaya_from_destination', default=Path(__file__).parents[1].resolve(), type=Path )

	option_parser.add_argument( "--build-only", dest='build_selection', default=False, action=argparse.BooleanOptionalAction )

	option_parser.add_argument( "--replace-spaces-by-dashes", dest='replace_spaces_by_dashes', default=True, action=argparse.BooleanOptionalAction )

	option_parser.add_argument( "--pack", default=False, action=argparse.BooleanOptionalAction )

	option_parser.add_argument( "--redirector", dest='redirector_destination', default=None, type=Path )

	option_parser.add_argument( "--debug", default=False, action=argparse.BooleanOptionalAction )

	option_parser.add_argument( "--debug-for-file", dest='debug_for_file', default=None, type=Path )

	options = option_parser.parse_args()

	builder = DocumentationBuilder( options )

	builder.build()
