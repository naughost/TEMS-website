# 設定 GitHub 自動部署 ＋ Cloudflare 流量分析

這份說明帶你完成兩件事：
1. **GitHub 自動部署** — 之後檔案一更新，網站就自動上線，不必再手動拖資料夾。
2. **Cloudflare Web Analytics** — 免費看每一期的點閱與流量。

> 我（Claude）已先幫你把能做的都做好了：Cloudflare 程式碼已加進全部 24 個頁面、Netlify 設定檔（`netlify.toml`）、`.gitignore` 都已就緒。你只需要照下面步驟完成需要你帳號登入的部分。

---

## ⚠️ 開始前：先刪掉一個資料夾

我在沙盒裡嘗試建立 git 時，因為 Dropbox 同步限制留下了一個壞掉的資料夾。請先刪除它：

- 打開 Finder 進到 `TEMS-website` 資料夾，找到名為 **`_git_broken_DELETE_ME`** 的資料夾，直接拖到垃圾桶。
- （若沒看到也沒關係，代表已經不存在。）

---

## 第一部分：GitHub 自動部署

用 **GitHub Desktop**（圖形介面，不必打指令），對非工程背景最友善。

### 步驟 1：安裝並登入 GitHub Desktop
1. 到 <https://desktop.github.com> 下載並安裝 GitHub Desktop。
2. 打開後用你的 GitHub 帳號登入（沒有帳號就先到 <https://github.com> 免費註冊一個）。

### 步驟 2：把網站資料夾變成一個 repository
1. GitHub Desktop 上方選 **File → Add Local Repository**。
2. 選擇資料夾：`.../Newsletter/TEMS-website`。
3. 它會說「this directory does not appear to be a Git repository」，點下方藍字 **create a repository**。
4. 名稱填 `tems-newsletter`（或你喜歡的），按 **Create Repository**。

### 步驟 3：發佈到 GitHub
1. 按右上角 **Publish repository**。
2. 建議**取消勾選** “Keep this code private”（若希望公開）；要保持私密就維持勾選（Netlify 兩者都支援）。
3. 按 **Publish Repository**。完成後，你的網站原始碼就在 GitHub 上了。

### 步驟 4：把 Netlify 改成「連 GitHub 自動部署」
1. 登入 <https://app.netlify.com>，進到你現在這個網站（tems-newsletter）。
2. 左側 **Site configuration → Build & deploy → Continuous deployment**。
3. 在 **Repository** 區塊按 **Link repository**（或 “Manage repository”）。
4. 選 **GitHub**，授權後選剛剛發佈的 `tems-newsletter`。
5. 部署設定（`netlify.toml` 已幫你填好，通常會自動帶入）：
   - **Base directory**：留空
   - **Build command**：留空
   - **Publish directory**：`.`（一個點）
6. 按 **Deploy / Save**。

完成後，**以後只要在 GitHub Desktop 按 Commit → Push，網站就自動更新**，不用再手動拖資料夾。

> 之後每兩個月更新流程：把新一期 Word 丟給我 → 我幫你做好頁面與圖片並更新首頁 → 你在 GitHub Desktop 按 **Commit to main** 再按 **Push origin** → 幾十秒後自動上線。

---

## 第二部分：Cloudflare Web Analytics（免費）

程式碼我已加進所有頁面，只差你去申請一組專屬 **token** 貼上。

### 步驟 1：取得 token
1. 到 <https://dash.cloudflare.com> 註冊/登入（免費，不需要把網域轉到 Cloudflare）。
2. 左側選 **Analytics & Logs → Web Analytics**（或搜尋 “Web Analytics”）。
3. 按 **Add a site**，Hostname 填 `tems-newsletter.netlify.app`（若日後換自訂網域再新增）。
4. 它會給你一段程式碼，裡面有 `data-cf-beacon='{"token": "xxxxxxxx..."}'`。**複製那串 token**（引號中間那串英數字）。

### 步驟 2：把 token 給我
把那串 token 貼給我，我會一次替換掉全部 24 個頁面裡的 `PASTE_YOUR_CLOUDFLARE_TOKEN_HERE`，你再 Push 上線即可。

> 也可以自己改：用文字編輯器打開每個 `.html`，把 `PASTE_YOUR_CLOUDFLARE_TOKEN_HERE` 換成你的 token。但頁面很多，交給我做比較快。

### 步驟 3：看報表
上線約 24 小時後，回到 Cloudflare 的 Web Analytics 就能看到：總瀏覽量、每個網址（＝每一期）的點閱數、來源、國家、裝置等。完全免費、不需 Cookie 同意條。

---

## 常見問題

- **會不會影響現在的網站？** 不會。連上 GitHub 後，Netlify 只是改成「從 GitHub 抓檔案」，網址、內容都不變。
- **舊的手動部署還能用嗎？** 連上 GitHub 後就以 GitHub 為準，不必再手動拖，但仍可隨時在 Netlify 後台手動觸發重新部署。
- **Cloudflare 沒填 token 會怎樣？** 頁面一切正常，只是分析不會記錄，等填了 token 就會開始統計。
