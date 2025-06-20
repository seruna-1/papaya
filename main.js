const headerTagNames = [ "H1", "H2", "H2", "H3", "H4", "H5", "H6" ];

class ButtonToSection
{
	constructor( avaiableElement )
	{
		if ( headerTagNames.includes( avaiableElement.tagName ) )
		{
			this.section = avaiableElement;

			this.element = document.createElement( "button" );

			this.element.textContent = this.section.textContent;
		}

		else if ( avaiableElement.tagName == "BUTTON" )
		{
			this.element = avaiableElement;
		}

		this.element.addEventListener( "click", this );
	}

	handleEvent( event )
	{
		if ( event.type === "click" )
		{
			this.section.scrollIntoView();
		}
	}

}

class Dialog
{
	constructor( name, parent )
	{
		if ( name === undefined ) { return null; }
		else { this.name = name; }

		if ( parent !== undefined ) { this.parent = parent; }

		const existing = document.querySelector( `dialog[name=\"${name}\"]` );

		if ( existing != null )
		{
			this.element = existing;
		}

		else
		{
			this.element = document.createElement( "dialog" );

			this.element.appendChild( this.buildContent() );
		}

		this.element.setAttribute( "name", name );

		this.buttonClose = document.createElement( "input" );

		this.buttonClose.setAttribute( "type", "button" );

		this.buttonClose.setAttribute( "value", "Close" );

		this.buttonClose.addEventListener( "click", this );

		this.element.prepend( this.buttonClose );

		this.buttonShow = document.createElement( "input" );

		this.buttonShow.setAttribute( "type", "button" );

		this.buttonShow.setAttribute( "value", this.name );

		this.buttonShow.addEventListener( "click", this );

		htmlBody.appendChild( this.element );
	}

	buildContent()
	{
		return document.createElement( "div" );
	}

	handleEvent( event )
	{
		if
		(
			event.target === this.buttonClose
			&& event.type === "click"
		)
		{
			this.close();
		}

		else if
		(
			event.target === this.buttonShow
			&& event.type === "click"
		)
		{
			this.element.showModal();
		}

		return
	}

	close()
	{
		this.element.close();
	}

	closePropagate()
	{
		this.close();

		this.parent.closePropagate();
	}
}

class DialogMain extends Dialog
{
	buildContent()
	{
		const content = document.createElement( "div" );

		content.setAttribute("id", "viewSelectors");

		const dialogs = [

			new DialogSections( "sections" ),

			new Dialog( "idioms" )

		];

		for ( const dialog of dialogs )
		{
			let paragraph = document.createElement( "p" );

			let buttonOfDialog = dialog.buttonShow;

			buttonOfDialog.setAttribute( "class", "buttonOfDialog" );

			paragraph.appendChild( buttonOfDialog );

			content.appendChild( paragraph );

			buttonOfDialog.setAttribute( "value", dialog.name );
		}

		return content;
	}
}

class DialogSections extends Dialog
{
	buildContent()
	{
		const content = document.createElement( "div" );

		for ( const title of titles )
		{
			let paragraph = document.createElement("p");

			let button = new ButtonToSection( title );

			button.element.addEventListener( "click", this );

			paragraph.appendChild( button.element );

			content.appendChild( paragraph );
		}

		return content;
	}
}

function createHeader ()
{
	const htmlHeader = document.createElement( "header" );

	htmlBody.insertBefore( htmlHeader, htmlMain );

	const title = document.createElement( "h1" );

	title.textContent = document.querySelector( "title" ).textContent;

	htmlHeader.appendChild( title );

	return htmlHeader;
}

function enumerateTitles ()
{
	let position = [ 0 ];

	let level;

	let last_level;

	for ( const title of titles )
	{

		if ( htmlHeader.contains( title ) ) { continue; }

		level = parseInt( title.tagName[1] );

		if ( level > last_level )
		{
			position.push( 0 );
		}

		else if ( level < last_level )
		{
			position.pop();

			position[ position.length - 1 ]++;
		}

		position[ position.length - 1 ]++;

		title.insertAdjacentHTML( "afterbegin", position.join( "." ) + " " );

		last_level = level
	}

	return;
}

function generateSelfAnchors ()
{
	const selfAnchors = document.querySelectorAll( "a" );

	console.log( selfAnchors.length );

	let i = 0;

	while ( ( i < selfAnchors.length ) && !( selfAnchors[i].hasAttribute( "href" ) ) )
	{
		let buffer = selfAnchors[i].textContent.toLowerCase();

		buffer = buffer.replace( " ", "-" );

		buffer = buffer.replace( "_", "-" );

		let start = 0;

		let end = buffer.length;

		console.log( "File: " + buffer );

		while ( ( start < end ) && ( buffer.at( start ) == "-" ) )
		{
			start++;
		}

		while ( ( end > start ) && ( buffer.at( end ) == "-" ) )
		{
			end--;
		}

		console.log( "Start: " + start + " , end: " + end );

		buffer = buffer.slice( start, end + 1 ) + "/index.html";

		console.log( buffer );

		selfAnchors[i].setAttribute( "href", buffer );

		i++;
	}

	return;
}

const htmlHead = document.querySelector( "head" );

const htmlBody = document.querySelector( "body" );

const htmlMain = document.querySelector( "main" );

const htmlHeader = createHeader();

const titles = document.querySelectorAll( "h1, h2, h3, h4, h5, h6" );

enumerateTitles();

const dialogMain = new DialogMain( "main" );

dialogMain.buttonShow.setAttribute( "value", "..." );

dialogMain.buttonShow.setAttribute( "id", "buttonShowDialogMain" );

htmlBody.appendChild( dialogMain.buttonShow );

generateSelfAnchors();
