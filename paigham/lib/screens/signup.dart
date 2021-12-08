import 'package:flutter/material.dart';
import 'package:paigham/screens/homePage.dart';
import 'dart:io';
import 'package:path_provider/path_provider.dart';

class SignupPage extends StatelessWidget {
  dynamic client_Socket;
  SignupPage({this.client_Socket});
  TextEditingController name = TextEditingController();
  TextEditingController mobile_num = TextEditingController();

  var _write = (String data) async {
    final Directory directory = await getApplicationDocumentsDirectory();
    print("\n\n\n\n\n\n\n\n\n\n PATH:\n\n\n\n\n\n\n" + directory.path);
    final File file = File('${directory.path}/data.txt');
    await file.writeAsString(data);
  };

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      resizeToAvoidBottomInset: true,
      backgroundColor: Colors.white,
      appBar: AppBar(
        elevation: 0,
        brightness: Brightness.light,
        backgroundColor: Colors.white,
        leading: IconButton(
          onPressed: () {
            Navigator.pop(context);
          },
          icon: Icon(
            Icons.arrow_back_ios,
            size: 20,
            color: Colors.black,
          ),
        ),
      ),
      body: SingleChildScrollView(
        child: Container(
          padding: EdgeInsets.symmetric(horizontal: 40),
          height: MediaQuery.of(context).size.height - 50,
          width: double.infinity,
          child: Column(
            mainAxisAlignment: MainAxisAlignment.spaceEvenly,
            children: <Widget>[
              Column(
                children: <Widget>[
                  Text(
                    "Sign up",
                    style: TextStyle(
                      fontSize: 30,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                  SizedBox(
                    height: 20,
                  ),
                  Text(
                    "Create an account, It's free ",
                    style: TextStyle(fontSize: 15, color: Colors.grey[700]),
                  )
                ],
              ),
              Expanded(
                child: TextField(
                  controller: name,
                  decoration: InputDecoration(
                    hintText: "Name",
                    hintStyle: TextStyle(color: Colors.black54),
                    border: const OutlineInputBorder(),
                    labelStyle: new TextStyle(color: Colors.black),
                  ),
                ),
              ),
              Expanded(
                child: TextField(
                  controller: mobile_num,
                  decoration: InputDecoration(
                    hintText: "Mobile Number",
                    hintStyle: TextStyle(color: Colors.black54),
                    border: const OutlineInputBorder(),
                    labelStyle: new TextStyle(color: Colors.black),
                  ),
                ),
              ),
              // Column(
              //   children: <Widget>[
              //     inputFile(label: "Name"),
              //     inputFile(label: "Mobile Number"),
              //     // inputFile(label: "Password", obscureText: true),
              //     // inputFile(label: "Confirm Password ", obscureText: true),
              //   ],
              // ),
              Container(
                padding: EdgeInsets.only(top: 3, left: 3),
                decoration: BoxDecoration(
                    borderRadius: BorderRadius.circular(50),
                    border: Border(
                      bottom: BorderSide(color: Colors.black),
                      top: BorderSide(color: Colors.black),
                      left: BorderSide(color: Colors.black),
                      right: BorderSide(color: Colors.black),
                    )),
                child: MaterialButton(
                  minWidth: double.infinity,
                  height: 60,
                  onPressed: () {
                    client_Socket.write("""
                    {
                      'name': '${name.text}',
                      'mobNo': '${mobile_num.text}',
                    }"""
                        .toString());
                    // final f = File('assets/data.txt');
                    var data = """
                    {
                      'name': '${name}',
                      'mobNo': '${mobile_num}',
                    }""";
                    _write(data);
                    Navigator.push(
                        context,
                        MaterialPageRoute(
                            builder: (context) =>
                                HomePage(client_Socket: client_Socket)));
                  },
                  color: Color(0xff0095FF),
                  elevation: 0,
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(50),
                  ),
                  child: Text(
                    "Done",
                    style: TextStyle(
                      fontWeight: FontWeight.w600,
                      fontSize: 18,
                      color: Colors.white,
                    ),
                  ),
                ),
              ),
              // Row(
              //   mainAxisAlignment: MainAxisAlignment.center,
              //   children: <Widget>[
              //     Text("Already have an account?"),
              //     Text(" Login", style:TextStyle(
              //         fontWeight: FontWeight.w600,
              //         fontSize: 18
              //     ),
              //     )
              //   ],
              // )
            ],
          ),
        ),
      ),
    );
  }
}

// we will be creating a widget for text field
Widget inputFile({label, obscureText = false}) {
  return Column(
    crossAxisAlignment: CrossAxisAlignment.start,
    children: <Widget>[
      Text(
        label,
        style: TextStyle(
            fontSize: 15, fontWeight: FontWeight.w400, color: Colors.black87),
      ),
      SizedBox(
        height: 5,
      ),
      TextField(
        obscureText: obscureText,
        decoration: InputDecoration(
            contentPadding: EdgeInsets.symmetric(vertical: 0, horizontal: 10),
            enabledBorder: OutlineInputBorder(
              borderSide: BorderSide(color: Colors.grey),
            ),
            border:
                OutlineInputBorder(borderSide: BorderSide(color: Colors.grey))),
      ),
      SizedBox(
        height: 10,
      )
    ],
  );
}
