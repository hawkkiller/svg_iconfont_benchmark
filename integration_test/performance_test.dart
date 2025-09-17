import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:integration_test/integration_test.dart';
import 'package:svg_benchmark/icon_font_display_screen.dart';
import 'package:svg_benchmark/svg_screen.dart';
import 'package:svg_benchmark/svg_vec_screen.dart';

void _runPerfTest(
  IntegrationTestWidgetsFlutterBinding binding, {
  required String description,
  required Widget home,
  required String reportKey,
}) {
  testWidgets(description, (WidgetTester tester) async {
    await tester.binding.setSurfaceSize(const Size(800, 200));
    await tester.pumpWidget(MaterialApp(home: home));

    await binding.traceAction(() async {
      final listFinder = find.byType(GridView);
      await tester.fling(listFinder, const Offset(0, -3000), 10000);
      await tester.pumpAndSettle();
    }, reportKey: reportKey);
  });
}

void main() {
  final binding = IntegrationTestWidgetsFlutterBinding.ensureInitialized();
  const itemCounts = [20, 200, 500, 2000];

  // Define configurations for each test type
  final testCases = [
    (
      name: 'SVG',
      widgetBuilder: (count) => SvgScreen(itemCount: count),
      reportKeyPrefix: 'svg',
    ),
    (
      name: 'SVG Vec',
      widgetBuilder: (count) => SvgVecScreen(itemCount: count),
      reportKeyPrefix: 'svg_vec',
    ),
    (
      name: 'IconFont',
      widgetBuilder: (count) => IconFontScreen(itemCount: count),
      reportKeyPrefix: 'iconfont',
    ),
  ];

  // Iterate over each icon count
  for (final count in itemCounts) {
    // And for each count, run all test types
    for (final testCase in testCases) {
      _runPerfTest(
        binding,
        description: '${testCase.name} Performance Test with $count items',
        home: testCase.widgetBuilder(count),
        reportKey: 'icons_${count}_${testCase.reportKeyPrefix}',
      );
    }
  }
}
