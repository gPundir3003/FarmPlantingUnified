import 'package:flutter/material.dart';
import 'package:flutter_map/flutter_map.dart';
import 'package:latlong2/latlong.dart';
import 'dart:math';

class MapPage extends StatefulWidget {
  @override
  _MapPageState createState() => _MapPageState();
}

class _MapPageState extends State<MapPage> {
  final MapController _mapController = MapController();
  final List<Marker> _cropMarkers = [];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      drawer: Drawer(
        child: ListView(
          padding: EdgeInsets.zero,
          children: [
            DrawerHeader(
              decoration: BoxDecoration(color: Colors.green[700]),
              child: Center(
                child: Image.asset('assets/logo.png', height: 60),
              ),
            ),
            ListTile(title: Text("Dashboard"), onTap: () => Navigator.pushNamed(context, "/")),
            ListTile(title: Text("Account Settings"), onTap: () => Navigator.pushNamed(context, "/settings")),
            ListTile(title: Text("Layout Planning"), onTap: () => Navigator.pushNamed(context, "/map")),
            ListTile(title: Text("Mapping"), onTap: () {
              Navigator.pop(context);
              Navigator.pushNamed(context, "/mapping");
            }),
            ListTile(title: Text("Task Manager"), onTap: () => Navigator.pushNamed(context, "/tasks")),
            ListTile(title: Text("Data Visualized"), onTap: () => Navigator.pushNamed(context, "/data")),
            ListTile(title: Text("Weather"), onTap: () => Navigator.pushNamed(context, "/weather")),
            ListTile(title: Text("Calendar"), onTap: () => Navigator.pushNamed(context, "/calendar")),
            ListTile(title: Text("Crop Database"), onTap: () => Navigator.pushNamed(context, "/database")),
          ],
        ),
      ),
      backgroundColor: const Color(0xFFF7F8F9),
      body: SafeArea(
        child: Column(
          children: [
            Padding(
              padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
              child: Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  Builder(
                    builder: (context) => IconButton(
                      icon: const Icon(Icons.menu, size: 28),
                      onPressed: () => Scaffold.of(context).openDrawer(),
                    ),
                  ),
                  const Row(
                    children: [
                      Text("Layout Planning", style: TextStyle(fontSize: 22, fontWeight: FontWeight.bold)),
                      SizedBox(width: 8),
                      Icon(Icons.add, size: 28),
                    ],
                  ),
                  const CircleAvatar(
                    backgroundColor: Colors.grey,
                    radius: 18,
                    child: Icon(Icons.person, color: Colors.white, size: 20),
                  ),
                ],
              ),
            ),
            const Padding(
              padding: EdgeInsets.symmetric(horizontal: 16),
              child: Align(
                alignment: Alignment.centerLeft,
                child: Text("My Area", style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold)),
              ),
            ),
            const SizedBox(height: 8),
            Stack(
              children: [
                Container(
                  margin: const EdgeInsets.symmetric(horizontal: 16),
                  height: 200,
                  width: double.infinity,
                  child: DragTarget<String>(
                    onAcceptWithDetails: (details) {
                      final localPos = details.offset;
                      final box = context.findRenderObject() as RenderBox;
                      final localOffset = box.globalToLocal(localPos);
                      final latlng = _mapController.pointToLatLng(
                        Point<double>(localOffset.dx, localOffset.dy),
                      );

                      setState(() {
                        if (["grid", "circle", "square"].contains(details.data)) {
                          print("Tool dropped: ${details.data}");
                          // Optionally add markers for tools too
                        } else {
                          _cropMarkers.add(
                            Marker(
                              width: 40,
                              height: 40,
                              point: latlng,
                              child: Image.asset("assets/crops/${details.data}.png", height: 40),
                            ),
                          );
                        }
                      });
                    },
                    builder: (context, candidateData, rejectedData) {
                      return FlutterMap(
                        mapController: _mapController,
                        options: MapOptions(
                          center: LatLng(-27.4698, 153.0251),
                          zoom: 16.0,
                          onTap: (_, __) {
                            _mapController.move(_mapController.center, _mapController.zoom + 1);
                          },
                        ),
                        children: [
                          TileLayer(
                            urlTemplate: 'https://tile.openstreetmap.org/{z}/{x}/{y}.png',
                            userAgentPackageName: 'com.example.farmapp',
                          ),
                          MarkerLayer(markers: _cropMarkers),
                        ],
                      );
                    },
                  ),
                ),
              ],
            ),
            const SizedBox(height: 16),
            Expanded(
              child: SingleChildScrollView(
                padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
                child: Container(
                  padding: const EdgeInsets.all(16),
                  decoration: BoxDecoration(
                    color: Colors.grey[100],
                    borderRadius: BorderRadius.circular(16),
                  ),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      const Text("My Tools", style: TextStyle(fontSize: 16, fontWeight: FontWeight.w600)),
                      const SizedBox(height: 12),
                      Row(
                        mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                        children: [
                          _draggableTool(Icons.grid_on, "grid"),
                          _draggableTool(Icons.circle_outlined, "circle"),
                          _draggableTool(Icons.crop_square, "square"),
                        ],
                      ),
                      const SizedBox(height: 24),
                      const Text("My Crops", style: TextStyle(fontSize: 16, fontWeight: FontWeight.w600)),
                      const SizedBox(height: 12),
                      Row(
                        mainAxisAlignment: MainAxisAlignment.spaceAround,
                        children: [
                          _draggableCrop("orange"),
                          _draggableCrop("wheat"),
                          _draggableCrop("leafy"),
                          _draggableCrop("tree"),
                          _draggableCrop("lettuce"),
                        ],
                      ),
                      const SizedBox(height: 16),
                      const TextField(
                        decoration: InputDecoration(
                          labelText: "Name",
                          border: OutlineInputBorder(),
                        ),
                      ),
                      const SizedBox(height: 12),
                      const TextField(
                        decoration: InputDecoration(
                          labelText: "Spacing",
                          border: OutlineInputBorder(),
                        ),
                      ),
                      const SizedBox(height: 12),
                      TextField(
                        decoration: InputDecoration(
                          labelText: "Planting Date",
                          border: const OutlineInputBorder(),
                          suffixIcon: Icon(Icons.calendar_today),
                        ),
                      ),
                    ],
                  ),
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _draggableCrop(String name) {
    return Draggable<String>(
      data: name,
      feedback: Image.asset("assets/crops/$name.png", height: 40),
      childWhenDragging: Opacity(
        opacity: 0.3,
        child: Image.asset("assets/crops/$name.png", height: 40),
      ),
      child: Image.asset("assets/crops/$name.png", height: 40),
    );
  }

  Widget _draggableTool(IconData icon, String label) {
    return Draggable<String>(
      data: label,
      feedback: Icon(icon, size: 40),
      childWhenDragging: Opacity(
        opacity: 0.3,
        child: Icon(icon, size: 40),
      ),
      child: Icon(icon, size: 40),
    );
  }
}
