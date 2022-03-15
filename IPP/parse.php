<?PHP
  ini_set('display_errors', 'stderr');
  #no instruction opcodes
  $NOP = ['CREATEFRAME','PUSHFRAME','POPFRAME','RETURN','BREAK'];
  #Opcodes followed by <var>
  $V = ['DEFVAR','POPS'];
  #Opcodes followed by <symb>
  $S = ['PUSHS','WRITE','EXIT','DPRINT'];
  #Opcodes followed by <label>
  $L = ['CALL','LABEL','JUMP'];
  #Opcodes followed by <var> <symb>
  $VS = ['MOVE','NOT','INT2CHAR','TYPE','STRLEN'];
  #Opcodes followed by <var> <type>
  $VT = ['READ'];
  #Opcodes followed by <var> <symb> <symb>
  $VSS = ['ADD','SUB','MUL','IDIV','LT','sGT','EQ','AND','OR','STRI2INT','CONCAT','GETCHAR','SETCHAR'];
  #Opcodes followed by <label> <symb> <symb>
  $LSS = ['JUMPIFEQ','JUMPIFNEQ'];
  #ALL opcodes
  $OP = array_merge($NOP,$V,$S,$L,$VS,$VT,$VSS,$LSS);
  
  # rm_hidden 
  #   1. removes part of string after "#" including "#"
  #   2. removes white_signs at the beginning and at the end of string
  #   3. replaces multiple white_space characters with single space
  function rm_hidden(&$string){
    $string = explode('#',$string);                       # "   string  str# string " => ["   string   str"," string "]
    $string = preg_replace("/^\s*|\s*$/",'',$string[0]);  # ["   string   str"," string "] => "string   str"
    $string = preg_replace('/\s+/',' ',$string);          # "string   str" => "string str"
  }
  #is_var returns true if $string matches criteria for <var>, false otherwise
  function is_var($string){
    $string = preg_match("/^(LF|TF|GF)@([a-z]|[A-Z]|[_,\-,$,&,%,*,!,?])([a-z]|[A-Z]|[_,\-,$,&,%,*,!,?]|[0-9])*$/",$string,$matches);
    if($string){
      return true;
    }
    return false;
  }
  #is_label returns true if $string matches criteria for <label>, false otherwise
  function is_label($string){
    $string = preg_match('/^([a-z]|[A-Z]|[_\-$&%*!?])+$/',$string);
    if($string){
      return true;
    }
    return false;
  }
  #is_type returns true if $string matches criteria for <type>, false otherwise
  function is_type($string){
    $string = preg_match('/^(int|bool|string|nil)$/',$string);
    if($string){
      return true;
    }
    return false;
  }
  #is_const returns true if $string matches criteria for constant, false otherwise
  function is_const($string){
    if($string == 'nil@nil'){
      return true;
    }    
    $string = explode('@',$string);
    switch ($string[0]) {
      case 'int':
        if($match = preg_match('/^[+\-]?[0-9]+$/',$string[1])){
          return true;
        }
        return false;
        break;
      case 'bool':
        if($string[1] == 'false' || $string[1] == 'true'){
          return true;
        }
        return false;
        break;
      case 'string':
        $string = implode('@',$string);
        $match = preg_match('/\\\.{0,2}[^0-9]|\\\.{0,2}$/',$string,$matches);
        if(!$match){
          return true;
        }
        return false;
        break;
      
      default:
        return false;
        break;
    }
  }
  #is_symb returns true if $string matches criteria for <var> or is_const(), false otherwise
  function is_symb($string){
    if(is_const($string) || is_var($string)){
      return true;
    }
    return false;
  }
  #get_type returns type of $string
  function get_type(&$string){
    if(is_var($string)){
      return 'var';
    }    
    $tmp = explode('@',$string);
    if(count($tmp) == 1 && is_type($tmp)){
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
  #xmlwriter simpler interface functions
  #
  #xml_start - prepares head and starts 1st element 'program' with its attributes
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
  #xml_instruction - starts element 'instruction' with its attributes
  function xml_instruction(&$xml, $order, $opcode){
    xmlwriter_start_element($xml,'instruction');
    xmlwriter_start_attribute($xml,'order');
    xmlwriter_text($xml,$order);
    xmlwriter_start_attribute($xml,'opcode');
    xmlwriter_text($xml,$opcode);
  }
  #xml_end_instruction - ends element 'instruction'
  function xml_end_instruction(&$xml){
    xmlwriter_end_element($xml);
  }
  #xml_arg - makes element 'arg$', where $ is number of argument, with its attributes and text
  function xml_arg(&$xml, $num, $type, $text){
    xmlwriter_start_element($xml, 'arg'.$num);
    xmlwriter_start_attribute($xml, 'type');
    xmlwriter_text($xml, $type);
    xmlwriter_end_attribute($xml);
    xmlwriter_text($xml, $text);
    xmlwriter_end_element($xml);
  }
  #xml_end - closes xml and prints it to STDOUT
  function xml_end(&$xml){
    xmlwriter_end_document($xml);
    echo(xmlwriter_output_memory($xml));
  }

  #parse.php takes no arguments but '--help', anything other than '--help' as argument results in exit code 10
  if($argc > 1){
    if($argv[1] == '--help' && $argc == 2){
      echo("Usage: parse.php [options]\n       --help    show this help\n".
           "");
      exit(0);
    }
    else{
      exit(10);
    }
  }
  else{
    #$header - false => no header in file yet
    #          true => header found
    $header = false;
    $order = 1;
    xml_start($xw);
    #reading from STDIN into $line whole line until end of input
    while($line = fgets(STDIN)){
      rm_hidden($line);
      #skip over empty $line
      if(strlen($line) > 0){
        #Search for header, if the 1st line of code is not header, results in exit code 21
        if(!$header){
            if(strtoupper($line) == ".IPPCODE22"){
              $header = true;
            }
            else{
              exit(21);
            }
        }
        #header has been found
        else{
          #Check if 1st word(string separated by white_space characters) is in list of opcodes
          #   Uknown opcode results in exit code 22 
          $line = explode(' ',$line);
          $line[0] = strtoupper($line[0]);
          if(!in_array($line[0],$OP)){
            exit(22);
          }
          #Sorting $lines by number of words as each group of opcodes has specified number of arguments
          #   and then sorting further by groups of arguments. Then check if arguments are correct for
          #   given opcode, incorrect argument results in exit code 23.
          xml_instruction($xw, $order, $line[0]);
          if(count($line) == 1){
            if(!in_array($line[0],$NOP)){
              exit(23);
            }
          }
          elseif(count($line) == 2){
            $type = '';
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
          }
          elseif(count($line) == 3){
            $type1 = '';
            $type2 = '';
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
          }
          elseif(count($line) == 4){
            $type1 = '';
            $type2 = '';
            $type3 = '';
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
          }
          else{
            exit(23);
          }
          xml_end_instruction($xw);
          $order++;
        }
      }
    }    
    #No header check - reaching EOF without header results in exit code 21
    if(!$header){
      exit(21);
    }
    xml_end($xw);
    exit(0);
  }
  exit(99);

?>