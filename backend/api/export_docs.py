"""
api/export_docs.py — Export the API documentation to docs/api/.

Writes:
  - docs/api/openapi.json — the OpenAPI spec FastAPI generates from the routes,
    models and docstrings.
  - docs/api/index.html   — a standalone Swagger UI page with the spec embedded,
    viewable without running the server ("Try it out" still needs it running).

Run from the backend/ directory after changing the API:
    python -m api.export_docs
"""
import json
from pathlib import Path

from .main import app

DOCS_DIR = Path(__file__).resolve().parents[2] / "docs" / "api"

HTML = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>{title} — API docs</title>
  <link rel="stylesheet" href="https://unpkg.com/swagger-ui-dist@5/swagger-ui.css">
</head>
<body>
  <div id="swagger-ui"></div>
  <script src="https://unpkg.com/swagger-ui-dist@5/swagger-ui-bundle.js"></script>
  <script>
    SwaggerUIBundle({{
      spec: {spec},
      dom_id: '#swagger-ui',
      defaultModelsExpandDepth: 1,
    }});
  </script>
</body>
</html>
"""


def inline_refs(node, schemas):
    """
    Replace {"$ref": "#/components/schemas/X"} with the schema itself.
    Swagger UI cannot resolve these refs when index.html is opened from disk
    (file:// URL), so the embedded copy carries the schemas inline.
    """
    if isinstance(node, dict):
        ref = node.get("$ref", "")
        if ref.startswith("#/components/schemas/"):
            return inline_refs(schemas[ref.rsplit("/", 1)[1]], schemas)
        return {key: inline_refs(value, schemas) for key, value in node.items()}
    if isinstance(node, list):
        return [inline_refs(item, schemas) for item in node]
    return node


def main() -> None:
    spec = app.openapi()
    spec["servers"] = [{"url": "http://localhost:8080", "description": "Local server"}]
    DOCS_DIR.mkdir(parents=True, exist_ok=True)

    spec_json = json.dumps(spec, indent=2, ensure_ascii=False)
    (DOCS_DIR / "openapi.json").write_text(spec_json + "\n", encoding="utf-8")

    schemas = spec.get("components", {}).get("schemas", {})
    page_spec = {**spec, "paths": inline_refs(spec["paths"], schemas)}
    (DOCS_DIR / "index.html").write_text(
        HTML.format(title=spec["info"]["title"], spec=json.dumps(page_spec, ensure_ascii=False)),
        encoding="utf-8",
    )
    print(f"API docs written to {DOCS_DIR}")


if __name__ == "__main__":
    main()
