<?PHP
$RED = '\033[0;31m';
$GREEN = '\033[0;32m';  
$NC = '\033[0m';
if($argv[1] == "--help"){
    echo("Usage: test.php [test_dir] [options]");
}
#$folder = scandir($argv[1]);
$dirs = glob($argv[1].'/*/');
foreach ($dirs as $i) {    
    $folder = glob($i.'/*.out');
    for($i = 0; $i < sizeof($folder); $i++){
        system("echo \"${NC}\"$folder[$i]\"\"");
        $tests = $folder[$i];
        $length = strlen($tests) - 4;
        $src = substr($tests,0,$length).".src";
        $resval = 0;
        exec("php8.1 parse.php <".$src." >parse.out", $output, $resval);
        #echo($resval."\n");

        filesize("parse.php");
        if(filesize("parse.out") == 0){
            #echo("empty .out\n");
            if(filesize("parse.out") == filesize($tests)){
                $len = strlen($tests)-4;
                $str = substr($tests, 0, $len).".rc";
                if(!strcmp(fgets(fopen($str, 'r')), $resval)){
                    #echo("RC okay\n");
                    #system("echo \"${GREEN}PASS\"");
                }
                else{                
                    system("echo \"${RED}FAIL\"");
                }
            }
            else{
                system("echo \"${RED}FAIL\"");
            }

            #exit(3);
        }
        else{
            exec("java -jar jexamxml/jexamxml.jar parse.out ".$tests." Testy\options",$output ,$result_code);
            #echo("res_code ".$result_code."\n");
            if(!$result_code){
                #system("echo \"${GREEN}PASS\"");
            }
            else{
                system("echo \"${RED}FAIL\"");
            }    
        }
    }
}
exit(0);
?>