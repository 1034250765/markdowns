window.slideDataMap.set(10, `
<div class="w-[1440px] h-[810px] shadow-2xl relative overflow-hidden slide-bg">
  <div class="w-[1350px] h-[700px] mx-auto my-[40px] flex gap-14">

    <div class="flex-1 flex flex-col justify-center">
      <h2 class="text-[36px] font-light text-gray-900 mb-7">第三步：固定检测器与训练协议</h2>
      <div class="space-y-6">
        <div class="border-l-4 border-gray-900 pl-6">
          <h3 class="text-[21px] font-semibold text-gray-800 mb-2">YOLOv9-C：单阶段实时检测器</h3>
          <p class="text-gray-600 text-[16px] leading-relaxed">采用 PGI 稳定梯度流、GELAN 减少训练瓶颈；单次前向输出检测结果。它只是「参考检测器」，不是本文研究对象。</p>
        </div>
        <div class="border-l-4 border-gray-300 pl-6">
          <h3 class="text-[21px] font-semibold text-gray-800 mb-2">训练协议：COCO 预训练 + 150 epochs</h3>
          <p class="text-gray-600 text-[16px] leading-relaxed">全部模型以 MS COCO 预训练权重初始化，统一训练 150 轮；报告 mAP@.5 与更严格的 mAP@.5:.95（10 个 IoU 阈值平均）。</p>
        </div>
        <div class="border-l-4 border-gray-300 pl-6">
          <h3 class="text-[21px] font-semibold text-gray-800 mb-2">两组设计对照</h3>
          <p class="text-gray-600 text-[16px] leading-relaxed">一是<b>全量微调 vs 冻结骨干</b>（看是否需要适配红外特征）；二是<b>是否引入 DAS</b>（看预测数据集来源是否有助于泛化）。</p>
        </div>
        <div class="border-l-4 border-gray-300 pl-6">
          <h3 class="text-[21px] font-semibold text-gray-800 mb-2">数据平衡：对固定机位序列下采样</h3>
          <p class="text-gray-600 text-[16px] leading-relaxed">避免冗余背景被反复采样。各数据集绝对量不等，但单数据集模型与池化模型从每个数据集取用的数据量一致。</p>
        </div>
      </div>
    </div>

    <div class="w-[330px] flex items-center justify-center border-l border-gray-100 overflow-hidden">
      <div class="text-center">
        <div class="text-[6rem] font-bold text-gray-100 leading-none mb-2">150</div>
        <p class="text-[22px] text-gray-700">epochs</p>
        <p class="text-gray-500 text-[15px] mt-3 leading-relaxed">所有模型统一训练轮数<br/>保证池化对比公平</p>
        <div class="w-12 h-px bg-gray-300 mx-auto my-6"></div>
        <p class="text-[14px] text-gray-500 leading-relaxed">MS COCO 预训练初始化<br/>mAP@.5 / mAP@.5:.95</p>
      </div>
    </div>
  </div>

  <div class="absolute bottom-4 left-12 right-12 flex justify-between text-[12px] text-gray-400 tracking-wide">
    <span>Fusion or Confusion? · Becker et al. · CVPRW 2025</span>
    <span>10 / 26</span>
  </div>
</div>
`);
