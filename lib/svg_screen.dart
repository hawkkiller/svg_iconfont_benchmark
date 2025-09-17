import 'package:flutter/material.dart';

import 'package:flutter_svg/flutter_svg.dart';
import 'package:svg_benchmark/gen/assets.gen.dart';

class SvgScreen extends StatelessWidget {
  const SvgScreen({super.key, this.itemCount = 20});

  final int itemCount;

  static final allIcons = <String>[
    Assets.icons.arrowBack,
    Assets.icons.arrowBackIos,
    Assets.icons.arrowDropDown,
    Assets.icons.arrowForward,
    Assets.icons.arrowForwardIos,
    Assets.icons.check,
    Assets.icons.checkBox,
    Assets.icons.checkCircle,
    Assets.icons.chevronRight,
    Assets.icons.close,
    Assets.icons.delete,
    Assets.icons.home,
    Assets.icons.logout,
    Assets.icons.menu,
    Assets.icons.moreVert,
    Assets.icons.search,
    Assets.icons.settings,
    Assets.icons.star,
  ];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('SVG Benchmark')),
      body: GridView.builder(
        gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
          crossAxisCount: 25,
        ),
        itemCount: itemCount,
        itemBuilder: (context, index) {
          return Center(
            child: SvgPicture.asset(
              allIcons[index % allIcons.length],
              width: 24,
              height: 24,
              colorFilter: const ColorFilter.mode(Colors.black, BlendMode.srcIn),
            ),
          );
        },
      ),
    );
  }
}
