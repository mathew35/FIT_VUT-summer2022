<?PHP
  ini_set('display_errors', 'stderr');

  $NOP = ['CREATEFRAME','PUSHFRAME','POPFRAME','RETURN','BREAK'];
  $V = ['DEFVAR','POPS'];
  $S = ['PUSHS','WRITE','EXIT','DPRINT'];
  $L = ['CALL','LABEL','JUMP'];
  $VS = ['MOVE','NOT','INT2CHAR','STRLEN'];
  $VT = ['READ','TYPE'];
  $VSS = ['ADD','SUB','MUL','IDIV','LT','GT','EQ','AND','OR','STRI2INT','CONCAT','GETCHAR','SETCHAR'];
  $LSS = ['JUMPIFEQ','JUMPIFNEQ'];
  
  function rm_hidden(&$string){
    $string = explode('#',$string);
    $string = preg_replace("/^\s*|\s*$/",'',$string[0]);
    $string = preg_replace('/\s+/',' ',$string);
    #if(strlen($string) > 0){
    #  $string =  $string."\n";
    #}
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
          if(count($line) == 1){
            if(in_array($line[0],$NOP)){
  
            }
            else{
              exit(22);
            }
          }
          if(count($line) == 2){
            if(in_array($line[0],$V)){
            }
            if(in_array($line[0],$S)){
            }
            if(in_array($line[0],$L)){
            }
          }
          if(count($line) == 3){
            if(in_array($line[0],$VS)){
            }
            if(in_array($line[0],$VT)){
            }
          }
          if(count($line) == 4){
            if(in_array($line[0],$VSS)){
            }
            if(in_array($line[0],$LSS)){
            }
          }
        }
      }
    }    
    if(!$header){
      exit(21);
    }
    exit(0);
  }
  exit(99);

?>