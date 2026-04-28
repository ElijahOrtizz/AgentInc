"""
Task classification service.
This is a direct port of the ROUTE_CONFIG + classifyTask() logic that previously
lived in the frontend JavaScript. Moving it here means:
  - The frontend stays thin
  - Classification can be improved / tested independently
  - We can later swap in an LLM-based classifier without touching the frontend
"""

from backend.models.task import RoutingResult


# Route config mirrors the frontend ROUTE_CONFIG array exactly.
# Each entry: keywords list, task_type label, workflow key, human label, reason.
ROUTE_CONFIG = [
    {
        "id": "r-code",
        "task_type": "R Code / Rmd",
        "keywords": [
            "rmd", "r markdown", "knit", "ggplot", "tidyverse", "dplyr",
            "read_csv", "lm(", "t.test", "chunk", "library(", "echo=",
            "r code", "r script",
        ],
        "workflow": "claude",
        "workflow_label": "Claude Build",
        "reason": "R code and Rmd are a Claude strength — correct syntax, clean chunk options, no guessing.",
    },
    {
        "id": "ggplot",
        "task_type": "ggplot Visualization",
        "keywords": [
            "ggplot", "geom_", "theme_", "aes(", "scale_", "facet",
            "boxplot", "scatter", "histogram", "bar chart",
            "visualization", "plot", "graph", "chart",
        ],
        "workflow": "claude",
        "workflow_label": "Claude Build",
        "reason": "ggplot design and styling — clean output ready to knit.",
    },
    {
        "id": "stats",
        "task_type": "Statistical Analysis",
        "keywords": [
            "regression", "hypothesis", "p-value", "confidence interval",
            "anova", "correlation", "t-test", "statistical", "significance",
            "model", "predict", "coefficient",
        ],
        "workflow": "claude",
        "workflow_label": "Claude Build",
        "reason": "Statistical reasoning handled best by Claude for accuracy.",
    },
    {
        "id": "build",
        "task_type": "Build From Scratch",
        "keywords": [
            "build", "create", "write", "make", "generate", "new",
            "from scratch", "design", "develop",
        ],
        "workflow": "claude",
        "workflow_label": "Claude Build",
        "reason": "Building from scratch — architecture, code, and content generation.",
    },
    {
        "id": "stryde",
        "task_type": "Stryde / Crypto",
        "keywords": [
            "stryde", "btc", "bitcoin", "pine script", "tradingview",
            "rsi", "ema", "vwap", "signal", "trading", "webhook",
            "traderspost", "webull", "candle", "indicator", "momentum", "sweep",
        ],
        "workflow": "claude",
        "workflow_label": "Claude Build",
        "reason": "Stryde development and trading signal logic.",
    },
    {
        "id": "agent",
        "task_type": "Agent Inc. Dev",
        "keywords": [
            "agent inc", "fastapi", "supabase", "baseagent", "jobagent",
            "strydeagent", "homeworkagent", "researchagent",
            "meetingorchestrator", "python backend",
        ],
        "workflow": "claude",
        "workflow_label": "Claude Build",
        "reason": "Agent Inc. architecture and Python backend.",
    },
    {
        "id": "integrate",
        "task_type": "Integrate Into File",
        "keywords": [
            "integrate", "insert", "add to", "plug in", "put into",
            "replace", "update existing", "drop in", "merge into", "chunks into", "into my existing", "into my rmd", "into my file",
        ],
        "workflow": "chatgpt",
        "workflow_label": "ChatGPT Integration",
        "reason": "Integrating chunks into existing files — ChatGPT preserves structure reliably.",
    },
    {
        "id": "reformat",
        "task_type": "Reformat Document",
        "keywords": [
            "reformat", "clean up", "restructure", "reorganize",
            "tidy", "fix formatting",
        ],
        "workflow": "chatgpt",
        "workflow_label": "ChatGPT Integration",
        "reason": "Document cleanup and reformatting — better for long-form assembly.",
    },
    {
        "id": "word",
        "task_type": "Word / Excel Output",
        "keywords": [
            "word doc", "docx", "excel", "xlsx", "spreadsheet", "word document",
        ],
        "workflow": "chatgpt",
        "workflow_label": "ChatGPT Integration",
        "reason": "Word and Excel outputs integrate more reliably through ChatGPT.",
    },
    {
        "id": "review",
        "task_type": "Review / Feedback",
        "keywords": [
            "review", "second opinion", "feedback", "critique", "check",
            "look at", "thoughts on", "is this right",
        ],
        "workflow": "general",
        "workflow_label": "General",
        "reason": "Reviews work well in any agent — use the most relevant specialist.",
    },
    {
        "id": "longdoc",
        "task_type": "Long Doc Assembly",
        "keywords": [
            "assemble", "compile", "full document", "full report",
            "entire", "complete document", "whole file",
        ],
        "workflow": "chatgpt",
        "workflow_label": "ChatGPT Integration",
        "reason": "Long document assembly — ChatGPT handles large context well.",
    },
]

# Default when no keywords match
DEFAULT_ROUTE = RoutingResult(
    task_type="General Help",
    workflow="general",
    workflow_label="General",
    reason="No specific task type detected — routing to general assistance.",
)


def classify_task(message: str) -> RoutingResult:
    """
    Keyword-based task classifier.
    Scores each route by counting how many of its keywords appear in the message.
    Returns the highest-scoring route, or DEFAULT_ROUTE if nothing matches.
    """
    lower = message.lower()
    best_route = None
    best_score = 0

    for route in ROUTE_CONFIG:
        score = sum(1 for kw in route["keywords"] if kw in lower)
        if score > best_score:
            best_score = score
            best_route = route

    if best_route is None or best_score == 0:
        return DEFAULT_ROUTE

    return RoutingResult(
        task_type=best_route["task_type"],
        workflow=best_route["workflow"],
        workflow_label=best_route["workflow_label"],
        reason=best_route["reason"],
    )
