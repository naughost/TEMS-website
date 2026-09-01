# TEMS Newsletter 每期更新 SOP（一頁備忘）

雙月刊，每兩個月一期。網站：**https://tems-newsletter.netlify.app**

---

## 每期流程（4 步）

**1. 你：把稿件交給 Claude**
- 給該期的 Word 檔（圖片直接嵌在 Word 裡即可，Claude 會自動抽出）。
- 一句話交代這期有哪些單元、誰是責任編輯（若和上期不同）。

**2. Claude：校稿 + 做頁面（你不用動手）**
- 校對錯字、夾雜英文、編號與標點一致性，並列出修正給你確認。
- 產生 `issues/YYYY-MM.html`（沿用固定版型與樣式）。
- 圖片存到 `assets/img/`，命名 `YYYY-MM-說明.png`。
- 更新首頁 `index.html`：最新一期卡片、歷期列表、近期活動。
- 每頁自動帶入 Cloudflare 分析碼。

**3. 你：在 GitHub Desktop 送出**
- 打開 GitHub Desktop，會看到一批修改的檔案。
- 左下 Summary 打一句（例如「新增 2026 年 8 月刊」）→ 按 **Commit to main** → 按 **Push origin**。

**4. 自動上線**
- Netlify 幾十秒後自動部署完成，網址不變。
- 上線後可自己開網頁捲一遍確認圖片與排版。

---

## 檔名與慣例

- 每期頁面：`issues/YYYY-MM.html`（例：`issues/2026-08.html`，用兩位數月份）。
- 圖片：放 `assets/img/`，命名 `YYYY-MM-用途.png`（例：`2026-08-blood-drill.png`）。
- 版型有四種常用單元標籤：`立場聲明`、`新知分享`、`人物訪談`／`發展紀實`、`好書報報`／`近期活動`；空白範本在 `issues/_範本.html`。

---

## 看流量（Cloudflare Web Analytics）

- 到 <https://dash.cloudflare.com> → 左側 **Analytics & Logs → Web Analytics** → 選 `tems-newsletter.netlify.app`。
- 可看整體與**每一期網址**的瀏覽數、來源、國家、裝置。免費、不需 Cookie 同意。
- 數據約每期上線後幾小時開始累積。

---

## 注意事項

- **不要**直接在 Netlify 用「拖曳資料夾」上傳了——現在一律走 GitHub。手動拖曳會和自動部署打架。
- 歷史各期（2023–2026/6）的圖片已在地化到 `assets/img/legacy/`，不依賴任何外部網站。
- 若首頁「近期活動」有過期活動，做新一期時順手請 Claude 一併更新。
- 資料夾內若還留著 `_git_broken_DELETE_ME`，可直接刪除（無用殘留）。

---

## 出問題時

- 部署失敗：到 Netlify → 該專案 → **Deploys** 看最新一筆的紅字錯誤訊息，截圖給 Claude。
- 圖片沒出來：多半是檔名大小寫或路徑不符；把該頁檔名和圖片檔名給 Claude 對一下。
- 其他：把畫面截圖或錯誤訊息貼給 Claude 即可。
