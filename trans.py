#encoding:utf-8
import os
from sys import exit
from util import * ;
from time import sleep;

rootPath = os.getcwd()
cachePath = os.path.join(rootPath, 'cache') + "\\";
distPath = os.getcwd() + "\\dist\\";
logFile = rootPath + "\\log\\log"
recordPath = os.path.join(os.getcwd(), "log\\record"); # record地址
d = '\"'
ffmpeg = os.getcwd() + '\\ffmpeg.exe'
# src = getFiles(os.getcwd()+'\\cache', '.flv')[0]
os.system('chcp 65001')
isDirsExists(rootPath)

# 中英字符串
menuText = """
* type 'c' to rename files;
* type 'p' to load up player.
* type 'h' to change Langage(中文).
* paste URL to splite audio from video.
  (music.163.com, bilibili.com ...)
""";
menuText_zh = """
* 重命名文件（按“C”）
* 播放音乐（按“P”）
* 切换语言 English(type 'h')
* 转换音频（输入 URL 地址）
  (music.163.com, bilibili.com ...)
""";
urlInput = "paste url/type 'c'/type 'p'：";
urlInput_zh = "输入 URL 地址/按“C”/按“P”";
hintText = 'try again.';
hintText_zh = "再试一次";
e_download = 'download error';
scolText = ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>";
e_download_zh = '下载错误';
# 判断 lang = ？
flag_lang = '0';
with open('setting', 'r+', encoding='utf-8') as f:
    settingStr = str(f.readlines());
    if('zh' in settingStr): # 显示中文
        flag_lang = '1';
    elif 'en' in settingStr: # 默认英文
        flag_lang = '0';
    else:
        f.write('lang=en\n');
# 转换语言
if flag_lang == '0':
    menuText_zh = menuText;
    e_download_zh = e_download;
    hintText_zh = hintText;
    urlInput_zh = urlInput;

# -------------下载flv-----------------
isPipInstalled(rootPath)
isYgInstalled(rootPath)
# os.system('down.bat')
# you_get = os.getcwd() + "\\you-get.exe"
os.chdir('cache') # 工作目录移动到cache
print(menuText_zh);
url = input("-----> ") 
while not (url.startswith('htt') or url.startswith('www.') or '.com' in url):
    if(url == 'p'):
        play(rootPath, distPath, flag_lang);
        print(menuText_zh);
    elif url == 'c':
        flag = True;
        while flag:
            flag = chFileName(distPath, rootPath);
    elif url == 'h':
        setLang(rootPath, flag_lang);
    else:
         print(hintText_zh);
    url = input(urlInput_zh);
url = url.split('?')[0];
print('\033[1;31m currentDir= \033[0m' + os.getcwd());
videoFormat = "\t--format=flv360 ";

if ('163.com' in url):
    videoFormat = '\t';
    print(scolText);
    os.system("you-get" + videoFormat + d + url + d + "\t>" + logFile); # 保存log，保存文件名
os.system("you-get" + videoFormat + d + url + d + "\t>" + logFile); # 保存log，保存文件名
with open(logFile, 'r', encoding='utf-8') as f:
    lst = f.readlines();
    if lst == []:
        print(e_download_zh);
        exit(0);
# mp3List = []
# mp3List_old = os.listdir(distPath);
# for item in mp3List_old:
    # if item.endswith('mp3'):
        # mp3List.append(item)
fileNameList = os.listdir(cachePath);
if(isMp3Exist(rootPath, logFile)):
    print("the file exists. ");
    # os.system('pause');
    exit(0);
timestampStr = writeNameRecord(rootPath, logFile, fileNameList); # 已下载记录
print('\033[1;31m timestampStr=\033[0m', timestampStr);
if timestampStr == '':
    print('timestampStr error');
    exit();
    
# command = you_get + " --format=flv360 " + url + " >log"
# os.popen(command, 'w')

# -------------转换成音频-------------
os.chdir(rootPath)
print('\033[1;31m currentDir= \033[0m', os.getcwd());
srcName = getName(recordPath, timestampStr); # 获取flv文件名
src_old = cachePath + srcName + '.flv'; # 旧flv文件地址
src = cachePath + timestampStr + '.flv';
print('\033[1;31m src_old= \033[0m' + src_old);
print('\033[1;31m src= \033[0m'  + src);
os.rename(src_old, src);
dst_1 = d + cachePath + "temp.m4a" + d; # m4a文件地址
# dst_2 = d + distPath + src.split('\\')[-1] + ".mp3" + d
dst_2 = d + distPath + srcName + ".mp3" + d; # mp3文件地址
print('\033[1;31m mp3 address= \033[0m', dst_2);
os.system(ffmpeg + " -i " + d + src + d + " -acodec copy -vn " + dst_1) # -------m4a
os.rename(src, src_old) # flv改回原来的文件名
os.system(ffmpeg + " -i " + dst_1 + "\t" + dst_2); # ------------mp3

# -------------清除cache---------------
os.chdir(cachePath);
cl_1 = "temp.m4a"
# cl_2 = rootPath + "\\log\\log"
os.remove(cl_1)
# os.remove(cl_2)