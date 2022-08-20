from heapq import merge
from logging import getLogger
from pathlib import Path
from psd2pngs.layer_info import LayerInfo, get_layer_info
from psd_tools import PSDImage
from typing import List, Dict, Tuple, Any, TypedDict, Union, Optional

from psd_generator_builder.typed_lua_table_serializer import deserialize


def generate_settings(psd_image: PSDImage) -> str:
    root_layer_info = get_layer_info(psd_image)
    d = {
        "type": "",
        "Tools": {
            "type": "Tools",
            "RootMacroTool": {
                "type": "MacroOperator",
                "Inputs": instance_inputs,
                "Outputs": output,
                "Tools": tools,
            },
        },
    }
    return deserialize(d)


def generate_comp(
    layer_info: LayerInfo, base_path: Path, used_ids: list[str] = []
) -> dict:
    if layer_info["is_group"]:
        last_merge_id = None
        for child in layer_info["children"]:
            inc = 0
            while True:
                base_id = (
                    layer_info["safe_name"] + str(inc)
                    if inc > 0
                    else layer_info["safe_name"]
                )
                inc += 1
                if base_id not in used_ids:
                    break

            loader_id = base_id + "Loader"
            merge_id = base_id + "Merge"
            yield (
                loader_id,
                {
                    "type": "Loader",
                    "Clips": {
                        None: {
                            "type": "Clip",
                            "Filename": base_path / child["local_path"],
                        }
                    },
                },
            )

            yield (
                merge_id,
                {
                    "type": "Merge",
                    "Inputs": {
                        "Blend": {"type": "Input", "Expression": "iif()==,1,0"},
                        "Background": {
                            "type": "Input",
                            "SourceOp": "",
                            "Source": last_merge_id,
                        },
                        "Foreground": {
                            "type": "Input",
                            "SourceOp": loader_id,
                            "Source": "Output",
                        },
                    },
                },
            )
            yield {"type": "TimeStretcher" ""}
