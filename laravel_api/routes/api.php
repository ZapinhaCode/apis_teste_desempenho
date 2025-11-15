<?php

use Illuminate\Support\Facades\Route;

// Health API Check Route
Route::get('/', function () {
    return ['message' => 'Welcome to the Laravel API'];
});
