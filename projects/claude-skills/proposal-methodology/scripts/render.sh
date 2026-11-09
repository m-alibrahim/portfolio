#!/usr/bin/env bash
# تحويل مخرج إلى صور للمعاينة البصرية. لا تسلّم أي ملف قبل تشغيل هذا.
# الاستخدام: bash render.sh out.docx [dpi] [first] [last]
set -e
F="$1"; DPI="${2:-75}"; A="${3:-1}"; B="${4:-0}"
D=$(dirname "$F"); N=$(basename "$F"); BASE="${N%.*}"
case "$F" in
  *.pptx|*.potx) S=/mnt/skills/public/pptx/scripts/office/soffice.py ;;
  *)             S=/mnt/skills/public/docx/scripts/office/soffice.py ;;
esac
( cd "$D" && rm -f "$BASE.pdf" && timeout 900 python3 "$S" --headless --convert-to pdf "$N" >/dev/null 2>&1 )
if [ "$B" -gt 0 ]; then
  pdftoppm -jpeg -r "$DPI" -f "$A" -l "$B" "$D/$BASE.pdf" "$D/pg"
else
  pdftoppm -jpeg -r "$DPI" "$D/$BASE.pdf" "$D/pg"
fi
ls "$D"/pg-*.jpg
echo "عايِن الصور بأداة view قبل التسليم."
