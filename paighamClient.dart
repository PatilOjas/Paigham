import 'dart:io';

class SocketConnection {
  SocketConnection();

  Future<String> con() async {
    String indexRequest = 'FLUTTER GET / HTTP/1.1\nConnection: close\n\n';
    String d = "";
    Future<String> readContent;

    await Socket.connect('192.168.1.205', 4445).then((socket) async {
      print('Connected to: '
          '${socket.remoteAddress.address}:${socket.remotePort}');

      //Establish the onData, and onDone callbacks
      socket.listen((data) {
        d = String.fromCharCodes(data);
        print(d);
      }, onDone: () {
        print("Done");
        socket.write("Erhalten");
        socket.destroy();
      });

      final f = File('a.mp4');

      // print(f.readAsBytesSync());
      //Send the request
      final byteString = await f.readAsBytes();
      socket.write("Be ready... Sending...");
      var q = () {
        socket.add(byteString);
        return Future.delayed(Duration(seconds: (byteString.length/9899136).toInt()), () => socket.write("0"));
      };
      print("Awaiting q...");
      final byteSent = (byteString.length * 4) / 130836;
      print("Asach: " + byteString.length.toString());
      print("UTF-8 Encoded: " + (byteString.length * 4).toString());
      print("byteSent " + byteSent.toString());
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
