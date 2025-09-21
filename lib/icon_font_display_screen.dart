import 'package:flutter/material.dart';
import 'package:svg_benchmark/icons/symbols.dart';

class IconFontScreen extends StatelessWidget {
  const IconFontScreen({super.key, this.itemCount = 20});

  final int itemCount;

  static const allSymbols = <IconData>[
    Symbols.search,
    Symbols.home,
    Symbols.logout,
    Symbols.arrowBack,
    Symbols.settings,
    Symbols.chevronRight,
    Symbols.check,
    Symbols.close,
    Symbols.checkCircle,
    Symbols.arrowDropDown,
    Symbols.star,
    Symbols.arrowBackIos,
    Symbols.delete,
    Symbols.checkBox,
    Symbols.arrowForward,
    Symbols.moreVert,
    Symbols.menu,
    Symbols.arrowForwardIos,
  ];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Icon Font Benchmark')),
      body: GridView.builder(
        gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
          crossAxisCount: 10,
        ),
        itemCount: itemCount,
        itemBuilder: (context, index) {
          final cycle = index ~/ allSymbols.length;
          final color = HSVColor.fromAHSV(
            1.0,
            (cycle * 30.0) % 360.0,
            1.0,
            1.0,
          ).toColor();
          final symbol = allSymbols[index % allSymbols.length];

          return Icon(symbol, size: 24, color: color);
        },
      ),
    );
  }
}
