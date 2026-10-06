# xml-ns-parse

解析 XML 的命名空间：前缀按作用域解析、默认命名空间只作用于元素、无前缀属性不带命名空间，并支持按展开名查找。只用 Python 标准库。

```
python3 -m unittest discover -s tests
python3 -m xmlns --sample=defaultns
python3 -m xmlns --sample=attr
python3 -m xmlns --sample=scope
python3 -m xmlns --sample=work
```

## 口径

- **默认命名空间**：`xmlns="..."` 声明的默认命名空间作用于本元素及其后代的**元素名**。
- **前缀**：`xmlns:p="..."` 声明的前缀绑定只在声明它的元素及其后代里有效；离开作用域后恢复外层绑定。
- **属性**：带前缀的属性按前缀解析；**不带前缀的属性不带命名空间**。
- **查找**：按展开名（命名空间 URI + 本地名）查找元素，走索引，不逐个比较。

## 不变量

- 每个元素的命名空间由它所在作用域内的绑定决定，与兄弟元素互不影响。
- 查找结果按文档顺序返回。
- `scanned` 不随元素数平方级放大：两千个元素查两千次的 `scanned` 不超过 6000。

## 输出契约

解析结果是元素列表，每个元素含 `ns` / `local` / `attrs`（属性为 `(ns, local, value)`）。
场景打印一行 JSON。`--sample=work` 打印 `{"elements": N, "scanned": N}`。
