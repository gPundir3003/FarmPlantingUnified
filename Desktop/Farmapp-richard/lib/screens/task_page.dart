import 'package:flutter/material.dart';

class TaskPage extends StatelessWidget {
  final List<String> tasks = [
    "Water tomato bed",
    "Fertilize orchard",
    "Plant new saplings",
  ];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('My Tasks')),
      body: ListView.builder(
        padding: const EdgeInsets.all(16.0),
        itemCount: tasks.length,
        itemBuilder: (context, index) {
          return ListTile(
            leading: Icon(Icons.task),
            title: Text(tasks[index]),
          );
        },
      ),
    );
  }
}
