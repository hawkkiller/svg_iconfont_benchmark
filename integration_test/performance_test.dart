import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:integration_test/integration_test.dart';
import 'package:svg_benchmark/icon_font_display_screen.dart';
import 'package:svg_benchmark/svg_screen.dart';

void main() {
  final binding = IntegrationTestWidgetsFlutterBinding.ensureInitialized();

  testWidgets('SVG Performance Test', (WidgetTester tester) async {
    tester.view.display.size = const Size(800, 50);
    await tester.pumpWidget(MaterialApp(home: SvgScreen()));

    await binding.traceAction(() async {
      final listFinder = find.byType(GridView);
      await tester.fling(listFinder, const Offset(-3000, 0), 10000);
      await tester.pumpAndSettle();
    }, reportKey: 'svg_scroll');
  });

  testWidgets('IconFont Performance Test', (WidgetTester tester) async {
    tester.view.display.size = const Size(800, 50);
    await tester.pumpWidget(MaterialApp(home: IconFontScreen()));

    await binding.traceAction(() async {
      final listFinder = find.byType(GridView);
      await tester.fling(listFinder, const Offset(-3000, 0), 10000);
      await tester.pumpAndSettle();
    }, reportKey: 'iconfont_scroll');
  });
}
