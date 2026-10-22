"""以 Study Image 母版和示意图生成精确排字的科研图表；仅写本目录派生产物。"""
from __future__ import annotations

import json
import re
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, PngImagePlugin

BASE = Path(__file__).resolve().parent
NAVY, TEAL, GRAY = "#143653", "#168A8A", "#526779"
FONT = "C:/Windows/Fonts/msyh.ttc"
BOLD = "C:/Windows/Fonts/msyhbd.ttc"
W, M = 2600, 96


def font(size, bold=False):
    return ImageFont.truetype(BOLD if bold else FONT, size)


def wrap(text, f, width):
    out = []
    for paragraph in str(text).split("\n"):
        line = ""
        for token in re.findall(r"[A-Za-z0-9_]+(?:[-./][A-Za-z0-9_]+)*|\s+|.", paragraph):
            if line and f.getlength(line + token) > width:
                out.append(line.rstrip())
                line = token.lstrip()
            else:
                line += token
        out.append(line.rstrip())
    return out


tables = [
    dict(
        id="表1-固定监控场景", title="表 1　固定监控与户外牧场：拍摄环境对照",
        subtitle="原论文 / 官方资源与 CowCV 子集分别记录｜采集参数未知处不补猜",
        headers=["数据集 / 来源", "场地与相机视角", "光照 / 场景难点", "CowCV 使用边界"],
        widths=[430, 660, 660, 658],
        rows=[
            ["Cows2021\nW1；L1 §4.1", "英国挤奶走道；D435\n约 4 m 垂直俯视\n1280×720 RGB", "固定背景；拥挤、边界裁切\n运动模糊；无公开昼夜分层", "来源资源 10,402 图\n原标为躯干旋转框\n派生 HBB 语义仍需核对"],
            ["8-Calves\nW2；L1 §4.2", "室内犊牛饲喂区；固定顶视\n9 段 × 1 h；600×800\n20 fps；型号 / 高度未公开", "快速运动与牛间严重遮挡\n不能推定为鱼眼或夜间域", "900 张静态检测帧\n不等于 67,760 帧完整\n跟踪序列"],
            ["COLO\nW3；L1 §4.3", "美国 free-stall barn\nTop / Side 均高 3.25 m\n侧机位与水平约 40°", "日光、人工光、NIR\n栏杆 / 卧栏 / 牛间遮挡\n不能由亮度单独判定模态", "Top 504 + Side 500\n合计 1,004 图\n排除 External 250 图"],
            ["MooTrack360\nW4；L1 §4.4", "丹麦两座商业奶牛场\n16 台顶装 180° 鱼眼\n安装高度 4.0–5.6 m", "RGB / 夜间 IR 辅助\n强畸变、密集牛群及遮挡\n成像差异需按相机 / 时段核实", "1,500 张检测图\n站 / 卧类合并 cow\n不并入完整 MOT 序列"],
            ["XGain\nW5；L1 §4.5", "比利时 ILVO 户外牧场\n高位相机：6 m / 型号\n沿用 L1，未独立确认", "自然光；大背景 / 小目标\n原视频有天气变化\n当前子集天气比例未知", "项目视图 1,657 图\n原资源 12,578 图\nUUID / _1 变体应同组"],
        ],
        note="图像数为对应资源 / 项目视图数量，不等于 2026-10 test 图数；XGain 相机细节保留证据限制。",
    ),
    dict(
        id="表2-侧视与异质来源", title="表 2　受控侧视、半开放与网络来源场景",
        subtitle="场景外观沿用 L1 已有观察｜本次未对原始图像包重新抽样",
        headers=["数据集 / 来源", "拍摄环境与视角", "主要变化 / 不确定性", "CowCV 使用边界"],
        widths=[430, 660, 660, 658],
        rows=[
            ["HCRD\nW6；L1 §4.6", "荷兰挤奶站出口\n单牛侧视；FLIR E6\n原资源成对 RGB + 热图", "金属管杆遮挡\n高度 / 距离 / 照明未知\n受控侧视不等于固定监控", "1,063 张配框 RGB\n只用 full photo\n不把它写成热红外检测域"],
            ["CID\nW7；L1 §4.7", "受控测量栏 / 半开放\n地面侧视，带高度标尺\n场地和机型未公开", "每牛 4 个规范视图\n单牛、背景相对统一\n划分需按牛 ID 关联", "images 共 2,056 图\n514 牛 × 4 视图\n排除 yt_images"],
            ["Dairy Cow\nL1 §4.8；L3 §7", "半开放院落 / 牛场\n高位斜俯视（既有观察）\n相机参数未核实", "白天 / 夜间或低照度\n多牛、栏杆、柱子干扰\n子集模态不能一概而论", "2,320 检测图 + 1,800\n姿态 / 行为图 = 4,120\n只保留 rectangle"],
            ["NWAFU_CD\nW8；L1 §4.9", "室内 / 半开放牛舍与院落\n地面侧视 / 斜侧视\n以上为既有观察", "多品种、多毛色与群体\n栏杆、人员、牛间遮挡\n是否视频抽帧待核实", "正式配框视图 1,878 图\n原任务是姿态估计\nHBB 为后续标注"],
            ["CBPD_ODD\nL1 §4.10；L3 §3", "室内帧 / 户外 / 网络混合\n没有统一农场或机位", "来源、尺度和遮挡异质\n不能解释为纯室内域", "365 张整牛重标图\n原任务检测 Back/Head/Leg\n原部位框不直接作整牛 GT"],
            ["CImage\nL1 §4.11；L3 §3", "开放网络独立图像为主\n无统一机位或拍摄参数", "构图 / 尺度 / 真实性混杂\n原包噪声不代表最终子集\n需要按图像核对", "正式检测视图 176 图\n原为方向分类\n后加整牛 HBB"],
            ["animals_10\nL1 §4.12；L3 §3", "Google Images 分类图像\nCowCV 只取牛类", "品种、背景与图像质量异质\n不能按名称分成单一户外域", "正式配框视图 1,616 图\n原生无牛只检测框"],
            ["COCO cow subset\nW9；L1 §4.13", "Flickr 等复杂日常图像\n无统一相机 / 机位", "多尺度、多物体、复杂遮挡\n数据集名不等于场景标签", "COCO 2017 牛类 1,720 图\n原生 HBB / 实例 mask\n项目保留单类别检测"],
            ["Google Open Images\nW10；L1 §4.14", "开放网络来源\n当前项目记录为 V6 子集", "场地、视角、构图异质\nV6 项目子集不等于整个 V7", "原类 Cattle → cow\n项目历史视图 2,916 图\n评测视图另按版本冻结"],
        ],
        note="侧视与光照特征只说明对应来源 / 子集；本表不提供图像级频率，也不提供因果归因。",
    ),
    dict(
        id="表3-十月测试视图", title="表 3　2026-10 本地记录中的 test 冻结视图",
        subtitle="依据 L4 §4.2 抄录测试数量｜本次未连接服务器重新计数",
        headers=["项目名称", "test 图数", "拍摄环境检索标签", "数量所代表的范围"],
        widths=[570, 260, 940, 638],
        rows=[
            ["Cows2021", "1,040", "室内 / 俯视 / 固定走道", "10 月权威 data/ 视图"],
            ["8-calves", "90", "室内 / 犊牛 / 顶视 / 严重遮挡", "同版 test；群组隔离需成员证据"],
            ["COLO", "100", "Top+Side / 混合光照", "排除 External；各子域比例未知"],
            ["MooTrack360", "150", "鱼眼 / 密集 / 多相机 / 日夜", "各相机与时段比例未知"],
            ["XGain", "163", "户外牧场 / 高位 / 小目标", "天气与距离标签尚未统计"],
            ["HCRD", "106", "受控单牛 / 侧视 RGB / 管杆遮挡", "不含 thermal 检测视图"],
            ["CID", "205", "受控测量 / 多视图 / 牛级关联", "不含 yt_images"],
            ["Dairy Cow（diarycow）", "408", "半开放 / 高位斜俯 / 日夜候选", "与 7 月 420 图 test 不同"],
            ["NWAFU_CD", "185", "牛舍 / 院落 / 地面侧视候选", "机位来源与子域比例待核实"],
            ["CBPD_ODD", "36", "混合来源 / 整牛重标", "原部位检测资源的派生视图"],
            ["CImage", "17", "开放网络 / 小样本", "17 图不宜再拆细作强结论"],
            ["animals_10", "161", "开放网络 / 牛类子集", "派生检测 test"],
            ["COCO", "172", "复杂日常场景 / cow", "10 月 test；不是旧 val=342"],
            ["Google_Open_Images", "291", "开放网络 / Cattle", "10 月 test；不是旧 val=576"],
            ["合计（14 数据集）", "3,124", "样本量合计，不是 14 个等价环境", "31,373 是 7 月全视图逻辑条目"],
        ],
        note="仅引用已有本地实验记录；未逐图读取 test、未复核远程 split/hash，不能据此声称场景覆盖率已验证。",
    ),
    dict(
        id="表4-场景登记字段", title="表 4　图像级场景与来源登记字段",
        subtitle="建议 SOP｜unknown 显式保留；来源陈述、视觉观察与推断分开",
        headers=["字段组", "建议字段 / 值", "登记规则", "验收要求"],
        widths=[370, 770, 740, 528],
        rows=[
            ["来源和版本", "dataset、image_relpath、sha256\nsource_url、annotation_version", "路径 + 内容 hash 绑定图像\n记录原始名称与项目别名", "任一图可追溯到\n批准的标签版本"],
            ["拍摄环境", "site_id；indoor / semi_open /\noutdoor / web / mixed / unknown", "web 是来源类别，不是场地\n网页图像仍可有 indoor 标签", "环境与来源分字段\n证据定位可打开"],
            ["机位和镜头", "camera_id；top / oblique / side\nheight_m；fisheye / unknown", "型号 / 高度取一手元数据\n无畸变外观不等于证实透视", "未知项保留 unknown\n不反推相机型号"],
            ["光照与模态", "daylight / artificial / low_light\nRGB / NIR / thermal / unknown", "低照度是现象，不等于 NIR\nNIR 辅助与热成像分别记录", "每个模态标签有\n论文或设备依据"],
            ["时序与关联组", "video_id、time_block、cow_id\nderivative_group、source_group", "按评估目标定义关联约束\n原图 / 变体 / 近重复同组", "组交集与泄漏审计\n报告为可检查清单"],
            ["尺度与拥挤", "image_W/H；box_w/h；cow_count\narea_ratio；occlusion；truncation", "尺度由当前批准框计算\n遮挡给可见证据或 unknown", "统一口径；原图与\n640 输入尺度分记"],
            ["标注与证据", "HBB / OBB；torso / whole\nvisible / inferred；evidence_ref", "格式、目标范围、遮挡规则\n拆开记录；不把转换等同重标", "多复核员冲突保留\n批准后再进入评估"],
        ],
        note="上述字段为本次设计建议，尚未对原始图像包批量填充；核查方法参考 W11–W15。",
    ),
    dict(
        id="表5-测试设计与限制", title="表 5　场景差异对应的测试设计与解释限制",
        subtitle="方案与待检验假设｜跨数据集结果同时包含外观、来源、标注和训练差异",
        headers=["比较因素", "建议对象 / 测试单元", "要回答的问题", "必须记录的限制"],
        widths=[390, 800, 665, 553],
        rows=[
            ["视角变化", "COLO Top→Side / Side→Top\n先验证 camera / time / cow 分组", "同场地视角改变后\n漏检和定位是否变化？", "侧视伴随遮挡差异\n不自动等于视角因果效应"],
            ["日夜 / 模态", "COLO；MooTrack360；Dairy Cow\n仅对已确认图像级模态分层", "暗光、辅助 NIR 下\n召回 / 定位有何差异？", "亮度不能代替模态标签\nHCRD 不作热图测试域"],
            ["鱼眼几何", "MooTrack360；补中心 / 边缘分层\n匹配目标尺度与密度后比较", "畸变与位置关联的\n失败模式是否集中？", "跨集还变了密度 / 标注\n不能称纯镜头控制实验"],
            ["小目标 / 遮挡", "XGain、8-calves、HCRD 等\n按相同尺度与遮挡规则分层", "远距离 / 牛间 / 栏杆\n分别影响哪些误差？", "图像数、实例数同时报告\n遮挡等级先定义再复核"],
            ["网络与农场", "4 个网络来源集与已确认农场集\nCBPD_ODD 单独标为混合", "来源 / 构图迁移后的\n平均与最差域表现如何？", "预训练重合与近重复需审计\n网络集无单一相机"],
            ["标注语义", "Cows2021 躯干框；COLO 遮挡框\n对批准版本核查边界规则", "误差是否有部分来自\nGT 目标范围差异？", "同为 cow + HBB\n仍未证明目标边界等价"],
        ],
        note="本表没有新增模型测试结果；跨域主表先用同一目标 test，分层分析另报子集数量与证据。",
    ),
    dict(
        id="表6-后续核查与验收", title="表 6　后续核查、补充采集与验收清单",
        subtitle="优先级是本次工作安排建议｜不把未执行事项写成已完成",
        headers=["优先级 / 对象", "待补信息与操作", "预期产物", "完成判据"],
        widths=[540, 855, 600, 413],
        rows=[
            ["P0：全部 test", "读取冻结 split；对齐标签版本\n统计场景 / 实例；保存内容 hash", "scene_manifest.csv\nsplit_audit.json", "成员级对应\n图像包可复查"],
            ["P0：语义和来源", "Cows2021 核对转换 / 重标链\nDairy Cow 核对论文与子集映射", "label_provenance.md\nconflict_notes.md", "冲突有证据\n不静默消除"],
            ["P0：关联泄漏", "视频 / 近重复 / 牛级关联\n按评估问题设置分组并审计", "group_manifest.csv\ncross_split_audit.json", "禁止边跨集=0\n或明确例外"],
            ["P1：设备缺项", "8-Calves、CID、NWAFU 等\n查元数据 / 论文补充；必要时问作者", "来源定位或 unknown\n原始回应归档", "不能用猜测\n填完设备字段"],
            ["P1：光照与天气", "确认子集包含哪些时段 / 模态\n记录 XGain 天气来源证据", "子域数量、unknown 比例\n分层协议", "依据可定位\n不伪造覆盖率"],
            ["P2：补充拍摄", "经授权后制定视角 / 时段配额\n保留原视频、标定与动物福利约束", "采集计划、设备日志\n独立预留测试批次", "拍摄完成后\n再填结果记录"],
            ["P2：分层评估", "冻结主表与分层口径\n按来源组估计不确定性", "每域 / 每层指标\n漏检与定位错例", "小样本限制\n与指标一起报"],
        ],
        note="P0 为进入正式场景解释前的必要核查；本次已完成资料整理和图表制作，未执行以上数据包操作。",
    ),
]


def table_image(t):
    assert sum(t["widths"]) == W - 2 * M
    assert all(len(row) == len(t["headers"]) for row in t["rows"])
    hf, bf = font(40, True), font(39)
    data = [t["headers"], *t["rows"]]
    lines, heights = [], []
    for i, row in enumerate(data):
        f = hf if i == 0 else bf
        line = [wrap(cell, f, width - 46) for cell, width in zip(row, t["widths"])]
        lines.append(line)
        heights.append(max(92, max(len(x) for x in line) * 57 + 38))
    y0 = 237
    foot_y = y0 + sum(heights) + 45
    footer = wrap(t["note"], font(31), W - 2 * M)
    height = foot_y + len(footer) * 46 + 110
    im = Image.open(BASE / "科研表格版式母图.png").convert("RGB").resize((W, height))
    d = ImageDraw.Draw(im)
    # 母版边缘装饰保留，正文表格按可审计的确定性规则重新布局。
    d.rectangle((40, 88, W - 40, height - 145), fill="white")
    d.rectangle((M, 104, M + 9, 167), fill=TEAL)
    d.text((M + 32, 97), t["title"], font=font(57, True), fill=NAVY)
    d.text((M, 177), t["subtitle"], font=font(31), fill=GRAY)
    y = y0
    for i, (row, cell_lines, rh) in enumerate(zip(data, lines, heights)):
        d.rectangle((M, y, W - M, y + rh), fill=NAVY if i == 0 else ("#F0F6F8" if i % 2 == 0 else "white"))
        x = M
        for cell, ll, width in zip(row, cell_lines, t["widths"]):
            f = hf if i == 0 else bf
            color = "white" if i == 0 else NAVY
            ty = y + (rh - len(ll) * 57) / 2 + 3
            for text in ll:
                assert f.getlength(text) <= width - 40, (t["id"], text)
                tx = x + 23
                if re.fullmatch(r"[\d,]+", str(cell)):
                    tx = x + (width - f.getlength(text)) / 2
                d.text((tx, ty), text, font=f, fill=color)
                ty += 57
            x += width
        y += rh
        d.line((M, y, W - M, y), fill=TEAL if i == 0 else "#CAD9E1", width=4 if i == 0 else 1)
    d.line((M, y, W - M, y), fill=NAVY, width=4)
    d.rectangle((40, foot_y - 15, W - 40, height - 60), fill="white")
    for i, text in enumerate(footer):
        d.text((M, foot_y + 46 * i), text, font=font(31), fill=GRAY)
    metadata = PngImagePlugin.PngInfo()
    metadata.add_text("table_data", json.dumps(t, ensure_ascii=False))
    im.save(BASE / (t["id"] + ".png"), pnginfo=metadata, dpi=(300, 300))


def title(d, text, sub, w):
    d.rectangle((0, 0, w, 92), fill="white")
    d.text((40, 15), text, font=font(37, True), fill=NAVY)
    d.text((42, 62), sub, font=font(20), fill=GRAY)


def labelled_scene():
    im = Image.open(BASE / "图1-六类拍摄场景-原图.png").convert("RGB")
    s = im.width / 1254
    d = ImageDraw.Draw(im)
    title(d, "用于测试的数据集：六类代表性拍摄场景", "依据资料绘制的场景示意 · 不代表真实采集照片或场景占比", im.width)
    panels = [
        (70, 103, 591, 409, "A  室内挤奶走道 · 顶视", "Cows2021｜方向、裁切与时序关联"),
        (669, 103, 1185, 409, "B  犊牛饲喂区 · 顶视", "8-Calves｜拥挤、运动与牛间遮挡"),
        (70, 477, 591, 781, "C  牛舍 · 顶视与斜侧视", "COLO｜Top+Side；光照与栏杆遮挡"),
        (669, 477, 1185, 781, "D  密集牛群 · 顶装鱼眼", "MooTrack360｜几何畸变与密集目标"),
        (70, 848, 591, 1150, "E  户外牧场 · 高位广角", "XGain｜大背景、远距离目标"),
        (669, 848, 1185, 1150, "F  受控侧视 · 单牛采集", "HCRD / CID｜侧视采集概念示意"),
    ]
    for x0, yt, x1, yb, h, caption in panels:
        x0, yt, x1, yb = [int(v * s) for v in (x0, yt, x1, yb)]
        d.rectangle((x0, yt, x1, yt + 28), fill="white")
        d.text((x0 + 4, yt + 1), h, font=font(23, True), fill=NAVY)
        d.rectangle((x0, yb, x1, yb + 29), fill="white")
        d.text((x0 + 4, yb + 3), caption, font=font(19), fill=GRAY)
    d.rectangle((0, im.height - 45, im.width, im.height), fill="white")
    d.text((42, im.height - 32), "Study Image 示意绘图；设备外形与动物布局不作事实证据。开放网络来源另见表 2。", font=font(19), fill=GRAY)
    im.save(BASE / "图1-六类拍摄场景.png", dpi=(300, 300))


def labelled_workflow():
    im = Image.open(BASE / "图2-场景核查与测试隔离-原图.png").convert("RGB")
    d = ImageDraw.Draw(im)
    title(d, "从拍摄场景档案到可信测试：工作流程", "本次完成资料核查；图像级登记、来源隔离和分层测试为后续 SOP", im.width)
    for x, y, h in [
        (60, 117, "01  来源登记与一手材料核查"),
        (694, 117, "02  视角、光照、标注语义登记"),
        (60, 679, "03  定义来源组与划分独立性"),
        (694, 679, "04  冻结 test 与分层报告"),
    ]:
        d.text((x, y), h, font=font(24, True), fill=NAVY)
    for x, y, text in [
        (62, 557, "论文 / 官方页 / 本地版本分别定位"),
        (694, 557, "事实、观察、推断、unknown 分开"),
        (62, 1107, "原图变体同组；独立性随测试目标定义"),
        (694, 1107, "统计每域 / 每层样本与失败类型"),
    ]:
        d.text((x, y), text, font=font(20), fill=GRAY)
    d.text((100, 1031), "train", font=font(24, True), fill=NAVY)
    d.text((295, 1031), "val", font=font(24, True), fill=TEAL)
    d.text((460, 1031), "test", font=font(24, True), fill="#B87523")
    d.text((42, im.height - 41), "流程示意中的曲线没有数值含义，不是本次模型实验结果。", font=font(20), fill=GRAY)
    im.save(BASE / "图2-场景核查与测试隔离.png", dpi=(300, 300))


def editable_tables():
    lines = ["# 可编辑科研表格", "", "> 与正文 PNG 对应；文字与数值按本文件 / 图表数据.json 维护。", ""]
    for t in tables:
        lines += [f"## {t['id']}", "", t["title"], "", t["subtitle"], ""]
        rows = [t["headers"], *t["rows"]]
        for i, row in enumerate(rows):
            lines.append("| " + " | ".join(x.replace("\n", "<br>") for x in row) + " |")
            if i == 0:
                lines.append("|" + "|".join("---" for _ in row) + "|")
        lines += ["", t["note"], ""]
    (BASE / "表格数据.md").write_text("\n".join(lines), encoding="utf-8")
    (BASE / "图表数据.json").write_text(json.dumps(tables, ensure_ascii=False, indent=2), encoding="utf-8")


def contact_sheet():
    paths = [BASE / "图1-六类拍摄场景.png", BASE / "图2-场景核查与测试隔离.png"] + [BASE / f"{t['id']}.png" for t in tables]
    result = Image.new("RGB", (1500, 4 * 780), "#E5EDF2")
    d = ImageDraw.Draw(result)
    for i, p in enumerate(paths):
        im = Image.open(p).convert("RGB")
        im.thumbnail((710, 710))
        x, y = (i % 2) * 750 + 20, (i // 2) * 780 + 50
        result.paste(im, (x + (710 - im.width) // 2, y))
        d.text((x, y - 35), p.stem, font=font(25), fill=NAVY)
    result.save(BASE / "图表总览.png")


if __name__ == "__main__":
    labelled_scene()
    labelled_workflow()
    for table in tables:
        table_image(table)
    editable_tables()
    contact_sheet()
    print(json.dumps({"tables": len(tables), "data_rows": sum(len(t["rows"]) for t in tables), "test_images": 3124}, ensure_ascii=True))
