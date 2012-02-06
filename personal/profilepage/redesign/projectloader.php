<?php

class xml_to_array {
    public $array = array();
    public $parse_error = false;
    private $parser;
    private $pointer;

    public function __construct($xml) {
        $this->pointer =& $this->array;
        $this->parser = xml_parser_create("UTF-8");
        xml_set_object($this->parser, $this);
        xml_parser_set_option($this->parser, XML_OPTION_CASE_FOLDING, false);
        xml_set_element_handler($this->parser, "tag_open", "tag_close");
        xml_set_character_data_handler($this->parser, "cdata");
        $this->parse_error = xml_parse($this->parser, ltrim($xml))? false : true;
    }

    public function __destruct() {
        xml_parser_free($this->parser);
    }

    public function get_xml_error() {
        if ($this->parse_error) {
            $err_code = xml_get_error_code($this->parser);
            $cur_error = "Error Code [" . $err_code . "] <strong style='color:red;'>" . xml_error_string($err_code) . "</strong>\", at char " . xml_get_current_column_number($this->parser) . " on line " . xml_get_current_line_number($this->parser) . ".\n";
        }
        else {
            $cur_error = $this->parse_error;
        }
        return $cur_error;
    }

    private function tag_open($parser,$tag, $attributes) {
        $this->convert_to_array($tag, 'attrib');
        $index = $this->convert_to_array($tag, 'cdata');
        if (isset($index)) {
            $this->pointer[$tag][$index] = Array('@index' => $index, '@parent' => &$this->pointer);
            $this->pointer =& $this->pointer[$tag][$index];
        }
        else {
            $this->pointer[$tag] = Array('@parent' => &$this->pointer);
            $this->pointer =& $this->pointer[$tag];
        }
        if (!empty($attributes)) {
            $this->pointer['attrib'] = $attributes;
        }
    }

    private function cdata($parser, $cdata) {
        $this->pointer['cdata'] = trim($cdata);
    }
    
    private function tag_close($parser, $tag) {
        $current = & $this->pointer;
        if (isset($this->pointer['@index'])) { unset($current['@index']); }
        
        $this->pointer = & $this->pointer['@parent'];
        unset($current['@parent']);
        
        if (isset($current['cdata']) && count($current) == 1) { $current = $current['cdata']; }
        else if (empty($current['cdata'])) { unset($current['cdata']); }
    }

    private function convert_to_array($tag, $item) {
        if (isset($this->pointer[$tag][$item])) {
            $content = $this->pointer[$tag];
            $this->pointer[$tag] = array((0) => $content);
            $index = 1;
        }
        else if (isset($this->pointer[$tag])) {
            $index = count($this->pointer[$tag]);
            if (!isset($this->pointer[$tag][0])) {
                foreach ($this->pointer[$tag] as $key => $val) {
                    unset($this->pointer[$tag][$key]);
                    $this->pointer[$tag][0][$key] = $val;
                }
            }
        }
        else {
            $index = null;
        }
        return $index;
    }
}

/* Parses data from an XML file (In this case project data ) */
function load_projects($filename) {
    // Read the XML file
    $data = implode("", file($filename));
    
    $xmld = new xml_to_array($data);

    $xmla = $xmld->array;

    //print_r($xmla);

    return $xmla;
}

//$db = load_projects("projects.xml");

?>