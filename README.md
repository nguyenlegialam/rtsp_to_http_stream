# Chuyển đổi rtsp stream thành http bằng cách cắt từng ảnh và stream lên web

Giải thích: Phương pháp này sử dụng cách cắt từng ảnh của luồng RTSP (bằng opencv) sau đó tạo luồng stream bằng và stream bằng Process và Threading (để tạo luồng cho nhiều camera)  
Điểm yếu: rất hao tốn tài nguyên server do phải xử lí phát luồng stream của nhiều camera, sử dụng như 1 biện pháp tạm thời hoặc nhà có ít camera
  
Yêu cầu:  
  - Link Rtsp của tất cả các camera trong nhà  
  - Máy tính được đặt chung mạng LAN hoặc VPN đến mạng LAN đó  
  - Cài đặt python >3.6 và các thư viện bên ngoài trong requirement  
  
Bước 1: Nhập địa chỉ IP rtsp cho từng camera  
![image](https://github.com/nguyenlegialam/rtsp_to_http_stream/assets/116132135/56dac0ab-8161-4014-ac7c-6327302d5045)

Bước 2: Tạo thêm manager  
![image](https://github.com/nguyenlegialam/rtsp_to_http_stream/assets/116132135/ea482c1c-9809-4c1f-802f-cb847ffe88da)

Bước 3: Tạo function cho các camera  
![image](https://github.com/nguyenlegialam/rtsp_to_http_stream/assets/116132135/4db478e5-3890-4431-bf00-5ee94e001bd7)

Bước 4: Thêm manager vào function stream  
![image](https://github.com/nguyenlegialam/rtsp_to_http_stream/assets/116132135/41b6cfae-fd32-41b2-883c-afe2590ff709)

Bước 5: Tạo url  
![image](https://github.com/nguyenlegialam/rtsp_to_http_stream/assets/116132135/5f273137-d5b3-4af9-8b9a-1ef9aa4cc9f9)

Bước 6: Thêm manager và function vào keepalive  
![image](https://github.com/nguyenlegialam/rtsp_to_http_stream/assets/116132135/f6c6b24d-f7ae-4f82-a819-d8b1e60f2e35)

