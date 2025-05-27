// login_page.dart
import 'package:flutter/material.dart';

class LoginScreen extends StatelessWidget {
  const LoginScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: SingleChildScrollView(
        child: Column(
          children: [
            Stack(
              children: [
                Image.asset('assets/farm.jpg'),
                Positioned(
                  bottom: 16,
                  left: 16,
                  child: Text(
                    '', // Remove title text over image
                    style: TextStyle(
                      fontSize: 28,
                      fontWeight: FontWeight.bold,
                      color: Colors.white,
                      shadows: [
                        Shadow(blurRadius: 10, color: Colors.black45, offset: Offset(2, 2)),
                      ],
                    ),
                  ),
                ),
              ],
            ),
            Padding(
              padding: const EdgeInsets.all(20.0),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.stretch,
                children: [
              
                  const Text('Get Started', style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold)),
                  const SizedBox(height: 16),
                  const TextField(decoration: InputDecoration(hintText: 'Email Address')),
                  const SizedBox(height: 16),
                  const TextField(
                    obscureText: true,
                    decoration: InputDecoration(hintText: 'Password'),
                  ),
                  const SizedBox(height: 8),
                  const Align(
                    alignment: Alignment.centerRight,
                    child: Text('Forgot password?', style: TextStyle(color: Colors.blue)),
                  ),
                  const SizedBox(height: 16),
                  ElevatedButton(
                    onPressed: () {
                      // Navigate to home page after login
                      print("Login button pressed");
                      Navigator.pushReplacementNamed(context, '/');
                    },
                    style: ElevatedButton.styleFrom(backgroundColor: Colors.green),
                    child: const Text('Login'),
                  ),
                  const SizedBox(height: 10),
                  const Center(child: Text("Not a member? Register now", style: TextStyle(color: Colors.blue))),
                  const SizedBox(height: 20),
                  const Center(child: Text('Or continue with')),
                  const SizedBox(height: 10),
                  const Row(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      CircleAvatar(backgroundColor: Colors.red, child: Icon(Icons.g_mobiledata, color: Colors.white)),
                      SizedBox(width: 16),
                      CircleAvatar(backgroundColor: Colors.black, child: Icon(Icons.apple, color: Colors.white)),
                      SizedBox(width: 16),
                      CircleAvatar(backgroundColor: Colors.blue, child: Icon(Icons.facebook, color: Colors.white)),
                    ],
                  )
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }
}

class SignUpScreen extends StatelessWidget {
  const SignUpScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Sign Up'), backgroundColor: Colors.white, foregroundColor: Colors.black),
      body: Padding(
        padding: const EdgeInsets.all(20.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            const Text('Sign Up', style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold)),
            const SizedBox(height: 16),
            const TextField(decoration: InputDecoration(hintText: 'Add name')),
            const SizedBox(height: 16),
            const TextField(decoration: InputDecoration(hintText: 'name@email.com')),
            const SizedBox(height: 16),
            const TextField(
              obscureText: true,
              decoration: InputDecoration(hintText: 'Create a password', suffixIcon: Icon(Icons.visibility_off)),
            ),
            const SizedBox(height: 16),
            const TextField(
              obscureText: true,
              decoration: InputDecoration(hintText: 'Confirm password', suffixIcon: Icon(Icons.visibility_off)),
            ),
            const SizedBox(height: 24),
            ElevatedButton(
              onPressed: () {
                // TODO: Implement sign-up functionality
                print("Sign Up button pressed");
              },
              style: ElevatedButton.styleFrom(backgroundColor: Colors.green),
              child: const Text('Login'),
            )
          ],
        ),
      ),
    );
  }
}
