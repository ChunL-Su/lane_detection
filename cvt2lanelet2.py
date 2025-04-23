from lxml import etree


def save_to_lanelet2(points, output_path):
    root = etree.Element("lanelet", id="1")
    left = etree.SubElement(root, "leftBound")
    linestring = etree.SubElement(left, "lineString")

    for x, y in points:
        etree.SubElement(linestring, "point", attrib={
            "x": str(x), "y": str(y), "z": "0.0"
        })

    tree = etree.ElementTree(root)
    tree.write(output_path, pretty_print=True, encoding='utf-8')


if __name__ == '__main__':
    save_to_lanelet2(lane_curve, r"C:\your_project\output\lanelet2.osm")