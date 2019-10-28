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

import aiohttp_apispec
from aiohttp import web
import webargs.core
# import marshmallow
# from marshmallow import fields

from deepaas import model

# Get the models (this is a singleton, so it is safe to call it multiple times
model.register_v2_models()

app = web.Application()
routes = web.RouteTableDef()


# In the next lines we iterate over the loaded models and create the different
# resources for each model. This way we can also load the expected parameters
# if needed (as in the training method).
for model_name, model_obj in model.V2_MODELS.items():
    args = webargs.core.dict2schema(model_obj.add_train_args(None))

    @routes.view('/models/%s/train' % model_name)
    class ModelTrain(web.View):
        model_name = model_name
        model_obj = model_obj
#        parser = model_obj.add_train_args(ns.parser())

        @aiohttp_apispec.docs(
            tags=["models"],
            name="Retrain model with available data"
        )
#        @ns.expect(parser)
        @aiohttp_apispec.querystring_schema(args)
        async def put(self):
            args = self.parser.parse_args()
            ret = self.model_obj.train(**args)
            # FIXME(aloga): what are we returning here? We need to take care
            # of these responses as well.
            return web.json_response(ret)
