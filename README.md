# Coding-Test-Submission
# Votee AI Tech Intern (Generalist) - Coding Test Submission

## 項目概覽
- 語言：Python + requests
- 功能：自動 Wordle solver，連接 Votee API 逐個猜字直到解到謎底
- 支持模式：
  - /daily：每日固定謎題，會累積歷史反饋嚟過濾（最推薦）
  - /random：每次都係全新隨機謎題，只用今次反饋過濾
  - /word/5 字母單詞

## 核心策略
- 開局用高資訊量嘅字：salet、crane 等（盡量一次排除最多可能性）
- 過濾規則：
  - correct（綠色）：呢個位一定要係呢個字母
  - present（黃色）：呢個字母一定要出現，但唔喺呢個位
  - absent（灰色）：呢個字母完全唔喺謎底入面

## 運行示例（daily 模式，實際輸出）
載入咗 14855 個 5 字母單詞
第 1 次: SALET → 剩 283 個可能
第 2 次: CRANE → 剩 25 個
第 3 次: CABLE → 剩 24 個
第 4 次: ILEAC → 剩 3 個
第 5 次: FECAL → 剩 2 個
第 6 次: DECAL → 成功！用咗 6 次

## 依賴 & 運行方法
- Python 3.x + requests
- words.txt：嚟自 https://gist.githubusercontent.com/dracos/dd0668f281e685bad51479e5acaadb93/raw （14855 個合法可猜單詞）
- 運行：python solver.py（MODE 可以喺 code 入面改 daily / word/5 字母單詞）

提交日期：2026年2月8日
