import json

import click
from rich.console import Console
from rich.table import Table

from .models import Index
from .plan import build_plan

console = Console()


@click.command()
@click.option("--repo", required=True, help="Snapshot repository name")
@click.option("--snapshot", required=True, help="Snapshot name to create")
def main(repo: str, snapshot: str) -> None:
    # Demo dataset
    data = [
        Index(name="logs-2025.07.01", size_gb=120.5, created_days_ago=20),
        Index(name="metrics-2024.02.10", size_gb=600.0, created_days_ago=500),
        Index(name="traces-2025.06.15", size_gb=80.0, created_days_ago=60),
    ]
    plan = build_plan(repo, data, snapshot)
    table = Table(title=f"Snapshot Plan: {snapshot} -> {repo}")
    table.add_column("Index")
    table.add_column("Size(GB)")
    table.add_column("Age(days)")
    for i in plan.indices:
        table.add_row(i.name, str(i.size_gb), str(i.created_days_ago))
    console.print(table)
    console.print("Manifest (JSON):")
    console.print_json(data=json.loads(plan.model_dump_json()))

if __name__ == "__main__":
    main()
