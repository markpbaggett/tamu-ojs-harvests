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
def harvest(endpoint: str, output: str) -> None:
    begin = arrow.now().shift(days=-180).format('YYYY-MM-DD')
    end = arrow.now().format('YYYY-MM-DD')
    harvester = OAIHarvester(endpoint, output_dir=f"oai_records/{output}")
    harvester.list_records(
        metadata_prefix="oai_dc",
        from_date=begin,
        until_date=end
    )

