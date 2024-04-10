import json


def to_result(
    path: str,
    line_number: int,
    column_number: int,
    rule_id: str,
    message: str,
    length: int,
    replacement: str = None,
    replacement_message: str = None,
):
    region = {
        "startColumn": column_number,
        "startLine": line_number,
        "endLine": line_number,
        "endColumn": column_number + length,
    }

    result = {
        "level": "error",
        "locations": [
            {
                "physicalLocation": {
                    "artifactLocation": {
                        "uri": path,
                    },
                    "region": region,
                }
            }
        ],
        "message": {
            "text": message,
        },
        "ruleId": rule_id,
    }

    if replacement:
        result["fixes"] = [
            {
                "description": {"text": replacement_message},
                "artifactChanges": [
                    {
                        "artifactLocation": {"uri": path},
                        "replacements": [
                            {
                                "deletedRegion": region,
                                "insertedContent": {"text": replacement},
                            }
                        ],
                    }
                ],
            }
        ]

    return result


def to_sarif_log(results: list, tool_name: str):
    return {
        "$schema": "https://raw.githubusercontent.com/oasis-tcs/sarif-spec/master/Schemata/sarif-schema-2.1.0.json",
        "version": "2.1.0",
        "runs": [{"results": results, "tool": {"driver": {"name": tool_name}}}],
    }


def print_sarif_log(results: list, tool_name: str):
    print(json.dumps(to_sarif_log(results, tool_name), indent=2))
