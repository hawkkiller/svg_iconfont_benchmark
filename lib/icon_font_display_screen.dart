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
        gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(crossAxisCount: 25),
        itemCount: itemCount,
        itemBuilder: (context, index) {
          final symbol = allSymbols[index % allSymbols.length];

          return Icon(symbol);
        },
      ),
    );
  }
}
