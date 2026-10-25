# 色彩検定UC級 暗記カード プロジェクト（AI引き継ぎルール）

このファイルは、Antigravity（AIアシスタント）が次回以降のセッションで作業を即座に再開するための引き継ぎメモです。

## 1. 基本方針・コミュニケーション
- **必ず日本語で簡潔に応答すること。**
- ユーザーは色彩検定UC級（色のユニバーサルデザイン級）の受験対策をしており、自分の弱点問題だけをまとめた暗記カードWebアプリと問題データ（Excel / CSV）を育てている。

## 2. リポジトリ内の主要ファイル
- `index.html`:
  - サーバー不要・ブラウザで開くだけで動く暗記カードWebアプリ（Tailwind CSS CDN + SheetJS `xlsx.full.min.js` 使用）。
  - **常時ダークモード固定**、本文フォントサイズは **16px以上（`text-base` 〜 `text-2xl`）** のシンプルUI。
  - 機能は最小限に絞っている（ヘッダー：カテゴリ絞り込み、ファイル選択、貼り付け、一覧切替 ／ 下部：前へ・次へ、クリック/スペースで解答表示）。
  - **不要な機能（復活させないこと）**：「解説」列、ライトモード切替、要復習/覚えた判定、弱点フィルタ、検索バー、シャッフル、学習記録リセット、テンプレートDL。
  - `<script type="text/plain" id="sample">` に最新の問題データ（CSV形式）を埋め込んでおり、更新時は `KEY`（例：`uc-flashcards-csv-v5` → `v6`）をインクリメントするとブラウザのリロードだけで最新データが反映される。
- `sample-uc-questions.xlsx`:
  - GridCraft / Excel 編集用のマスターファイル。
  - 列構成は **`カテゴリ, 問題, 解答`** の3列（A列: 160px, B列: 360px, C列: 500px、全セル折り返し表示 `home.wrapText: true`、1行目太字）。
  - `index.html` にそのままドラッグ＆ドロップして読み込むことも可能。
- `sample-uc-questions.csv`:
  - `sample-uc-questions.xlsx` と同期されたCSVファイル（`カテゴリ,問題,解答` の3列）。

## 3. GridCraft との連携手順（MCP / CLI）
- `/usr/local/bin/gridcraft-cli` がインストール済み、`~/.gemini/config/mcp_config.json` にも登録済み。
- **GridCraft GUI をリモート操作モードで起動するコマンド**:
  ```bash
  nohup /Applications/GridCraft.app/Contents/MacOS/GridCraft --control 7979 /Users/hongoujun/Documents/GitHub/flashcards/sample-uc-questions.xlsx >/dev/null 2>&1 &
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
  gridcraft-cli convert /Users/hongoujun/Documents/GitHub/flashcards/sample-uc-questions.xlsx /Users/hongoujun/Documents/GitHub/flashcards/sample-uc-questions.csv
  ```
- **ヘッドレス（GUIなし）で XLSX を更新・整形する場合**:
  ```bash
  gridcraft-cli run \
    --in /Users/hongoujun/Documents/GitHub/flashcards/sample-uc-questions.csv \
    --cmd 'home.columnWidth={"cols":"A:A","width":160}' \
    --cmd 'home.columnWidth={"cols":"B:B","width":360}' \
    --cmd 'home.columnWidth={"cols":"C:C","width":500}' \
    --cmd 'home.wrapText={"range":"A1:C50","on":true}' \
    --cmd 'home.bold={"range":"A1:C1","on":true}' \
    --out /Users/hongoujun/Documents/GitHub/flashcards/sample-uc-questions.xlsx
  ```

## 4. 問題追加・編集を頼まれたときの標準ワークフロー
1. `sample-uc-questions.xlsx`（および起動中ならポート7979のGridCraft）の行を更新・追加し、折り返し表示（`home.wrapText`）を適用して保存する。
2. `sample-uc-questions.csv` にも同じ内容を出力する。
3. `index.html` 内の `<script type="text/plain" id="sample">` も同じCSV内容に更新し、LocalStorage の `KEY` バージョン番号を `+1` して、ブラウザをリロードするだけで新しい問題セットが見えるようにする。
