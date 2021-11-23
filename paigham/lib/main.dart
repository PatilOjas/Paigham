import 'package:flutter/material.dart';

import 'package:paigham/templates/chatroom.dart';
import 'package:paigham/screens/homePage.dart';
import 'package:paigham/screens/loginMain.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({Key? key}) : super(key: key);
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Flutter Demo',
      theme: ThemeData(
        primarySwatch: Colors.blue,
      ),
      debugShowCheckedModeBanner: false,
      // home: HomePage(),
      home: LoginMain(),
    );
  }
}


// class MyApp extends StatelessWidget {
//   const MyApp({Key? key}) : super(key: key);

//   // This widget is the root of your application.
//   @override
//   Widget build(BuildContext context) {
//     return MaterialApp(
//       debugShowCheckedModeBanner: false,
//       home: Scaffold(
//         appBar: AppBar(
//           title: Text(
//             'Paigham',
//              style: TextStyle(
//                fontSize: 40.0,
//                fontFamily: "Samaran"
//                ),
//             ),
//           backgroundColor: Colors.blue[900],
        
//           actions: [
//             Row(mainAxisAlignment: MainAxisAlignment.end, children: [
//               TextButton(
//                 onPressed: () {
//                   print("Setting opened");
//                 },
//                 child: Icon(
//                   Icons.settings,
//                   color: Colors.white,
//                 ),
//               ),
//             ]),
//           ],
//           // bottom: TabBar(
//           //   controller: TabController(length: 2, vsync: TickerProvider ),
//           //   tabs: [
//           //     Text("Chat"),
//           //     Text("Payments"),
//           //   ],
//           // ),
//         ),
//         body: Container(
//           child: Center(child: Text("Chat")),
//       ),
//       bottomNavigationBar: BottomNavigationBar(
//         selectedItemColor: Colors.blue,
//         unselectedItemColor: Colors.grey.shade600,
//         selectedLabelStyle: TextStyle(fontWeight: FontWeight.w600),
//         unselectedLabelStyle: TextStyle(fontWeight: FontWeight.w600),
//         type: BottomNavigationBarType.fixed,
//         items: [
//           BottomNavigationBarItem(
//             icon: Icon(Icons.message),
//             title: Text("Chats"),
//           ),
//           BottomNavigationBarItem(
//             icon: Icon(Icons.group_work),
//             title: Text("Channels"),
//           ),
//           BottomNavigationBarItem(
//             icon: Icon(Icons.account_box),
//             title: Text("Profile"),
//           ),
//         ],
//       ),
//       ),
//       routes: {
//         'chatrrom/': (context) => ChatRoom(),
//       },
//     );
//   }
// }
