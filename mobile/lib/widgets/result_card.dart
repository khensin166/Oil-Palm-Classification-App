import 'package:flutter/material.dart';
import 'package:percent_indicator/percent_indicator.dart';
import '../models/prediction_result.dart';

class ResultCard extends StatelessWidget {
  final PredictionResult result;

  const ResultCard({Key? key, required this.result}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    if (!result.success) {
      return Container(
        decoration: BoxDecoration(
          color: Colors.red[50],
          borderRadius: BorderRadius.circular(20),
          border: Border.all(color: Colors.red[200]!),
        ),
        padding: const EdgeInsets.all(20.0),
        child: Row(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Container(
              padding: const EdgeInsets.all(10),
              decoration: BoxDecoration(
                color: Colors.red[100],
                shape: BoxShape.circle,
              ),
              child: const Icon(Icons.warning_rounded, color: Colors.red, size: 28),
            ),
            const SizedBox(width: 16),
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  const Text(
                    'Tidak Valid',
                    style: TextStyle(
                      color: Colors.red,
                      fontWeight: FontWeight.bold,
                      fontSize: 18,
                    ),
                  ),
                  const SizedBox(height: 6),
                  Text(
                    result.message ?? 'Gambar tidak memenuhi kriteria prediksi.',
                    style: TextStyle(
                      color: Colors.red[800],
                      height: 1.4,
                    ),
                  ),
                ],
              ),
            ),
          ],
        ),
      );
    }

    final double confValue = result.confidence ?? 0.0;
    final Color progressColor = confValue > 0.85
        ? Colors.green
        : (confValue > 0.70 ? Colors.orange : Colors.red);

    return Container(
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(24),
        boxShadow: [
          BoxShadow(
            color: Colors.black.withOpacity(0.05),
            blurRadius: 24,
            offset: const Offset(0, 8),
          ),
        ],
      ),
      padding: const EdgeInsets.all(24.0),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            crossAxisAlignment: CrossAxisAlignment.center,
            children: [
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      'Jenis Sawit:',
                      style: TextStyle(
                        fontSize: 14,
                        color: Colors.grey[500],
                        fontWeight: FontWeight.w600,
                        letterSpacing: 0.5,
                      ),
                    ),
                    const SizedBox(height: 4),
                    Text(
                      (result.prediction ?? '').toUpperCase(),
                      style: TextStyle(
                        fontSize: 32,
                        fontWeight: FontWeight.w900,
                        color: Theme.of(context).colorScheme.primary,
                        height: 1.1,
                      ),
                    ),
                  ],
                ),
              ),
              CircularPercentIndicator(
                radius: 40.0,
                lineWidth: 8.0,
                animation: true,
                percent: confValue,
                center: Text(
                  "${(confValue * 100).toStringAsFixed(0)}%",
                  style: const TextStyle(
                    fontWeight: FontWeight.bold,
                    fontSize: 16.0,
                  ),
                ),
                circularStrokeCap: CircularStrokeCap.round,
                progressColor: progressColor,
                backgroundColor: Colors.grey[200]!,
              ),
            ],
          ),
          
          if (result.description != null && result.description!.isNotEmpty) ...[
            const SizedBox(height: 24),
            Container(
              padding: const EdgeInsets.all(16),
              decoration: BoxDecoration(
                color: Colors.green[50],
                borderRadius: BorderRadius.circular(16),
                border: Border.all(color: Colors.green[100]!),
              ),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Row(
                    children: [
                      Icon(Icons.info_outline_rounded, size: 20, color: Colors.green[700]),
                      const SizedBox(width: 8),
                      Text(
                        'Deskripsi',
                        style: TextStyle(
                          fontWeight: FontWeight.bold,
                          color: Colors.green[800],
                        ),
                      ),
                    ],
                  ),
                  const SizedBox(height: 8),
                  Text(
                    result.description!,
                    style: TextStyle(
                      height: 1.5,
                      color: Colors.green[900],
                      fontSize: 14,
                    ),
                  ),
                ],
              ),
            ),
          ],
          
          const SizedBox(height: 24),
          const Divider(height: 1),
          const SizedBox(height: 24),
          
          Text(
            'Detail Probabilitas',
            style: TextStyle(
              fontWeight: FontWeight.bold,
              fontSize: 16,
              color: Colors.grey[800],
            ),
          ),
          const SizedBox(height: 16),
          
          if (result.allPredictions != null)
            ...result.allPredictions!.where((p) => p.label.toLowerCase() != 'unknown').map((p) {
              final val = p.confidence;
              final isTop = p.label == result.prediction;
              return Padding(
                padding: const EdgeInsets.only(bottom: 12),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Row(
                      mainAxisAlignment: MainAxisAlignment.spaceBetween,
                      children: [
                        Text(
                          p.label.toUpperCase(),
                          style: TextStyle(
                            fontWeight: isTop ? FontWeight.bold : FontWeight.normal,
                            color: isTop ? Theme.of(context).colorScheme.primary : Colors.grey[700],
                          ),
                        ),
                        Text(
                          '${(val * 100).toStringAsFixed(1)}%',
                          style: TextStyle(
                            fontWeight: isTop ? FontWeight.bold : FontWeight.normal,
                            color: isTop ? Theme.of(context).colorScheme.primary : Colors.grey[600],
                          ),
                        ),
                      ],
                    ),
                    const SizedBox(height: 6),
                    LinearPercentIndicator(
                      lineHeight: 8.0,
                      animation: true,
                      percent: val,
                      linearStrokeCap: LinearStrokeCap.roundAll,
                      progressColor: isTop ? Theme.of(context).colorScheme.primary : Colors.grey[400],
                      backgroundColor: Colors.grey[200],
                      padding: EdgeInsets.zero,
                    ),
                  ],
                ),
              );
            }).toList(),
        ],
      ),
    );
  }
}
