import os
import httpx
from lxml import etree


class OAIHarvester:
    def __init__(self, base_url, output_dir="oai_records"):
        self.base_url = base_url
        self.ns = {'oai': 'http://www.openarchives.org/OAI/2.0/'}
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

    def fetch(self, params):
        try:
            response = httpx.get(self.base_url, params=params, timeout=30.0)
            response.raise_for_status()
            return etree.fromstring(response.content)
        except httpx.RequestError as e:
            print(f"An error occurred while requesting: {e}")
            return None
        except etree.XMLSyntaxError as e:
            print(f"An error occurred while parsing XML: {e}")
            return None

    def save_record_to_disk(self, record, record_number):
        record_xml = etree.tostring(record, pretty_print=True, encoding="utf-8", xml_declaration=True)
        file_path = os.path.join(self.output_dir, f"{record_number}.xml")
        with open(file_path, "wb") as f:
            f.write(record_xml)
        print(f"Saved record to {file_path}")

    def list_records(self, metadata_prefix, from_date=None, until_date=None):
        params = {
            "verb": "ListRecords",
            "metadataPrefix": metadata_prefix,
        }
        if from_date:
            params["from"] = from_date
        if until_date:
            params["until"] = until_date

        record_number = 1

        while True:
            xml = self.fetch(params)
            if xml is None:
                break

            records = xml.xpath("//oai:record", namespaces=self.ns)
            for record in records:
                identifier = record.find(".//oai:identifier", namespaces=self.ns).text
                file_name = f"{identifier.replace(':', '_').replace('/', '_')}.xml"
                self.save_record_to_disk(record, file_name)
                record_number += 1

            resumption_token = xml.find(".//oai:resumptionToken", namespaces=self.ns)
            if resumption_token is not None and resumption_token.text:
                params = {"verb": "ListRecords", "resumptionToken": resumption_token.text}
            else:
                break


if __name__ == "__main__":
    base_url = "https://awl-ojs-tamu.tdl.org/awl/oai"  # Replace with your OAI-PMH base URL
    harvester = OAIHarvester(base_url)
    print("\nHarvesting Records:")
    harvester.list_records(metadata_prefix="oai_dc", from_date="1999-01-01", until_date="2024-12-01")
