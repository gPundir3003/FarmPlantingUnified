import 'package:flutter/material.dart';
import 'auth_service.dart';

class AuthPage extends StatefulWidget {
  const AuthPage({Key? key}) : super(key: key);

  @override
  State<AuthPage> createState() => _AuthPageState();
}

class _AuthPageState extends State<AuthPage> {
  final _emailController = TextEditingController();
  final _usernameController = TextEditingController();
  final _passwordController = TextEditingController();
  final AuthService _authService = AuthService();

  String _message = '';

  void _registerAndLogin() async {
    final email = _emailController.text.trim();
    final username = _usernameController.text.trim();
    final password = _passwordController.text.trim();

    setState(() {
      _message = '⏳ Registering...';
    });

    final registered = await _authService.register(email, username, password);
    if (registered) {
      setState(() {
        _message = '✅ Registered! Logging in...';
      });

      final loggedIn = await _authService.login(email, password);
      if (loggedIn) {
        setState(() {
          _message = '✅ Logged in successfully!';
        });
      } else {
        setState(() {
          _message = '❌ Login failed';
        });
      }
    } else {
      setState(() {
        _message = '❌ Registration failed';
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Auth Test')),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          children: [
            TextField(controller: _emailController, decoration: InputDecoration(labelText: 'Email')),
            TextField(controller: _usernameController, decoration: InputDecoration(labelText: 'Username')),
            TextField(controller: _passwordController, decoration: InputDecoration(labelText: 'Password'), obscureText: true),
            SizedBox(height: 20),
            ElevatedButton(
              onPressed: _registerAndLogin,
              child: Text('Register & Login'),
            ),
            SizedBox(height: 20),
            Text(_message),
          ],
        ),
      ),
    );
  }
}
