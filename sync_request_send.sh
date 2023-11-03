while true; do 
    echo "\nSending "
    date
    time curl http://172.17.0.52:8080/predictions/resnet18 -T image_medium2.jpg
    sleep 5
done  
