"""解析元素与属性的展开名。"""

import xml.parsers.expat as expat


class Counter:
    """记录处理的元素数。"""

    def __init__(self):
        self.scanned = 0


class Elem:
    def __init__(self, ns, local, attrs):
        self.ns = ns
        self.local = local
        self.attrs = attrs


class Doc:
    def __init__(self):
        self.elems = []

    def find(self, ns, local, counter):
        out = []
        for elem in self.elems:
            counter.scanned += 1
            if elem.ns == ns and elem.local == local:
                out.append(elem)
        return out


def parse(raw, counter):
    doc = Doc()
    parser = expat.ParserCreate()
    ns = {}
    default = [""]

    def start(name, attrs):
        counter.scanned += 1
        for key, value in attrs.items():
            if key == "xmlns":
                default[0] = value
            elif key.startswith("xmlns:"):
                ns[key[6:]] = value
        if ":" in name:
            prefix, local = name.split(":", 1)
            uri = ns.get(prefix, "")
        else:
            uri = ""
            local = name
        out_attrs = []
        for key, value in attrs.items():
            if key == "xmlns" or key.startswith("xmlns:"):
                continue
            if ":" in key:
                prefix, local_attr = key.split(":", 1)
                attr_ns = ns.get(prefix, "")
            else:
                local_attr = key
                attr_ns = default[0]
            out_attrs.append((attr_ns, local_attr, value))
        doc.elems.append(Elem(uri, local, out_attrs))

    parser.StartElementHandler = start
    parser.Parse(raw.encode("utf-8"))
    return doc
