import 'dart:convert';
import 'dart:io';

import 'package:integration_test/integration_test_driver.dart';

Future<void> main() {
  return integrationDriver(
    responseDataCallback: (data) async {
      if (data != null) {
        for (final key in data.keys) {
          // The performance test is returning a summary, not the raw timeline data.
          // We just need to write this summary data to a file.
          final file = File('build/$key.timeline_summary.json');
          await file.writeAsString(
            const JsonEncoder.withIndent('  ').convert(data[key]),
          );
        }
      }
    },
  );
}
