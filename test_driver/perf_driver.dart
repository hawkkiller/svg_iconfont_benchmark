import 'package:integration_test/integration_test_driver.dart';
import 'package:flutter_driver/flutter_driver.dart' as driver;

Future<void> main() {
  return integrationDriver(
    responseDataCallback: (data) async {
      if (data != null) {
        final svgTimeline = driver.Timeline.fromJson(data['svg_scroll']);
        final iconfontTimeline = driver.Timeline.fromJson(data['iconfont_scroll']);
        final svgSummary = driver.TimelineSummary.summarize(svgTimeline);
        final iconfontSummary = driver.TimelineSummary.summarize(iconfontTimeline);
        
        await svgSummary.writeTimelineToFile('svg', pretty: true, includeSummary: true);
        await iconfontSummary.writeTimelineToFile('iconfont', pretty: true, includeSummary: true);
      }
    },
  );
}
