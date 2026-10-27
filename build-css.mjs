// tailwind.css から CSS を生成し、anki.html の <style id="tw"> に埋め込む
// 使い方: anki.html をコミットすると .githooks/pre-commit が自動で実行する（手動なら node build-css.mjs）
import { execSync } from 'node:child_process';
import { readFileSync, writeFileSync } from 'node:fs';

const HTML = new URL('./anki.html', import.meta.url);
const css = execSync('npx -y tailwindcss@3.4.17 -i tailwind.css --content ./anki.html --minify', {
  cwd: new URL('.', import.meta.url),
  stdio: ['ignore', 'pipe', 'ignore'],
}).toString().trim();

const html = readFileSync(HTML, 'utf8');
const re = /<style id="tw">[\s\S]*?<\/style>/;
if (!re.test(html)) throw new Error('anki.html に <style id="tw"> が見つかりません');
writeFileSync(HTML, html.replace(re, () => `<style id="tw">${css}</style>`));
console.log(`anki.html に CSS を埋め込みました（${css.length} bytes）`);
