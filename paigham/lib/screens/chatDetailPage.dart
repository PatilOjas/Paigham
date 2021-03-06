import 'package:flutter/material.dart';
import 'package:paigham/main.dart';
import 'package:paigham/models/chatMessageModel.dart';
import 'dart:io';

class ChatDetailPage extends StatefulWidget {
  dynamic client_Socket;
  ChatDetailPage({this.client_Socket});
  @override
  _ChatDetailPageState createState() => _ChatDetailPageState(client_Socket: client_Socket);
}

class _ChatDetailPageState extends State<ChatDetailPage> {
  TextEditingController message = TextEditingController();
  // TextEditingController message = TextEditingController();

  // late Socket client_Socket;
  // void getSocket() async {
  //   client_Socket = await Socket.connect("192.168.1.201", 4444);
  //   client_Socket.write("""{
  //                       'name': 'Ojas',
  //                       'mobNo': '9619542526',
  //                     }"""
  //       .toString());
  // }

  List<ChatMessage> messages = [
    ChatMessage(messageContent: "Hello, Will", messageType: "receiver"),
    ChatMessage(messageContent: "How have you been?", messageType: "receiver"),
    ChatMessage(
        messageContent: "Hey Kriss, I am doing fine dude. wbu?",
        messageType: "sender"),
    ChatMessage(messageContent: "ehhhh, doing OK.", messageType: "receiver"),
    ChatMessage(
        messageContent: "Is there any thing wrong?", messageType: "sender"),
  ];

  dynamic client_Socket;
  _ChatDetailPageState({required this.client_Socket});
  // @override
  // void initState() {
  //   super.initState();
  //   getSocket();
  // }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        elevation: 0,
        automaticallyImplyLeading: false,
        backgroundColor: Colors.white,
        flexibleSpace: SafeArea(
          child: Container(
            padding: EdgeInsets.only(right: 16),
            child: Row(
              children: <Widget>[
                IconButton(
                  onPressed: () {
                    Navigator.pop(context);
                  },
                  icon: Icon(
                    Icons.arrow_back,
                    color: Colors.black,
                  ),
                ),
                SizedBox(
                  width: 2,
                ),
                CircleAvatar(
                  backgroundImage: NetworkImage(
                      "https://randomuser.me/api/portraits/men/5.jpg"),
                  maxRadius: 20,
                ),
                SizedBox(
                  width: 12,
                ),
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: <Widget>[
                      Text(
                        "Kriss Benwat",
                        style: TextStyle(
                            fontSize: 16, fontWeight: FontWeight.w600),
                      ),
                      SizedBox(
                        height: 6,
                      ),
                      Text(
                        "Online",
                        style: TextStyle(
                            color: Colors.grey.shade600, fontSize: 13),
                      ),
                    ],
                  ),
                ),
                SizedBox(
                  width: 15,
                ),
                Container(
                  height: 50.0,
                  width: 50.0,
                  child: FittedBox(
                    child: FloatingActionButton(
                      backgroundColor: Colors.white,
                      onPressed: () {
                        print("print Dictionaries");
                      },
                      child: Icon(
                        Icons.call_rounded,
                        color: Colors.blue[800],
                        size: 30,
                      ),
                      elevation: 0,
                    ),
                  ),
                ),
                SizedBox(
                  width: 5,
                ),
                Container(
                  height: 50.0,
                  width: 50.0,
                  child: FittedBox(
                    child: FloatingActionButton(
                      backgroundColor: Colors.white,
                      onPressed: () {},
                      child: Icon(
                        Icons.video_call_rounded,
                        color: Colors.blue[800],
                        size: 32,
                      ),
                      //backgroundColor: Colors.blue,
                      elevation: 0,
                    ),
                  ),
                ),
                SizedBox(
                  width: 5,
                ),
                Container(
                  height: 50.0,
                  width: 50.0,
                  child: FittedBox(
                    child: FloatingActionButton(
                      backgroundColor: Colors.white,
                      onPressed: () {},
                      child: Icon(
                        Icons.receipt_long_rounded,
                        color: Colors.blue[800],
                        size: 30,
                      ),
                      //backgroundColor: Colors.blue,
                      elevation: 0,
                    ),
                  ),
                ),
                //Icon(Icons.settings,color: Colors.black54,),
              ],
            ),
          ),
        ),
      ),
      body: Stack(
        children: <Widget>[
          ListView.builder(
            itemCount: messages.length,
            shrinkWrap: true,
            padding: EdgeInsets.only(top: 10, bottom: 10),
            physics: NeverScrollableScrollPhysics(),
            itemBuilder: (context, index) {
              return Container(
                padding:
                    EdgeInsets.only(left: 14, right: 14, top: 10, bottom: 10),
                child: Align(
                  alignment: (messages[index].messageType == "receiver"
                      ? Alignment.topLeft
                      : Alignment.topRight),
                  child: Container(
                    decoration: BoxDecoration(
                      borderRadius: BorderRadius.circular(20),
                      color: (messages[index].messageType == "receiver"
                          ? Colors.grey.shade200
                          : Colors.blue[200]),
                    ),
                    padding: EdgeInsets.all(16),
                    child: Text(
                      messages[index].messageContent,
                      style: TextStyle(fontSize: 15),
                    ),
                  ),
                ),
              );
            },
          ),
          Align(
            alignment: Alignment.bottomLeft,
            child: Container(
              padding: EdgeInsets.only(left: 10, bottom: 10, top: 10),
              height: 60,
              width: double.infinity,
              color: Colors.white,
              child: Row(
                children: <Widget>[
                  GestureDetector(
                    onTap: () {},
                    child: Container(
                      height: 30,
                      width: 30,
                      decoration: BoxDecoration(
                        color: Colors.lightBlue,
                        borderRadius: BorderRadius.circular(30),
                      ),
                      child: Icon(
                        Icons.add,
                        color: Colors.white,
                        size: 20,
                      ),
                    ),
                  ),
                  SizedBox(
                    width: 15,
                  ),
                  Expanded(
                    child: TextField(
                      controller: message,
                      decoration: InputDecoration(
                          hintText: "Write message...",
                          hintStyle: TextStyle(color: Colors.black54),
                          border: InputBorder.none),
                    ),
                  ),
                  SizedBox(
                    width: 15,
                  ),
                  FloatingActionButton(
                    onPressed: () {
                      client_Socket.write("""{
                        'name': 'Ojas',
                        'mobNo': '9619542526',
                        'msgType': 'chatBotMsg',
                        'message': '${message.text}',
                        'command': ''
                      }"""
                          .toString());
                      print(message.text);
                    },
                    child: Icon(
                      Icons.send,
                      color: Colors.white,
                      size: 18,
                    ),
                    backgroundColor: Colors.blue,
                    elevation: 0,
                  ),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }
}
