#  Copyright 2022 Google LLC
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      https://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import logging

import apache_beam as beam
from apache_beam import DoFn
from apache_beam import ParDo
from apache_beam.io import ReadFromPubSub
from apache_beam.io import WriteToPubSub
from apache_beam.options.pipeline_options import PipelineOptions

input_topic = "projects/kissam-testing-project/topics/topic1"


class PubsubToPubsub(DoFn):
  def process(self, element):
    # Assuming pubsub input is a byte string
    data = element.decode("utf-8")
    # Perform some custom transformation here
    data = data.encode("utf-8")
    yield data


def run():
  """Write PubSub topic function."""

  class WritePubSubOptions(PipelineOptions):

    @classmethod
    def _add_argparse_args(cls, parser):
      parser.add_argument(
        "--topic",
        required=True,
        help="PubSub topic to write to.")

  options = WritePubSubOptions(streaming=True)

  with beam.Pipeline(options=options) as p:

    (p | "Read from PubSub" >> ReadFromPubSub(topic=input_topic)
       | "EncodeString" >> ParDo(PubsubToPubsub())
       | "Write to PubSub" >> WriteToPubSub(topic=options.topic))


if __name__ == "__main__":
  logging.getLogger().setLevel(logging.INFO)
  run()
