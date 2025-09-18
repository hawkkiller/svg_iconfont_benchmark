import 'package:flutter/material.dart';
import 'package:vector_graphics/vector_graphics.dart';
import 'package:flutter_svg/flutter_svg.dart';
import 'package:svg_benchmark/gen/assets.gen.dart';

class SvgVecScreen extends StatelessWidget {
  const SvgVecScreen({super.key, this.itemCount = 20});

  final int itemCount;

  static final allIcons = <String>[
    Assets.iconsVec.arrowBackSvg,
    Assets.iconsVec.arrowBackIosSvg,
    Assets.iconsVec.arrowDropDownSvg,
    Assets.iconsVec.arrowForwardSvg,
    Assets.iconsVec.arrowForwardIosSvg,
    Assets.iconsVec.checkSvg,
    Assets.iconsVec.checkBoxSvg,
    Assets.iconsVec.checkCircleSvg,
    Assets.iconsVec.chevronRightSvg,
    Assets.iconsVec.closeSvg,
    Assets.iconsVec.deleteSvg,
    Assets.iconsVec.homeSvg,
    Assets.iconsVec.logoutSvg,
    Assets.iconsVec.menuSvg,
    Assets.iconsVec.moreVertSvg,
    Assets.iconsVec.searchSvg,
    Assets.iconsVec.settingsSvg,
    Assets.iconsVec.starSvg,
  ];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('SVG compiled Benchmark')),
      body: GridView.builder(
        gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
          crossAxisCount: 10,
        ),
        itemCount: itemCount,
        itemBuilder: (context, index) {
          final cycle = index ~/ allIcons.length;
          final color = HSVColor.fromAHSV(
            1.0,
            (cycle * 30.0) % 360.0,
            1.0,
            1.0,
          ).toColor();

          return Center(
            child: SvgPicture(
              AssetBytesLoader(allIcons[index % allIcons.length]),
              width: 24,
              height: 24,
              colorFilter: ColorFilter.mode(color, BlendMode.srcIn),
            ),
          );
        },
      ),
    );
  }
}
