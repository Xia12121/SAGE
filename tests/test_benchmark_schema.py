import json

from benchmarks.common.schema import BenchmarkSpec, load_spec


def test_load_spec_reads_generated_json_spec(tmp_path):
    spec_path = tmp_path / "spec.json"
    spec_data = {
        "name": "demo",
        "task_file": "tasks/demo.jsonl",
        "output_dir": str(tmp_path / "outputs"),
        "command": ["python", "-m", "demo"],
        "env": {"TOKENIZERS_PARALLELISM": "false"},
        "description": "Demo benchmark",
    }
    spec_path.write_text(json.dumps(spec_data), encoding="utf-8")

    spec = load_spec(spec_path)

    assert spec == BenchmarkSpec(
        name="demo",
        task_file="tasks/demo.jsonl",
        output_dir=str(tmp_path / "outputs"),
        command=["python", "-m", "demo"],
        env={"TOKENIZERS_PARALLELISM": "false"},
        description="Demo benchmark",
    )
