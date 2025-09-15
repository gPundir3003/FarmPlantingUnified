import 'package:flutter/material.dart';
import 'edit_profile_page.dart';

class SettingsPage extends StatefulWidget {
  final bool isDarkMode;
  final Function(bool) onToggleDarkMode;

  const SettingsPage({
    super.key,
    required this.isDarkMode,
    required this.onToggleDarkMode,
  });

  @override
  State<SettingsPage> createState() => _SettingsPageState();
}

class _SettingsPageState extends State<SettingsPage> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Theme.of(context).scaffoldBackgroundColor,
      appBar: AppBar(
        backgroundColor: Colors.green[700],
        title: const Text('Profile'),
        centerTitle: true,
        elevation: 0,
      ),
      body: ListView(
        children: [
          Container(
            color: Colors.green[700],
            padding: const EdgeInsets.symmetric(vertical: 24),
            child: Column(
              children: [
                const CircleAvatar(
                  radius: 50,
                  backgroundColor: Colors.white,
                  child: Icon(Icons.person, size: 60, color: Colors.black),
                ),
                const SizedBox(height: 12),
                ElevatedButton(
                  onPressed: () {
                    Navigator.push(
                      context,
                      MaterialPageRoute(builder: (_) => const EditProfilePage()),
                    );
                  },
                  child: const Text("Edit Profile"),
                  style: ElevatedButton.styleFrom(
                    backgroundColor: Colors.black,
                    foregroundColor: Colors.white,
                    padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
                    shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(12),
                    ),
                  ),
                ),
              ],
            ),
          ),

          _buildSection("Mimi Headline", [
            _buildListItem(context, "Popular", icon: Icons.trending_up),
            _buildListItem(context, "Trending", icon: Icons.swap_horiz),
            _buildListItem(context, "Today", icon: Icons.calendar_today),
          ]),

          _buildSection("Content", [
            _buildListItem(context, "Favourite", icon: Icons.favorite_border),
            _buildListItem(context, "Download", icon: Icons.download),
          ]),

          _buildSection("Preferences", [
            _buildListItem(context, "Language", icon: Icons.language),
            SwitchListTile(
              title: const Text("Darkmode"),
              value: widget.isDarkMode,
              secondary: const Icon(Icons.dark_mode),
              onChanged: widget.onToggleDarkMode,
            ),
            _buildListItem(context, "Only Download via Wifi", icon: Icons.wifi),
          ]),

          const SizedBox(height: 16),
          Padding(
            padding: const EdgeInsets.symmetric(horizontal: 100.0),
            child: ElevatedButton(
              onPressed: () {
                ScaffoldMessenger.of(context).showSnackBar(
                  const SnackBar(content: Text("Logging out...")),
                );
              },
              child: const Text("Log out"),
              style: ElevatedButton.styleFrom(
                backgroundColor: Colors.red[400],
              ),
            ),
          ),
          const SizedBox(height: 16),
          Padding(
            padding: const EdgeInsets.symmetric(horizontal: 40.0),
            child: ElevatedButton(
              onPressed: () {
                ScaffoldMessenger.of(context).showSnackBar(
                  const SnackBar(content: Text("Changes saved!")),
                );
              },
              child: const Text("Save"),
              style: ElevatedButton.styleFrom(
                backgroundColor: Colors.green[700],
              ),
            ),
          ),
          const SizedBox(height: 32),
        ],
      ),
    );
  }

  Widget _buildSection(String title, List<Widget> children) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Padding(
          padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
          child: Text(
            title,
            style: const TextStyle(fontWeight: FontWeight.bold),
          ),
        ),
        ...children,
      ],
    );
  }

  Widget _buildListItem(BuildContext context, String text, {IconData? icon}) {
    return ListTile(
      leading: icon != null ? Icon(icon) : null,
      title: Text(text),
      trailing: const Icon(Icons.arrow_forward_ios, size: 16),
      onTap: () {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text("Tapped on $text")),
        );
      },
    );
  }
}
