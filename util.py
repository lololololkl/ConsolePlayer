#encoding=utf-8

import time;
import os;
from pygame import mixer ;
os.system('cls');
import time;
from mutagen.mp3 import MP3;
from sys import exit;
from random import randint;

# 获得文件名 1
def getFiles(path, suffix):
    return [os.path.join(root, file) for root, dirs, files in os.walk(path) for file in files if file.endswith(suffix)]
# 获得文件名 2 （根据timestampStr获取
def getName(recordPath, timestampStr): 
    # recordPath = os.getcwd() + "\\cache\\log"
    sperater = ':f90e3s8e0x;'
    file = open(recordPath, mode='r', encoding='utf-8');
    log = file.readlines(); # log: 整个record文件内容 list类型
    # name = log[1].replace("title:               ", '').replace('\n', '');
    for name in log: # name: log的每一行
        if timestampStr in name:
            name = name.split(sperater)[1].replace('\n', '').replace('.flv', '');
            print('\033[1;31m name=\033[0m', name);
            file.close()
            return name;
    name = name.split(sperater)[1].replace('\n', '').replace('.flv', '');
    file.close()
    return name;
# 检查是否已经下载到缓存目录
# 写入log\record，保存最后的下载记录，
# 返回当时的timestampStr或已经存在的对应的timestampStr
def writeNameRecord(rootPath, logFile, cacheFileList):
    # print(cacheFileList[seq]);
    # rootPath = os.getcwd();
    recordPath = rootPath + r"\log\record"
    file = open(recordPath, 'r+', encoding='utf-8');
    sperater = ':f90e3s8e0x;' #分隔符
    recordList = file.readlines();  # 所有已经存在的记录  
    timestampStr = '';
    # 读取下载记录logFile
    log = open(logFile, 'r', encoding='utf-8');
    logList = log.readlines();
    # flvName = logList[10].replace('Downloading', '').replace('.cmt.xml', '').replace('\n', '').replace('...', '').strip(); # 下载文件名
    sub_strict = str(logList).index('--format=');
    logList_refilted = str(logList)[sub_strict:];
    subf = str(logList_refilted).index('Downloading');
    subs = str(logList_refilted).index('...');
    flvName = str(logList_refilted)[subf : subs].replace('Downloading', '').replace('.cmt.xml', '').replace('.flv', '').strip();
    print('\033[1;31m flvName(from util.writeNameRecord)=\033[0m'+flvName);
    log.close();
    for item in recordList:
        if(flvName in item): # 文件记录是否存在，是则返回对应的timestampStr
            timestampStr = item.split(sperater)[0]; 
            print('\033[1;31m file exists in record. \033[0m'); 
            file.close();
            return timestampStr;
    # timestampStr = recordList[-1].split(sperater)[0]; # 最后一条记录
    # print(recordList);
    # cacheFileList = os.listdir(os.path.join(rootPath, 'cache')) 
    
    for index in range(0, len(cacheFileList)):
        
        fileName = cacheFileList[index];
        isFormatRight = fileName.endswith('.flv') or fileName.endswith('.mp4');
        # 文件记录不存在 recordList 中则写入记录
        if (isFormatRight and fileName not in str(recordList)) : 
            timestampStr = str(int(time.time()));
            file.write(timestampStr + sperater +  fileName + '\n'); 
            print('\033[1;31m file not exist. \033[0m');
            file.close();
            return timestampStr;
    file.close();
    return timestampStr;
# 音频文件已经存在
def isMp3Exist(rootPath, logFile):
    recordPath = rootPath + r"\log\record"
    file = open(recordPath, 'r', encoding='utf-8');
    # sperater = ':f90e3s8e0x;' #分隔符
    # 读取旧的log
    recordList = file.readlines();    
    # 读取下载记录logFile
    log = open(logFile, 'r', encoding='utf-8');
    logList = log.readlines();
    # flvName = logList[10].replace('Downloading', '').replace('.cmt.xml', '').replace('\n', '').replace('...', '').strip(); # 下载文件名
    sub_strict = str(logList).index('--format=');
    logList = str(logList)[sub_strict:];
    subf = logList.index('Downloading');
    subs = logList.index('...');
    flvName = logList[subf : subs].replace('Downloading', '').replace('.cmt.xml', '').replace('.flv', '').strip();
    print('\033[1;31m flvName(from util.isMp3Exist)=\033[0m'+flvName);
    log.close();
    if (flvName in str(recordList)): # 音频文件名已经存在record记录中
        return True;
    return False;
# 修改文件名
def chFileName(distPath, rootPath):
    fileList_old = os.listdir(distPath);
    fileList = [];
    for item in fileList_old:
        if item.endswith('.mp3'):
            fileList.append(item);
    print('id\t' + 'Name');
    for index in range(len(fileList)):
        print( str(index) + '\t' + fileList[index].replace('.mp3', ''));
    print("select one/type 'e' to exit/type 'del [id] to delete one. ");
    id = '';
    while (not id.isdigit() or int(id)>len(fileList)):
        id = input("select id: ");
        if id == 'e':
            return False;
    if (id.startswith('del ')):
        id = int(id.split(' ')[1]);
        os.remove(distPath + fileList[id]);
        print("delete succeeded. ")
        return;
    src = os.path.join(distPath, fileList[int(id)]);
    print(src.split('\\')[-1] + " is selected");    
    dst = ".mp3";
    while dst.startswith('.mp3'):
        dst = input("change to: ") + ".mp3";
    fileName = dst.replace('.mp3', '');
    dst = os.path.join(distPath, dst);
    os.rename(src, dst);
    # 写入记录
    recordPath = rootPath + r"\log\record"
    file = open(recordPath, 'a', encoding='utf-8');
    sperater = ':f90e3s8e0x;' #分隔符
    timestampStr = str(int(time.time()));
    file.write(timestampStr + sperater +  fileName + sperater + '\tdeleted' '\n');
    file.close();
# you-get 是否安装
# def isYgInstalled(rootPath):
    # # packages_list 是否存在
    # if (os.path.exists(rootPath + '\\log\\packages_list')) == False:
        # os.system('python -m pip list >' + rootPath + '\\log\\packages_list');
    # elif(open(rootPath + '\\log\\packages_list', 'r').readlines()==[]):
        # os.system('python -m pip list >' + rootPath + '\\log\\packages_list');
    # # setting是否存在
    # if(os.path.exists(rootPath + '\\setting') == False):
        # # you-get 是否已经安装
        # if 'you-get' in str(open(rootPath + '\\log\\packages_list', 'r').readlines()):
            # file = open(rootPath + '\\setting', 'w', encoding='utf-8');
            # file.write('isYgInstalled=1')
            # file.close();    
            # return;
        # else:
            # print("you-get lib does not installed. ");
            # os.system("python -m pip install you-get -i https://pypi.douban.com/simple");
            
    # else:
        # file = open(rootPath + '\\setting', 'r');
        # if(file.readlines()[0].split('=')[1] == '1'): 
            # return;
# def isPipInstalled(rootPath):
    # pipLogPath = rootPath + '\\log\\pip_ver'
    # if os.path.exists(rootPath + '\\setting'):
        # with open(rootPath + '\\setting') as f:
            # str_0 = f.readlines();
            # if('isPipInstalled=1' in str_0):
                # return;
    # if not os.path.exists(pipLogPath):
        # os.system('pip -V >' + pipLogPath);
        # f = open(pipLogPath, 'r', encoding='utf-8');
        # lst_0 = f.readlines();
        # f.close();
        # if 'from' in str(lst_0):
            # f = open(rootPath + '\\setting', 'r+', encoding='utf-8');
            # lst_1 = f.readlines();
            # str_1 = str(lst_1);
            # if('isPipInstalled=1' in str_1):
                # pass;
            # else:
                # f.write('isPipInstalled=1\n');
                # f.close();
        # else:
            # print('pip not installed');
def isPipInstalled(rootPath):
    pipLogPath = rootPath + '\\log\\pip_ver';
    def InnerFunction():
        if not os.path.exists(pipLogPath): # pipLogPath 不存在
            os.system('pip -V >' + pipLogPath);
            f = open(pipLogPath, 'r', encoding='utf-8');
            lst_0 = f.readlines();
            f.close();
            if 'from' in str(lst_0): 
                f = open(rootPath + '\\setting', 'r+', encoding='utf-8'); # setting 存在才能用 r+
                lst_1 = f.readlines();
                str_1 = str(lst_1);
                
                if('isPipInstalled=1' in str_1):# 判断是否写入 isPipInstalled
                    f.close();
                    pass;
                else:
                    f.write('isPipInstalled=1\n');
                    f.close();
            else:
                print('pip not installed');
        else: # pipLogPath 存在:
            f = open(pipLogPath, 'r', encoding='utf-8');
            lst_0 = f.readlines();
            f.close();
            if 'from' in str(lst_0):
                f = open(rootPath + '\\setting', 'r+', encoding='utf-8'); # setting 存在才能用 r+
                lst_1 = f.readlines();
                str_1 = str(lst_1);
                
                if('isPipInstalled=1' in str_1): # 判断是否写入 isPipInstalled
                    f.close();
                    pass;
                else:
                    f.seek(0, 2);
                    f.write('isPipInstalled=1\n');
                    f.close();
            else:
                print('pip not installed');

    if os.path.exists(rootPath + '\\setting'): # setting已经存在
        with open(rootPath + '\\setting') as f:
            str_0 = f.readlines();
            if('isPipInstalled=1' in str_0): # isPipInstalled已经写入
                # return;
                pass;
            else:
                InnerFunction();
    else:
        fs = open(rootPath + '\\setting', 'w', encoding='utf-8');
        fs.close();
        InnerFunction();
        
def isYgInstalled(rootPath):
    # setting是否存在      
    if(os.path.exists(rootPath + '\\setting') == False):
        print("setting does not exists")
        file = open(rootPath + '\\setting', 'w', encoding='utf-8');
        file.close();
    file = open(rootPath + '\\setting', 'r+');
    if(file.readlines() == []): # setting 空白文件
        print("setting abnormal")
        # file = open(rootPath + '\\setting', 'w', encoding='utf-8');
        file.write('isYgInstalled=0\n');
    file.close();   
    file = open(rootPath + '\\setting', 'r');
    # setting存在且已安装
    if 'isYgInstalled=1' in str(file.readlines()): 
        # print("lib installed.");
        file.close();
        return;
    # setting存在但未安装    
    else:           
        if (os.path.exists(rootPath + '\\log\\packages_list')) == False: # packages_list 不存在
            print("packages_list not exists")
            os.system('python -m pip list >' + rootPath + '\\log\\packages_list');
        elif(open(rootPath + '\\log\\packages_list', 'r').readlines()==[]): # packages_list 存在但空白
            os.system('python -m pip list >' + rootPath + '\\log\\packages_list');
        # isYgInstalled==0 ?
        file = open(rootPath + '\\setting', 'r')
        # you-get 是否已经安装
        if 'you-get' in str(open(rootPath + '\\log\\packages_list', 'r').readlines()):
            file = open(rootPath + '\\setting', 'a', encoding='utf-8');
            file.write('isYgInstalled=1\n')
            file.close();    
            return;
        else:
            print("lib does not installed. ");
            os.system("python -m pip install you-get -i https://pypi.douban.com/simple");
def isDirsExists(rootPath):
    cachePath = rootPath + "\\cache";
    distPath = rootPath + "\\dist";
    logPath = rootPath + "\\log";
    recordFile = rootPath + "\\log\\record";
    settingFile = rootPath + '\\setting';
    if not os.path.exists(cachePath):
        print("cache created. ");
        os.mkdir(cachePath);
    if not os.path.exists(distPath):
        print("dist created. ");
        os.mkdir(distPath);
    if not os.path.exists(logPath):
        print("log created. ");
        os.mkdir(logPath);
    if not os.path.exists(recordFile):
        print("record created. ");
        with open(recordFile, 'w+') as f:
            pass;
    if not os.path.exists(settingFile):
        print("setting file created. ");
        with open(settingFile, 'w') as f:
            pass;
            
# 播放
def play(rootPath, distPath, flag_lang):
    settingPath = rootPath + '\\setting';
    fileList_old = os.listdir(distPath);
    fileList = [];
    for item in fileList_old:
        if item.endswith('.mp3'):
            fileList.append(item);
    # 获取播放模式
    with open(settingPath, 'r', encoding='utf-8') as f:
        ContentList = f.readlines();
    pMode = getPlayMode(ContentList); 
    # 颜色
    color_red = '\033[0;31m';
    color_blue = '\033[0;36m'
    color_green = '\033[0;32m';
    color_yellow = '\033[1;33m';
    color_brown = '\033[0;33m';
    color_end = '\033[0m';
    skipText = "type 'c' to play record/type 'Enter' to continue: ";
    skipText_zh = "输入 ’c‘ 继续上一首; 回车跳过： "
    playModeMenu = """
playback mode:
    type 'o': order,
    type 's': shuffle.
    """
    playModeMenu_zh = """
播放模式：
    ‘o’：顺序播放，
    ‘s’：随机播放。
    """
    playModeHint = 'playback mode: ';
    playModeHint_zh = '播放模式：';
    pMode_zh = pMode;
    # 切换语言，当选择英文时。
    if(flag_lang == '0'):
        skipText_zh = skipText;
        playModeMenu_zh = playModeMenu;
        playModeHint_zh = playModeHint;
    if(flag_lang == '1'):
        if pMode == 'default':
            pMode_zh = '默认';
        elif pMode == 'order':
            pMode_zh = '顺序播放';
        else:
            pMode_zh = '随机播放';
    # menu
    def menu(): # 输出播放列表
        print(color_yellow + 'id\t' + color_end + color_blue + 'Name' + color_end);
        print(color_blue + '-'*110 + color_end );
        for index in range(len(fileList)):
            print(color_yellow + str(index) + color_end + '\t' + color_blue + fileList[index].replace('.mp3', '') + color_end);
        print(color_blue + '-'*110 + color_end );
    # print('pMode='+pMode);
    
    menu();
    # 获得 id
    print(color_blue + playModeMenu_zh + color_end);
    def findRecentId():
        id = "1";
        # global id;
        # with open(settingPath, 'r', encoding='utf-8') as f:
        #     global ContentList 
        #     ContentList = f.readlines();
        ContentStr = str(ContentList);
        if('playId' in ContentStr): # 找到上次的 playId
            for item in ContentList:
                if('playId' in item):
                    ContentStr = item;
            sub = ContentStr.replace('\n', '').replace('\\', '').strip().index('playId=');
            id = ContentStr[sub+7:];
            id = str(int(id));
            # print('findRecentId->str(id)=' + str(id), 'isdigit=', id.isdigit()); # 1 False
            if id.isdecimal(): # playId 记录是否出错
                # print('findRecentId->isdigit passed.')
                print(color_blue + "record: ", fileList[int(id)] + color_end);  
                flagStr = 'a';
                while not ('' == flagStr or flagStr == 'c'):
                    flagStr = input(color_blue + skipText_zh + color_end); # 单引号和双引号有区别
                    # print('flagStr: ', str(flagStr))
                    # print(flagStr);
                    if flagStr == '': # 按了 enter，将 id = k
                        # print('flagStr set.');
                        id = str('k');
                        break;
            else:
                id = 'k';
                # return False; # playId 出错了
        else: # 没有找到 playId，没有保存过
            print('playId not exists.')
            id = 'k';
        return id; # 不明原因，只有返回值 id 才有改变的效果
    id = findRecentId();
    
    # print('after_findRecentId->id=', id);
    try: # 不能放到 findRecentId 里，不能改变 id 值。
        if id == 'k':
            # id = input(color_blue + "type [id]: " + color_end);    
            id = '';
            # print('try passed');
            if id == 'e':return False; # 退出
            while False == id.isdigit() or int(id)>len(fileList) : # 输入 id         
                if id == 'e':
                    return False;
                id = input(color_blue + "type [id]: " + color_end);
                # print(type(id), id)
                ## 设置 playMode
                if 'o' in id or 's' in id:
                    if id == 'o':
                        pMode = 'order';
                        setPlayMode(settingPath, pMode);
                    elif id == 's':
                        pMode = 'shuffle';
                        setPlayMode(settingPath, pMode);
            # print('else passed');
            # print('inside_except=', id);
    except KeyboardInterrupt: # ctrl + c 返回上级
        return False;
    # if findRecentId() == False:
        # print('findRecentId->playId error. ');
        # print(type(id));
        # print('playId=', id);
        # return False;
    id = str(id);
    # print('after_except id=', id);# None
    def findId(): # 判断输入的 id 是否已经保存 && 设置 id
        with open(settingPath, 'r+', encoding='utf-8') as f: # 查看 playId
            lst = f.readlines();
            flag = '2';
            for i in range(len(lst)): 
                if 'playId=' + id in lst[i]: # 存在相同的 Id，跳过
                    flag = '0';
                    break;
                elif 'playId' in lst[i]: # 不同的Id，写入
                    lst[i] = 'playId='+ id +'\n';
                    flag = '1';
                    break;
                else: # 'playId' 不存在，写入
                    flag = '2';
            if flag == '1':
                f.seek(0); # 文件读取指针放到最前面是下一条语句生效
                f.truncate(); # 清空文件
                for i in range(len(lst)):
                    # print(lst[i]);
                    f.write(lst[i]);
            elif flag == '2':
                f.write('playId='+ id +'\n');
            else:
                pass;
        return id;
    findId();
    def play(id):
        mp3File = os.path.join(distPath, fileList[id]); # MP3 文件地址
        audio = MP3(mp3File)
        # print(audio.info.length)
        tLen = audio.info.length;
        mixer.init();
        mixer.music.load(mp3File);
        mixer.music.play();
        mp3Name = fileList[id].replace('.mp3', '');
        print(color_blue + playModeHint_zh + pMode_zh + color_end);
        print('\033[0;36mplaying [{}]\t{}\033[0m'.format(id, mp3Name));
        # print('playing ' + fileList[id].replace('.mp3', ''));
        # print('\033[0;36mDuration: ' + '{:.2f} min\033[0m'.format(tLen/60));
        # 播放
        para = 1;
        start = time.perf_counter(); # 数值类型
        blockLen = 100;
        try:
            while para < blockLen: # 进度
                dur = time.perf_counter() - start;
                para = int((dur/tLen) * blockLen);
                f_min = int(dur / 60);
                f_sec = int(dur % 60);
                if f_sec < 10:
                    f_sec = '0' + str(f_sec);
                e_min = int(tLen / 60);
                e_sec = int(tLen % 60);
                if e_sec < 10:
                    e_sec = '0' + str(e_sec);
                t_dur = str(f_min) + ':' + str(f_sec);
                t_total = str(e_min) + ':' + str(e_sec);
                f = para * '-';
                e = (blockLen - para) * '-';                
                print('\r' + color_yellow + '{}\033[0m\033[0;32m[{}'.format(t_dur, f) + color_end + color_yellow + '*' + color_end + '\033[0;32m' + 
                    '{}]\033[0m'.format(e) + color_yellow + '{}\033[0m'.format(t_total), end=' ');
                time.sleep(0.5);
                # os.system('cls');
                # para += 1;
        # except:
            # mixer.music.stop();
        finally:
            os.system('cls');
            mixer.music.stop();
        # time.sleep(tLen);
    # play(id);
    # id = int(id);
    musicSum = len(fileList);
    while(id != 'e'):
        # print('while->id=', id);
        id = int(id);
        try: # 捕获异常
            play(id);
            menu();
            if pMode == 'default':
                print('default');
                id = '';
            else:
                id = getId(id, pMode, musicSum); # 按照播放模式获取 id，如果要退出程序可以ctl+c
                
            #     print('getId: id=' + id);
            # print('while:try: id=', id);
            while ((not id.isdigit()) or (int(id)>len(fileList))): # 输入 id，播放完后
                try:
                    # print('while:while: pass');
                    id = input(color_blue + 'type [id]: ' + color_end);
                except: # 播放完一首歌曲，要两次InterruptBoardException才能退出程序
                    # id = input(color_blue + 'type [id]: ' + color_end);
                    pass;
                # print('while->except:');
                finally:
                    if id == 'e':
                      return 0;
                # print((not id.isdigit()), ' ', (id != 'e'), ' ', int(id)>len(fileList) );
                # print(type(id), ' id=', id);
                    id = str(id);
            # os.system('cls');
            # id = 'e'
        except BaseException as e:
            # print("产生了", e);
            # print('type: {} id={}'.format(type(id), id))
            # if isinstance(e, KeyboardInterrupt):
            # os.system('cls');
            menu();
            # print('play:while:except: pMode='+ pMode)
            # print('\nwhile->KeyBoardException');
            id = '';
            while ((not id.isdigit()) or (int(id)>len(fileList))): # 输入 id
                try: # 播放完一首歌曲，要两次InterruptBoardException才能退出程序
                    id = input(color_blue + 'type [id]: ' + color_end);
                except:
                    id = input(color_blue + 'type [id]: ' + color_end);
                # print('while->except:');
                finally:
                    if id == 'e':
                        return 0;
                # print((not id.isdigit()), ' ', (id != 'e'), ' ', int(id)>len(fileList) );
                # print(type(id), ' id=', id);
                    id = str(id);
                
            # print('\ncatched ctrl + c');
            if(id != 'e'):
                findId();
            # play(id);
        finally:
            if(id != 'e'):
                # print('while->finally:')
                # print('\n', type(id), ' id=', id);
                if type(id) == int or id.isdigit():
                    id = str(id);
                    findId();
                # if type(id) == int:
                    # id = str(id);

# 设置播放模式
def setPlayMode(settingPath, pMode):
    with open(settingPath, 'r+', encoding='utf-8') as f:
        lst = f.readlines();
        lst_new = [];
        for line in lst:
            if 'playMode=' in line:
                if pMode in line:
                    pass;
                else:
                    line = 'playMode=' + pMode + '\n';
            lst_new.append(line);
        if 'playMode' not in str(lst): # setting中没有 playMode 设置
            lst_new.append('playMode='+pMode+'\n');
        f.seek(0);
        f.truncate();
        for line in lst_new:
            f.write(line);
        print('setPlayMode: set playback=', pMode);
# 获取播放模式     
def getPlayMode(ContentList):
    pMode = 'default'; # 没有pMode设置的话就是default。
    ContentStr = str(ContentList);
    if 'playMode=order' in ContentStr:
        pMode = 'order'; # 顺序播放
    elif 'playMode=shuffle' in ContentStr:
        pMode = 'shuffle'; # 随机播放
    return pMode;
# 获得id
def getId(id, pMode, musicSum):
    if 'default' in pMode:
        return id;
    if pMode == 'order':
        return str(int(id) + 1);
    else:
        return str(randint(0, musicSum));
# 设置Language
def setLang(rootPath, flag_lang):
    settingPath = rootPath + '\\setting';
    with open(settingPath, 'r', encoding='utf-8') as file, open(settingPath + '.bak', 'w', encoding='utf-8') as file_bak:   
        flag = '0';
        lst = file.readlines();
        file.seek(0); # 指针回到头部
        if flag_lang == '1':
            for line in file:
                if 'zh' in line:
                    line = line.replace('zh', 'en');
                    flag = '1';
                file_bak.write(line);
        else:
            for line in file:
                if 'en' in line:
                    line = line.replace('en', 'zh');
                    flag = '1';
                file_bak.write(line);  
        
        if 'lang' not in str(lst):
            print('setLang: lang=None. ');
            file_bak.write('lang=en\n');
    os.remove(settingPath);
    os.rename(settingPath + '.bak', settingPath);
    if(flag == '1'):
        if flag_lang == '1':
            print('restart to take effect. ');
        else:
            print('重启软件以生效');
        time.sleep(1.5);
        exit(0);
        