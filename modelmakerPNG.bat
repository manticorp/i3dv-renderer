echo %1
IF "%2"=="" (set /p color="What colour would you like the background (format #ABCDEF)?") ELSE (set color=%2%)
IF "%color%"=="" (set color="#00FF00")
echo Color equals %color%
@Echo OFF
Set "AbsolutePath=%1%"
for /f "delims=" %%A in (%AbsolutePath%) do (
    set foldername=%%~nxA
)
Echo Folder 1 : %foldername%
IF "%foldername%"=="" (GOTO NoFolder) ELSE (GOTO GotFolder)
:NoFolder
set "AbsolutePath=%AbsolutePath:\= %"
FOR %%# in (%AbsolutePath%) do (
    Set "LastFolder=%%#"
)
Echo Folder 2 : %LastFolder%
:GotFolder
md %1\videos
mogrify -background "%color%" -flatten -verbose -format jpg %1\*.png
copy /y %1\%LastFolder%0149.jpg %1\videos\thumb.jpg
ffmpeg -y -f image2 -r 25 -i %1\%LastFolder%%%04d.jpg -c:v libvpx  -g 36 -b:v 1.5M -r 25 -s 960x960 %1\videos\960.webm
ffmpeg -y -f image2 -r 25 -i %1\%LastFolder%%%04d.jpg -c:v libx264 -g 36 -b:v 1.5M -r 25 -s 960x960 %1\videos\960.mp4
ffmpeg -y -f image2 -r 25 -i %1\%LastFolder%%%04d.jpg -c:v libvpx  -g 36 -b:v 1M   -r 25 -s 720x720 %1\videos\720.webm
ffmpeg -y -f image2 -r 25 -i %1\%LastFolder%%%04d.jpg -c:v libx264 -g 36 -b:v 1M   -r 25 -s 720x720 %1\videos\720.mp4
ffmpeg -y -f image2 -r 25 -i %1\%LastFolder%%%04d.jpg -c:v libvpx  -g 36 -b:v 0.5M -r 25 -s 360x360 %1\videos\360.webm
ffmpeg -y -f image2 -r 25 -i %1\%LastFolder%%%04d.jpg -c:v libx264 -g 36 -b:v 0.5M -r 25 -s 360x360 %1\videos\360.mp4
md %1\sprites
md %1\sprites\960
Echo Now doing montage...
cd %1
move *.jpg sprites
cd sprites
montage *.jpg -verbose -tile 36x1 -geometry +0+0 960/sprite.jpg
md 720
md 460
md 380
xcopy 960 720 /s /y /i
xcopy 960 460 /s /y /i
xcopy 960 380 /s /y /i
cd 380
mogrify -quality 75 -verbose -resize x380 *.jpg
cd ..
cd 460
mogrify -quality 75 -verbose -resize x460 *.jpg
cd ..
cd 720
mogrify -quality 75 -verbose -resize x720 *.jpg
cd ..
cd 960
mogrify -quality 75 -verbose *.jpg
cd ..
DEL *.jpg /F /Q
cd ..
DEL *.png /F /Q
ECHO FINISHED
pause