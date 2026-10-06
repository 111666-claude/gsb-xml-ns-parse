"""固定场景，用来复现题面里的锚点。"""

import json

from . import core


def _line(obj):
    print(json.dumps(obj, ensure_ascii=False))


def run(name):
    if name == "defaultns":
        doc = core.parse('<root xmlns="urn:a"><child/></root>', core.Counter())
        _line({"ns": doc.elems[1].ns})
        return 0
    if name == "attr":
        doc = core.parse('<r xmlns="urn:a" k="1"/>', core.Counter())
        _line({"ns": doc.elems[0].attrs[0][0]})
        return 0
    if name == "scope":
        raw = ('<r xmlns:p="urn:outer">'
               '<a xmlns:p="urn:inner"><p:x/></a>'
               '<p:y/></r>')
        doc = core.parse(raw, core.Counter())
        _line({"ns": doc.elems[3].ns})
        return 0
    if name == "work":
        inner = "".join("<e%04d/>" % i for i in range(2000))
        doc = core.parse("<r>%s</r>" % inner, core.Counter())
        counter = core.Counter()
        for i in range(2000):
            doc.find("", "e%04d" % i, counter)
        _line({"elements": 2000, "scanned": counter.scanned})
        return 0
    raise SystemExit("未知场景：" + name)
