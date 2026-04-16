<?php
define("PYTHON_API_URL", "http://127.0.0.1:8000/convert");
define("UPLOAD_DIR", __DIR__ . "/../../storage/uploads/");
define("OUTPUT_DIR", __DIR__ . "/../../storage/outputs/");
define("MAX_FILE_SIZE", 10 * 1024 * 1024); // 10MB
define("ALLOWED_EXTENSIONS", ["pdf", "docx"]);