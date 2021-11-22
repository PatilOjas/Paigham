import 'dart:io';

// class with mediafile sender and receiver
class MediaShare {

  // execute receiver first
  void receiver(Socket socket) async {
    String extension = ".txt";
    List<int> fileChunks = [];
    const extensionList = [
      '.png',
      '.mp4',
      '.jpg',
      '.mp3',
      '.jpeg',
      '.webm',
      '.wav',
      '.pdf',
    ];

    const imageExtList = ['.png', '.jpg', '.jpeg'];

    const audioExtList = ['.mp3', '.wav'];

    const videoExtList = ['.mp4', '.mkv', '.webm'];

    socket.listen((data) async {
      if (extensionList.contains(String.fromCharCodes(data))) {
        extension = String.fromCharCodes(data);
        print("extension " + extension);
      } else {
        List<int> I_quit = await new List.from(data);
        fileChunks.addAll(I_quit);
      }
    }, onDone: () async {
      print("Completed");
      final fileName = DateTime.now()
          .toString()
          .replaceAll(RegExp(r'[^\w\s]+'), "")
          .split(" ")
          .join("-");
      var initialname = "";
      if (extension == '.pdf') {
        initialname = 'PDF';
      }
      if (imageExtList.contains(extension)) {
        initialname = 'IMG';
      }
      if (audioExtList.contains(extension)) {
        initialname = 'AUD';
      }
      if (videoExtList.contains(extension)) {
        initialname = 'VID';
      }
      File clientFile = await File('$initialname$fileName$extension');
      await clientFile.writeAsBytes(fileChunks, mode: FileMode.writeOnlyAppend);
    });
  }

// execute sender whenever you need to send any file by passing its file path and socket object 
  void sender(Socket socket, String fileName) async {
    final f = File(fileName);

    final byteString = await f.readAsBytes();

    final fileNameList = fileName.split(".");
    final ext = "." + fileNameList[fileNameList.length - 1];
    socket.write(ext);

    var q = () {
      socket.add(byteString);
      return Future.delayed(
          Duration(seconds: (byteString.length / 3000000).ceil() + 10), () {
        socket.write("0");
        print("0 has been sent & single tick received");
      });
    };
    print("Awaiting q...");
    await q();
  }
}

// Refer this main function for further use of MediaShare class
// Replace file path with actual path of file and replace ipAddr with ipAddress of server
void main(List<String> args) async {
  var s = MediaShare();
  Socket socket = await Socket.connect("ipAddr", 4445);
  s.receiver(socket);
  s.sender(socket, 'filepath');
}
