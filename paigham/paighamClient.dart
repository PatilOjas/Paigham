import 'dart:io';
import 'dart:async';
import 'package:synchronized/synchronized.dart';
import 'dart:typed_data';

class SocketConnection {
  SocketConnection();

  Future<String> con() async {
    String indexRequest = 'FLUTTER GET / HTTP/1.1\nConnection: close\n\n';
    String d = "";
    Future<String> readContent;

    await Socket.connect('192.168.1.202', 4445).then((socket) async {
      print('Connected to: '
          '${socket.remoteAddress.address}:${socket.remotePort}');

      //Establish the onData, and onDone callbacks
      int counter = 0;
      File g = await new File('b.png');
      socket.listen(
        (data) async {
          List<int> imgData = new List.from(data);
          await g.writeAsBytes(imgData);
        },
        onDone: () {
          print("Done");
          socket.destroy();
        },
      );

      final f = File('a.jpg');

      // print(f.readAsBytesSync());
      //Send the request
      final byteString = await f.readAsBytes();
      print("Data type byteString: " + byteString.runtimeType.toString());
      socket.write("Be ready... Sending...");
      var q = () {
        socket.add(byteString);
        return Future.delayed(
            Duration(seconds: (byteString.length / 9899136).ceil() + 5),
            () => socket.write("0"));
      };
      print("Awaiting q...");
      final byteSent = byteString.length / 9899136;
      print("Asach: " + byteString.length.toString());
      print("UTF-8 Encoded: " + (byteString.length * 4).toString());
      print("byteSent " + byteSent.ceil().toString());
      q();
      print("Awaiting completed..");
      print("0 has been sent");
    });
    return d;
  }
}

void main(List<String> args) {
  var s = SocketConnection();
  print(s.con());
}
