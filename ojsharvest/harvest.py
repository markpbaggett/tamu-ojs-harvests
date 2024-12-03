import click
from ojsharvest import OAIHarvester
import arrow

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

