import 'package:flutter/material.dart';

import 'package:paigham/templates/chatroom.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({Key? key}) : super(key: key);

  // This widget is the root of your application.
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      home: Scaffold(
        appBar: AppBar(
          title: Text("Paigham"),
          backgroundColor: Colors.green,
          actions: [
            Row(mainAxisAlignment: MainAxisAlignment.end, children: [
              TextButton(
                onPressed: () {
                  print("Setting opened");
                },
                child: Icon(
                  Icons.settings,
                  color: Colors.white,
                ),
              ),
            ]),
          ],
          // bottom: TabBar(
          //   controller: TabController(length: 2, vsync: TickerProvider ),
          //   tabs: [
          //     Text("Chat"),
          //     Text("Payments"),
          //   ],
          // ),
        ),
        body: Column(
          children: [],
        ),
      ),
      routes: {
        'chatrrom/': (context) => ChatRoom(),
      },
    );
  }
}
