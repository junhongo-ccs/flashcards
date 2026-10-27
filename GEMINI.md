# 色彩検定UC級 暗記カード プロジェクト（AI引き継ぎルール）

このファイルは、Antigravity（AIアシスタント）が次回以降のセッションで作業を即座に再開するための引き継ぎメモです。

## 1. 基本方針・コミュニケーション
- **必ず日本語で簡潔に応答すること。**
- ユーザーは色彩検定UC級（色のユニバーサルデザイン級）の受験対策をしており、自分の弱点問題だけをまとめた暗記カードWebアプリと問題データ（Excel / CSV）を育てている。

## 0. Mac 側でやること（Windows 側からの申し送り）
- [ ] **Git フックを有効にする**（2026-10-27 に追加。Windows 側は設定済み）。`git pull` のあと、リポジトリで一度だけ `git config core.hooksPath .githooks` を実行する（`python3 publish.py` を一度実行しても有効になる）。`git config core.hooksPath` が `.githooks` を返せば完了。これで `anki.html` をコミットすると埋め込み CSS が自動で作り直される（詳細は下の `anki.html` の項）。終わったらこの項目を消すこと。

## 2. リポジトリ内の主要ファイル
- `anki.html`（**同僚に渡す版**。ローカルでファイルを開くだけで動く PC 向け）:
  - サーバー不要・ブラウザで開くだけで動く暗記カードWebアプリ（SheetJS `xlsx.full.min.js` 使用）。
  - **Tailwind CSS は CDN を使わず、生成済み CSS を `<style id="tw">` に埋め込んでいる**（拡張機能などで CDN がブロックされる環境でも崩れないように）。元の定義は `tailwind.css`。**anki.html をコミットすると Git フック（`.githooks/pre-commit`）が `node build-css.mjs` を自動実行して CSS を作り直し、一緒にコミットする**（node と、初回はネット接続が必要）。フックは各マシンで一度 `git config core.hooksPath .githooks` を実行すると有効になる（`publish.py` を実行しても自動で有効になる）。コミット前に画面で確認したいときは手動で `node build-css.mjs`。
  - **アイコンはアイコンフォントを使わず、Material Symbols（Outlined, weight 400）の SVG を直接埋め込んでいる**（`<svg class="inline-block w-[20px] h-[20px] ..." viewBox="0 -960 960 960" fill="currentColor">`、色は `text-*` で指定）。新しいアイコンは `https://cdn.jsdelivr.net/npm/@material-symbols/svg-400@0.48.1/outlined/<名前>.svg` の path をコピーして使う。
  - **常時ダークモード固定**、本文フォントサイズは **16px以上（`text-base` 〜 `text-2xl`）** のシンプルUI。
  - ヘッダー：タイトル（左に `lightbulb` アイコン）、`再読込`（File System Access API + IndexedDB）、`QAファイル選択`。
  - ヘッダー下（背景・線なし）：カテゴリ絞り込み、`QA順 [ 設定のまま | シャッフル ]` スイッチ（シャッフルはカテゴリをまたがずカテゴリ内だけで並べ替え、押すたびにシャッフルし直し。QA一覧は資料用なので常に元の順）、`[ 問題 | QA一覧 ]` セグメントスイッチ。
  - カードの左右に `<` `>` ボタン。`>`（→ キー）は「解答を表示 → 次のカードへ」の2段階、`<`（← キー）は常に解答を隠した状態で前のカードへ。カード内に「解答を表示」ボタン。カード右上に `QUESTION N / 全数`（全数はカテゴリ絞り込み後の問題数）、カード下端に進み具合バー。
  - **不要な機能（復活させないこと）**：「解説」列、ライトモード切替、要復習/覚えた判定、弱点フィルタ、検索バー、学習記録リセット、テンプレートDL、QA貼り付け（Excel に保存されず紛らわしいため削除）。
- `index.html`（**自分用の GitHub Pages 版**。`https://junhongo-ccs.github.io/flashcards/`）:
  - **スマホ横持ち（Android にインストールして全画面）に最適化**。カードは上に問題・下に解答の上下配置。ホーム画面に追加して使う PWA（`manifest.webmanifest`、アイコン `icon-*.png`）。
  - 問題はリポジトリの `my-weakness.csv` を毎回取得（push すれば最新になる）。**ファイル選択・再読込・ドロップは無い**（不要）。
  - オフライン対応（`sw.js`：ネット優先、取れなければ保存済みを使う）。前回のカテゴリ・順番・問題位置から再開（localStorage）。
  - 操作：カードをタップ / `>` / 左スワイプ＝「解答を表示 → 次へ」、`<` / 右スワイプ＝前へ。
  - Tailwind は CDN（`https://cdn.tailwindcss.com/3.4.17`）のままでよい（自分しか使わないため。anki.html と違い埋め込み不要）。
  - `sw.js` のキャッシュに入れるファイルを増やしたら、`CACHE` の名前（`uc-flashcards-v1`）を上げる。
- `my-weakness.xlsx`:
  - ユーザーの弱点データ。**GitHub で管理する（コミット対象）**。リポジトリは公開（誰が見てもよいとユーザー確認済み）。同僚はこのファイルをそのまま使うか、別名で新規保存してカスタマイズして使う。
  - 列構成は **`カテゴリ, 問題, 解答`** の3列（A列: 160px, B列: 360px, C列: 500px、全セル折り返し表示 `home.wrapText: true`、1行目太字）。
  - **`my-weakness.csv` も xlsx と一緒にコミットして管理する**（同僚が Excel なしでも使え、GitHub 上で差分も読める）。CSV は自動では更新されないので、**xlsx を編集したら毎回 `python3 publish.py` を実行すること**（CSV 作り直し → xlsx と CSV だけコミット → push まで行い、GitHub Pages 版に反映される。CSV だけ作りたいときは `python3 build-csv.py`）（UTF-8・BOM なし・LF 改行）。
- **配布用サンプル Excel（`sample-*.xlsx` など）は作らない。** `my-weakness.xlsx` がその役割を兼ねる。
- `anki.html` の内蔵サンプルデータ（ファイル未読込時の初期表示用）の中身は、勝手に決めずユーザーと相談すること。

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
