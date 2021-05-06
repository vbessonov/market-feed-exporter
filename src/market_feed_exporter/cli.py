import logging
import sys
from types import TracebackType
from typing import Type

import click as click

from market_feed_exporter.exporter import MarketFeedExporter


def excepthook(
    exception_type: Type[BaseException],
    exception_instance: BaseException,
    exception_traceback: TracebackType,
) -> None:
    """Function called for uncaught exceptions
    :param exception_type: Type of an exception
    :param exception_instance: Exception instance
    :param exception_traceback: Exception traceback
    """
    logging.fatal(
        f"Exception hook has been fired: {exception_instance}",
        exc_info=(exception_type, exception_instance, exception_traceback),
    )


sys.excepthook = excepthook


@click.group()
@click.pass_context
def cli(*args, **kwargs) -> None:  # type: ignore
    """market-feed-exporter is a CLI tool allowing to export ODL market feeds into a .CSV file."""
    logging.basicConfig(level=logging.INFO)


@cli.command()
@click.option(
    "--feed-url",
    "-u",
    help="Market feed's URL",
    required=False,
    type=str,
    default="https://market.feedbooks.com/api/libraries/harvest.json",
)
@click.option(
    "--feed-login",
    "-l",
    help="Login of the user allowed to access the feed",
    required=True,
    type=str,
)
@click.option(
    "--feed-password",
    "-p",
    help="Password of the user allowed to access the feed",
    required=True,
    type=str,
)
@click.option(
    "--output-file",
    "-o",
    help="Name of the CSV file used to store the result of export",
    required=False,
    type=str,
    default="output.csv",
)
def export(feed_url: str, feed_login: str, feed_password: str, output_file: str) -> None:
    """Export the specific market feed into a .CSV file."""
    exporter = MarketFeedExporter()
    exporter.export(feed_url, feed_login, feed_password, output_file)
