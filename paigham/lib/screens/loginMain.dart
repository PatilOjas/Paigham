// import 'dart:html';
import 'dart:ui';
import 'package:flutter/material.dart';
import 'package:paigham/screens/login.dart';
import 'package:paigham/screens/signup.dart';
import 'package:paigham/main.dart';

class LoginMain extends StatelessWidget {
  dynamic client_Socket;
  LoginMain({this.client_Socket});
  @override
  Widget build(BuildContext context) {
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
                    height: 35,
                  ),
                  Text(
                    "Take a deep dive into this multipurpose messaging App",
                    textAlign: TextAlign.center,
                    style: TextStyle(
                      color: Colors.grey[700],
                      fontSize: 15,
                    ),
                  )
                ],
              ),
              Container(
                height: MediaQuery.of(context).size.height / 3,
                decoration: BoxDecoration(
                    image: DecorationImage(
                        image: AssetImage("/assets/welcome.png"))),
              ),
              Column(
                children: <Widget>[
                  // the login button
                  // MaterialButton(
                  //   minWidth: double.infinity,
                  //   height: 60,
                  //   onPressed: () {
                  //     Navigator.push(context, MaterialPageRoute(builder: (context) => LoginPage()));

                  //   },
                  // defining the shape
                  // shape: RoundedRectangleBorder(
                  //   side: BorderSide(
                  //     color: Colors.black
                  //   ),
                  //   borderRadius: BorderRadius.circular(50)
                  // ),
                  //   child: Text(
                  //     "Login",
                  //     style: TextStyle(
                  //       fontWeight: FontWeight.w600,
                  //       fontSize: 18
                  //     ),
                  //   ),
                  // ),
                  // creating the signup button
                  SizedBox(height: 20),
                  MaterialButton(
                    minWidth: double.infinity,
                    height: 60,
                    onPressed: () {
                      
                        Navigator.push(
                            context,
                            MaterialPageRoute(
                                builder: (context) =>
                                    SignupPage(client_Socket: client_Socket)));
                    },
                    color: Color(0xff0095FF),
                    shape: RoundedRectangleBorder(
                        borderRadius: BorderRadius.circular(50)),
                    child: Text(
                      "Sign up",
                      style: TextStyle(
                          color: Colors.white,
                          fontWeight: FontWeight.w600,
                          fontSize: 18),
                    ),
                  )
                ],
              )
            ],
          ),
        ),
      ),
    );
  }
}
