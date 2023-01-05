## WaterMarker简介
用于 pdf 添加水印的小工具，能够自适应的为 pdf 文件每页添加水印，支持脚本运行和编译器内执行
同时支持如下自定义
- 水印文字      (text)
- 水印透明度    (alpha)
- 水印字体      (font)
- 水印字体大小   (size)
- 水印旋转角度   (angle)

## 使用案例
由于支持使用脚本运行，以下内容将重点介绍脚本执行方式

### 脚本具体参数如下
``` bash
optional arguments:
  -h, --help            show this help message and exit
  --text TEXT           Text to add watermark
  -F FILE, --file FILE  The path to the file to add the watermark to
  --font FONT           Font used for watermark text
  --size SIZE           Font size used for watermark text, defaults to 30, the
                        size will adjust itself as the page changes
  --alpha ALPHA         Transparency of watermark text, between 0.0 and 1.0
  --angle ANGLE         Rotate the canvas by the angle theta (in degrees)
  -O OUTPUT, --output OUTPUT
                        File output path after adding watermark (including the
                        file name), the default is the original file directory
```

### 具体案例
- 以下为具体使用案例，其中除 `-F` 和 `-O` 参数外均为默认值
- 若未使用 `--text` 或 `-F` 参数将会要求用户手动输入
```bash
python watermarker.py --text "WaterMarker" -F "C:\test.pdf" --font "SimSun" --alpha 0.1 --size 30 --angle 30 -O "./result.pdf"
```

### 写在最后
- 感谢大家使用，若有更好的想法或者任何疑问，欢迎提交 issue 或者 邮件 <huang_wen_huan@163.com> 联系我，我将及时更新和回复
- 本工具采用 GPL2 开源协议，详细内容参见 [协议](https://github.com/HWH-2019/WaterMarker/blob/main/LICENSE)
