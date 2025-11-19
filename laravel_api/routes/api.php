<?php

use Illuminate\Support\Facades\Route;
use App\Http\Controllers\UserController;

// Health API Check Route
Route::get('/health', function () {
    return response()->json(['status' => 'Laravel API is running']);
});

// User Routes All
Route::resource('users', UserController::class)->only([
    'index', 'store', 'show', 'update', 'destroy'
]);

// Gateway
Route::get('/whoami', function () {
    return [
        "api" => "laravel",
        "instance" => gethostname()
    ];
});