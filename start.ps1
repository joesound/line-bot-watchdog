# Start the first Python server
Start-Process python -ArgumentList "" # D:\sideproject\line-app-by\app.py 參考範例 需要包含檔案名稱

# Wait for the first server to start (adjust the sleep time if needed)
Start-Sleep -Seconds 5

# Start the second Python server
Start-Process python -ArgumentList "" #D:\sideproject\line-app-by\dirwatchq.py 參考範例 需要包含檔案名稱