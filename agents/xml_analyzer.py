import xml.etree.ElementTree as ET


class XMLAnalyzer:

    def analyze(self, xml_path: str) -> dict:

        tree = ET.parse(xml_path)
        root = tree.getroot()

        result = {
            "views": [],
            "actions": [],
            "menus": [],
            "records": [],
            "view_fields": [],
            "reports": [],
        }

        for element in root.iter():

            # ==========================================
            # RECORD
            # ==========================================

            if element.tag == "record":

                record_id = element.attrib.get("id")
                model = element.attrib.get("model")

                result["records"].append({
                    "id": record_id,
                    "model": model,
                })

                # ======================================
                # VIEW
                # ======================================

                if model == "ir.ui.view":

                    view_info = {
                        "id": record_id,
                        "model": None,
                        "type": None,
                        "fields": [],
                        "xpaths": [],
                    }

                    for field in element.findall("field"):

                        field_name = field.attrib.get("name")

                        if field_name == "model":

                            view_info["model"] = (
                                field.text or ""
                            ).strip()

                        elif field_name == "arch":

                            arch = list(field)

                            if arch:

                                view_info["type"] = arch[0].tag

                                for node in arch[0].iter():

                                    # ======================================
                                    # XPATH
                                    # ======================================

                                    if node.tag == "xpath":

                                        view_info["xpaths"].append({
                                            "expr": node.attrib.get("expr"),
                                            "position": node.attrib.get("position"),
                                        })

                                    # ======================================
                                    # FIELD
                                    # ======================================

                                    elif node.tag == "field":

                                        name = node.attrib.get("name")

                                        if name:
                                            view_info["fields"].append(name)

                    result["views"].append(view_info)

                # ======================================
                # ACTION
                # ======================================

                elif model == "ir.actions.act_window":

                    result["actions"].append(
                        record_id
                    )

                elif model == "ir.actions.report":

                    report_info = {
                        "id": record_id,
                        "model": None,
                        "report_type": None,
                        "report_name": None,
                    }

                    for field in element.findall("field"):

                        field_name = field.attrib.get("name")
                        value = (field.text or "").strip()

                        if field_name == "model":
                            report_info["model"] = value

                        elif field_name == "report_type":
                            report_info["report_type"] = value

                        elif field_name == "report_name":
                            report_info["report_name"] = value

                    result["reports"].append(report_info)

            # ==========================================
            # MENU
            # ==========================================

            elif element.tag == "menuitem":

                result["menus"].append({
                    "id": element.attrib.get("id"),
                    "name": element.attrib.get("name"),
                })

        return result