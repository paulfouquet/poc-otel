import argparse
import json
from typing import List

from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import ConsoleSpanExporter, SimpleSpanProcessor

trace.set_tracer_provider(TracerProvider())
trace.get_tracer_provider().add_span_processor(SimpleSpanProcessor(ConsoleSpanExporter()))

tracer = trace.get_tracer(__name__)


def format_source(source: List[str]) -> List[str]:
    """Due to Argo constraints if using the basemaps cli list command
    the source has a string that contains a list that needs to be split.
    example: ["[\"s3://test/image_one.tiff\", \"s3://test/image_two.tiff\"]"]
    """
    if len(source) == 1 and source[0].startswith("["):
        source_json: List[str] = json.loads(source[0])
        return source_json
    return source


def non_visual_qa():
    """non visual qa

    Returns:
        _type_: _description_
    """
    with tracer.start_as_current_span("non_visual_qa"):
        # Do stuffs
        print("I am the non visual QA!")
        raise Exception("An error occured!")


def start_standardising(source):
    """blabla

    Args:
        source (_type_): _description_
        preset (_type_): _description_
        concurrency (_type_): _description_
    """
    with tracer.start_as_current_span("standardising"):
        # Do stuffs
        print(f"I am the start standardising! {source}")
        non_visual_qa()


def main() -> None:
    """just a main"""
    with tracer.start_as_current_span("main"):
        span = trace.get_current_span()
        parser = argparse.ArgumentParser()
        parser.add_argument("--source", dest="source", nargs="+", required=True)
        arguments = parser.parse_args()

        source = format_source(arguments.source)
        try:
            start_standardising(source)
        except Exception as e:
            span.record_exception(e)
            span.set_status(trace.StatusCode.ERROR, "an error happened")


if __name__ == "__main__":
    main()
