# 問題を更新して公開する: my-weakness.xlsx → CSV を作り直し → コミット → push（GitHub Pages に反映）
# 使い方: python3 publish.py （Windows は py publish.py）。コミットメッセージを変えたいときは python3 publish.py "メッセージ"
import os, subprocess, sys

DIR = os.path.dirname(os.path.abspath(__file__))
git = lambda *args, **kw: subprocess.run(['git', *args], cwd=DIR, **kw)

# anki.html のコミット時に CSS を自動生成するフックを有効にしておく（.githooks/pre-commit）
git('config', 'core.hooksPath', '.githooks')

subprocess.run([sys.executable, os.path.join(DIR, 'build-csv.py')], check=True)
git('add', 'my-weakness.xlsx', 'my-weakness.csv', check=True)
if git('diff', '--cached', '--quiet', 'my-weakness.xlsx', 'my-weakness.csv').returncode == 0:
    print('問題データに変更はありません')
    sys.exit(0)
msg = sys.argv[1] if len(sys.argv) > 1 else 'Update questions'
git('commit', '-m', msg, '--', 'my-weakness.xlsx', 'my-weakness.csv', check=True)
git('push', check=True)
print('push しました。数分で GitHub Pages に反映されます')
