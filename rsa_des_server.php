<?php

function step1() {
    //$client_e = strval($_POST['e']);
    //$client_n = strval($_POST['n']);
    exec('python -c "print __import__(\'json\').dumps([str(x) for x in __import__(\'rsa\').gen_key_pair()])"', $output);
    $key_pair = json_decode($output[0]);
    $server_d = $key_pair[0];
    $server_e = $key_pair[1];
    $server_n = $key_pair[2];
    file_put_contents('/tmp/my_rsa_d.txt', $server_d);
    file_put_contents('/tmp/my_rsa_n.txt', $server_n);
    echo json_encode([
        'e' => $server_e,
        'n' => $server_n,
    ]);
}

function step2() {
    $d = file_get_contents('/tmp/my_rsa_d.txt');
    $n = file_get_contents('/tmp/my_rsa_n.txt');
    $cipher = strval($_POST['des_key']);
    file_put_contents('/tmp/my_rsa_cipher.txt', $cipher);
    exec('python -c "f=open(\'/tmp/my_des_key.txt\',\'wb\');f.write(__import__(\'rsa\').decrypt(open(\'/tmp/my_rsa_cipher.txt\', \'rb\').read(), ' . $d . ', ' . $n . '));f.close()"');
    echo 'success';
}


function step3() {
    $cipher = strval($_POST['cipher']);
    require('des.php');
    $des_key = file_get_contents('/tmp/my_des_key.txt');
    $des = new Des($des_key);
    $content = $des->decrypt($cipher);
    $response_num = intval($content)+1;
    $response = strval($response_num);
    echo $des->encrypt($response);
}

switch($_GET['step']) {
    case 1:
        step1();
        break;
    case 2:
        step2();
        break;
    case 3:
        step3();
        break;
}

?>