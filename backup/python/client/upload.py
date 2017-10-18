#!/usr/bin/python


import urllib
import urllib2
import mimetools, mimetypes
import os, stat


class Callable:
    def __init__(self, anycallable):
        self.__call__ = anycallable


doseq = 1


class PostHandler(urllib2.BaseHandler):
    handler_order = urllib2.HTTPHandler.handler_order - 10  # needs to run first

    def http_request(self, request):
        data = request.get_data()
        if data is not None and type(data) != str:
            v_files = []
            v_vars = []
            try:
                for (key, value) in data.items():
                    if type(value) == file:
                        v_files.append((key, value))
                    else:
                        v_vars.append((key, value))
            except TypeError:
                systype, value, traceback = sys.exc_info()
                raise TypeError, "not a valid non-string sequence or mapping object", traceback

            if len(v_files) == 0:
                data = urllib.urlencode(v_vars, doseq)
            else:
                boundary, data = self.multipart_encode(v_vars, v_files)
                contenttype = 'multipart/form-data; boundary=%s' % boundary
                if (request.has_header('Content-Type')
                    and request.get_header('Content-Type').find('multipart/form-data') != 0):
                    print "Replacing %s with %s" % (request.get_header('content-type'), 'multipart/form-data')
                request.add_unredirected_header('Content-Type', contenttype)

            request.add_data(data)
        return request

    def multipart_encode(vars, files, boundary=None, buffer=None):
        if boundary is None:
            boundary = mimetools.choose_boundary()
        if buffer is None:
            buffer = ''
        for (key, value) in vars:
            buffer += '--%s\r\n' % boundary
            buffer += 'Content-Disposition: form-data; name="%s"' % key
            buffer += '\r\n\r\n' + str(value) + '\r\n'
        for (key, fd) in files:
            file_size = os.fstat(fd.fileno())[stat.ST_SIZE]
            filename = fd.name.split('/')[-1]
            contenttype = mimetypes.guess_type(filename)[0] or 'application/octet-stream'
            buffer += '--%s\r\n' % boundary
            buffer += 'Content-Disposition: form-data; name="%s"; filename="%s"\r\n' % (key, filename)
            buffer += 'Content-Type: %s\r\n' % contenttype
            # buffer += 'Content-Length: %s\r\n' % file_size
            fd.seek(0)
            buffer += '\r\n' + fd.read().decode("ISO-8859-1") + '\r\n'
        buffer += '--%s--\r\n\r\n' % boundary
        return boundary, buffer.encode("utf-8")

    multipart_encode = Callable(multipart_encode)

    https_request = http_request


def uploadFile(filepath, remotepath, config):
    if config["remoteSwitch"] != 1:
        return
    offset = "10086";
    successCode = "200";
    sign = hash(config["username"] + config["passport"] + offset);

    opener = urllib2.build_opener(PostHandler)
    params = {"to": remotepath, "sign": sign,
              "file": open(filepath, "r")}
    code = opener.open(config["remoteServer"], params).read()
    if code == successCode:
        print "remote back up successed"
    else:
        print "remote back up failed , error code:" + code;
