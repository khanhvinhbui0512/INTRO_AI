# IntroAI
Trước hết để kết nối với Folder ở máy tính thì dùng lệnh 
```
$ git remote add origin https://github.com/khanhvinhbui0512/IntroAI.git
```
Sau đó dùng lệnh sau để cập nhật lại dữ liệu trên git xuống máy tính. 
```
$ git pull
```
Nhánh main là nhánh làm việc chính nên mọi người chỉ cập nhật lại nhánh này khi đã hoàn thiện xong file. Vì vậy mọi người cần phải tự tạo branch khi làm việc và cập nhật code trên nhánh của mình. Khi đã hoàn thiện thì cập nhật lại ở nhánh main. Cách để tạo nhánh là
```
$ git branch newbranch
```
Để chuyển sang nhánh "newbranch" thì ta dùng lệnh 
```
$ git checkout newbranch
```
Khi đổi nhánh thì dữ liệu cũng sẽ được cập nhật lại ở máy tính những vẫn nên cẩn thận khi chuyển nhánh dữ liệu.

Lệnh để cập nhật dữ liệu cho các nhánh (***Chú ý bắt buộc phải pull code trước push để tránh gây ra đụng độ và đặt tên cho mỗi lần commit để khi cần coi lại code hoặc sử dụng code cũ***) 
```
$ git add .
$ git commit -m "update" 
$ git pull
$ git push 
```