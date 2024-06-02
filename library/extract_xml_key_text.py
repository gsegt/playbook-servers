from pathlib import Path
from xml.etree.ElementTree import Element, ElementTree, parse

from ansible.module_utils.basic import AnsibleModule


def main() -> None:
    module_args: dict[str, dict[str, str | bool]] = {
        "xml_file_path": {"type": "str", "required": True},
        "xml_key_xpath": {"type": "str", "required": True},
    }

    result: dict[str, str] = {
        "key_text": "",
    }

    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)

    xml_file_path: Path = Path(module.params["xml_file_path"])
    xml_key_xpath: str = module.params["xml_key_xpath"]

    try:
        # Open and parse the XML file
        with xml_file_path.open("r") as xml_file:
            tree: ElementTree = parse(xml_file)  # noqa: S314 keeping regular xml for native compatibility
        root: Element = tree.getroot()
        key: Element | None = root.find(xml_key_xpath)

    except FileNotFoundError:
        message = f"{xml_file_path.as_posix()} does not exist!"
        module.fail_json(msg=message, **result)

    except IsADirectoryError:
        message = f"{xml_file_path.as_posix()} is a directory!"
        module.fail_json(msg=message, **result)

    # Ensure the XPath exists and contains text before returning its value
    if key is None:
        message = f"The XPath {xml_key_xpath} did not return a valid element!"
        module.fail_json(msg=message, **result)
    elif key.text is None:
        message = f"The XPath {xml_key_xpath} has no text!"
        module.fail_json(msg=message, **result)
    else:
        result["key_text"] = key.text
        module.exit_json(**result)


if __name__ == "__main__":
    main()
