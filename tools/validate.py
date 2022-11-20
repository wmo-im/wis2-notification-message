###############################################################################
#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
#
###############################################################################

import json

import click
from jsonschema import validate
from jsonschema.protocols import Validator
import yaml


def validate_schema(schema: dict) -> bool:
    """
    Validate schema
    """

    Validator.check_schema(schema)

    return True


def validate_instance(instance: dict, schema: dict) -> bool:
    """
    Validate JSON instance against schema
    """

    validate(instance, schema)

    return True


@click.group()
def cli():
    """Validation utilities"""
    pass


@click.command('instance')
@click.argument('schema', type=click.File())
@click.argument('instance', type=click.File())
def instance_(schema, instance):
    """Validate instance against schema"""

    instance2 = json.load(instance)
    schema2 = yaml.load(schema, Loader=yaml.SafeLoader)

    try:
        validate_instance(instance2, schema2)
    except Exception as err:
        raise click.ClickException(repr(err))


@click.command('schema')
@click.argument('schema', type=click.File())
def schema_(schema):
    """Validate schema"""

    schema2 = yaml.load(schema, Loader=yaml.SafeLoader)

    try:
        validate_schema(schema2)
    except Exception as err:
        raise click.ClickException(repr(err))


cli.add_command(instance_)
cli.add_command(schema_)


if __name__ == '__main__':
    cli()
