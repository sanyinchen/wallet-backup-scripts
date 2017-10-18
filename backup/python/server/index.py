#!/usr/bin/python
# -*- coding:utf-8 -*-

import errno
import os, sys
import web, io, json

urls = (
    '/', 'index'
)

_index = 0;


class index:
    def GET(self):
        return 'I\'m ready for that, you know.'

    def POST(self):
        offset = "10086";
        configFile = io.open(os.path.join(os.getcwd(), 'server.config'), mode="r", encoding="utf-8");
        content = configFile.read();
        config = json.loads(content.replace('\r\n', '\\r\\n'), encoding="utf-8");
        localSign = hash(config["username"] + config["passport"] + offset);
        print "localSign:" + str(localSign)

        i = web.input()
        print "sign:" + i.sign
        path = i.to;
        if str(localSign) != i.sign:
            print "illegal upload"
            return -1;
        if os.path.isfile(path):
            os.remove(path);
            print path + ' clear!';

        _dir = os.path.dirname(os.path.abspath(path));
        if os.path.exists(_dir) == False:
            self.mkdir_p(_dir)

        print 'storage file:' + path;
        fout = open(path, 'w')
        fout.write(i.file)
        fout.close()
        # print 'pos-receive:' + i.to;
        return 200

    def mkdir_p(self, path):
        try:
            print "path" + path
            os.makedirs(path)
        except OSError as exc:  # Python >2.5 (except OSError, exc: for Python <2.5)
            if exc.errno == errno.EEXIST and os.path.isdir(path):
                pass
            else:
                raise


class MyApplication(web.application):
    def run(self, port=8080, *middleware):
        func = self.wsgifunc(*middleware)
        return web.httpserver.runsimple(func, ('0.0.0.0', port))


if __name__ == '__main__':
    app = MyApplication(urls, globals())
    app.run(port=8991)
