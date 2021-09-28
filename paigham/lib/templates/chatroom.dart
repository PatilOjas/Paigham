import 'package:flutter/material.dart';

class ChatRoom extends StatefulWidget {
  const ChatRoom({Key? key}) : super(key: key);

  @override
  _ChatRoomState createState() => _ChatRoomState();
}

class _ChatRoomState extends State<ChatRoom> {
  @override
  Widget build(BuildContext context) {
    return SafeArea(
      child: Scaffold(
        appBar: AppBar(
          title: Row(
            children: [
              TextButton(
                onPressed: () => Navigator.pushNamed(context, 'displayprofilepicture/'),
                child: CircleAvatar(
                  backgroundImage: NetworkImage(
                      'https://images.unsplash.com/photo-1632252387383-2e53ff6bfd62?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=387&q=80'),
                ),
              ),
              SizedBox(
                width: 5,
              ),
              Text("Paigham"),
            ],
          ),
          actions: [
            TextButton(
              onPressed: () {},
              child: Icon(Icons.phone),
            ),
            TextButton(
              onPressed: () {},
              child: Icon(Icons.videocam),
            ),
          ],
        ),
      ),
    );
  }
}
