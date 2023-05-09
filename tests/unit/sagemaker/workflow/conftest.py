# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"). You
# may not use this file except in compliance with the License. A copy of
# the License is located at
#
#     http://aws.amazon.com/apache2.0/
#
# or in the "license" file accompanying this file. This file is
# distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF
# ANY KIND, either express or implied. See the License for the specific
# language governing permissions and limitations under the License.
from __future__ import absolute_import

from unittest.mock import Mock, PropertyMock

import pytest

from sagemaker.workflow.pipeline_context import PipelineSession

REGION = "us-west-2"
BUCKET = "my-bucket"
ROLE = "DummyRole"
IMAGE_URI = "fakeimage"
INSTANCE_TYPE = "ml.m4.xlarge"


@pytest.fixture(scope="module")
def mock_client():
    """Mock client.

    Considerations when appropriate:

        * utilize botocore.stub.Stubber
        * separate runtime client from client
    """
    client_mock = Mock()
    client_mock._client_config.user_agent = (
        "Boto3/1.14.24 Python/3.8.5 Linux/5.4.0-42-generic Botocore/1.17.24 Resource"
    )
    client_mock.describe_model.return_value = {"PrimaryContainer": {}, "Containers": {}}
    return client_mock


@pytest.fixture(scope="module")
def mock_boto_session(client):
    role_mock = Mock()
    type(role_mock).arn = PropertyMock(return_value=ROLE)

    resource_mock = Mock()
    resource_mock.Role.return_value = role_mock

    session_mock = Mock(region_name=REGION)
    session_mock.resource.return_value = resource_mock
    session_mock.client.return_value = client

    return session_mock


@pytest.fixture(scope="module")
def pipeline_session(mock_boto_session, mock_client):
    pipeline_session = PipelineSession(
        boto_session=mock_boto_session,
        sagemaker_client=mock_client,
        default_bucket=BUCKET,
    )
    # For tests which doesn't verify config file injection, operate with empty config

    pipeline_session.sagemaker_config = {}
    return pipeline_session
