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
        self._index = None

    def _build_index(self):
        self._index = {}
        for elem in self.elems:
            self._index.setdefault((elem.ns, elem.local), []).append(elem)

    def find(self, ns, local, counter):
        if self._index is None:
            self._build_index()
        counter.scanned += 1
        return list(self._index.get((ns, local), []))


def parse(raw, counter):
    doc = Doc()
    parser = expat.ParserCreate()
    scopes = [({}, "")]

    def start(name, attrs):
        counter.scanned += 1
        bindings, default = scopes[-1]
        bindings = dict(bindings)
        for key, value in attrs.items():
            if key == "xmlns":
                default = value
            elif key.startswith("xmlns:"):
                bindings[key[6:]] = value
        scopes.append((bindings, default))
        if ":" in name:
            prefix, local = name.split(":", 1)
            uri = bindings.get(prefix, "")
        else:
            uri = default
            local = name
        out_attrs = []
        for key, value in attrs.items():
            if key == "xmlns" or key.startswith("xmlns:"):
                continue
            if ":" in key:
                prefix, local_attr = key.split(":", 1)
                attr_ns = bindings.get(prefix, "")
            else:
                local_attr = key
                attr_ns = ""
            out_attrs.append((attr_ns, local_attr, value))
        doc.elems.append(Elem(uri, local, out_attrs))

    def end(name):
        scopes.pop()

    parser.StartElementHandler = start
    parser.EndElementHandler = end
    parser.Parse(raw.encode("utf-8"))
    return doc
