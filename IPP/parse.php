<?PHP
  ini_set('display_errors', 'stderr');
  $NOP = ['CREATEFRAME','PUSHFRAME','POPFRAME','RETURN','BREAK'];
  $V = ['DEFVAR','POPS'];
  $S = ['PUSHS','WRITE','EXIT','DPRINT'];
  $L = ['CALL','LABEL','JUMP'];
  $VS = ['MOVE','NOT','INT2CHAR','TYPE','STRLEN'];
  $VT = ['READ'];
  $VSS = ['ADD','SUB','MUL','IDIV','LT','GT','EQ','AND','OR','STRI2INT','CONCAT','GETCHAR','SETCHAR'];
  $LSS = ['JUMPIFEQ','JUMPIFNEQ'];
  $OP = array_merge($NOP,$V,$S,$L,$VS,$VT,$VSS,$LSS);
  
  function rm_hidden(&$string){
    $string = explode('#',$string);
    $string = preg_replace("/^\s*|\s*$/",'',$string[0]);
    $string = preg_replace('/\s+/',' ',$string);
    #if(strlen($string) > 0){
    #  $string =  $string."\n";
    #}
  }
  function is_name($string){
    $string = preg_match('/^([a-z]|[A-Z]|[_\-$&%*!?])+$/',$string);
    if($string){
      return true;
    }
    return false;
  }
  function is_bool_check($string){
    if($string == 'false' || $string == 'true'){
      return true;
    }
    return false;
  }
  function is_int_check($string){
    $string = preg_match('/^[+\-]?[0-9]+$/',$string);
    if($string){
      return true;
    }
    return false;
  }
  function is_string_check($string){
    $match = preg_match('/\\\.{0,2}[^0-9]|\\\.{0,2}$/',$string,$matches);
    if($match){
      return false;
    }
    global $order;
    return true;
  }
  function is_var($string){
    $string = preg_match("/^(LF|TF|GF)@([a-z]|[A-Z]|[_,\-,$,&,%,*,!,?])([a-z]|[A-Z]|[_,\-,$,&,%,*,!,?]|[0-9])*$/",$string,$matches);
    if($string){
      return true;
    }
    return false;
  }
  function is_label($string){
    if(is_name($string)){
      return true;
    }
    return false;
  }
  function is_type($string){
    $string = preg_match('/^(int|bool|string|nil)$/',$string);
    if($string){
      return true;
    }
    return false;
  }
  function is_const($string){
    if($string == 'nil@nil'){
      return true;
    }    
    $string = explode('@',$string);
    switch ($string[0]) {
      case 'int':
        if(is_int_check($string[1])){
          return true;
        }
        return false;
        break;
      case 'bool':
        if(is_bool_check($string[1])){
          return true;
        }
        return false;
        break;
      case 'string':
        $string = implode('@',$string);
        if(is_string_check($string)){
          return true;
        }
        return false;
        break;
      
      default:
        return false;
        break;
    }
  }
  function is_symb($string){
    if(is_const($string) || is_var($string)){
      return true;
    }
    return false;
  }
  function get_type(&$string){
    if(is_var($string)){
      return 'var';
    }    
    $tmp = explode('@',$string);
    if(count($tmp) == 1){
      return 'type';
    }
    else{
      if(is_type($tmp[0])){
        $string = $tmp;
        $string[0] = '';
        $string = implode('@',$string);
        $string = preg_replace('/^@/','',$string);
        return $tmp[0];
      }
      else{
        exit(23);
      }
    }
  }
  function xml_start(&$xml){
    $xml = xmlwriter_open_memory();
    xmlwriter_set_indent($xml, 1);
    xmlwriter_set_indent_string($xml, '    ');
    xmlwriter_start_document($xml, '1.0', 'UTF-8');
    xmlwriter_start_element($xml, 'program');
    xmlwriter_start_attribute($xml,'language');
    xmlwriter_text($xml,'IPPcode22');
    xmlwriter_end_attribute($xml);
  }
  function xml_instruction(&$xml, $order, $opcode){
    xmlwriter_start_element($xml,'instruction');
    xmlwriter_start_attribute($xml,'order');
    xmlwriter_text($xml,$order);
    xmlwriter_start_attribute($xml,'opcode');
    xmlwriter_text($xml,$opcode);
  }
  function xml_end_instruction(&$xml){
    xmlwriter_end_element($xml);
  }
  function xml_arg(&$xml, $num, $type, $text){
    xmlwriter_start_element($xml, 'arg'.$num);
    xmlwriter_start_attribute($xml, 'type');
    xmlwriter_text($xml, $type);
    xmlwriter_end_attribute($xml);
    xmlwriter_text($xml, $text);
    xmlwriter_end_element($xml);
  }
  function xml_end(&$xml){
    xmlwriter_end_document($xml);
    echo(xmlwriter_output_memory($xml));
  }

  if($argc > 1){
    if($argv[1] == '--help' && $argc == 2){
      echo("Usage: parse.php [options]\n       --help    show this help\n");
      exit(0);
    }
    else{
      exit(10);
    }
  }
  else{
    $header = false;
    $order = 1;
    xml_start($xw);

    while($line = fgets(STDIN)){
      rm_hidden($line);
      if(strlen($line) > 0){
        if(!$header){
            if(strtoupper($line) == ".IPPCODE22"){
              $header = true;
            }
            else{
              exit(21);
            }
        }
        else{
          $line = explode(' ',$line);
          $line[0] = strtoupper($line[0]);
          if(!in_array($line[0],$OP)){
            exit(22);
          }
          if(count($line) == 1){
            if(in_array($line[0],$NOP)){
              xml_instruction($xw, $order, $line[0]);
            }
            else{
              exit(23);
            }
            xml_end_instruction($xw);
          }
          elseif(count($line) == 2){
            $type = '';
            xml_instruction($xw, $order, $line[0]);
            if(in_array($line[0],$V)){
              if(is_var($line[1])){
                $type = 'var';
              }
              else{
                exit(23);
              }
            }
            elseif(in_array($line[0],$S)){
              if(is_symb($line[1])){
                $type = get_type($line[1]);
              }
              else{
                exit(23);
              }
            }
            elseif(in_array($line[0],$L)){
              if(is_label($line[1])){
                $type = 'label';
              }
              else{
                exit(23);
              }
            }
            else{
              exit(23);
            }
            xml_arg($xw, 1, $type, $line[1]);
            xml_end_instruction($xw);
          }
          elseif(count($line) == 3){
            $type1 = '';
            $type2 = '';
            xml_instruction($xw, $order, $line[0]);
            if(in_array($line[0],$VS)){
              if(is_var($line[1])){
                $type1 = 'var';
              }
              else{
                exit(23);
              }
              if(is_symb($line[2])){
                $type2 = get_type($line[2]);
              }
              else{
                exit(23);
              }
            }
            elseif(in_array($line[0],$VT)){
              if(is_var($line[1])){
                $type1 = 'var';
              }
              else{
                exit(23);
              }
              if(is_type($line[2])){
                $type2 = 'type';
              }
              else{
                exit(23);
              }
            }
            else{
              exit(23);
            }
            xml_arg($xw, 1, $type1, $line[1]);
            xml_arg($xw, 2, $type2, $line[2]);
            xml_end_instruction($xw);
          }
          elseif(count($line) == 4){
            $type1 = '';
            $type2 = '';
            $type3 = '';
            xml_instruction($xw, $order, $line[0]);
            if(in_array($line[0],$VSS)){
              if(is_var($line[1])){
                $type1 = 'var';
              }
              else{
                exit(23);
              }
              if(is_symb($line[2])){
                $type2 = get_type($line[2]);
              }
              else{
                exit(23);
              }
              if(is_symb($line[3])){
                $type3 = get_type($line[3]);
              }
              else{
                exit(23);
              }
            }
            elseif(in_array($line[0],$LSS)){
              if(is_label($line[1])){
                $type1 = 'label';
              }
              else{
                exit(23);
              }
              if(is_symb($line[2])){
                $type2 = get_type($line[2]);
              }
              else{
                exit(23);
              }
              if(is_symb($line[3])){
                $type3 = get_type($line[3]);
              }
              else{
                exit(23);
              }
            }
            else{
              exit(23);
            }
            xml_arg($xw, 1, $type1, $line[1]);
            xml_arg($xw, 2, $type2, $line[2]);
            xml_arg($xw, 3, $type3, $line[3]);
            xml_end_instruction($xw);
          }
          else{
            exit(23);
          }
          $order++;
        }
      }
    }    
    if(!$header){
      exit(21);
    }
    xml_end($xw);
    exit(0);
  }
  exit(99);

?>