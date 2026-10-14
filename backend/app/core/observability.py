from phoenix.otel import register
from openinference.instrumentation.langchain import LangChainInstrumentor
from openinference.instrumentation.openai import OpenAIInstrumentor


def setup_observability():
    tracer_provider = register(
        project_name="ai-real-estate",
        endpoint="http://localhost:6006/v1/traces",
    )

    LangChainInstrumentor().instrument(
        tracer_provider=tracer_provider
    )

    OpenAIInstrumentor().instrument(
        tracer_provider=tracer_provider
    )