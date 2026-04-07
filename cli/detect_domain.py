"""Detect research domain via researchclaw.domains.detector."""
from __future__ import annotations

import json
import sys
from typing import Any

from researchclaw.domains.detector import detect_domain


def format_profile_json(profile: Any) -> dict[str, Any]:
    """Convert a DomainProfile to a JSON-serializable dict."""
    return {
        "domain_id": profile.domain_id,
        "display_name": profile.display_name,
        "experiment_paradigm": profile.experiment_paradigm,
        "core_libraries": profile.core_libraries,
        "metric_types": profile.metric_types,
        "standard_baselines": profile.standard_baselines,
        "figure_types": profile.figure_types,
        "statistical_tests": profile.statistical_tests,
        "dataset_guidance": profile.dataset_guidance,
        "code_generation_hints": profile.code_generation_hints,
        "compute_budget_guidance": profile.compute_budget_guidance,
    }


def run_detect(topic: str) -> str:
    """Detect domain and return JSON string."""
    profile = detect_domain(topic=topic)
    return json.dumps(format_profile_json(profile), indent=2, ensure_ascii=False)


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="Detect research domain")
    parser.add_argument("--topic", required=True, help="Research topic")
    args = parser.parse_args()
    try:
        print(run_detect(args.topic))
    except Exception as exc:
        print(json.dumps({"error": str(exc)}), file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
