from unittest import TestCase

from psd_generator_builder.typed_lua_table_serializer import deserialize


class TestTypedLuaTableSerializer(TestCase):
    def test_normal(self):
        d = {
            "type": "",
            "Tools": {
                "type": "Tools",
                "RootMacroTool": {
                    "type": "MacroOperator",
                    "Inputs": {
                        "type": "oredered()",
                    },
                },
            },
        }
        result = deserialize(d)
        expected = "{ Tools = Tools { RootMacroTool = MacroOperator { Inputs = oredered() {  },  },  },  }"
        self.assertEqual(result, expected)
    
    def test_non_dict(self):
        obj = "abc"
        result = deserialize(obj)
        expected = '"abc"'
        self.assertEqual(result, expected)
