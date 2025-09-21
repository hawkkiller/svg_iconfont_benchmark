import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:integration_test/integration_test.dart';
import 'package:svg_benchmark/icon_font_display_screen.dart';
import 'package:svg_benchmark/svg_screen.dart';
import 'package:svg_benchmark/svg_vec_screen.dart';

// Function to run a performance test with scrolling.
void _runPerfTestWithScrolling(
  IntegrationTestWidgetsFlutterBinding binding, {
  required String description,
  required Widget home,
  required String reportKey,
}) {
  testWidgets(description, (WidgetTester tester) async {

    // Warm-up: render the widget to let the system prepare
    await tester.pumpWidget(MaterialApp(home: home));
    await tester.pumpAndSettle();

    // Start collecting performance data during scrolling
    await binding.watchPerformance(
      () async {
        // Simulate scrolling:
        // Fling the list to render new items.
        await tester.fling(
          find.byType(GridView), 
          const Offset(0, -10000), 
          5000, 
        );
        // Wait for the scroll animation to complete.
        await tester.pumpAndSettle();
      },
      reportKey: reportKey,
    );
  });
}

void main() {
  final binding = IntegrationTestWidgetsFlutterBinding.ensureInitialized();
  const itemCounts = [20, 500, 2000]; 

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

  for (final count in itemCounts) {
    for (final testCase in testCases) {
      _runPerfTestWithScrolling(
        binding,
        description: 'Scrolling ${testCase.name} with $count items',
        home: testCase.widgetBuilder(count),
        reportKey: 'icons_${count}_${testCase.reportKeyPrefix}',
      );
    }
  }
}