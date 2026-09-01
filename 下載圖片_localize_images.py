#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
下載 Weebly 圖片並在地化 (localize images)
=================================================
把歷史刊物頁面裡連到 temsnewsletter.weebly.com 的圖片，全部下載到
assets/img/legacy/，並把所有 .html 內的網址改成本機相對路徑。
如此一來，Weebly 9/27 關站後圖片仍可正常顯示。

用法（在 Mac 上）:
    1. 打開「終端機」(Terminal)
    2. cd 到本資料夾，例如：
         cd "/Users/ricklin/Dropbox/Work/Medical Director/急診醫學會緊急救護委員會/Newsletter/TEMS-website"
    3. 執行：
         python3 下載圖片_localize_images.py

需要網路。只用 Python 內建模組，Mac 內建的 python3 即可。
可重複執行：已下載的圖會略過；下載失敗的圖會保留原本的 Weebly 連結，頁面仍可顯示。
"""

import os, re, sys, glob, time, urllib.request, urllib.error

BASE   = os.path.dirname(os.path.abspath(__file__))
IMGDIR = os.path.join(BASE, "assets", "img", "legacy")
DOMAIN = "https://temsnewsletter.weebly.com"
# 抓 weebly 的 /uploads 或 /files 圖片網址（可含 ?快取參數）
URL_RE = re.compile(r'https://temsnewsletter\.weebly\.com(/(?:uploads|files)/[^"\'\)\s]+)')
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
      "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36")

def local_name(path_no_query):
    """把 /uploads/1/4/4/7/144761285/xxx/yyy.png 轉成安全的本機檔名。"""
    p = re.sub(r'^/uploads/\d+/\d+/\d+/\d+/\d+/', '', path_no_query)  # 去掉固定前綴
    p = p.lstrip('/')
    p = re.sub(r'[^\w.\-]', '__', p)   # 斜線等改成 __
    return p or "img"

def download(url, dest):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as r:
        data = r.read()
    if not data:
        raise ValueError("空檔案")
    with open(dest, "wb") as f:
        f.write(data)
    return len(data)

def main():
    os.makedirs(IMGDIR, exist_ok=True)
    html_files = glob.glob(os.path.join(BASE, "**", "*.html"), recursive=True)

    # 1) 蒐集所有唯一圖片網址
    url_to_name = {}   # 完整網址(含query) -> 本機檔名
    for hf in html_files:
        txt = open(hf, encoding="utf-8").read()
        for m in URL_RE.finditer(txt):
            full = m.group(0)
            path = m.group(1).split("?")[0]
            url_to_name[full] = local_name(path)

    if not url_to_name:
        print("沒有找到任何 Weebly 圖片連結，或圖片已全部在地化。")
        return

    print(f"找到 {len(url_to_name)} 張待下載圖片，開始下載到 {IMGDIR}\n")

    # 2) 下載
    ok, failed = {}, {}
    for i, (full, name) in enumerate(sorted(url_to_name.items()), 1):
        dest = os.path.join(IMGDIR, name)
        if os.path.exists(dest) and os.path.getsize(dest) > 0:
            ok[full] = name
            print(f"[{i}/{len(url_to_name)}] 已存在，略過 {name}")
            continue
        url = full  # 保留 query，weebly 需要
        for attempt in range(3):
            try:
                size = download(url, dest)
                ok[full] = name
                print(f"[{i}/{len(url_to_name)}] OK  {name}  ({size//1024} KB)")
                break
            except Exception as e:
                if attempt == 2:
                    failed[full] = str(e)
                    print(f"[{i}/{len(url_to_name)}] 失敗 {name} -> {e}")
                else:
                    time.sleep(1.5)

    # 3) 改寫 HTML（只改成功下載的；失敗的保留 weebly 連結，頁面仍能顯示）
    total_repl = 0
    for hf in html_files:
        txt = open(hf, encoding="utf-8").read()
        orig = txt
        def repl(m):
            full = m.group(0)
            if full in ok:
                # issues/ 內的頁面用 ../ ；根目錄的頁面用 ./
                rel = os.path.relpath(IMGDIR, os.path.dirname(hf)).replace(os.sep, "/")
                return f"{rel}/{ok[full]}"
            return full
        txt = URL_RE.sub(repl, txt)
        if txt != orig:
            open(hf, "w", encoding="utf-8").write(txt)
            n = orig.count("temsnewsletter.weebly.com/uploads") - txt.count("temsnewsletter.weebly.com/uploads")
            total_repl += n
            print(f"改寫 {os.path.relpath(hf, BASE)}：{n} 處")

    print("\n================ 完成 ================")
    print(f"成功下載/存在：{len(ok)} 張")
    print(f"改寫連結：約 {total_repl} 處")
    if failed:
        print(f"\n下載失敗 {len(failed)} 張（頁面仍保留 Weebly 連結，可稍後重跑本程式再試）：")
        for u, e in failed.items():
            print(f"  - {u}  ({e})")
    else:
        print("全部圖片已在地化，之後不再依賴 Weebly。")

if __name__ == "__main__":
    main()
