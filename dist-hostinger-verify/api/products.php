<?php
declare(strict_types=1);

// Ensure CORS allows frontend to fetch API regardless of domain setup
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: GET, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type, Authorization');

if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    http_response_code(200);
    exit;
}

require_once __DIR__ . '/db.php';

if (($_SERVER['REQUEST_METHOD'] ?? 'GET') !== 'GET') {
    json_response(405, [
        'success' => false,
        'error' => 'Method not allowed. Use GET.',
    ]);
}

$limit = isset($_GET['limit']) ? (int)$_GET['limit'] : 200;
$limit = max(1, min($limit, 500));

$connection = db();
$result = $connection->query(
    "SELECT id, name, category, price, description, image_path, stock
     FROM products
     ORDER BY id ASC
     LIMIT {$limit}"
);

if (!$result) {
    json_response(500, [
        'success' => false,
        'error' => 'Unable to fetch products.',
        'details' => $connection->error,
    ]);
}

// Dynamically determine the base URL so image paths always resolve correctly on Hostinger
$scheme = (isset($_SERVER['HTTPS']) && $_SERVER['HTTPS'] === 'on') ? 'https' : 'http';
$host = $_SERVER['HTTP_HOST'] ?? 'localhost';
$base_path = rtrim(dirname(dirname($_SERVER['SCRIPT_NAME'])), '/\\');
$base_url = $scheme . '://' . $host . $base_path . '/';

$rows = [];
while ($row = $result->fetch_assoc()) {
    // Convert relative paths to absolute URLs to prevent broken images
    if (!empty($row['image_path']) && !preg_match('/^http/', $row['image_path'])) {
        $row['image_path'] = $base_url . ltrim($row['image_path'], '/');
    }
    $rows[] = $row;
}

json_response(200, [
    'success' => true,
    'count' => count($rows),
    'data' => $rows,
]);
