<?PHP
$RED = '\033[0;31m';
$GREEN = '\033[0;32m';  
$NC = '\033[0m';
if($argv[1] == "--help"){
    echo("Usage: test.php [test_dir] [options]\n");
}
#$folder = scandir($argv[1]);
$dirs = glob($argv[1].'/*/');
foreach ($dirs as $i) {    
    $folder = glob($i.'*.out');
    for($i = 0; $i < sizeof($folder); $i++){
        #system("echo \"${NC}\"$folder[$i]\"\"");
        $tests = $folder[$i];
        $length = strlen($tests) - 4;
        $src = substr($tests,0,$length).".src";
        $inp = substr($tests,0,$length).".in";
        $resval = 0;
        exec("python3 interpret.py --source=".$src." --input=".$inp." >interpret.out", $output, $resval);
        #echo($resval."\n");

        filesize("interpret.py");
        if(filesize("interpret.out") == 0){
            #echo("empty .out\n");
            if(filesize("interpret.out") == filesize($tests)){
                $len = strlen($tests)-4;
                $str = substr($tests, 0, $len).".rc";
                if(!strcmp(fgets(fopen($str, 'r')), $resval)){
                    #echo("RC okay\n");
                    system("echo \"${GREEN}\"$src\"\"");   
                    #system("echo \"${GREEN}PASS\"");
                }
                else{
                    system("echo \"${RED}\"$src\"\"");                
                    #system("echo \"${RED}FAIL\"");
                    exit(8);
                }
            }
            else{
                system("echo \"${RED}\"$src\"\"");
                #system("echo \"${RED}FAIL\"");
                exit(9);
            }

            #exit(3);
        }
        else{
            exec("diff interpret.out ".$tests,$output ,$result_code);
            #echo("res_code ".$result_code."\n");
            if(!$result_code){
                system("echo \"${GREEN}\"$src\"\"");   
                #system("echo \"${GREEN}PASS\"");
            }
            else{
                system("echo \"${RED}\"$src\"\"");
                #system("echo \"${RED}FAIL\"");
                exit(1);
            }    
        }
    }
}
exit(0);
?>