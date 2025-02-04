import click
from ojsharvest import OAIHarvester
import arrow
import os
from pathlib import Path

@click.group()
def cli() -> None:
    pass

@cli.command("harvest", help="Harvest an endpoint")
@click.option(
    "--endpoint",
    "-e",
    help="An endpoint URL (e.g. https://awl-ojs-tamu.tdl.org/awl/oai)",
    required=True
)
@click.option(
    "--output",
    "-o",
    help="Subdirectory to output harvested records to",
    required=True
)
@click.option(
    "--begin",
    "-b",
    default="45",
    help="Number of days ago to harvest from"
)
def harvest(endpoint: str, output: str, begin: str) -> None:
    beginning = arrow.now().shift(days=-int(begin)).format('YYYY-MM-DD')
    end = arrow.now().format('YYYY-MM-DD')
    print(f"Harvesting data from {beginning} ...")
    harvester = OAIHarvester(endpoint, output_dir=f"oai_records/{output}")
    harvester.list_records(
        metadata_prefix="oai_dc",
        from_date=beginning,
        until_date=end
    )

@cli.command("count", help="Count records an endpoint")
@click.option(
    "--endpoint",
    "-e",
    help="An endpoint URL (e.g. https://awl-ojs-tamu.tdl.org/awl/oai)",
    required=True
)
@click.option(
    "--begin",
    "-b",
    default="45",
    help="Number of days ago to harvest from"
)
def count(endpoint: str, begin: str) -> None:
    beginning = arrow.now().shift(days=-int(begin)).format('YYYY-MM-DD')
    end = arrow.now().format('YYYY-MM-DD')
    print(f"Counting data from {beginning} ...")
    harvester = OAIHarvester(endpoint)
    x = harvester.list_identifiers(
        metadata_prefix="oai_dc",
        from_date=begin,
        until_date=end
    )
    print(x)

@cli.command("stats", help="Count records on disk and update README.")
@click.option(
    "--path",
    "-p",
    default="oai_records",
    help="Where to read on disk"
)
def stats(path: str) -> None:
    all_journals = {}
    for new_path, directories, files in os.walk(path):
        for directory in directories:
            count = sum(1 for _ in Path(f"{path}/{directory}").rglob("*") if _.is_file())
            all_journals[directory] = count
    with open("README.md", "w") as readme:
        readme.write("# tamu-ojs-harvest\n\nA Simple OAI PMH Harvester to Get All Records from TAMU OJS Instances on a regular basis with Actions.\n\n## Stats\n\n")
        readme.write("| Journal | Total Articles |\n| -------- | ------- |\n")
        sorted(all_journals.keys())
        for k, v in all_journals.items():
            readme.write(f"| {k} | {v} |\n")

