<?php

class Project {
    public $project = null;

    public function __construct($proj_array){
        $this->project = $proj_array;
    }

    public function project_to_string_short() {
        $ret = "";
        $ret .= "<h1>" . $this->project['title'] . "</h1>\n";
        $ret .= "<b>Project Type:</b> " . $this->project['type'] . "\n";
        $ret .= "<b>Short Description:</b> " . $this->project['short_desc'] . "\n";

        $ret .= "<b>Started:</b> " . $this->project['started'] . "\n";
        if (isset($this->project['completed'])) {
            $ret .= "<b>Completed:</b> " . $this->project['completed'] . "\n";
        }
        else {
            $ret .= "<b>Status:</b> " . $this->project['status'] . "\n";
        }

        $tret = "<b>Contributers:</b> ";
        foreach ($this->project['contributor'] as $c) {
            if (isset($c['href'])) {
                $tret .= "<a href=\"" . $c['href'] . "\">" . $c['name'] . "</a>, ";
            }
            else {
                $tret .= $c['name'] . ", ";
            }
        }
        $ret .= substr($tret, 0, -2) . "\n";
        
        $tret = "<b>Skills:</b> ";
        foreach ($this->project['skill'] as $s) {
            $tret .= $s . ", ";
        }
        $ret .= substr($tret, 0, -2) . "\n";
        
        return $ret;
    }
}

?>