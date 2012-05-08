<?php
$title = "Tea And Muskets";
$content = "";
$menu = "";

// The main print function
function printPage() {
	global $title, $content, $menu;
	
	// Start HTML stuff
	echo "<html>";
	echo "<head><link href=\"style.css\" rel=\"stylesheet\" type=\"text/css\">";
	echo "<title>" . $title . "</title>";
	echo "</head>";
	echo "<body class=\"bg-grad\">";
	
	echo "<div class=\"main\">";
	echo "<div class=\"menu\">" . $menu . "</div>";
	echo "<div class=\"content\">" . $content . "</div>";
	
	echo "</div>"; //main
	
	// Close out
	echo "</body>";
	echo "</html>";
}

//Add a menu item
function addMenuItem($href, $name) {
    return "<td id=\"menuentry\"><a class=\"menuitem\" href=\"" . $href . "\" title=\"" . $name . "\">" . $name . "</a></td>";
}

// Add a box to the page
function addBox($box_content) {
	$ret = "";
	$ret .= "<div class=\"content_box\">" . $box_content . "</div>";
	return $ret;
}

$header = "<p>Header Here</p>";




$about_team = "About The Team";
$about_game = "About The Game";
$menu = addBox("Menu goes here");

/////////////////
// PAGE CHOICE //
/////////////////

$page = $_REQUEST["page"];

$content = addBox("CONTENTCONTENTCONTENT");

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

printPage();

?>