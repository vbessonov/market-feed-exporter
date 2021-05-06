import logging
import os

from requests.auth import HTTPBasicAuth
from webpub_manifest_parser.odl.ast import ODLFeed
from webpub_manifest_parser.odl.parsers import ODLDocumentParserFactory
from webpub_manifest_parser.opds2.registry import OPDS2LinkRelationsRegistry
from webpub_manifest_parser.utils import first_or_default


class MarketFeedExporter:
    def __init__(self):
        self._logger = logging.getLogger(__name__)

    def _parse_feed(
        self, feed_url: str, feed_login: str, feed_password: str
    ) -> ODLFeed:
        self._logger.info(f"Started parsing {feed_url}")

        parser_factory = ODLDocumentParserFactory()
        parser = parser_factory.create()
        feed = parser.parse_url(
            feed_url, "utf-8 ", HTTPBasicAuth(feed_login, feed_password)
        )

        self._logger.info(f"Finished parsing {feed_url}")

        return feed

    def export(
        self, feed_url: str, feed_login: str, feed_password: str, output_file: str
    ) -> None:

        self._logger.info(f"Started exporting {feed_url}")

        with open(output_file, "w") as output_file:
            output_file.write(
                "{0}\t{1}\t{2}\t{3}\t{4}\t{5}\n".format(
                    "url",
                    "page",
                    "title",
                    "identifier",
                    "self_link",
                    "oa_acquisition_link",
                )
            )

            page = 1

            while True:
                try:
                    feed = self._parse_feed(feed_url, feed_login, feed_password)

                    for publication in feed.publications:
                        identifier = publication.metadata.identifier
                        title = publication.metadata.title.replace(
                            "&#39;", "'"
                        )
                        self_link = first_or_default(
                            publication.links.get_by_rel(
                                OPDS2LinkRelationsRegistry.SELF.key
                            )
                        )
                        self_link_href = self_link.href if self_link is not None else ""
                        oa_acquisition_link = first_or_default(
                            publication.links.get_by_rel(
                                OPDS2LinkRelationsRegistry.OPEN_ACCESS.key
                            )
                        )
                        oa_acquisition_link_href = (
                            oa_acquisition_link.href
                            if oa_acquisition_link is not None
                            else ""
                        )

                        output_file.write(
                            "{0}\t{1}\t{2}\t{3}\t{4}\t{5}\n".format(
                                feed_url,
                                page,
                                title,
                                identifier,
                                self_link_href,
                                oa_acquisition_link_href,
                            )
                        )

                    next_link = first_or_default(feed.links.get_by_rel("next"))

                    if not next_link:
                        break

                    feed_url = next_link.href
                    page += 1
                except Exception:
                    self._logger.exception(
                        "An unexpected error occurred during parsing {0}".format(feed_url)
                    )

        output_file_path = os.path.join(os.getcwd(), output_file.name)

        self._logger.info(f"Finished exporting. The results have been saved to {output_file_path}")
