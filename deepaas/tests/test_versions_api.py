# -*- coding: utf-8 -*-

# Copyright 2018 Spanish National Research Council (CSIC)
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import unittest

from aiohttp import web

from deepaas.api import v1
from deepaas.api import v2
from deepaas.api import versions
from deepaas.tests import base


class TestApiVersions(base.TestCase):
    async def get_application(self):
        app = web.Application(debug=True)
        app.add_routes(versions.routes)

        return app

    async def test_get_no_versions(self):
        ret = await self.client.get("/")
        self.assertEqual(200, ret.status_code)
        self.assertEqual({'versions': []}, ret.json)

    async def test_v1_version(self):
        versions.register_version("v1", "v1.models_models")
        self.client.register_blueprint(v1.get_blueprint())
        ret = await self.client.get("/")
        self.assertEqual(200, ret.status_code)
        expect = {
            'versions': [
                {'links': [{'href': '/v1/models/', 'rel': 'self'},
                           {'href': '/v1/', 'rel': 'help'},
                           {'href': '/v1/swagger.json', 'rel': 'describedby'}],
                 'version': 'v1'}
            ]
        }
        self.assertDictEqual(expect, ret.json)

    async def test_v1_version_no_doc(self):
        versions.register_version("v1", "v1.models_models")
        self.client.register_blueprint(v1.get_blueprint(doc=False))
        ret = await self.client.get("/")
        self.assertEqual(200, ret.status_code)
        expect = {
            'versions': [
                {'links': [{'href': '/v1/models/', 'rel': 'self'},
                           {'href': '/v1/swagger.json', 'rel': 'describedby'}],
                 'version': 'v1'}
            ]
        }
        self.assertDictEqual(expect, ret.json)

    @unittest.skip("Blocked by this stal pull request"
                   "https://github.com/noirbizarre/flask-restplus/pull/553")
    async def test_v1_version_no_swagger(self):
        versions.register_version("v1", "v1.models_models")
        self.client.register_blueprint(v1.get_blueprint(add_specs=False))
        ret = await self.client.get("/")
        self.assertEqual(200, ret.status_code)
        expect = {
            'versions': [
                {'links': [{'href': '/v1/models/', 'rel': 'self'},
                           {'href': '/v1/', 'rel': 'help'}],
                 'version': 'v1'}
            ]
        }
        self.assertDictEqual(expect, ret.json)

    async def test_v2_version_no_doc(self):
        versions.register_version("v2", "v2.models_models")
        self.client.register_blueprint(v2.get_blueprint(doc=False))
        ret = await self.client.get("/")
        self.assertEqual(200, ret.status_code)
        expect = {
            'versions': [
                {'links': [{'href': '/v2/models/', 'rel': 'self'},
                           {'href': '/v2/swagger.json', 'rel': 'describedby'}],
                 'version': 'v2'}
            ]
        }
        self.assertDictEqual(expect, ret.json)

    @unittest.skip("Blocked by this stal pull request"
                   "https://github.com/noirbizarre/flask-restplus/pull/553")
    async def test_v2_version_no_swagger(self):
        versions.register_version("v2", "v2.models_models")
        self.client.register_blueprint(v2.get_blueprint(add_specs=False))
        ret = await self.client.get("/")
        self.assertEqual(200, ret.status_code)
        expect = {
            'versions': [
                {'links': [{'href': '/v2/models/', 'rel': 'self'},
                           {'href': '/v2/', 'rel': 'help'}],
                 'version': 'v2'}
            ]
        }
        self.assertDictEqual(expect, ret.json)
