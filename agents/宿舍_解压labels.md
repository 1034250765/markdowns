服务器主要工作总结

一、CMBN 数据集(本次会话核心)

1. 上传
- 本地 F:\ZCOW\pig-cow-sheep_dataset\CMBN(1.9G,3540 train + 394 val + 2 COCO JSON)打包成 tar
- 发现 sshpass+scp/rsync 走新连接会卡死(传到 ~393M 挂起),改用 MCP ssh_sync(走常驻池化连接,稳定 9-13 MB/s)
- 本地 split -b 200M 分 10 块逐块上传,服务器 cat 拼接,校验 1.9G 完整
- 解压到 /data1/yxli/CowsDatabases/CMBN/

2. 预处理(写 self_mAP/CMBN/prepare_cmbn.py)
- CMBN 是 COCO 格式牛关键点数据集(17 关键点 + bbox,单类 cow),与其它数据集 image+txt 结构不同,故独立脚本
- bbox 容错:真实 bbox 轻微越界直接 clamp;占位符/整图 bbox(area≥90% 图像,1940 张)从可见关键点 min/max 派生
- 保留数据集自带 3540/394 划分,转 YOLO 0 cx cy w h 归一化格式
- 结果:3934 图全部有标注,真实 bbox 1777 个 + 关键点回退 2157 个

3. 配置训练文件
- common.py 的 DATASETS 加入 CMBN(nc=1, cow)
- 生成 CMBN.yaml + train.py(复用 common.train())
- 目录:self_mAP/CMBN/{CMBN.yaml, prepare_cmbn.py, train.py, yolo_data/}

4. 标签回传本地
- 打包 /tmp/CMBN_labels.tar(3.9M)→ 你手动下载到 F:\ZCOW\labels\CMBN_labels.tar
- 解压成 CMBN/labels/{train,val}/,校验 3540+394 一致

二、数据集本地化(全部 7 个变实体)

把 /data1/yxli/CowsDatabases 从顶层软链(指向 NAS /data2/youw/...)改为实体目录:
- 7 个数据集(CMBN + animals_10/CBPD_ODD/CImage/COCO/HCRD/NWAFU_CD)全部从 NAS 复制成 /data1 本地实体副本(共 ~4.2G)
- 重跑 prepare(force=True) 重建全部 yolo_data 软链,使训练图片指向本地实体
- 校验:7 个数据集 on_data1=True、PIL 可打开、0 个残留指向 /data2;NAS 原数据保留作备份
- 现在训练全读本地盘,不依赖 NAS,更快更稳

三、CID 预标注(之前会话延续,本次补充说明)

- D:\CODEX\imageLabels.tar.gz(17899 txt)是 merged_cow 模型对 CID 数据集推理生成的检测预标注框,已写 README 说明



我完成的训练(之前会话)

这 3 批是我在服务器上启动并监控完成的(写脚本、发训练命令、查结果):
- 6 个数据集 YOLO11m 基线:CImage / COCO / animals_10 / CBPD_ODD / HCRD / NWAFU_CD
- RT-DETR-L(FP32):NWAFU_CD(0.363)、COCO(0.280)
- merged_cow 模型:CBPD_ODD+HCRD+animals_10 合并训练(mAP50-95=0.789,用于 CID 预标注)

训练计算本身在服务器 A100 GPU 上跑,我负责启动+监控+读结果,结果都记到了 7月工作.md。

我没做的

- CMBN 训练:这次会话我只做了上传 + 预处理(转 YOLO 格式、建 yolo_data、写 yaml/train.py),没有启动训练。你当时只要求"上传,然后做预处理"。CMBN 现在处于"数据就绪、随时可训"状态。
- 模型权重文件、原始数据集本身不是我创建的(是数据集原有的/我下载的预训练权重)。

这次会话做的(都不涉及训练)

CMBN 上传+预处理、标签回传、7 个数据集本地化(软链换实体)、写 README/memory。全程没跑任何训练。

完成CMBN预训练