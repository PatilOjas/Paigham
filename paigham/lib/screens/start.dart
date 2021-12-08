import 'dart:ui';
import 'package:flutter/material.dart';
import 'package:paigham/screens/homePage.dart';
import 'package:paigham/screens/signup.dart';
import 'dart:io';
import 'dart:ui';
import 'package:flutter/material.dart';
import 'package:paigham/screens/login.dart';
import 'package:paigham/screens/signup.dart';

class Start extends StatelessWidget {
  dynamic client_Socket;
  Start({this.client_Socket});
  var flag = 0;
  @override
  Widget build(BuildContext context) {
    var q = () async {
      final f = File('data.txt');
      final data = await f.readAsString();
      if (data.length > 0) {
        flag = 1;
      }
    };
    q();
    return Scaffold(
        body: SafeArea(
            child: Container(
                // we will give media query height
                // double.infinity make it big as my parent allows
                // while MediaQuery make it big as per the screen

                width: double.infinity,
                height: MediaQuery.of(context).size.height,
                padding: EdgeInsets.symmetric(horizontal: 30, vertical: 50),
                child: Column(
                    // even space distribution
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    crossAxisAlignment: CrossAxisAlignment.center,
                    children: <Widget>[
                      Column(
                        children: <Widget>[
                          Text(
                            "Paigham",
                            style: TextStyle(
                              fontFamily: 'Rolasand',
                              fontWeight: FontWeight.bold,
                              fontSize: 40,
                            ),
                          ),
                          SizedBox(
                            height: 20,
                          ),
                          Text(
                            "Take a deep dive into this multipurpose messaging App",
                            textAlign: TextAlign.center,
                            style: TextStyle(
                              color: Colors.grey[700],
                              fontSize: 15,
                            ),
                          ),
                          SizedBox(
                            height: 20,
                          ),
                          TextButton(
                            onPressed: () {
                              if (flag == 0) {
                                Navigator.push(
                                    context,
                                    MaterialPageRoute(
                                        builder: (context) => SignupPage(
                                            client_Socket: client_Socket)));
                              } else {
                                Navigator.push(
                                    context,
                                    MaterialPageRoute(
                                        builder: (context) => HomePage(
                                            client_Socket: client_Socket)));
                              }
                            },
                            child: Text(
                              "Go",
                              style: TextStyle(
                                fontWeight: FontWeight.w600,
                                fontSize: 18,
                                color: Colors.black,
                              ),
                            ),
                          )
                        ],
                      ),
                    ]))));
  }
}
