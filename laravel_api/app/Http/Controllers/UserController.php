<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use App\Models\Users;
use Illuminate\Support\Facades\Hash;
use Illuminate\Validation\Rule;
use Illuminate\Support\Facades\DB;

class UserController extends Controller
{
    public function index() {
        try {
            return response()->json(Users::all(), 200);
        } catch (\Exception $e) {
            return response()->json(["error" => $e->errors()], 500);
        }
    }

    public function store(Request $request) {
        try {
            DB::beginTransaction();

            $validated = $request->validate([
                'name' => 'required|string|max:255|unique:users,name',
                'email' => 'required|string|email|max:120|unique:users,email',
                'username' => 'required|string|max:80|unique:users,username',
                'password' => 'required|string|min:6',
            ]);

            $plain_password = $validated['password'];
            foreach (Users::all() as $user) {
                if (Hash::check($plain_password, $user->password)) {
                    return response()->json(["error" => "Password already exists"], 409);
                }
            }

            $validated['password'] = Hash::make($plain_password);
            $user = Users::create($validated);
            DB::commit();
            return response()->json($user->toArray(), 201);
        } catch (\Illuminate\Validation\ValidationException $e) {
            DB::rollBack();
            return response()->json(["error" => $e->errors()], 422);
        }
    }

    public function show(Users $user) {
        try {
            return response()->json($user->toArray(), 200);
        } catch (\Exception $e) {
            return response()->json(["error" => $e->errors()], 404);
        }
    }

    public function update(Request $request, Users $user) {
        try {
            DB::beginTransaction();
            $validated = $request->validate([
                'name' => ['sometimes', 'string', 'max:255', Rule::unique('users', 'name')->ignore($user->id)],
                'email' => ['sometimes', 'string', 'email', 'max:120', Rule::unique('users', 'email')->ignore($user->id)],
                'username' => ['sometimes', 'string', 'max:80', Rule::unique('users', 'username')->ignore($user->id)],
                'password' => 'sometimes|string|min:6',
            ]);
    
            if (isset($validated['password'])) {
                $new_plain = $validated['password'];
                
                foreach (Users::all() as $u) {
                    if ($u->id !== $user->id && Hash::check($new_plain, $u->password)) {
                        return response()->json(["error" => "Password already exists"], 409);
                    }
                }
    
                $validated['password'] = Hash::make($new_plain);
            }
    
            $user->update($validated);   
            DB::commit();
            return response()->json($user->toArray(), 200);
        } catch (\Illuminate\Validation\ValidationException $e) {
            DB::rollBack();
            return response()->json(["error" => $e->errors()], 422);
        }
    }

    public function destroy(Users $user){
        try {
            DB::beginTransaction();
            $user->delete();
            DB::commit();
            return response()->json(["message" => "User deleted successfully"], 200);
        } catch (\Exception $e) {
            DB::rollBack();
            return response()->json(["error" => "Failed to delete user"], 500);
        }
    }
}
