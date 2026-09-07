from importlib.resources import files
from pathlib import Path
from typing import Annotated

from pytask import Product, mark

from wp3_d_quest import common, metadata

common.dotenv.load_env_vars()

SRC = Path(str(files("wp3_d_quest"))).joinpath("..").resolve()
BLD = SRC.joinpath("..", "bld").resolve()

BLD_REDCAP = BLD / "redcap"

METADATA_PATH = BLD_REDCAP / "metadata.json"
DATAPACKAGE_PATH = SRC / "datapackage.json"


@mark.metadata
def task_download_metadata(
    metadata_path: Annotated[Path, Product] = METADATA_PATH,
) -> None:
    """Download the metadata to `BLD_REDCAP`."""
    redcap_metadata = common.redcap.get_json("metadata")
    common.json.write(metadata_path, redcap_metadata)


@mark.metadata
def task_create_datapackage_json(
    datapackage_path: Annotated[Path, Product] = DATAPACKAGE_PATH,
    metadata_path: Path = METADATA_PATH,
) -> None:
    """Create the datapackage.json file from the REDCap metadata."""
    redcap_metadata = common.json.read(metadata_path)
    datapackage = metadata.redcap.create_datapackage(redcap_metadata)
    common.json.write(datapackage_path, datapackage)
