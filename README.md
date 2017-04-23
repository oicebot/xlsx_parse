xlsx 影像诊断结果分析脚本
===================

此脚本尝试提取xlsx电子表格中固定位置的内容，并加以处理，以提取具体肿块位置及相关描述等信息。

#### :information_source: **依赖**：

目前版本使用 Python 3.5.2 编写，依赖 `openpyxl` 库进行读写操作。

* py文件运行测试方法：右键，用 Python IDLE 打开，按 `F5` 运行
* 依赖安装说明：用管理员权限打开命令提示符，然后 cd 进入 Python 安装目录下，依次运行：
```bash
cd Scripts
pip install openpyxl
```
 等待自动安装完毕即可（不知需不需要科学上网）


####Table of Contents

   * [xlsx 影像诊断结果分析脚本](#xlsx-影像诊断结果分析脚本)
            * [<g-emoji alias="information_source" fallback-src="https://assets-cdn.github.com/images/icons/emoji/unicode/2139.png" ios-version="6.0">ℹ️</g-emoji> <strong>依赖</strong>：](#information_source-依赖)
      * [想法1：字符串分割及分析](#想法1字符串分割及分析)
            * parse_functions.py
            * xlsx_parse.py
      * [想法2：利用语义识别](#想法2利用语义识别)

Created by [gh-md-toc](https://github.com/ekalinin/github-markdown-toc)

-----

想法1：字符串分割及分析
-------------

目前从给的字符串的结构来看，暂时采用的是用句号和逗号分隔描述单元并判断类型予以归类的办法。将字符串分开后，用正则或者if语句来判断归类，用几个变量追踪当前的描述是描述哪个或哪几个对象的。

#### :page_facing_up: parse_functions.py

文件中包含4个处理函数：

* :hash: **parse_sonography()** ： 处理超声描述
 * 提取具体超声下的各类描述，并分类。
 * 输入字符串，输出一个 `list` ，元素数量为发现的病灶个数，每个元素是一个 `dict` 
* :hash: **parse_sonography_result()** ：处理超声诊断结果
 * //TODO: 提取诊断结果 `US-Birads` 等级
* :hash: **parse_operation()** ：处理手术过程
 * //TODO: 提取手术过程切了些什么
* :hash: **parse_pathology()** ：处理病理分析
 * 提取分析结果是什么细胞，并将结果分类输出
 * 由大锤充当NLP核心，人工标记后由软件自动输出。
 * 简写：{ 'wz':'位置','dx':'定性','fj':'分级','dz':'单发/多灶','bs':'伴随病变的情况','lj':'累及周围组织情况','ln':'淋巴结转移情况' }

#### :page_facing_up: xlsx_parse.py

* 读取 `testdata.xlsx` ，A、C、D单元格直接存入，F单元格内容使用 `parse_sonography()`  进行处理，并按病灶数量每个单独新起一行。
* 生成的每一行都使用一个 `dict`对象保存其数据，整个表为一个存了许多 `dict` 对象的 `list`
 * 详见代码……？

想法2：利用语义识别
-------------------

//TODO




