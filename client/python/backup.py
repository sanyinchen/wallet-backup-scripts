#!/usr/bin/python
# -*- coding:utf-8 -*-

import os, sys, shutil, json, time,io


def main(workspaceFolder, backUpspaceFolder):
    backUpspaceFolder = os.path.join(backUpspaceFolder,
                                     time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime(time.time())));
    if os.path.exists(backUpspaceFolder) == False:
        os.makedirs(backUpspaceFolder)
    else:
        print backUpspaceFolder + ' has existed!'
        sys.exit()

    print 'rootpath:' + workspaceFolder;
    print 'backpath:' + backUpspaceFolder;
    traverseAllFile(workspaceFolder, backUpspaceFolder, workspaceFolder)


def traverseAllFile(rootPath, backUpspaceFolder, originalPath):
    if rootPath.startswith(backUpspaceFolderflag):
        return;
    for i in os.listdir(rootPath):
        if i in blacklist:
            continue;
        filepath = os.path.join(rootPath, i);
        if isDestFile(filepath):

            childFilePath = filepath.split(originalPath);
            if len(childFilePath) != 2:
                print 'dosomething is wrong in childFilePath:' + childFilePath;
                sys.exit();

            backUpFilePath = os.path.join(backUpspaceFolder, getPathWithoutSeparate(childFilePath[1]));
            backDirpath = os.path.dirname(backUpFilePath);
            if os.path.exists(backDirpath) == False:
                os.makedirs(backDirpath)

            shutil.copy(filepath, backUpFilePath);
            print 'backup file:' + filepath + ' to ' + backUpFilePath;

        if os.path.isdir(filepath):
            traverseAllFile(filepath, backUpspaceFolder, originalPath)


def getPathWithoutSeparate(path):
    newpath = '';
    trans = False;
    for i in path:
        if i == os.path.sep and trans == False:
            continue
        else:
            trans = True;
            newpath += i;
    return newpath;


def isDestFile(path):
    return path.endswith(fileType) and os.path.isfile(path);


if __name__ == '__main__':
    global fileType;
    global backUpspaceFolderflag;
    global blacklist;
    num = 0;
    configFile = None;
    timeStep = 3600;
    loop = 0;
    try:
        configFile = io.open(os.path.join(os.getcwd(), 'backup.config'),mode="r", encoding="utf-8");
        content = configFile.read();
        jsonObj = json.loads(content.replace('\r\n', '\\r\\n'),encoding="utf-8");
        WorkspaceFolder = os.path.abspath(jsonObj["rootpath"]);
        backUpspaceFolder = os.path.abspath(jsonObj["destpath"]);
        fileType = jsonObj["fileType"];
        timeStep = jsonObj["cycleTime"] * 3600;
        loop = jsonObj["loop"];
        blacklist=jsonObj["blackList"];

    except IOError:
        print 'can not load config'
        sys.exit()
    finally:
        if configFile != None:
            configFile.close();
    backUpspaceFolderflag = backUpspaceFolder
    if os.path.exists(backUpspaceFolder) == False:
        os.makedirs(backUpspaceFolder)

    if os.path.exists(WorkspaceFolder) == False:
        print WorkspaceFolder + ' no such dir'
        sys.exit()
    while (1):
        num = num + 1;
        if loop > 0:
            print '--------------------the ' + str(num) + ' times of backup---------------------'
        main(WorkspaceFolder, backUpspaceFolder)
        if loop > 0:
            print 'next back up is after ' + str(timeStep) + ' s';
            time.sleep(timeStep)
        else:
            break;
