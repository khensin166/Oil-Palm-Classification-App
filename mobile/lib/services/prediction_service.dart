import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:http_parser/http_parser.dart';
import 'package:mime/mime.dart';
import '../models/prediction_result.dart';

class PredictionService {
  // Gunakan IP laptop jika menggunakan device fisik
  // Gunakan IP laptop jika menggunakan device fisik
  static const String baseUrl = "http://192.168.137.243:8000";

  Future<PredictionResult> predictImage(String imagePath) async {
    var uri = Uri.parse('$baseUrl/predict');

    try {
      var request = http.MultipartRequest('POST', uri);

      var mimeTypeData = lookupMimeType(imagePath, headerBytes: [0xFF, 0xD8])?.split('/');
      
      var file = await http.MultipartFile.fromPath(
        'image', 
        imagePath,
        contentType: mimeTypeData != null ? MediaType(mimeTypeData[0], mimeTypeData[1]) : null,
      );

      request.files.add(file);

      var streamedResponse = await request.send().timeout(const Duration(seconds: 30));
      var response = await http.Response.fromStream(streamedResponse);

      if (response.statusCode == 200) {
        var jsonData = json.decode(response.body);
        return PredictionResult.fromJson(jsonData);
      } else {
        var jsonData = json.decode(response.body);
        return PredictionResult(
          success: false, 
          message: jsonData['message'] ?? 'Failed with status ${response.statusCode}'
        );
      }
    } catch (e) {
      return PredictionResult(success: false, message: 'Error: Cannot connect to server. Check backend URL.');
    }
  }
}
