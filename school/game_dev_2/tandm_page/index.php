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
	
	echo "<div class=\"center\">";
    echo "<table class=\"sitetable\"><tr><td id=\"borderless\" class=\"left\"></td>";
    echo "<td id=\"borderless\" class=\"middle\">";
    
    echo "<div class=\"main\">";
    echo "<div class=\"header\">";
    echo "<div class=\"logo\"></div>";
	echo "<div class=\"menu\">" . $menu . "</div>";
    echo "</div>"; // header
    
	echo "<div class=\"content\">" . $content . "</div>";
	
    echo "</div>"; // main
    
    echo "</td>";
    echo "<td id=\"borderless\" class=\"right\"></td>";
    echo "</tr></table>";
    
	echo "</div>"; // content
	
	// Close out
	echo "</body>";
	echo "</html>";
}

//Add a menu item
function addMenu() {
	$ret =  "<ul id=\"gradmenu\">";
	$ret .= "<li id=\"menuhome\"><a href=\"/\"></a></li>";
	$ret .= "<li id=\"menuproject\"><a href=\"/?page=project\"></a></li>";
	$ret .= "<li id=\"menuimages\"><a href=\"/?page=images\"></a></li>";
	$ret .= "<li id=\"menuvideos\"><a href=\"/?page=videos\"></a></li>";
	$ret .= "<li id=\"menuabout\"><a href=\"/?page=about\"></a></li>";
	$ret .= "<li id=\"menudownloads\"><a href=\"/?page=downloads\"></a></li>";
	$ret .= "</ul>";
    return $ret;
}

// Add a box to the page
function addBox($heading, $box_content) {
	$ret = "";
	$ret .= "<div class=\"content_box\">";
    $ret .= "<center><h2>" . $heading . "</h2></center>";
    $ret .= $box_content;
    $ret .= "<br>";
    $ret .= "</div>";
	return $ret;
}

// Add all images
function addImages($images) {
    $ret = "";
    foreach($images as $i) {
        $ret .= "<a href=\"" . $i . "\"><img src=\"" . $i . "\"/></a><br><br><br>";
    }
    $ret .= "<p>Images available for download on the Downloads page.</p>";
	return $ret;
}

// Add all videos
function addVideos($videos) {
	$ret = "";
    $preret = "";
    foreach($videos as $v_name => $v) {
        $ret .= "<video width=\"458\" height=\"258\" controls>";
        foreach($v as $key => $val) {
            if($key == "webm") {
                $ret .= "<source src=\"" . $val . "\" type=\"video/webm; codexs=\"vp8, vorbis\"\">";
            }
        }
        $ret .= "\"You appear to not have HTML5 support\"";
        $ret .= "</video><br><br><br>";
    }
    $ret .= "<p>Videos available for download on the Downloads page.</p><p>(They're also bigger)</p>";
	return $ret;
}

// Add all downloads
function addDownloads($downloadables) {
	$ret = "";
    $ret .= "<table class=\"centered\">";
    foreach($downloadables as $dl_name => $dl_src) {
        $ret .= "<tr><th align=right width=50%>" . $dl_name . ": </th><td width=50%><a href=\"" . $dl_src . "\">Here</a></td></tr>";
    }
    $ret .= "</table>";
	return $ret;
}

function addTeamInfo($team) {
    $ret = "";
    foreach($team as $member) {
        $ret .= "<table class=\"centered\">";
        $ret .= "<tr><th align=right width=50%>Name:</th><td width=50%>" . $member['name'] . "</td></tr>";
        if($member['personalsite']) {
            $ret .= "<tr><th align=right width=50%>Personal Site:</th><td width=50%><a href=\"" . $member['personalsite']['link'] . "\">" . $member['personalsite']['name'] . "</a></td></tr>";
        }
        $ret .= "<tr><th align=right width=50%>Contributions:</th><td width=50%>" . $member['contributions'] . "</td></tr>";
        $ret .= "</table><br>";
    }
    return $ret;
}

$downloadables['Standalone Player'] = "src/teaandmuskets_standalone.zip";
$downloadables['Videos'] = "media/vid/teaandmuskets_videos.zip";
$downloadables['Images'] = "media/img/teaandmuskets_images.zip";

$videos['Video 1']['webm'] = "media/vid/teaandmuskets.webm";
$videos['Video 1']['WebM HD'] = "media/vid/teaandmusketsHD.webm";

$images[] = "media/img/Snapshot-1.png";
$images[] = "media/img/Snapshot-2.png";
$images[] = "media/img/Snapshot-3.png";

$team['tom']['name'] = "Tom Alexander";
$team['tom']['personalsite']['name'] = "Paphus.com";
$team['tom']['personalsite']['link'] = "http://paphus.com";
$team['tom']['contributions'] = "Maps and Networking Functionality";

$team['chap']['name'] = "Michael \"Chap\" Gruar";
$team['chap']['contributions'] = "Unit and Town Creation";

$team['tate']['name'] = "Tate Larsen";
$team['tate']['personalsite']['name'] = "Ahumm.net";
$team['tate']['personalsite']['link'] = "http://ahumm.net";
$team['tate']['contributions'] = "Menus, GUI, Fog of War, and Player Interaction";

$team['pete']['name'] = "Peter Skinner";
$team['pete']['contributions'] = "Art Assets";

$team['nate']['name'] = "Nathan West";
$team['nate']['contributions'] = "Unit Pathfinding";


$about_team = "About The Team";
$about_game = "About The Game";
$about_short = "<p class=\"ju\">Tea and Muskets is an asymmetric multiplayer Realtime Strategy game where players play as either the British or Revere in a creative recreation of Revere's ride.</p>";
$menu = addMenu();




/////////////////
// PAGE CHOICE //
/////////////////

$page = $_REQUEST["page"];



switch($page) {
	case "project":
		$title .= " - About the Game";
		$content .= addBox("About the Game", $about_game);
		break;
	case "images":
		$title .= " - Images";
		$imagestxt = addImages($images);
		$content .= addBox("Images", $imagestxt);
		break;
	case "videos":
		$title .= " - Videos";
        $videostxt = addVideos($videos);
		$content .= addBox("Videos", $videostxt);
		break;
	case "about":
		$title .= " - About the Team";
        $about_team = addTeamInfo($team);
		$content .= addBox("About the Team", $about_team);
		break;
	case "downloads":
		$title .= " - Downloads";
        $downloads = addDownloads($downloadables);
		$content .= addBox("Downloads", $downloads);
		break;
	default:
        $content = addBox("Tea and Muskets", $about_short);
		break;
}

printPage();

?>