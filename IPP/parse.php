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
    
    exit(0);
  }
  exit(99);

?>