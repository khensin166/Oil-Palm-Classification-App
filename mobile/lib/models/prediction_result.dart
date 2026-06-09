class PredictionScore {
  final String label;
  final double confidence;

  PredictionScore({required this.label, required this.confidence});

  factory PredictionScore.fromJson(Map<String, dynamic> json) {
    return PredictionScore(
      label: json['label'] ?? '',
      confidence: (json['confidence'] ?? 0.0).toDouble(),
    );
  }
}

class PredictionResult {
  final bool success;
  final String? prediction;
  final double? confidence;
  final String? confidencePercent;
  final String? description;
  final List<PredictionScore>? allPredictions;
  final String? message;

  PredictionResult({
    required this.success,
    this.prediction,
    this.confidence,
    this.confidencePercent,
    this.description,
    this.allPredictions,
    this.message,
  });

  factory PredictionResult.fromJson(Map<String, dynamic> json) {
    var allPredictionsList = json['all_predictions'] as List?;
    List<PredictionScore>? predictions;
    if (allPredictionsList != null) {
      predictions = allPredictionsList.map((i) => PredictionScore.fromJson(i)).toList();
    }

    return PredictionResult(
      success: (json['success'] == true) && (json['is_valid'] != false),
      prediction: json['prediction'],
      confidence: json['confidence']?.toDouble(),
      confidencePercent: json['confidence_percent'],
      description: json['description'],
      allPredictions: predictions,
      message: json['message'],
    );
  }
}
