# steam 遊戲查詢機器人

![](https://i.imgur.com/m2UBMj2.png)
## 功能 
主要功能有兩項
第一項為查詢遊戲的資訊
第二項為查詢遊戲的價格與歷史最低價格

### 遊戲資訊
直接從steam的頁面爬取

### 價格資訊
利用第3方網站isThereAnyDeal所提供的API來獲取打折的%數

因為isThereAnyDeal上沒有台灣區遊戲的定價

所以爬取steam商店頁面上的價格再利用獲得的折扣%數來計算最後價格

## isThereAnyDeal API
要先去申請並建立app後 拿到app的key後才能使用
![](https://i.imgur.com/VPEp2X8.jpg)


[API文件](https://itad.docs.apiary.io/#)

[網站app 註冊頁面](https://new.isthereanydeal.com/apps/create/)
