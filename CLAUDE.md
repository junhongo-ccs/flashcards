# 色彩検定UC級 暗記カード プロジェクト（Claude Code 引き継ぎルール）

Windows 環境で Claude Code が作業を引き継ぐためのメモ。Mac 側（Antigravity / Gemini）の引き継ぎ内容は `GEMINI.md` にあり、共通ルールは同じ。

## 1. 基本方針・コミュニケーション
- **必ず日本語で簡潔に応答すること。**
- ユーザーは色彩検定UC級（色のユニバーサルデザイン級）の受験対策をしており、自分の弱点問題だけをまとめた暗記カードWebアプリと問題データ（Excel / CSV）を育てている。
- ユーザーは Mac と Windows の両方で作業する。弱点データ（`my-weakness.xlsx`）は Mac から持ってきてこのフォルダ直下に置く。

## 2. リポジトリ内の主要ファイル
- `anki.html`:
  - サーバー不要・ブラウザで開くだけで動く暗記カードWebアプリ（SheetJS `xlsx.full.min.js` 使用）。
  - **Tailwind CSS は CDN を使わず、生成済み CSS を `<style id="tw">` に埋め込んでいる**（拡張機能などで CDN がブロックされる環境でも崩れないように）。元の定義は `tailwind.css`。**anki.html のクラスを追加・変更したら `node build-css.mjs` を実行して再生成すること**（しないと新しいクラスにスタイルが当たらない）。
  - **アイコンはアイコンフォントを使わず、Material Symbols（Outlined, weight 400）の SVG を直接埋め込んでいる**（`<svg class="inline-block w-[20px] h-[20px] ..." viewBox="0 -960 960 960" fill="currentColor">`、色は `text-*` で指定）。新しいアイコンは `https://cdn.jsdelivr.net/npm/@material-symbols/svg-400@0.48.1/outlined/<名前>.svg` の path をコピーして使う。
  - **常時ダークモード固定**、本文フォントサイズは **16px以上（`text-base` 〜 `text-2xl`）** のシンプルUI。
  - ヘッダー：タイトル（左に `lightbulb` アイコン）、`再読込`（File System Access API + IndexedDB）、`QAファイル選択`。
  - ヘッダー下（背景・線なし）：カテゴリ絞り込み、`QA順 [ 設定のまま | シャッフル ]` スイッチ（シャッフルはカテゴリをまたがずカテゴリ内だけで並べ替え、押すたびにシャッフルし直し。QA一覧は資料用なので常に元の順）、`[ 問題 | QA一覧 ]` セグメントスイッチ。
  - カードの左右に `<` `>` ボタン。`>`（→ キー）は「解答を表示 → 次のカードへ」の2段階、`<`（← キー）は常に解答を隠した状態で前のカードへ。カード内に「解答を表示」ボタン。カード右上に `QUESTION N / 全数`（全数はカテゴリ絞り込み後の問題数）、カード下端に進み具合バー。
  - **不要な機能（復活させないこと）**：「解説」列、ライトモード切替、要復習/覚えた判定、弱点フィルタ、検索バー、学習記録リセット、テンプレートDL、QA貼り付け（Excel に保存されず紛らわしいため削除）。
- `my-weakness.xlsx`:
  - ユーザーの弱点データ。**GitHub で管理する（コミット対象）**。リポジトリは本人と同僚しか見ないため問題ない。同僚はこのファイルをそのまま使うか、別名で新規保存してカスタマイズして使う。
  - 列構成は **`カテゴリ, 問題, 解答`** の3列（A列: 160px, B列: 360px, C列: 500px、全セル折り返し表示、1行目太字）。
  - **`my-weakness.csv` も xlsx と一緒にコミットして管理する**（同僚が Excel なしでも使え、GitHub 上で差分も読める）。CSV は自動では更新されないので、**xlsx を編集したら毎回 `python3 build-csv.py` で作り直してから一緒にコミットすること**（UTF-8・BOM なし・LF 改行）。
  - Mac 側でも編集されるため、編集前に最新版がこのフォルダにあるかユーザーに確認すること。
- **配布用サンプル Excel（`sample-*.xlsx` など）は作らない。** `my-weakness.xlsx` がその役割を兼ねる。
- `anki.html` の内蔵サンプルデータ（ファイル未読込時の初期表示用）の中身は、勝手に決めずユーザーと相談すること。
- `GEMINI.md`: Mac 側 AI 用の引き継ぎメモ。共通ルールを変えたときは両方を更新すること。

## 3. GridCraft（MCP）での Excel 編集手順
**ユーザーは開いている GridCraft 画面でリアルタイムに修正されるのを好む。** 基本は GUI のリモート操作で編集する:

```powershell
# GUI をリモート操作モードで起動（既に通常モードで開いている場合は、ユーザーに「保存せず閉じて」もらってから）
Start-Process "C:\Program Files\GridCraft\gridcraft.exe" -ArgumentList '--control','7979','"C:\github\flashcard\my-weakness.xlsx"'
```
```bash
"/c/Program Files/GridCraft/gridcraft-cli.exe" send 7979 range.setValues '{"range":"C15","values":[["d (dull)"]]}'
"/c/Program Files/GridCraft/gridcraft-cli.exe" send 7979 file.save '{}'
```

以下は GridCraft MCP サーバー（`mcp__gridcraft__*`、**ヘッドレス＝画面には反映されない**）を使う場合の手順。コマンド ID は Mac 版 `gridcraft-cli` と同じ。

1. `open_workbook` で `C:\github\flashcard\my-weakness.xlsx` を開く
2. `write_range` で追記・修正（例: `{"range":"A10","values":[["カテゴリ","問題","解答"]]}`）
3. 書式を整える（`execute_command`）:
   - `home.columnWidth` `{"cols":"A:A","width":160}` / `{"cols":"B:B","width":360}` / `{"cols":"C:C","width":500}`
   - `home.wrapText` `{"range":"A1:C<最終行>","on":true}`
   - `home.bold` `{"range":"A1:C1"}`
4. `save_workbook`（引数なし）で xlsx を上書き保存
5. `save_workbook` `{"path":"C:\\github\\flashcard\\my-weakness.csv"}` で CSV も出力
   - CSV で保存するとアクティブブックの保存先が CSV に変わる可能性があるため、続けて編集する場合は xlsx を開き直すこと。
