# Bencode Parser

## 介绍

`.torrent`文件解析器，把人类不可读的二进制种子文件，解析成可读的 `json` 格式

所示的例子是 Ubuntu20.04.2 的种子文件。

`.torrent` 文件格式为 `Bencode` 编码，具体定义参见官方文档：[bep_0003](http://www.bittorrent.org/beps/bep_0003.html)

## 使用

```bash
./main.py ./ubuntu-20.04.2.0-desktop-amd64.iso.torrent > result.json
```
