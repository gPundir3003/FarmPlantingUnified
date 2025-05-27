import 'package:flutter/material.dart';

import 'screens/home_page.dart';
import 'screens/map_page.dart';
import 'screens/task_page.dart';
import 'screens/add_task.dart';
import 'screens/settings_page.dart';
import 'screens/notifications_page.dart';
import 'screens/cropdata.dart';
import 'screens/calender_page.dart';
import 'screens/weather_page.dart';
import 'screens/mapping.dart';
import 'screens/login_page.dart';
import 'screens/signup_page.dart';

void main() {
  runApp(OrefoxApp());
}

class OrefoxApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Orefox Farm Planting App',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        primarySwatch: Colors.green,
        scaffoldBackgroundColor: const Color(0xFFF7F8F9),
        fontFamily: 'Roboto',
        appBarTheme: const AppBarTheme(
          backgroundColor: Colors.white,
          elevation: 0.5,
          iconTheme: IconThemeData(color: Colors.black),
          titleTextStyle: TextStyle(
            color: Colors.black,
            fontSize: 20,
            fontWeight: FontWeight.w600,
          ),
        ),
        textTheme: const TextTheme(
          bodyMedium: TextStyle(fontSize: 14, color: Colors.black87),
        ),
        elevatedButtonTheme: ElevatedButtonThemeData(
          style: ElevatedButton.styleFrom(
            backgroundColor: Colors.green,
            foregroundColor: Colors.white,
            padding: const EdgeInsets.symmetric(vertical: 16),
            shape: RoundedRectangleBorder(
              borderRadius: BorderRadius.circular(12),
            ),
          ),
        ),
      ),

      /// 👇 Start the app at the Login screen
      initialRoute: '/login',

      /// 👇 Define all named routes
      routes: {
        '/login': (ctx) => LoginScreen(),
        '/signup': (ctx) => SignUpScreen(),
        '/': (ctx) => HomePage(),
        '/map': (ctx) => MapPage(),
        '/mapping': (ctx) => MappingPage(),
        '/tasks': (ctx) => TaskPage(),
        '/add': (ctx) => AddTaskPage(),
        '/settings': (ctx) => SettingsPage(),
        '/notifications': (ctx) => NotificationsPage(),
        '/cropdata': (ctx) => CropDataPage(),
        '/calendar': (ctx) => CalendarPage(),
        '/weather': (ctx) => WeatherPage(),
      },
    );
  }
}
