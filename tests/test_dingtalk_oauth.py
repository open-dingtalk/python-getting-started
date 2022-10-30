#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest

from dingtalk import oauth


class TestStorageService(unittest.TestCase):
    def test_load_token_return_euccess_on_regularcase(self):
        storage = oauth.StorageService()
        storage.save_token("token")
        self.assertEqual(storage.load_token(), "token")

    def test_load_token_return_none_on_default(self):
        storage = oauth.StorageService()
        self.assertEqual(storage.load_token(), None)


if __name__ == "__main__":
    unittest.main()
