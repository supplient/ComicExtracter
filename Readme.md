# ComicExtracter
这是我自用的一个漫画解压用工具。功能有：
1. 将压缩包自动解压到指定目录
    * 支持zip, rar, 7z
    * 支持密码，需要指定一个密码集
2. 将只包含一个文件/一个文件夹的文件夹里的文件/文件夹取出来，然后删掉空了的文件夹

# 用法
1. 将所有压缩包都放到config.py的src_folder中，文件的后缀名无所谓，txt后缀也照样解压。
2. 填写password_filepath指定的密码集，一行一个密码，程序会逐个尝试。
2. 指定dst_folder作为解压后的目标目录。对于每个压缩包，会自动在该目录下创建一个以压缩包名为名字的目录，然后解压到该目录下。
3. 指定failed_folder作为解压失败的目录。解压的时候如果密码不对，或者格式不支持，或者各种奇怪的情况导致解压失败时，就会把压缩包给移到这个目录下方便后续手动处理。
4. 执行```python extract.py```。此时就会开始根据password_filepath解压src_folder目录下的压缩包到dst_folder目录下，失败的会直接移到failed_folder中。
5. 执行```python move.py```。此时会把dst_folder目录中，仅包含一个文件或一个文件夹的目录里的东西给拿出来，直接放到dst_folder下，然后把空了的目录给删掉。这个过程会反复迭代，直到没有空目录了。
6. 自行删掉src_folder里的解压成功压缩包。自行移走dst_folder中解压后的内容。自行处理failed_folder中解压失败的压缩包。
    * 不建议直接解压到想解压过去的地方，毕竟是程序执行，只能保证src_folder和failed_folder里的东西不会出问题，不能保证dst_folder会不会变奇怪。

# 依赖
* python包
    * zipfile
    * rarfile
    * tqdm
* 7z.exe
* UnRAR.exe
    * 这俩直接扔这个目录下就行了
    * 我也不清楚用这俩要不要啥license……不过没用源码，只用了二进制文件应该没事吧？