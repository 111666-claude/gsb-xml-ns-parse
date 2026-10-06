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
        self._index = {}

    def add(self, ns, local, attrs):
        elem = Elem(ns, local, attrs)
        self.elems.append(elem)
        self._index.setdefault((ns, local), []).append(elem)

    def find(self, ns, local, counter):
        bucket = self._index.get((ns, local), ())
        counter.scanned += len(bucket)
        return list(bucket)


def parse(raw, counter):
    doc = Doc()
    parser = expat.ParserCreate()
    scopes = [{"": ""}]

    def start(name, attrs):
        counter.scanned += 1
        ns = dict(scopes[-1])
        for key, value in attrs.items():
            if key == "xmlns":
                ns[""] = value
            elif key.startswith("xmlns:"):
                ns[key[6:]] = value
        scopes.append(ns)
        if ":" in name:
            prefix, local = name.split(":", 1)
            uri = ns.get(prefix, "")
        else:
            uri = ns.get("", "")
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
                attr_ns = ""
            out_attrs.append((attr_ns, local_attr, value))
        doc.add(uri, local, out_attrs)

    def end(name):
        scopes.pop()

    parser.StartElementHandler = start
    parser.EndElementHandler = end
    parser.Parse(raw.encode("utf-8"))
    return doc
