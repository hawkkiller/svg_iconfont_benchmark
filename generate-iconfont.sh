# ensure icon_font_generator is installed globally
if ! command -v dart pub run icon_font_generator &> /dev/null
then
  echo "icon_font_generator could not be found, installing..."
  dart pub global activate icon_font_generator
fi

dart pub global run icon_font_generator:generator \
  assets/icons \
  assets/iconfont/Symbols.otf \
  --font-name Symbols \
  --class-name Symbols \
  -r \
  -v \
  --normalize \
  -o lib/icons/symbols.dart \
  --no-ignore-shapes
