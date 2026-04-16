<?php
function callPythonAPI($filePath, $filename) {
    
    // URL de l'API Python
    $pythonUrl = "http://127.0.0.1:8000/convert";

    // Vérifier si le fichier existe
    if (!file_exists($filePath)) {
        return ["error" => "Fichier introuvable : " . $filePath];
    }

    // Vérifier si curl est disponible
    if (!function_exists('curl_init')) {
        return ["error" => "curl n'est pas installé sur ce PHP"];
    }

    $curl = curl_init();
    curl_setopt_array($curl, [
        CURLOPT_URL            => $pythonUrl,
        CURLOPT_POST           => true,
        CURLOPT_RETURNTRANSFER => true,
        CURLOPT_TIMEOUT        => 120,
        CURLOPT_POSTFIELDS     => [
            "file" => new CURLFile(
                $filePath,
                mime_content_type($filePath),
                basename($filename)
            )
        ]
    ]);

    $response = curl_exec($curl);
    $httpCode = curl_getinfo($curl, CURLINFO_HTTP_CODE);
    $curlError = curl_error($curl);
    curl_close($curl);

    // Erreur curl
    if ($curlError) {
        return ["error" => "Connexion impossible : " . $curlError];
    }

    // Erreur HTTP
    if ($httpCode !== 200) {
        return ["error" => "Erreur Python HTTP : " . $httpCode . " - " . $response];
    }

    // Décoder la réponse
    $data = json_decode($response, true);

    if (!$data) {
        return ["error" => "Réponse Python invalide : " . $response];
    }

    if (isset($data["error"])) {
        return ["error" => $data["error"]];
    }

    // Construire l'URL de téléchargement
    $outputFilename = $data["output_filename"];
    $data["download_url"] = "http://localhost:3000/storage/output/" . $outputFilename;

    return $data;
}