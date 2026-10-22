# RT-DETR-L 域内检测重测：过程与结果

> 执行时间：2026-10-14 19:39 起（主实验进行中，预计 ~26 h 训练 + ~1 h 评测）
> 实验定位：《10月域内重测计划.md》第 1 节"四架构（RT-DETR-L / Faster R-CNN / RetinaNet）与 YOLO11s/l 复核另行排期"中的 **RT-DETR-L 部分**，随 YOLO11m 主实验完成后的排期启动（2026-10-14 用户确认）
> 训练与推理服务器：实验室服务器 `yxli@211.69.141.71`，项目根 `/data1/yxli/LODOANDClassbyDomain`
> 硬件：NVIDIA A100-PCIE-40GB（单卡），Ultralytics 8.4.92 + PyTorch 2.5.1+cu124（与 YOLO 10 月域内重测同一环境）
> 机器可读协议：服务器 `indomain/protocol_rtdetr.yaml`（2026-10-14 冻结）

---

## 一、背景与范围

YOLO11m 域内重测（`域内重测-10月.md`）解决的三个旧问题，RT-DETR-L 的 7 月旧结果同样存在：参数不统一、无独立测试集（val 口径）、数据版本旧（self_mAP 时代划分）。本轮核实还发现**第四个问题**：

- **7 月 RT-DETR 的 `optimizer=auto` 实际按数据集摇摆**。8.4.92 `build_optimizer` 的 auto 规则为 `iterations>10000 → MuSGD(0.01) else AdamW(0.002)`。经逐 run 训练日志核验（`self_mAP/logs/rtdetr_14/*.log`）：**仅 Cows2021（train 7248、batch=12，约 6 万迭代）实际为 MuSGD(lr=0.01)，其余 13 个 run 全部是 AdamW(lr=0.002)**。
- 《域内模型与架构比较.md》1.6 节原记录"RT-DETR-L 实际 MuSGD(0.01)"把 Cows2021 的日志当成了全部口径，**已于 2026-10-14 更正**（经用户确认）。

本轮范围：**RT-DETR-L × 14 个数据集、单轮 seed=42**。LODO 9 月实验仅含 YOLO11m，无 RT-DETR-L 分子侧，因此本结果的"对齐"对象是 **YOLO11m 域内协议本身**（优化器/预算/数据/视图），`R^{LODO}_{target}` 配对比较不适用于本轮结果。产出服务文章 4.3 节 RT-DETR-L 列的 test 口径正式结果。

优化器决策（2026-10-14 用户确认）：**显式统一为 AdamW lr=0.002**——与 YOLO11m 10 月协议一致（跨架构优化器口径相同），且与 7 月 14 个 RT-DETR run 中 13 个的实际选择一致；备选 MuSGD(0.01)（8.4.92 auto 对长调度 transformer 的原生选择，但只匹配 1/14 旧 run 且与 YOLO 协议分叉）未采用。

## 二、训练与评测协议（2026-10-14 冻结，14 个数据集一致，不得按数据集调整）

| 项目 | 值 | 与 YOLO11m 域内协议（indomain/protocol.yaml）对照 |
| --- | --- | --- |
| 检测器 | RT-DETR-L，nc=1 `cow` | 同规则（YOLO11m → RT-DETR-L） |
| 初始化 | `pretrained/rtdetr-l.pt`（与 2026-07 全部 14 个旧 run 同一份权重，md5 `8e6bae256b16e9623c050979bb47c224`，记录于各 run_info.json） | 同一份文件原则（YOLO 用 lodo/yolo11m.pt） |
| imgsz / epochs / patience | 640 / 100 / 100 | 同 |
| batch / nbs | 16 / 16 → **accumulate=1**（断言核验） | 同 |
| 优化器 | **AdamW、lr0=0.002**（显式固定，禁止 auto） | **逐项相同**（跨架构可比） |
| AMP | **False** | **声明性差异**（YOLO 为 True）：RT-DETR AMP 有 NaN 风险（8.4.92 官方注明，bipartite matching），7 月 14 个旧 run 同为 `--no-amp` |
| 数据增强 | Ultralytics 默认（close_mosaic=10 等） | 同 |
| 随机种子 | 42、deterministic=True | 数值相同，**语义不同**（见三、3） |
| 末 batch | 保留（drop_last=False，compile=False 下断言核验） | 同 |
| 保存 | save_period=1 每 epoch 保存后剥离（66.3MB/个，14×100≈92 GB） | 同规则 |
| 每 epoch 验证 | 本域 val（results.csv 完整记录） | 同 |
| 训练池 | `data/<t>/train` 全量 | 同 |
| checkpoint 选择 | val mAP@0.5:0.95 最高、并列取较早（同脚本 `indomain_select_checkpoint.py --run train_rtdetr`）；epoch100_final.pt 敏感性对照；stock best.pt 不作依据 | 同规则同脚本 |
| 评测 | `RTDETR(ckpt).val(split="test", imgsz=640, device=0, plots=False)`，RT-DETR 默认评估器与 RTDETRPostProcessor（无 NMS） | 规则同（split/尺寸/不调参）；评估器随架构走 stock 行为 |

- **test 隔离链不变**：test 冻结视图不参与训练、验证、早停、checkpoint 选择与阈值搜索，仅在全部 14 域完成后统一评测一次。
- **运行名与产物隔离**：run=`train_rtdetr`；脚本硬报错禁止写入 YOLO11m 冻结目录（train / train_s\<N\> / train_es\<N\> / determinism_check，冒烟验证三种拒绝路径均生效）；结果文件固定 `indomain_test_results_rtdetr.{csv,json}`，与 YOLO 主结果互不覆盖。

## 三、机制核验（实现前的源码级核验，Ultralytics 8.4.92 + PyTorch 2.5.1，服务器实测）

1. **auto 优化器不统一**（第一节）：auto 规则按迭代数分叉，是本轮显式统一优化器的直接动机。
2. **nc=1 初始化迁移 926/941**：15 个类别头键（`model.28.enc_score_head` / `dec_score_head`×6 / `denoising_class_embed`）80→1 形状不匹配，且 `_remap_cls_by_names`（cls_remap）不覆盖 RT-DETR 解码器命名 → **随机初始化**。YOLO11m 为 649/649 全确定性迁移（`Transferred 649/649`），两架构初始化通道性质不同。
3. **RT-DETR 下 seed 真实生效**（与 YOLO11m 的"seed 空操作"结论相反）：`init_seeds(seed+1)` 位于 `BaseTrainer.__init__` 第 16 行、先于模型构建，随机类别头初始化受 seed=42 控制。**已直接实证**（2026-10-14，服务器 CPU 复刻 `init_seeds(seed+1) → 构建 nc=1 模型` 路径）：同 seed=42 两次构建的类别头权重逐位相同，seed=43 则不同——类别头初值是 seed 的确定函数。注意：同 seed 不可逐位复现（第 4 条）的噪声来源在反传算子而非初始化，两者是不同环节。
4. **同 seed 不可逐位复现（结构性）**：训练中出现 `grid_sampler_2d_backward_cuda does not have a deterministic implementation` 警告——`torch.use_deterministic_algorithms(True, warn_only=True)` 放行该算子的非确定性反传。**调用链定位**（8.4.92 源码）：RT-DETR 解码器 cross-attention（`TransformerDecoderLayer.cross_attn`，transformer.py:642）→ `MSDeformAttn` 可变形注意力 → `multi_scale_deformable_attention` 的 `F.grid_sample` 双线性采样（nn/modules/utils.py:140）；其反传 kernel 以非确定顺序累加梯度且无确定性实现。**冒烟判别实验**（CImage × 2 epochs × 2 次，同为 seed=42）：两轮第 1 epoch 即分叉（train/giou_loss 1.257 vs 1.309、val mAP50 0.0418 vs 0.0028）；结合第 3 条的初始化实证（同 seed 初值逐位相同），分叉来源锁定在反传算子而非初始化。**同 seed 重跑不构成逐位复现**，仅当独立重复运行对待。这与 YOLO11m 的 HCRD 同 seed 判别（域内重测-10月.md 5.3 节）性质相同，但对 RT-DETR 是全数据集的结构性属性（YOLO 图内全部 kernel 有确定性实现，RT-DETR 恰有此一处）。
5. **AMP**：`RTDETRTrainer` 文档注明 AMP 可能 NaN；7 月 14 个旧 run 均为 amp=False；本轮冻结 amp=False。
6. **选择/评测脚本复用性**：`indomain_select_checkpoint.py` 架构无关（只读 results.csv、复制权重、核验剥离）直接复用；评测必须用 `RTDETR()` 类加载（`YOLO()` 走 NMS 后处理，语义与训练期验证不一致），故新建 `indomain_eval_test_rtdetr.py`（字段与 YOLO 版同构，test 图像数断言同表同源）。

## 四、工程实现

| 资产 | 说明 |
| --- | --- |
| `indomain_train_rtdetr.py` | 单数据集训练（第二节协议）：断言链（accumulate=1、AdamW@0.002、**amp=False**、末批保留、splits 一致、resume=False）+ run_info.json（协议快照、权重 md5、seed_note、transfer_note）+ 每 epoch 剥离；运行名保护（见第二节） |
| `run_indomain_rtdetr_all.sh` | 串行驱动器（独立 flock 锁、results.csv 满 100 行跳过、崩溃下一轮从头重跑最多 3 轮）；**全部完成后自动衔接选择 + test 评测**，一次性产出 `indomain_test_results_rtdetr.{csv,json}` |
| `indomain_eval_test_rtdetr.py` | test 冻结视图评测（RTDETR 类、默认评估器、test 图数断言、`--out-tag` 防覆盖） |
| `indomain/protocol_rtdetr.yaml` | 第二节协议的机器可读冻结版 |
| `pretrained/rtdetr-l.pt` | 初始化权重副本（md5 与 self_mAP/models/rtdetr-l.pt 逐字节一致） |
| 目录 | `indomain/<ds>/runs/train_rtdetr/`、`indomain/<ds>/logs/train_rtdetr/`、日志 `indomain/logs/driver_rtdetr.log`、`select_rtdetr.log`、`eval_rtdetr.log` |

本地镜像：`D:\牛只数据集实验\rtdetr_deploy\`（脚本 + 协议 yaml）。

## 五、冒烟测试（CImage × 2 epochs，2026-10-14，验证后产物已删除）

| 检查项 | 结果 |
| --- | --- |
| 运行名保护 | `--run-name train` / `train_s43` / 非法名 三种拒绝路径全部硬报错 ✓ |
| 断言链 | accumulate=1、AdamW@0.002、AMP=False、末批保留、train 141 张与 splits 清单一致 ✓ |
| 预训练迁移 | `Transferred 926/941 items`（与核验预测一致）✓ |
| 显存 | batch=16 fp32 → **19.7–20.0 GB / 40 GB**，余量充足，batch=16 冻结成立 ✓ |
| 保存/剥离 | 每 epoch `epoch{N}.pt` 66.3MB，均剥离优化器 ✓ |
| results.csv | 2 行完整（epoch/metrics/lr 列齐全）✓ |
| checkpoint 选择 | e*=1 → selected.pt + epoch100_final.pt，selection.json 完整 ✓ |
| test 评测 | 17 图断言通过、RT-DETR 评估器（postprocess 0.2ms，无 NMS）、CSV 字段同构 ✓ |
| 同 seed 判别 | **两轮从第 1 epoch 分叉**（见三、4），RT-DETR 不可逐位复现，记录为协议性质 |

## 六、执行记录

- 2026-10-14 19:39：串行驱动器启动（setsid 脱离会话，服务器自主推进：训练 → 选择 → test 评测），启动时 GPU 空闲（2.4GB/40GB）。
- 驱动器按 `8-calves → animals_10 → CBPD_ODD → CID → CImage → COCO → COLO → Cows2021 → diarycow → Google_Open_Images → HCRD → MooTrack360 → NWAFU_CD → XGain` 串行训练；7 月旧 run（batch=12、torch 2.6.0+cu118）总耗时 26.1 h 可作参照（Cows2021 6.9h、diarycow 3.4h、Google 2.6h 为大头），本轮 batch=16、torch 2.5.1+cu124，预计相近。
- 2026-10-14 20:37：**用户改为四轮追加设计**（推翻 20:15 的两轮方案）：主实验完成后接力执行
  1. `train_rtdetr_rep1`（stock seed=42）：数据流与类别头初值均与主实验逐位相同 → 与主实验成对，**纯隔离 grid_sampler 反传噪声**（n=2）；
  2. `train_rtdetr_es42` / `es43` / `es44`（种子重复协议 `--effective-seed`）：loader generator 按 seed 派生（洗牌+增强激活）+ 类别头初始化 + 反传噪声 → **全训练随机性**（n=3，对应 YOLO es 表口径）。
  两套口径不可混写（rep 只变反传噪声；es 变全部四通道）。es patch 自 YOLO es 协议移植（同一实现），RT-DETR 版 **CPU 机制测试全通过**（同 seed 复现/异 seed 分叉/逐 epoch 洗牌/worker RNG 分离/stock 不变）；端到冒烟设为接力器**门禁**（rep1 后、es 轮前自动执行 CImage×2 epochs×{es42,es43}，通过才启动三轮 es，任一失败跳过 es 保护 78h）。RT-DETR 因反传噪声不存在"同 seed 逐位一致"，YOLO es 验证标准中的该项检查不适用（有意省略）。
  磁盘策略（必须项）：四轮 4×92GB≈368GB > 剩余 ~350GB → 每轮评测核验（28 行）后清理该轮逐 epoch checkpoint（保留 selected/final/results/selection 等审计件），主实验产物全保留；峰值占用 ≈184GB。运行名保护：stock 禁用 es 命名、es 禁写 stock 目录（门控三路径实测通过）。
  接力器 `run_rtdetr_rounds_relay.sh` 已启动（PID 152891，独立锁，等待主实验）。
- **2026-10-14 ~20:49 执行事故与恢复**：主驱动器、animals_10 训练进程（32/100）、接力器 v2 全进程树死亡。当时已完成 8-calves（100/100，产物完整无损）。排查：服务器未重启（up 135 天）、logind KillUserProcesses 默认关闭、无 OOM 痕迹；死亡范围恰好为经 SSH 会话 + setsid 启动的全部进程（19:39 启动的主驱动器存活约 70 分钟后与 20:37 启动的接力器几乎同时死亡），用户的其他进程（10-09 启动的服务）无损——**死因未完全定位**，最大嫌疑为 SSH 会话/通道清理波及 setsid 进程。恢复（22:28）：①现场日志归档 `indomain/logs/driver_rtdetr{,_reps}_run1_20261014.log`；②animals_10 部分产物清除（防 results.csv 追加污染，全新重训）；③驱动器与接力器改由 **atd 系统服务托管启动**（`at now`，进程树父链 atd→sh→bash→脚本，完全脱离任何 SSH 会话生命周期）。8-calves 因 results.csv 满 100 行被驱动器正确跳过，animals_10 从头重训。
- 主实验训练与评测于 **10-15 21:43 全部完成**：14/14 训练退出码 0、断言链全通过、`indomain_test_results_rtdetr.csv` 28 条、selection.json 14/14。逐域耗时（22:28 恢复起，含事故前 8-calves 首次 45min）：Cows2021 7h24m、diarycow 3h、Google 2h12m、NWAFU 1h26m、MooTrack360 1h25m、CID 1h33m、COCO 1h19m、animals_10（重训）1h20m、COLO 51m、HCRD 50m、8-calves 45m（首次）、CBPD_ODD 24m、XGain 1h16m、CImage 13m；选择 21s、test 评测 2.5min。驱动器结束，接力器于 21:43:23 自动进入 rep1（8-calves 起）。
- **rep1（反传噪声对照）于 10-16 22:01 完成**（14/14、评测产出 `indomain_test_results_train_rtdetr_rep1.{csv,json}`）；结果见 7.5。**es 门禁 22:02:54 通过**（es42 vs es43 首轮分叉，patch 训练级生效），冒烟产物已清理，es42 于 22:02 自动启动。
- **es42/43/44 三种子轮全部完成**：es42 训练/评测 10-17 22:34 完成、es43 10-18 23:11、es44 10-20 04:58（均 14/14、退出码 0）。三轮评测都被接力器 `eval_csv_ok` 竞态误报为"异常"并保留 checkpoint，但三个 CSV 逐一手工核验均为 29 行（28 条）有效——最终汇总直接读取 CSV，不受该误报影响。接力器 10-20 04:58:13 打印"追加轮接力器 v2 结束"正常退出。**es 三种子宏平均 0.6917 ± 0.0129**（详见 7.6）。
- 2026-10-20：四轮追加（rep1 + es42/43/44）全部完成，执行记录与三项产出（主表 7.2、反传噪声 7.5、全训练随机性 7.6）齐备。

## 七、域内结果 $M_{t\to t}$（test 冻结视图，selected.pt）

### 7.1 Checkpoint 选择（依据 val mAP@0.5:0.95 最高、并列取较早）

| 数据集 | e* | val 峰值 | test $M_{t\to t}$ | | 数据集 | e* | val 峰值 | test $M_{t\to t}$ |
| --- | --: | --: | --: | --- | --- | --: | --: | --: |
| HCRD | 98 | 0.9088 | **0.9274** | | Cows2021 | 99 | 0.8676 | 0.8575 |
| CBPD_ODD | 97 | 0.9632 | 0.8860 | | diarycow | 100 | 0.8768 | 0.8768 |
| CID | 92 | 0.8782 | 0.8516 | | XGain | 100 | 0.8203 | 0.8155 |
| NWAFU_CD | 96 | 0.7063 | 0.7334 | | COLO | 99 | 0.6390 | 0.6568 |
| animals_10 | 100 | 0.6347 | 0.6389 | | MooTrack360 | 100 | 0.6286 | 0.6259 |
| COCO | 98 | 0.4774 | 0.4774 | | 8-calves | 85 | 0.5907 | 0.5767 |
| Google_Open_Images | 85 | 0.3893 | 0.3792 | | CImage | 97 | 0.5681 | 0.3973 |

全部无并列；e* 集中在 85–100。注：test mAP50-95 高于 val 峰值的域（HCRD 0.9088→0.9274、NWAFU 0.7063→0.7334、animals_10、COLO）系小样本 val/test 视图间波动，非选择泄漏（test 全程未参与选择）。

### 7.2 域内结果 $M_{t\to t}$（selected.pt，test 冻结视图）

| 数据集 | test 图 | mAP@0.5 | mAP@0.5:0.95 | P | R |
| --- | --: | --: | --: | --: | --: |
| HCRD | 106 | 0.9811 | **0.9274** | 0.9582 | 0.9848 |
| CBPD_ODD | 36 | 0.9608 | 0.8860 | 0.8674 | 0.9792 |
| diarycow | 408 | 0.9902 | 0.8768 | 0.9760 | 0.9894 |
| Cows2021 | 1040 | 0.9695 | 0.8575 | 0.8741 | 0.9939 |
| CID | 205 | 0.9614 | 0.8516 | 0.9037 | 0.9410 |
| XGain | 163 | 0.9782 | 0.8155 | 0.9339 | 0.9443 |
| NWAFU_CD | 185 | 0.8960 | 0.7334 | 0.8315 | 0.8348 |
| COLO | 100 | 0.9459 | 0.6568 | 0.9182 | 0.9153 |
| animals_10 | 161 | 0.8030 | 0.6389 | 0.8736 | 0.7567 |
| MooTrack360 | 150 | 0.9390 | 0.6259 | 0.9054 | 0.8699 |
| 8-calves | 90 | 0.9694 | 0.5767 | 0.9547 | 0.9544 |
| COCO | 172 | 0.7033 | 0.4774 | 0.7380 | 0.6612 |
| CImage | 17 | 0.5229 | 0.3973 | 0.5103 | 0.6317 |
| Google_Open_Images | 291 | 0.6205 | 0.3792 | 0.7290 | 0.5691 |
| **宏平均（14 域等权）** | — | **0.8744** | **0.6929** | **0.8553** | **0.8590** |

test 图与 `data/README.md` 构成表逐域一致（合计 3,124，评测前后断言通过）。**RT-DETR-L 域内参照宏平均 mAP@0.5:0.95 = 0.6929**。

### 7.3 敏感性对照（selected vs 第 100 epoch）

14 域 mAP@0.5:0.95 的 selected−epoch100 平均绝对差 **0.0054**；绝大多数域 ≤0.014，仅 **CImage 0.0354**（17 张 test 的小样本高方差，且 6/14 域 selected 与 epoch100 逐位相同——animals_10、diarycow、MooTrack360、XGain、COCO 选择即最后一轮）。checkpoint 选择规则对结果不敏感。

### 7.4 与 7 月旧 RT-DETR 结果（val 口径、auto 优化器、旧数据）的描述性对照

双方不可直接比较（数据版本与 8:1:1 重切、val-vs-test 视图、auto 不统一 vs 显式 AdamW、batch 12 vs 16 / 有效优化批 60 vs 16、torch 2.6.0 vs 2.5.1）。仅记录量级提示：旧 RT-DETR 宏平均（val）约 0.74、本轮 test 口径 0.69——差异主要来自视图与协议，不作可比性结论。

### 7.5 运行间噪声：反传噪声通道（主实验 vs rep1，同 seed=42，n=2）

`train_rtdetr_rep1` 与主实验数据流（常数 generator）与类别头初值（seed=42）**逐位相同**，差异纯来自 `grid_sampler_2d_backward` 反传非确定性（三、4）。

| 数据集 | 主实验 | rep1 | diff (rep1−main) |
| --- | --: | --: | --: |
| HCRD | 0.9274 | 0.9425 | +0.015 |
| CBPD_ODD | 0.8860 | 0.8980 | +0.012 |
| CImage | 0.3973 | 0.5077 | **+0.110** |
| diarycow | 0.8768 | 0.8741 | −0.003 |
| Cows2021 | 0.8575 | 0.8621 | +0.005 |
| CID | 0.8516 | 0.8536 | +0.002 |
| XGain | 0.8155 | 0.8087 | −0.007 |
| NWAFU_CD | 0.7334 | 0.7167 | −0.017 |
| animals_10 | 0.6389 | 0.6512 | +0.012 |
| COLO | 0.6568 | 0.6402 | −0.017 |
| MooTrack360 | 0.6259 | 0.5967 | **−0.029** |
| 8-calves | 0.5767 | 0.5655 | −0.011 |
| COCO | 0.4774 | 0.4798 | +0.002 |
| Google_Open_Images | 0.3792 | 0.3957 | +0.017 |
| **宏平均** | **0.6929** | **0.6995** | **+0.0066** |

**结论（描述性）：RT-DETR 的反传噪声通道使同 seed 重复轮产生不可忽视的运行间波动**——逐域绝对差均值 **0.018**、中位数 **0.012**、9/14 域 ≥0.01、宏平均级差异 **0.0066**；MooTrack360 −0.029 最大、CImage +0.110 为小样本（17 test 图）高方差离群。**该波动量级（宏平均约 ±0.007）明显大于 YOLO11m 主方案宏平均（0.7214）与 RT-DETR 主方案（0.6929）之差（0.028）的量级参考意义需谨慎**——但逐域单值在 n=2 下不可作精确排名。完整的总随机性（含初始化/洗牌/增强）由 es 三种子轮（第八节）在 n=3 下给出。**引用任一主表单个数字时应结合本表波动**；该噪声是 RT-DETR 结构性属性（架构声明性），非实验失误（详见三、4）。

### 7.6 全训练随机性：es 三种子 42/43/44（n=3 对照）

`train_rtdetr_es{42,43,44}` 为种子重复协议（`--effective-seed`）：类别头初始化、洗牌、增强、反传噪声四通道同时随 seed 变化；数据流协议与主实验 **stock（常数 generator）不同**，故 es 表以 es42/43/44 内部计算 mean/SD，主实验数字不并入，与 7.5 的 rep 口径**不可混写**。

| 数据集 | es42 | es43 | es44 | mean | 样本 SD |
| --- | --: | --: | --: | --: | --: |
| HCRD | 0.9410 | 0.9346 | 0.9340 | 0.9365 | 0.0039 |
| CBPD_ODD | 0.8758 | 0.8784 | 0.8855 | 0.8799 | 0.0050 |
| Cows2021 | 0.8785 | 0.8670 | 0.8801 | 0.8752 | 0.0072 |
| diarycow | 0.8824 | 0.8736 | 0.8872 | 0.8811 | 0.0069 |
| CID | 0.8553 | 0.8604 | 0.8687 | 0.8615 | 0.0067 |
| XGain | 0.8138 | 0.8202 | 0.8159 | 0.8166 | 0.0032 |
| NWAFU_CD | 0.7263 | 0.7304 | 0.7268 | 0.7278 | 0.0022 |
| COLO | 0.6524 | 0.6499 | 0.6509 | 0.6511 | 0.0012 |
| MooTrack360 | 0.6511 | 0.6329 | 0.6467 | 0.6436 | 0.0095 |
| animals_10 | 0.6495 | 0.6242 | **0.3199** | 0.5312 | **0.1834** |
| 8-calves | 0.5579 | 0.5633 | 0.5648 | 0.5620 | 0.0036 |
| COCO | 0.4643 | 0.4764 | 0.4886 | 0.4764 | 0.0122 |
| CImage | 0.3120 | 0.5699 | 0.4584 | 0.4468 | **0.1294** |
| Google_Open_Images | 0.3926 | 0.3959 | 0.3928 | 0.3937 | 0.0019 |
| **宏平均** | **0.6895** | **0.7055** | **0.6800** | **0.6917** | **0.0129** |

**结论（描述性）**：
1. **es 三种子宏平均 mean ± 样本 SD = 0.6917 ± 0.0129**（单种子 0.6895 / 0.7055 / 0.6800，极差 0.0255）。跨 seed 的全训练随机性在宏平均级约 **±0.013**，显著大于反传噪声通道单独的量级（7.5，宏平均差 0.0066），说明初始化/洗牌/增强通道是 RT-DETR 种子波动的更大来源。
2. **离散度由两个小/难域主导**：animals_10（es44 单种子崩到 **0.3199**，SD 0.183）与 CImage（17 张 test，SD 0.129）——前者是某一种子在该域上明显欠拟合的单点事件（14/14 完成、退出码 0、非数值报错），后者是小样本高方差（与 YOLO es 的 CImage 最大 SD 0.018 方向一致但更极端）。剔除这两域后，逐域 SD 中位数 0.005、最大 0.012。
3. **与 YOLO 对比**：YOLO11m es 宏平均 SD 仅 0.0016，RT-DETR 为 0.0129——**RT-DETR 的域内参照对训练随机性显著更敏感**（尤其少数难域），这强化了"引用 RT-DETR 单一 run 数字时必须带不确定性"的必要性；14 域主方案宏平均 0.6929 落在 es 三种子散布（0.680–0.706）之内，与 es 均值 0.6917 一致。
4. **animals_10 es44=0.32 单独核查建议**：该值为合法但离散的单点（n=3 描述性口径不剔除），若该域要在文中作强调，建议追加一轮 seed 确认其非异常导引（协议可在 rep 体系内加跑）；目前按 n=3 原样报告。

## 八、结论边界

- 主实验为**单轮 seed=42 结果**；RT-DETR 下 seed 真实生效但**同 seed 不可逐位复现**（三、4）。运行不确定性按四轮设计（2026-10-14，第六节）分两个口径量化，**两套数字不可混写**：
  - **反传噪声通道**（n=2）：主实验 vs `train_rtdetr_rep1`——数据流（常数 generator）与类别头初值逐位相同，差异纯来自 grid_sampler_2d_backward 反传非确定性；
  - **全训练随机性**（n=3，7.6）：`train_rtdetr_es{42,43,44}`——类别头初始化 + 洗牌 + 增强 + 反传噪声四通道同时变化（es 口径，对应 YOLO es 表）；**宏平均 0.6917 ± 0.0129**（单种子 0.6895/0.7055/0.6800）。es 轮与主实验 stock 轮数据流协议不同，es 表以 es42/43/44 内部计算 mean±SD，主实验数字不并入。
  两口径均报逐域极差/样本 SD 与宏平均级离散度；n=2/n=3 为描述性离散度，不构成置信区间。
- **RT-DETR 的域内参照对训练随机性（seed）显著敏感**：宏平均级 seed SD 0.0129，远大于 YOLO11m 的 es 0.0016；离散度主要来自小/难域（animals_10 与 CImage 的极端单种子点），其余域 SD 中位 0.005。文中引用 RT-DETR 任一域内数值时应以 es 表（n=3）备注不确定性，不宜以单 run 作精确排名。
- animals_10 的 es44 = 0.3199 为 n=3 下的合法单点（非数值报错、14/14 退出码 0）；已在 7.6 标注，若该域进入正文强调建议补一轮 seed 复核。
- RT-DETR-L 的 AMP=False 与 YOLO11m 的 AMP=True 是架构声明性差异，两架构 mAP 对比时不作"除架构外全部同"的强声明（优化器、数据、预算、视图、选择规则一致，AMP/评估器后处理随架构走 stock）。
- 无 LODO 分子侧，$R^{LODO}_{target}$ 不适用于 RT-DETR-L 本轮结果。
- CImage（17 张 test）等小 test 集方差大的注意事项与 YOLO 轮相同。
- 与 7 月旧 RT-DETR 结果**不可直接比较**（数据版本与重切、val-vs-test 视图、优化器统一与否、batch/accumulate 全部不同）。
