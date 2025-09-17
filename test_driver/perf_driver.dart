import 'package:integration_test/integration_test_driver.dart';
import 'package:flutter_driver/flutter_driver.dart' as driver;

Future<void> main() {
  return integrationDriver(
    responseDataCallback: (data) async {
      if (data != null) {
        // The performance test saves timeline data in a map with a key for each
        // test. We'll iterate through the map and write a timeline file for each entry.
        for (final key in data.keys) {
          final timeline = driver.Timeline.fromJson(data[key]);
          final summary = driver.TimelineSummary.summarize(timeline);
          // The key, for example, is 'svg_scroll'. We want the file to be named 'svg.timeline_summary.json'.
          final fileKey = key.replaceAll('_scroll_', '_');
          await summary.writeTimelineToFile(
            fileKey,
            pretty: true,
            includeSummary: true,
          );
        }
      }
    },
  );
}
