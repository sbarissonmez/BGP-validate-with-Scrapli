import asyncio
from typing import Dict, Tuple

import yaml
from jinja2 import Environment, FileSystemLoader
from scrapli.driver.core import AsyncIOSXEDriver
from scrapli.response import MultiResponse

from inventory import DEVICES
from validation_models import BGPConfig


def generate_config(device: Dict[str, str]) -> str:
    """
    Function that retrieves YAML data from host variables.
    Verify that the data meets the specified constraints.
    Process the configuration.


    Args:
        device (Dict[str, str]): Each device in the inventory

    Returns:
        str: BGP configuration processed for each device
    """

    hostname = device["hostname"]
    with open(f"host_vars/bgp/{hostname}.yaml", "r", encoding="utf8") as file:
        config_data = yaml.safe_load(file)
    my_data = [BGPConfig(**line) for line in config_data]
    cfg = my_data[0].dict()
    env = Environment(
        loader=FileSystemLoader("./templates"), trim_blocks=True, lstrip_blocks=True
    )
    template = env.get_template("bgp.j2")
    configuration = template.render(cfg)
    return configuration


async def push_config(device: Dict[str, str]) -> Tuple[str, MultiResponse]:
    """
    Function to send the processed configurations to the device


    Args:
        device (Dict[str, str]): Each device in the inventory

    Returns:
        Tuple[str, MultiResponse]: Returns the Device Prompt
        & Scrapli MultiResponse Object
    """

    async with AsyncIOSXEDriver(
        host=device["host"],
        auth_username="cisco",
        auth_password="cisco",
        auth_strict_key=False,
        transport="asyncssh",
    ) as conn:
        prompt_result = await conn.get_prompt()
        cfg = generate_config(device).splitlines()
        configs_result = await conn.send_configs(configs=cfg)
    return prompt_result, configs_result


async def main() -> None:
    """
    Major coroutine
    """

    coroutines = [push_config(device) for device in DEVICES]
    results = await asyncio.gather(*coroutines)
    for result in results:
        print(result[0])
        print(result[1].result)
        print("\n")


asyncio.run(main())
