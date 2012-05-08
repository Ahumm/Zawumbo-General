<?php 
$title = "Tate Larsen Portfolio";
$headleft = "";
$header = "";
$headright = "";
$contentleft = "";
$content = "";
$contentright = "";
$footerleft = "";
$footer = "";
$footerright = "";

//Main function
function printPage() {
    //Variable declaration
    global $title, $headleft, $header, $headright, $contentleft, $content, $contentright, $footer;
    
    //Start HTMLing
    echo "<html>";
    echo "<head><link href=\"style.css\" rel=\"stylesheet\" type=\"text/css\">";
	echo "<title>" . $title . "</title>";
	echo "</head>";
    echo "<body class=\"bg-grad\">";
    
    //Main Stuff
    echo "<table id=\"sitetable\">";
    echo "<tr><td id=\"headerleft\">" . $headleft ."</td><td id=\"header\">" . $header . "</td><td id=\"headerright\">" . $headerright . "</td></tr>";
    echo "<tr><td id=\"contentleft\">" . $contentleft . "</td><td id=\"content\">" . $content . "</td><td id=\"contentright\">" . $contentright . "</td></tr>";
    echo "<tr><td id=\"footerleft\">" . $footerleft . "</td><td id=\"footer\">" . $footer . "</td><td id=\"footerright\">" . $footerright . "</td></tr>";

    echo "</table>";
    
    //Close out
    echo "</body>";
    echo "</html>";
}


/*    HELPER FUNCTIONS    */

//Separate elements in $list by commas
function commalist($list) {
    $ret = "";
    foreach ($list as $item) {
        $ret .= $item . ", ";
    }
    $ret = substr($ret, 0, -2);
    return $ret;
}

function unknown() {
    $ret = "";
    $ret .= "<br><br><center>This Space Intentionally Left Blank</center><br><br>";
    return $ret;
}


/*    MENU    */

//Add a menu item
function addMenuItem($href, $name) {
    return "<td id=\"menuentry\"><a class=\"menuitem\" href=\"" . $href . "\" title=\"" . $name . "\">" . $name . "</a></td>";
}

//Add a project menu item
function addProjectMenuItem($href, $name) {
    return "<td id=\"projectmenuentry\"><a class=\"projectmenuitem\" href=\"" . $href . "\" title=\"" . $name . "\">" . $name . "</a></td>";
}

//Make the menu
function makeMenu() {
    $ret = "<table id=\"headertable\"><tr>";
    $ret .= "<td id=\"menuleft\"></td>";
    $ret .=  addMenuItem("/", "Home");
    $ret .=  "<td id=\"menuslice\"></td>";
    $ret .=  addMenuItem("/tatelarsenresume.pdf", "R&eacute;sum&eacute;");
    $ret .=  "<td id=\"menuslice\"></td>";
    $ret .=  addMenuItem("/?page=projectlist", "Projects");
    $ret .=  "<td id=\"menuslice\"></td>";
    $ret .=  addMenuItem("/?page=contact", "About / Contact");
    $ret .=  "<td id=\"menuright\"></td>";
    $ret .= "</tr></table>";
    return $ret;
}


//Make a project menu
function makeProjectMenu($project, $projectpage) {
    $ret = "<table id=\"headertable\"><tr>";
    //$ret .= "<td id=\"menuleft\"></td>";
    if($projectpage) {
	$ret .= addProjectMenuItem("/?page=project&project=" . $project["id"], "Project Page");
    }
    if($project["sourcehref"]) {
	if($projectpage) {
	    $ret .=  "<td id=\"projectmenuslice\"></td>";
	}
	$ret .= addProjectMenuItem($project["sourcehref"], "Source");
    }
    if($project["binaryhref"]) {
	if($projectpage || $project["sourcehref"]) {
	    $ret .=  "<td id=\"projectmenuslice\"></td>";
	}
	$ret .= addProjectMenuItem($project["binaryhref"], "Binaries");
    }
    if($project["githref"]) {
	if($projectpage || $project["sourcehref"] || $project["binaryhref"]) {
	    $ret .=  "<td id=\"projectmenuslice\"></td>";
	}
	$ret .= addProjectMenuItem($project["githref"], "Git");
    }
    //$ret .=  "<td id=\"menuright\"></td>";
    $ret .= "</tr></table>";
    return $ret;
}

//Header will always include the menu
$header .= makeMenu();


/* Project Media */

// Load in all images, $project["screenshots"] should store array("image_location", "width", "height")
function addProjectScreenshots($project) {
    $ret = "";
    $ret .= "<center><h2>Screenshots</h2></center>";

    $ret .= "<center>";

    $c = 0;

    foreach($project["screenshots"] as $i) {
	$ret .= "<a href=" . $i[0] . "><img src=" . $i[0] . " width=" . ($i[1] * $project["screenshotsscale"]) . " height=" . ($i[2] * $project["screenshotsscale"]) . " hspace=5 vspace=5 /></a>";
	$ret .= "<br>";
    }

    $ret .= "</center>";

    return $ret;
}

function addProjectVideos($project) {
    $ret = "";
    $ret .= "<center><h2>Videos</h2></center>";

    return $ret;
}



/*    TEXT BLOCKS    */

//Add a block
function addBlock($text) {
    $ret = "<table id=\"projecttable\">";
    $ret .= "<tr><td id=\"projecthead\"></td></tr>";
    $ret .= "<tr><td id=\"projectbody\">" . $text . "</td></tr>";
    $ret .= "<tr><td id=\"projectfoot\"></td></tr>";
    $ret .= "</table>";
    return $ret;
}


/*    PROJECTS    */

//Add project summary
function addProject($project) {
    $ret = "";
    $ret .= "<h1>" . $project["title"] . "</h1>";
    $ret .= "<b>Course:</b> " . $project["course"] . "<br>";
    $ret .= "<b>Short Description:</b> " . $project["shortdesc"] . "<br>";
    $ret .= "<b>Started:</b> " . $project["started"] . "<br>";
    if ($project["completed"] !== false) {
        $ret .= "<b>Completed:</b> " . $project["completed"] . "<br>";
    }
    $ret .= "<b>Contributors:</b> " . commalist($project["contributors"]) . "<br>";
    $ret .= "<b>Skills:</b> " . commalist($project["skills"]) . "<br>";

    $ret .= "<br><br>";
    
    $ret .= makeProjectMenu($project, true);

    return $ret;
}

//Add full project
function addFullProject($project) {
    $ret = "";
    $ret .= "<h1>" . $project["title"] . "</h1>";
    $ret .= "<b>Course:</b> " . $project["course"] . "<br>";
    $ret .= "<b>Short Description:</b> " . $project["shortdesc"] . "<br>";
    $ret .= "<b>Started:</b> " . $project["started"] . "<br>";
    if($project["completed"] !== false) {
        $ret .= "<b>Completed:</b> " . $project["completed"] . "<br>";
    }
    $ret .= "<b>Status:</b> " . $project["status"] . "<br>";
    $ret .= "<b>Contributors:</b> " . commalist($project["contributors"]) . "<br>";
    $ret .= "<b>Skills:</b> " . commalist($project["skills"]) . "<br>";
    if($project["requires"]) {
	$ret .= "<b>Requires:</b> " . commalist($project["requires"]) . "<br>";
    }
    $ret .= "<b>Full Description:</b> " . $project["description"] . "<br>";

    $ret .= "<br><br>";

    $ret .= makeProjectMenu($project, false);

    return $ret;
}




  ///////////////////////////
 // Add All Personal Data //
///////////////////////////

/* Project Data */

$wold["id"] = "wold";
$wold["title"] = "Wold";
$wold["shortdesc"] = "A world simulation game";
$wold["course"] = "Personal Project";
$wold["started"] = "Fall 2010";
$wold["completed"] = false;
$wold["contributors"] = array("<a href=http://paphus.com>Tom Alexander</a>", "Michael \"Chap\" Gruar");
$wold["dochref"] = "http://wolddoc.paphus.com/";
$wold["sourcehref"] = "http://tate.paphus.com/src/wold.zip";
$wold["binaryhref"] = "http://tate.paphus.com/bin/wold.zip";
$wold["githref"] = false;
$wold["purpose"] = array("Learn and Implement Perlin Noise", "Gain Experience working with a team");
$wold["skills"] = array("CMake", "Git", "Doxygen", "Noise Algorithms");
$wold["requires"] = false;
$wold["status"] = "Still in the early stages with working OBJ model loading, camera movement functions, limited height map generation, lighting, and vertex buffer objects. Temporarily on hiatus.";
$wold["description"] = "Project goal is to create an open world environment for the player to explore and affect. The player can attack and \"subjugate\" NPCs to build a following and form a control structure while the NPCs go about doing the same for various resources.";
$wold["screenshots"] = array(array("img/wold-1.png",960,718));
$wold["screenshotsscale"] = 0.5;
$wold["videos"] = false;

$tumorraider["id"] = "tumorraider";
$tumorraider["title"] = "Tumor Raider";
$tumorraider["shortdesc"] = "Short Schmup";
$tumorraider["course"] = "Game Development I";
$tumorraider["started"] = "Fall 2011";
$tumorraider["completed"] = "Fall 2011";
$tumorraider["contributors"] = array("Brett Kaplan", "Jossued Rivera-Nazario", "Peter Skinner");
$tumorraider["sourcehref"] = "https://github.com/Ahumm/Tumor-Raider/zipball/master";
$tumorraider["binaryhref"] = false;
$tumorraider["githref"] = "https://github.com/Ahumm/Tumor-Raider/";
$tumorraider["purpose"] = array("Learn the pygame module.");
$tumorraider["skills"] = array("Git", "Pygame", "Python");
$tumorraider["requires"] = array("<a href=http://python.org/>Python 2.7</a>", "<a href=http://pygame.org/>Pygame</a>");
$tumorraider["status"] = "Completed";
$tumorraider["description"] = "The assignment was to create a short shoot-em-up style game (Roughly 3 to 5 minutes) using pygame in two weeks. We decided to create a game where the player controls a nanobot traveling through the blood stream destroying various malignant cells. The player has a short shield and can improve their weapon temporarily ";
$tumorraider["screenshots"] = array(array("img/tumorraider-1.png",800,600),array("img/tumorraider-2.png",800,600),array("img/tumorraider-3.png",800,600),array("img/tumorraider-4.png",800,600));
$tumorraider["screenshotsscale"] = 0.6;
$tumorraider["videos"] = false;

$bookofquakes["id"] = "bookofquakes";
$bookofquakes["title"] = "Book of Quakes";
$bookofquakes["shortdesc"] = "A Mobile game based on the verbs \"Collapse\" and \"Find\"";
$bookofquakes["course"] = "Game Development I";
$bookofquakes["started"] = "Fall 2011";
$bookofquakes["completed"] = "Fall 2011";
$bookofquakes["contributors"] = array("Dan Hawkins", "Marshall Hendrick", "Ryan Knight", "Alan Lummis");
$bookofquakes["sourcehref"] = "https://github.com/Ahumm/Book-of-Quakes/zipball/master";
$bookofquakes["binaryhref"] = false;
$bookofquakes["githref"] = "https://github.com/Ahumm/Book-of-Quakes/";
$bookofquakes["purpose"] = array("Learn the Corona SDK and LUA and gain an introduction to mobile game programming.");
$bookofquakes["skills"] = array("Git", "LUA", "Corona SDK", "Mobile Development");
$bookofquakes["status"] = "Completed";
$bookofquakes["requires"] = array("<a href=http://www.anscamobile.com/corona/>Corona SDK</a>");
$bookofquakes["description"] = "The assignment was to create a game for Android using the Corona SDK besed on a pair of verbs drawn at random in two weeks. We drew the words \"Collapse\" and \"Find\" so we wrote a game wherein the player has the ability to create earthquakes by shaking the device and is attempting to destroy certain buildings in a city while leaving others intact.";
$bookofquakes["screenshots"] = array(array("img/bookofquakes-1.png",960,549),array("img/bookofquakes-2.png",960,549),array("img/bookofquakes-3.png",960,549),array("img/bookofquakes-4.png",960,549),array("img/bookofquakes-5.png",960,549),array("img/bookofquakes-6.png",960,549));
$bookofquakes["screenshotsscale"] = 0.5;
$bookofquakes["videos"] = false;

$desertwasp["id"] = "desertwasp";
$desertwasp["title"] = "Desert W.A.S.P.";
$desertwasp["shortdesc"] = "A vehicle combat game";
$desertwasp["course"] = "Game Development I";
$desertwasp["started"] = "Fall 2011";
$desertwasp["completed"] = "Fall 2011";
$desertwasp["contributors"] = array("Ben Shippee", "Phelan Lemieux", "David Estrella", "Randy Sabella");
$desertwasp["sourcehref"] = "https://github.com/Ahumm/GD1P3/zipball/master";
$desertwasp["binaryhref"] = false;
$desertwasp["githref"] = "https://github.com/Ahumm/GD1P3/";
$desertwasp["purpose"] = array("Learn Panda3D and 3D game programming basics.");
$desertwasp["skills"] = array("Git", "Python", "Panda3D");
$desertwasp["status"] = "Completed";
$desertwasp["requires"] = array("<a href=http://python.org/>Python 2.7</a>", "<a href=http://www.panda3d.org/>Panda3D</a>");
$desertwasp["description"] = "The assignment was to create a 3D vehicle combat game in 2 weeks with vehicle headlights. We made a relatively simple wave based tank survival game featuring an experimental hovercraft. WARNING: SLOW TO LOAD. As in I don't have screenshots other than one of the loading screen because it takes too long to load.";
$desertwasp["screenshots"] = array(array("img/desertwasp-1.png",800,625));
$desertwasp["screenshotsscale"] = 0.6;
$desertwasp["videos"] = false;

$coralcleanup["id"] = "coralcleanup";
$coralcleanup["title"] = "Coral Clean-Up";
$coralcleanup["shortdesc"] = "A Tranquil 3D underwater fish game";
$coralcleanup["course"] = "Game Development I";
$coralcleanup["started"] = "Fall 2011";
$coralcleanup["completed"] = "Fall 2011";
$coralcleanup["contributors"] = array("Anisha Smith", "Jon Brenner", "Ivy Kwan");
$coralcleanup["sourcehref"] = "http://tate.paphus.com/zip/coralcleanup.zip";
$coralcleanup["binaryhref"] = "http://tate.paphus.com/bin/coralcleanup.zip";
$coralcleanup["githref"] = false;
$coralcleanup["purpose"] = array("Learn The Unity 3 engine and further develop 3D game programming skills.");
$coralcleanup["skills"] = array("Unity 3");
$coralcleanup["status"] = "Completed";
$coralcleanup["requires"] = array("<a href=http://unity3d.com/>Unity 3</a> (For source only)");
$coralcleanup["description"] = "The assignment was to create a 3D game based on the ideas of \"Tranquility\" and \"Order from Chaos.\" We designed a game in which the player takes on the role of a fish using their ability to spew bubbles to clean up trash in their underwater home. The Unity 3 project is unfortunately somewhat messy at present.";
$coralcleanup["screenshots"] = array(array("img/coralcleanup-1.png",960,540),array("img/coralcleanup-2.png",960,540),array("img/coralcleanup-3.png",960,540));
$coralcleanup["screenshotsscale"] = 0.5;
$coralcleanup["videos"] = false;


$projects = array("wold" => $wold, "tumorraider" => $tumorraider, "bookofquakes" => $bookofquakes, "desertwasp" => $desertwasp, "coralcleanup" => $coralcleanup);


/*    About Me    */

$aboutmeshort = "<center><img src=\"img/profile_pic.jpg\" width=200 height=280/></center><br><br>Hello and welcome to my portfolio site. My name is Tate Larsen and I am currently pursuing a dual degree in Computer Science and Games & Simulation Arts & Science (GSAS) at Rensselaer Polytechnic Institute.";

$aboutmefull = "";

$aboutmefull .= "<center><h4>Personal</h4></center>";
$aboutmefull .= "<table>";
$aboutmefull .= "<tr><th align=right>Name:</th><td>Tate Larsen</td></tr>";
$aboutmefull .= "<tr><th align=right>E-Mail:</th><td>talarsen@qwestoffice.net</td></tr>";
$aboutmefull .= "<tr><th align=right>Current Address:</th><td>16 Belle Ave Troy, NY 12180</td></tr>";
$aboutmefull .= "<tr><th align=right>Permenant Address:</th><td>9845 NE 27th st Bellevue, WA, 98004</td></tr>";
$aboutmefull .= "<tr><th align=right>Phone:</th><td>(425) 283-3847</td></tr>";
$aboutmefull .= "</table>";

$aboutmefull .= "<center><h4>Academics</h4></center>";
$aboutmefull .= "<table>";
$aboutmefull .= "<tr><th align=right>College:</th><td>Rensselaer Polytechnic Institute</td></tr>";
$aboutmefull .= "<tr><th align=right>Expected Graduation:</th><td>May 2013</td></tr>";
$aboutmefull .= "<tr><th align=right>Majors:</th><td>Computer Science</br>Games & Simulation Arts & Sciences</td></tr>";
$aboutmefull .= "<tr><th align=right>Status:</th><td>Dean's List</td></tr>";
$aboutmefull .= "</table>";

$aboutmefull .= "<center><h4>Programming</h4></center>";
$aboutmefull .= "<table>";
$aboutmefull .= "<tr><th align=right>Editor:</th><td>Emacs(Linux), Notepad++(Windows)</td></tr>";
$aboutmefull .= "<tr><th align=right>Languages Known:</th><td>C++, C#, C, Java, Lisp, PHP, Python</td></tr>";
$aboutmefull .= "<tr><th align=right>Languages Used:</th><td>Perl, Ruby, SQL, LUA</td></tr>";
$aboutmefull .= "<tr><th align=right>Version Control:</th><td>Git, Perforce, SVN</td></tr>";
$aboutmefull .= "<tr><th align=right>Operating Systems:</th><td>ArchLinux, Windows 7</td></tr>";
$aboutmefull .= "</table>";

$aboutmefull .= "<br><center><img src=img/stormtrooper.jpg /></center>";



/*    Contact Info    */

$contactinfo = "";



/*    Page Logic    */

$page = $_REQUEST["page"];

switch($page) {
    case "contact":
        $title .= " - About / Contact";
        $content .= addBlock($aboutmefull);
        break;
    case "projectlist":
        $title .= " - Projects";
        foreach ($projects as $p) {
            $content .= addBlock(addProject($p));
        }
        break;
    case "project":
        $project = $_REQUEST["project"];
	if($projects[$project]) {
	    $proj = $projects[$project];
	    $title .= " - " . $project;
	    $content .= addBlock(addFullProject($proj));
	    if($proj["screenshots"]) {
		$content .= addBlock(addProjectScreenshots($proj));
	    }
	    if($proj["videos"]) {
		$content .= addBlock(addProjectVideos($proj));
	    }
	}
	else {
	    $content .= addBlock(unknown());
	}
        break;
    default:
        $content .= addBlock($aboutmeshort);
        break;
}

printPage();
?>