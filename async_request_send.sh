ab -t 5 -g responses.txt -v 4  -n 100 -c 100 -p image_medium2.jpg -T 'application/octet-stream' -H 'Content-Type: application/octet-stream' -T 'multipart/form-data' http://172.17.0.52:6060/predictions/yolov8n 
