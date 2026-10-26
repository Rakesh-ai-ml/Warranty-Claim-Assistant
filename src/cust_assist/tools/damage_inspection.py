from crewai.tools import BaseTool
import ollama
import json


class DamageInspectionTool(BaseTool):
    
    name: str = "damage_inspection"
    description: str = "Inspect uploaded product image and identify physical damage."

    def _run(self, image_path: str):

        if not image_path:
            return {
                "damage_detected": False,
                "inspection_decision": "no_image"
            }

        response = ollama.chat(
            model="qwen3-vl:2b",
            messages=[
                {
                    "role": "user",
                    "content": """
                    Examine this product image.

                    Check for:

                    - cracks
                    - broken plastic
                    - broken earbuds
                    - dents
                    - burn marks
                    - severe scratches
                    - missing parts
                    - signs of impact damage

                    Return ONLY JSON.

                    {
                        "damage_detected": true,
                        "damage_type": "",
                        "confidence": 0.95,
                        "inspection_decision": "fail",
                        "reason": ""
                    }

                    If no visible physical damage:

                    {
                        "damage_detected": false,
                        "damage_type": "",
                        "confidence": 0.90,
                        "inspection_decision": "pass",
                        "reason": ""
                    }
                    """
                    ,
                    "images": [image_path]
                }
            ]
        )

        try:
            return json.loads(
                response["message"]["content"]
            )

        except Exception:

            return {
                "damage_detected": False,
                "damage_type": "",
                "confidence": 0,
                "inspection_decision": "unknown",
                "reason": response["message"]["content"]
            }