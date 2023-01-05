"""

[WaterMarker: A small tool for adding watermarks to pdf]

Copyright (C) 2023 Huang Wenhuan <huang_wen_huan@163.com>

This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public
License as published by the Free Software Foundation; either version 2 of the License, or (at your option) any later
version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied
warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with this program; if not, write to the Free
Software Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.

"""

import os
import argparse
from PyPDF2 import PdfReader, PdfWriter
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics

''' =============================================
# @Time  : 2023-01-04
# @Author : HWH
# @FileName: WaterMarker.py
# @Description: 用于 pdf 添加水印的小工具，支持脚本运行和手动执行，
#               能够自适应的为 pdf 文件每页添加水印，并支持如下自定义
#               - 水印文字      (text)
#               - 水印透明度    (alpha)
#               - 水印字体      (font)
#               - 水印字体大小   (size)
#               - 水印旋转角度   (angle)
 ============================================= '''

pdfmetrics.registerFont(TTFont('SimSun', './fonts/SimSun.ttf'))  # 注册字体

last_width = 0
last_height = 0


def create_watermark(content, width, height, args):
    # 默认大小为21cm*29.7cm
    file_name = "mark.pdf"
    # 比例，用于自适应 pdf 页面大小
    width = float(width) * 0.0352
    height = float(height) * 0.0352
    ratio_w = width / 21
    ratio_h = height / 29.7
    c = canvas.Canvas(file_name, pagesize=(width * cm, height * cm))
    # 移动坐标原点(坐标系左下为(0,0))
    c.translate(10 * cm * ratio_w, 5 * cm * ratio_h)

    # 设置字体，默认采用 SimSun 字体
    c.setFont(args.font, args.size * (ratio_w + ratio_h) / 2)
    # 指定描边的颜色
    c.setStrokeColorRGB(0, 1, 0)
    # 默认旋转30度,坐标系被旋转
    c.rotate(args.angle)
    # 指定填充颜色
    c.setFillColorRGB(0, 0, 0, args.alpha)

    # 画几个文本,注意坐标系旋转的影响
    for i in range(5):
        for j in range(10):
            # 使用 比例 自适应水印文字位置
            a = 10 * (i - 1) * ratio_w
            b = 5 * (j - 2) * ratio_h
            c.drawString(a * cm, b * cm, content)
    # 关闭并保存pdf文件
    c.save()
    return file_name


def add_watermark(pdf_file_in, pdf_file_out, args):
    global last_height, last_width
    pdf_watermark = []

    pdf_output = PdfWriter()
    input_stream = open(pdf_file_in, 'rb')
    pdf_input = PdfReader(input_stream, strict=False)

    # 获取PDF文件的页数
    pageNum = len(pdf_input.pages)

    # 给每一页打水印
    for i in range(pageNum):
        page = pdf_input.pages[i]
        # 获取当前页面实际宽高
        width = pdf_input.pages[i].mediabox.width
        height = pdf_input.pages[i].mediabox.height
        if width != last_width or height != last_height:
            pdf_file_mark = create_watermark(watermark_text, width, height, args)  # 生成水印文件
            pdf_watermark = PdfReader(open(pdf_file_mark, 'rb'), strict=False)  # 读入水印pdf文件
            last_width = width
            last_height = height
        page.merge_page(pdf_watermark.pages[0])
        page.compress_content_streams()  # 压缩内容
        pdf_output.add_page(page)
    pdf_output.write(open(pdf_file_out, 'wb'))


if __name__ == '__main__':
    # 定义命令行解析器对象
    parser = argparse.ArgumentParser(description='WaterMarker of argparse')

    # 添加命令行参数
    parser.add_argument('--text', default='watermark', help="Text to add watermark")
    parser.add_argument('-F', '--file', default='', help="The path to the file to add the watermark to")
    parser.add_argument('--font', default='SimSun', help="Font used for watermark text")
    parser.add_argument('--size', type=int, default=30, help="Font size used for watermark text, defaults to 30, "
                                                             "the size will adjust itself as the page changes")
    parser.add_argument('--alpha', type=float, default=0.1, help="Transparency of watermark text, between 0.0 and 1.0")
    parser.add_argument('--angle', type=int, default=30, help="Rotate the canvas by the angle theta (in degrees)")
    parser.add_argument('-O', '--output', default='', help="File output path after adding watermark (including the "
                                                           "file name), the default is the original file directory")

    # 从命令行中结构化解析参数
    args = parser.parse_args()

    print("WaterMarker, Copyright (C) 2023 Huang Wenhuan")
    text = ''
    if args.text == 'watermark':
        text = input("请输入水印文字：")
    watermark_text = args.text if text == '' else text

    pdf_file_in = ''
    pdf_file_out = ''
    if args.file == '':
        pdf_file_in = input("请输入文件路径：").strip('"').strip(' ')
    else:
        pdf_file_in = args.file

    if os.path.splitext(pdf_file_in)[-1] == ".pdf":
        pdf_file_in = pdf_file_in.replace('\\', '/')
        # 文件输出路径
        if args.output == '':
            pdf_file_out = pdf_file_in.replace('.pdf', '') + '（添加水印）.pdf'
        else:
            pdf_file_out = args.output.replace('\\', '/')
        add_watermark(pdf_file_in, pdf_file_out, args)
        print("添加水印成功")
        print("文件路径为: {}".format(pdf_file_out.replace('/', '\\')))
    else:
        print("输入文件不为pdf格式!!!")
