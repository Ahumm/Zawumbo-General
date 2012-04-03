<?php 

$title = "Tate Larsen Portfolio";
$optional = "";

include 'header.php';

include 'menu.php';

include 'main.php';

include 'footer.php';

?>


<?php
/*

include 'projectlistpage.php';
include 'basepage.php';
include 'projectpage.php';
include 'aboutpage.php';

$title = "Tate Larsen Portfolio";
$headleft = "";
$headright = "";
$contentleft = "";
$content = "";
$contentright = "";
$footer = "";

function print_page() {
    global $title, $headleft, $header, $headright, $contentleft, $content, $contentright, $footer;

    $page_out = "";

    $page_out .= "<html>";
    $page_out .= "<head><title>" . $title . "</title></head>";
    $page_out .= "<body><link href=\"style.css\" rel=\"stylesheed\" type=\"text/css\">";

    $pdb = load_projects("projects.xml");
    $project_data = $pdb['projects']['project'];

    $projects = array();
    foreach ($project_data as $p) {
        $projects[] = new Project($p);
    }

    echo project_shorts($projects);
}

function project_shorts($projects) {
    $ret = "";
    foreach ($projects as $p) {
        $ret .= ($p->project_to_string_short() . "\n\n");
    }
    return substr($ret,0,-2);
}


print_page();
*/
?>