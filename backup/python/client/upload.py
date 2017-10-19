#!/usr/bin/python
# coding:utf-8


import requests
import hashlib, time;


def uploadFile(filepath, remotepath, config):
    if config["remoteSwitch"] != 1:
        return
    offset = "10086";
    successCode = 200;
    ticks = str(time.time());
    sign = hashlib.md5(config["username"] + config["passport"] + offset + ticks).hexdigest();

    # zipfileName='temp'+ticks+'.zip';
    # _zipfile = zipfile.ZipFile(zipfileName, 'w', zipfile.ZIP_DEFLATED)
    # _zipfile.write(filepath);
    # _zipfile.close();
    # opener = urllib2.build_opener(PostHandler)
    print 'upload------------------->>>>>>'
    with open(filepath, 'rb') as md5File:
        md5obj = hashlib.md5()
        md5obj.update(md5File.read())
        hash = md5obj.hexdigest()
        print "upload file's md5:" + hash;
    params = {"to": remotepath, "sign": str(sign), "ticks": ticks,
              "file": open(filepath, "rb")}
    response = requests.post(config["remoteServer"], files=params)
    # print response.status_code;
    # code = opener.open(config["remoteServer"], params).read()
    if response.status_code == successCode:
        print "remote back up successed"
    else:
        print "remote back up failed , error code:" + str(response.status_code);
