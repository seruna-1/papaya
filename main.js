const htmlHead = document.querySelector( "head" );

const htmlBody = document.querySelector( "body" );

const htmlMain = document.querySelector( "main" );

const titles = document.querySelectorAll( "h1, h2, h3, h4, h5, h6" );

class ButtonToSection
{
	constructor( avaiableElement )
	{
		if ( [ "H1", "H2", "H2", "H3", "H4", "H5", "H6" ].includes( avaiableElement.tagName ) == true )
		{
			this.section = avaiableElement;

			this.element = document.createElement( "button" );

			this.element.textContent = this.section.textContent;
		}

		else if ( avaiableElement.tagName == "BUTTON" )
		{
			this.element = avaiableElement;
		}

		this.element.addEventListener( "click", ( event ) => { this.replyClick( event ) } );
	}

	replyClick( event )
	{
		console.log(this.section);
		this.section.scrollIntoView();
	}
}

class ButtonGoTop
{
	constructor()
	{
		this.element = document.createElement( "input" );

		this.element.setAttribute( "type", "button" );

		this.element.setAttribute("value", "Top");

		this.element.setAttribute("ID", "buttonGoTop");

		this.element.addEventListener( "click", ButtonGoTop.replyClick );
	}

	static replyClick( event )
	{
		return window.scrollTo( 0, 0 );
	}
}

class Dialog
{
	constructor( name )
	{
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

		this.name = name;

		this.element.setAttribute( "name", name );

		this.element.prepend( this.buildButtonClose() );

		this.buttonShow = document.createElement( "input" );

		this.buttonShow.setAttribute( "type", "button" );

		this.buttonShow.setAttribute( "value", this.name );

		this.buttonShow.addEventListener( "click", ( event ) => { this.replyButtonShow( event ) } );

		htmlBody.appendChild( this.element );
	}

	buildContent()
	{
		return document.createElement( "div" );
	}

	buildButtonClose()
	{
		const button = document.createElement( "input" );

		button.setAttribute( "type", "button" );

		button.setAttribute( "value", "Close" );

		button.addEventListener( "click", () => { this.replyButtonClose( event ) } );

		return button;
	}

	replyButtonShow( event )
	{
		this.element.showModal();
	}

	replyButtonClose( event )
	{
		this.element.close();
	}
}

class DialogMain extends Dialog
{
	buildContent()
	{
		const content = document.createElement( "div" );

		content.setAttribute("id", "viewSelectors");

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

			paragraph.appendChild( button.element );

			content.appendChild( paragraph );
		}

		return content;
	}
}

enumerateTitles();

let dialogs = [

	new DialogSections( "sections" ),

	new Dialog( "idioms" )

];

const dialogMain = new DialogMain( "main" );

const htmlHeader = createHeader();

const buttonGoTop = new ButtonGoTop()

htmlBody.appendChild( buttonGoTop.element );

dialogMain.buttonShow.setAttribute( "value", "..." );

dialogMain.buttonShow.setAttribute( "id", "buttonShowDialogMain" );

htmlBody.appendChild( dialogMain.buttonShow );

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

		title.textContent = position.join( "." ) + " " + title.textContent;

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

generateSelfAnchors();
