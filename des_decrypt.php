<?php

require('des.php');
$content = file_get_contents('/tmp/my_des_cipher.txt');
$key = file_get_contents('/tmp/my_des_key.txt');

$des = new Des($key);
file_put_contents('/tmp/my_des_decrypt_result.txt', $des->decrypt($content));

?>