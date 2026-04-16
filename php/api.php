<?php
header("Access-Control-Allow-Origin: *");
header("Access-Control-Allow-Methods: POST, GET, OPTIONS");
header("Access-Control-Allow-Headers: Content-Type");
header("Content-Type: application/json");

// Gérer la requête OPTIONS (preflight)
if ($_SERVER["REQUEST_METHOD"] === "OPTIONS") {
    http_response_code(200);
    exit;
}

if (!isset($_FILES["file"])) {
    echo json_encode(["error" => "Aucun fichier reçu"]);
    exit;
}

$file = $_FILES["file"];
$extension = strtolower(pathinfo($file["name"], PATHINFO_EXTENSION));

if (!in_array($extension, ["pdf", "docx"])) {
    echo json_encode(["error" => "Format non supporté"]);
    exit;
}

$filename = uniqid() . "_" . basename($file["name"]);
$uploadPath = __DIR__ . "/../storage/uploads/" . $filename;

if (!move_uploaded_file($file["tmp_name"], $uploadPath)) {
    echo json_encode(["error" => "Erreur upload fichier"]);
    exit;
}

require_once __DIR__ . "/services/pythonservice.php";
$result = callPythonAPI($uploadPath, $filename);

echo json_encode($result);