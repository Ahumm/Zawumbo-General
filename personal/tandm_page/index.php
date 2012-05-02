<?php
$title = "Tea And Muskets";
$headerleft = "";
$header = "";
$headerright = "";
$contentleft = "";
$content = "";
$contentright = "";
$footerleft = "";
$footer = "";
$footerright = "";

// The main print function
function printPage() {
	global $title, $headerleft, $header, $headerright, $contentleft, $content, $contentright, $footerleft, $footer, $footerright;
	
	// Start HTML stuff
	echo "<html>";
	echo "<head><link href=\"style.css\" rel=\"stylesheet\" type=\"text/css\">";
	echo "<title>" . $title . "</title>";
	echo "</head>";
	echo "<body class=\"bg-grad\">";
	
	echo "<table id=\"sitetable\">";
	echo "<tr><td id=\"headerleft\">" . $headerleft . "</td><td id=\"header\">" . $header . "</td><td id=\"headerright\">" . $headerright . "</td></tr>";
	echo "<tr><td id=\"contentleft\">" . $contentleft . "</td><td id=\"content\">" . $content . "</td><td id=\"contentright\">" . $contentright . "</td></tr>";
	echo "<tr><td id=\"footerleft\">" . $fooderleft . "</td><td id=\"footer\">" . $footer . "</td><td id=\"footerright\">" . $footerright . "</td></tr>";
	
	echo "</table>";
	
	// Close out
	echo "</body>";
	echo "</html>";
}

// Add a box to the page
function addBox($box_content) {
	$ret = "";
	$ret .= "<contentbox>" . $box_content . "</contentbox>";
	return $ret;
}

$header = "<p>Header Here</p>";
$content = "<p>Menu Here</p>";
$footer = "<p>Footer Here</p>";




$about_team = "About The Team";
$about_game = "About The Game";
$menu = "Menu";

/////////////////
// PAGE CHOICE //
/////////////////

$page = $_REQUEST["page"];

$content = "<table><td class=\"menu\">" . $menu . "</td><td class=\"content-box\">";

switch($page) {
	case "about":
		$title .= " - About the Game";
		$content .= addBox($about_game);
		break;
	case "team":
		$title .= " - About the Team";
		$content .= addBox($about_team);
		break;
	case "screenshot":
		break;
	case "videos":
		break;
	case "media":
		break;
	case "downloads":
		break;
	default:
		break;
}

$content .= "</td></table>";

printPage();

?>