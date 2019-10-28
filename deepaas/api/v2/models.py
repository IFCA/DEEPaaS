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
import marshmallow
from marshmallow import fields

from deepaas import model

# Get the models (this is a singleton, so it is safe to call it multiple times
model.register_v2_models()

app = web.Application()
routes = web.RouteTableDef()


class Location(marshmallow.Schema):
    rel = fields.Str()
    href = fields.Str()


class ModelMeta(marshmallow.Schema):
    id =  fields.Str(required=True, description='Model identifier'),  # noqa
    name = fields.Str(required=True, description='Model name'),
    description = fields.Str(required=True,
                             description='Model description'),
    license = fields.Str(required=False, description='Model license'),
    author = fields.Str(required=False, description='Model author'),
    version = fields.Str(required=False, description='Model version'),
    url = fields.Str(required=False, description='Model url'),
    links = fields.List(fields.Nested(Location))


@aiohttp_apispec.docs(
    tags=["models"],
    name="Return loaded models and its information",
    description="DEEPaaS can load several models and server them on the same "
                "endpoint, making a call to the root of the models namespace "
                "will return the loaded models, as long as their basic "
                "metadata.",
)
@routes.get('/models')
async def get(self):
    """Return loaded models and its information.

    DEEPaaS can load several models and server them on the same endpoint,
    making a call to the root of the models namespace will return the
    loaded models, as long as their basic metadata.
    """

    models = []
    for name, obj in model.V2_MODELS.items():
        m = {
            "id": name,
            "name": name,
            "links": [{
                "rel": "self",
                "href": "%s/%s" % (self.path, name),
            }]
        }
        meta = obj.get_metadata()
        m.update(meta)
        models.append(m)
    return web.json_response({"models": models})


# In the next lines we iterate over the loaded models and create the different
# resources for each model. This way we can also load the expected parameters
# if needed (as in the training method).
for model_name, model_obj in model.V2_MODELS.items():
    @routes.view('/models/%s' % model_name)
    class BaseModel(web.View):
        model_name = model_name
        model_obj = model_obj

        @aiohttp_apispec.docs(
            tags=["models"],
            name="Return model metadata",
        )
        async def get(self):
            """Return the model's metadata."""

            print(type(self))
            print(dir(self))
            m = {
                "id": self.model_name,
                "name": self.model_name,
                "links": [{
                    "rel": "self",
                    "href": "%s" % self.request.path,
                }]
            }
            meta = self.model_obj.get_metadata()
            m.update(meta)

            return web.json_response(m)
