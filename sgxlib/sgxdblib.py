#!/usr/bin/env python
#coding:utf8

import ctypes
import os

PACKAGE_PATH = os.path.abspath(os.path.dirname(__file__))


class SGXDB(object):
    LIB = None

    @classmethod
    def get_lib(cls):
        if cls.LIB is None:
            lib_path = os.path.join(PACKAGE_PATH, "sgxdb.so")
            cls.LIB = ctypes.cdll.LoadLibrary(lib_path)
            if cls.LIB.initialize_enclave() != 0:
                raise RuntimeError(u"Fail to initialize enclave!")
        return cls.LIB

    @classmethod
    def destroy(cls):
        if cls.get_lib().destroy_enclave() != 0:
            raise RuntimeError(u"Fail to destroy enclave!")

    @classmethod
    def insert(cls, data): 
        if cls.get_lib().insert_record(ctypes.c_char_p(data)) != 0:
            raise RuntimeError(u"Fail to insert data!")

    @classmethod
    def delete(cls, data):
        if cls.get_lib().delete_record(ctypes.c_char_p(data)) != 0:
            raise RuntimeError(u"Fail to delete data")

    @classmethod
    def query(cls, data):
        retval = ctypes.c_int()
        if cls.get_lib().query_record(ctypes.byref(retval), ctypes.c_char_p(data)) != 0:
            raise RuntimeError(u"Fail to execute the query")
        return retval.value == 1

def test_api():
    SGXDB.insert("bad")
    print repr(SGXDB.query("good"))
    SGXDB.insert("good")

    print repr(SGXDB.query("good"))
    SGXDB.delete("good")

    print repr(SGXDB.query("good"))
    SGXDB.destroy()

if __name__ == '__main__':
    test_api()
