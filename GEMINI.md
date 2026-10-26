# 色彩検定UC級 暗記カード プロジェクト（AI引き継ぎルール）

このファイルは、Antigravity（AIアシスタント）が次回以降のセッションで作業を即座に再開するための引き継ぎメモです。

## 1. 基本方針・コミュニケーション
- **必ず日本語で簡潔に応答すること。**
- ユーザーは色彩検定UC級（色のユニバーサルデザイン級）の受験対策をしており、自分の弱点問題だけをまとめた暗記カードWebアプリと問題データ（Excel / CSV）を育てている。

## 2. リポジトリ内の主要ファイル
- `index.html`:
  - サーバー不要・ブラウザで開くだけで動く暗記カードWebアプリ（Tailwind CSS CDN + SheetJS `xlsx.full.min.js` 使用）。
  - **常時ダークモード固定**、本文フォントサイズは **16px以上（`text-base` 〜 `text-2xl`）** のシンプルUI。
  - ヘッダー：タイトル（左に Material Symbols の `lightbulb` アイコン）、`再読込`（File System Access API + IndexedDB）、`QAファイル選択`。
  - ヘッダー下（背景・線なし）：カテゴリ絞り込み、`QA順 [ 設定のまま | シャッフル ]` スイッチ（シャッフルはカテゴリをまたがずカテゴリ内だけで並べ替え、押すたびにシャッフルし直し。QA一覧は資料用なので常に元の順）、`[ 問題 | QA一覧 ]` セグメントスイッチ。
  - カードの左右に `<` `>` ボタン。`>`（→ キー）は「解答を表示 → 次のカードへ」の2段階、`<`（← キー）は常に解答を隠した状態で前のカードへ。カード内に「解答を表示」ボタン。カード右上に `QUESTION N / 全数`（全数はカテゴリ絞り込み後の問題数）、カード下端に進み具合バー。
  - **不要な機能（復活させないこと）**：「解説」列、ライトモード切替、要復習/覚えた判定、弱点フィルタ、検索バー、学習記録リセット、テンプレートDL、QA貼り付け（Excel に保存されず紛らわしいため削除）。
- `my-weakness.xlsx`:
  - ユーザーの弱点データ。**GitHub で管理する（コミット対象）**。リポジトリは本人と同僚しか見ないため問題ない。同僚はこのファイルをそのまま使うか、別名で新規保存してカスタマイズして使う。
  - 列構成は **`カテゴリ, 問題, 解答`** の3列（A列: 160px, B列: 360px, C列: 500px、全セル折り返し表示 `home.wrapText: true`、1行目太字）。
- **配布用サンプル Excel（`sample-*.xlsx` など）は作らない。** `my-weakness.xlsx` がその役割を兼ねる。
- `index.html` の内蔵サンプルデータ（ファイル未読込時の初期表示用）の中身は、勝手に決めずユーザーと相談すること。

## 3. GridCraft との連携手順（MCP / CLI）
- `/usr/local/bin/gridcraft-cli` がインストール済み、`~/.gemini/config/mcp_config.json` にも登録済み。
- **GridCraft GUI をリモート操作モードで起動するコマンド**:
  ```bash
  nohup /Applications/GridCraft.app/Contents/MacOS/GridCraft --control 7979 /Users/hongoujun/Documents/GitHub/flashcards/my-weakness.xlsx >/dev/null 2>&1 &
  ```
- **起動中の GridCraft ウィンドウを操作するコマンド例**:
  ```bash
  # セルの書き込み
  gridcraft-cli send 7979 range.setValues '{"range":"A2","values":[["カテゴリ","問題","解答"]]}'
  # 折り返し表示と列幅設定
  gridcraft-cli send 7979 home.columnWidth '{"cols":"A:A","width":160}'
  gridcraft-cli send 7979 home.columnWidth '{"cols":"B:B","width":360}'
  gridcraft-cli send 7979 home.columnWidth '{"cols":"C:C","width":500}'
  gridcraft-cli send 7979 home.wrapText '{"range":"A1:C50","on":true}'
  # 保存とCSV変換
  gridcraft-cli send 7979 file.save '{}'
  gridcraft-cli convert /Users/hongoujun/Documents/GitHub/flashcards/my-weakness.xlsx /Users/hongoujun/Documents/GitHub/flashcards/my-weakness.csv
  ```
