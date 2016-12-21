#!/usr/bin/env python
#coding:utf8

import ctypes
import os
import copy

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
    def insert(cls, key, data): 
        if cls.get_lib().insert_record(ctypes.c_char_p(key), ctypes.c_char_p(data)) != 0:
            raise RuntimeError(u"SGX: Fail to insert data!")

    @classmethod
    def delete(cls, key):
        if cls.get_lib().delete_record(ctypes.c_char_p(key)) != 0:
            raise RuntimeError(u"SGX: Fail to delete data")

    @classmethod
    def query(cls, key):
        retval = ctypes.c_char_p()
        if cls.get_lib().query_record(ctypes.byref(retval), ctypes.c_char_p(key)) != 0:
            raise RuntimeError(u"SGX: Fail to execute the query")
        res = copy.copy(retval.value)
        if res is not None:
            cls.get_lib().freeptr(retval);
        return res

    @classmethod
    def get_export_size(cls):
        retval = ctypes.c_int()
        if cls.get_lib().get_export_size(ctypes.byref(retval)) != 0:
            raise RuntimeError(u"SGX: Fail to get the export size")
        return retval.value

    @classmethod
    def export_sealed_data(cls):
        retval = ctypes.c_int()
        size = cls.get_export_size()
        data = (ctypes.c_char * size)()
        if cls.get_lib().export_sealed_data(ctypes.byref(retval), data, size) != 0:
            raise RuntimeError(u"SGX: Fail to export sealed data")
        if retval.value != 0:
            raise RuntimeError(u"Error occurs when getting the export sealed data")
        return data.raw

    @classmethod
    def import_sealed_data(cls, data):
        retval = ctypes.c_int()
        if cls.get_lib().import_sealed_data(ctypes.byref(retval), ctypes.c_char_p(data), len(data)) != 0:
            raise RuntimeError(u"SGX: Fail to import sealed data")
        if retval.value != 0:
            raise RuntimeError(u"Error occurs when getting the import sealed data")


def test_api():
    print 'SGXDB.insert("bad")'
    SGXDB.insert("bad", "bad_value")

    print 'repr(SGXDB.query("good"))', repr(SGXDB.query("good"))

    print 'SGXDB.insert("good")'
    SGXDB.insert("good", "good_value")

    print 'repr(SGXDB.query("good"))', repr(SGXDB.query("good"))

    print 'SGXDB.delete("good")'
    SGXDB.delete("good")

    print 'repr(SGXDB.query("good"))', repr(SGXDB.query("good"))

    print "SGXDB.get_export_size():",  repr(SGXDB.get_export_size())

    sealed_data = SGXDB.export_sealed_data()
    print "SGXDB.export_sealed_data():", repr(sealed_data)

    print 'SGXDB.delete("good")'
    SGXDB.delete("good")
    print 'SGXDB.delete("bad")'
    SGXDB.delete("bad")

    print 'repr(SGXDB.query("bad"))', repr(SGXDB.query("bad"))
    print 'repr(SGXDB.query("good"))', repr(SGXDB.query("good"))

    print "Importing the sealed data"
    SGXDB.import_sealed_data(sealed_data)

    print 'repr(SGXDB.query("bad"))', repr(SGXDB.query("bad"))
    print 'repr(SGXDB.query("good"))', repr(SGXDB.query("good"))

    SGXDB.destroy()


if __name__ == '__main__':
    test_api()
