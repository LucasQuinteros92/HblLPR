<?php
    if ( $_POST ) {
        foreach ( $_POST as $key => $value ) {
            echo "llave: ".$key."- Valor:".$value."<br />";
            $fp = fopen('lidn.txt', 'w');
            fwrite($fp, 'Cats chase mice');
            fclose($fp);
        }
    }
?>  