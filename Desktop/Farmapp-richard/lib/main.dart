import 'package:flutter/material.dart';
import 'screens/home_page.dart';
import 'screens/map_page.dart';
import 'screens/mapping_page.dart'; // ✅ new import
import 'screens/task_page.dart';
import 'screens/settings_page.dart';
import 'screens/notifications_page.dart';
import 'screens/taskmanager.dart';

void main() {
  runApp(OrefoxApp());
}

class OrefoxApp extends StatefulWidget {
  @override
  State<OrefoxApp> createState() => _OrefoxAppState();
}

class _OrefoxAppState extends State<OrefoxApp> {
  bool _isDarkMode = false;

  void _toggleDarkMode(bool value) {
    setState(() {
      _isDarkMode = value;
    });
  }

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Orefox Farm Planting App',
      debugShowCheckedModeBanner: false,
      themeMode: _isDarkMode ? ThemeMode.dark : ThemeMode.light,
      theme: ThemeData(
        primarySwatch: Colors.green,
        scaffoldBackgroundColor: Color(0xFFF7F8F9),
        fontFamily: 'Roboto',
        appBarTheme: AppBarTheme(
          backgroundColor: Colors.white,
          elevation: 0.5,
          iconTheme: IconThemeData(color: Colors.black),
          titleTextStyle: TextStyle(
            color: Colors.black,
            fontSize: 20,
            fontWeight: FontWeight.w600,
          ),
        ),
        textTheme: TextTheme(
          bodyMedium: TextStyle(fontSize: 14, color: Colors.black87),
        ),
        elevatedButtonTheme: ElevatedButtonThemeData(
          style: ElevatedButton.styleFrom(
            backgroundColor: Colors.green[600],
            foregroundColor: Colors.white,
            padding: EdgeInsets.symmetric(vertical: 16),
            shape: RoundedRectangleBorder(
              borderRadius: BorderRadius.circular(12),
            ),
          ),
        ),
      ),
      darkTheme: ThemeData.dark(),
      initialRoute: '/',
      onGenerateRoute: (settings) {
        switch (settings.name) {
          case '/':
            return MaterialPageRoute(builder: (_) => HomePage());
          case '/map':
            return MaterialPageRoute(builder: (_) => MapPage());
          case '/mapping': // ✅ new route
            return MaterialPageRoute(builder: (_) => MappingPage());
          case '/tasks':
            return MaterialPageRoute(builder: (_) => TaskPage());
          case '/notifications':
            return MaterialPageRoute(builder: (_) => NotificationsPage());
          case '/settings':
            return MaterialPageRoute(
              builder: (_) => SettingsPage(
                isDarkMode: _isDarkMode,
                onToggleDarkMode: _toggleDarkMode,
              ),
            );
          default:
            return MaterialPageRoute(
              builder: (_) => Scaffold(
                body: Center(child: Text('Page not found')),
              ),
            );
        }
      },
    );
  }
}
