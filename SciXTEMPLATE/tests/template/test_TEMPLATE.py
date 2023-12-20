from unittest import TestCase

import base
from confluent_kafka.avro import AvroProducer
from mock import patch

from TEMPLATE import db
from TEMPLATE.template import TEMPLATE_APP
from tests.common.mockschemaregistryclient import MockSchemaRegistryClient


class test_TEMPLATE(TestCase):
    def test_template_task(self):
        mock_job_request = base.mock_job_request()
        with base.base_utils.mock_multiple_targets(
            {
                "update_job_status": patch.object(db, "update_job_status", return_value=True),
                "write_status_redis": patch.object(db, "write_status_redis", return_value=True),
            }
        ) as mocked:
            mock_app = TEMPLATE_APP(proj_home="SciXTEMPLATE/tests/stubdata/")
            mock_app.schema_client = MockSchemaRegistryClient()
            producer = AvroProducer({}, schema_registry=mock_app.schema_client)
            mock_app.template_task(mock_job_request, producer)
            self.assertTrue(mocked["update_job_status"].called)
            self.assertTrue(mocked["write_status_redis"].called)
