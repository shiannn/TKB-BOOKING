### TKB CHROME DRIVER BOOKING
0.  填上 access.json
    -   "USERID": "身份證字號",
    -   "PASSWORD": "密碼",
    -   "DRIVERLOCATION": "chromedriver路徑"

1.  填上 config.json
    -   "course": "預訂課程"
    -   "date": "日期"
    -   "position": "場次"
    
2.  手動執行訂位
    -   python3.6 driver_parser.py
3.  使用 scheduler 在背景執行，於時間(11:50), (23:50)到時自動訂位
    -   python3.6 driver_parser.py -s &