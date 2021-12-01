import 'package:flutter/material.dart';
import 'package:paigham/screens/chatPage.dart';

class HomePage extends StatelessWidget {
  dynamic client_Socket;
  HomePage({this.client_Socket});
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: ChatPage(client_Socket: client_Socket),
      bottomNavigationBar: BottomNavigationBar(
        selectedItemColor: Colors.red,
        unselectedItemColor: Colors.grey.shade600,
        selectedLabelStyle: TextStyle(fontWeight: FontWeight.w600),
        unselectedLabelStyle: TextStyle(fontWeight: FontWeight.w600),
        type: BottomNavigationBarType.fixed,
        items: [
          BottomNavigationBarItem(
            icon: Icon(Icons.message),
            title: Text("Chats"),
          ),
          BottomNavigationBarItem(
            icon: Icon(Icons.money),
            title: Text("Transactions"),
          ),
          BottomNavigationBarItem(
            icon: Icon(Icons.account_box),
            title: Text("Profile"),
          ),
        ],
      ),
    );
  }
}
