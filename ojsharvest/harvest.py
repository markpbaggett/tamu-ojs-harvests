import click
from ojsharvest import OAIHarvester

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
def harvest(endpoint: str) -> None:
    harvester = OAIHarvester(endpoint)
    harvester.list_records(
        metadata_prefix="oai_dc",
        from_date="1900-01-01",
        until_date="2024-12-01"
    )

