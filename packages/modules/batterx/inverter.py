#!/usr/bin/env python3
from typing import Dict, Union

from dataclass_utils import dataclass_from_dict
from modules.batterx.config import BatterXInverterSetup
from modules.common.component_state import InverterState
from modules.common.component_type import ComponentDescriptor
from modules.common.fault_state import ComponentInfo
from modules.common.simcount import SimCounter
from modules.common.store import get_inverter_value_store


class BatterXInverter:
    def __init__(self, device_id: int, component_config: Union[Dict, BatterXInverterSetup]) -> None:
        self.__device_id = device_id
        self.component_config = dataclass_from_dict(BatterXInverterSetup, component_config)
        self.__sim_counter = SimCounter(self.__device_id, self.component_config.id, prefix="pv")
        self.__store = get_inverter_value_store(self.component_config.id)
        self.component_info = ComponentInfo.from_component_config(self.component_config)

    def update(self, resp: Dict) -> None:
        power = resp["1634"]["0"] * -1

        _, exported = self.__sim_counter.sim_count(power)

        inverter_state = InverterState(
            power=power,
            exported=exported
        )
        self.__store.set(inverter_state)


component_descriptor = ComponentDescriptor(configuration_factory=BatterXInverterSetup)
