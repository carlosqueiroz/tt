<?php



// Array
$data = array(
    "gantryAngle"  => 0,
    "collAngle" => 0,
    "couchAngle" => 0,
    "SAD" => 100,
   
);

// Executar Python Script e enviar dados JSON
$result = shell_exec('python coordinatespt.py ' . escapeshellarg(json_encode($data)));

// Decodificar o Resultado 
$resultData = json_decode($result, true);

// Plotar na Tela o Resultado
print_r($resultData);
