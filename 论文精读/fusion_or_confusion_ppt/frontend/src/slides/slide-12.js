window.slideDataMap.set(12, `
<div class="w-[1440px] h-[810px] shadow-2xl relative overflow-hidden slide-bg">
  <div class="w-[1350px] h-[700px] mx-auto my-[40px] flex gap-14">

    <div class="flex-1 flex flex-col justify-center gap-7">
      <div>
        <h2 class="text-[38px] font-light text-gray-900 mb-5 pb-4 border-b-2 border-gray-300">第五步：用什么判断「该不该合」</h2>
        <p class="text-gray-700 text-[17px] leading-relaxed mb-4">
          检测性能只能事后评价，且每试一种组合就要重训一次。论文因此引入两类分析手段，希望在训练之前先圈出候选范围。
        </p>
        <p class="text-gray-700 text-[17px] leading-relaxed">
          两者观察的对象完全不同：一个看<b>图像看起来像不像</b>，一个看<b>模型认为它来自哪</b>。
        </p>
      </div>

      <div class="border-l-4 border-gray-300 pl-6 py-2">
        <p class="text-gray-600 text-[16px] italic leading-relaxed">"低维可视化帮助理解域关系，但不能可靠地指导数据池选择。"</p>
        <p class="text-gray-400 text-[14px] mt-2">— 原文对两类方法的定位</p>
      </div>
    </div>

    <div class="flex-1 flex flex-col justify-center">
      <h3 class="text-[22px] font-semibold text-gray-500 mb-5 tracking-wide">TWO ANALYSIS TOOLS</h3>
      <ul class="space-y-[22px]">
        <li class="flex items-start gap-4">
          <span class="flex-shrink-0 w-8 h-8 rounded-full bg-gray-800 text-white text-[14px] flex items-center justify-center mt-0.5">A</span>
          <div>
            <p class="text-gray-900 text-[17px] font-semibold mb-1">CLIP 特征 + t-SNE 降维</p>
            <p class="text-gray-600 text-[15px] leading-relaxed">提取每个数据集的图像特征，降到二维观察聚类与距离。只能定性回答「域差有多大」，无法告诉你怎么选。</p>
          </div>
        </li>
        <li class="flex items-start gap-4">
          <span class="flex-shrink-0 w-8 h-8 rounded-full bg-primary text-white text-[14px] flex items-center justify-center mt-0.5">B</span>
          <div>
            <p class="text-gray-900 text-[17px] font-semibold mb-1">Dataset Affinity Score（DAS）</p>
            <p class="text-gray-600 text-[15px] leading-relaxed">让检测器顺带预测每个检测框「来自哪个训练集」，把域匹配变成可统计的分布——这是本文更看重的一种。</p>
          </div>
        </li>
      </ul>

      <div class="mt-8 bg-gray-50 border border-gray-200 px-6 py-4">
        <p class="text-[15px] text-gray-600 leading-relaxed"><span class="font-semibold text-gray-800">共同定位：</span>它们都不改变训练目标（DAS 除外），只负责「提出候选」，最终仍要用 mAP 裁决。</p>
      </div>
    </div>
  </div>

  <div class="absolute bottom-4 left-12 right-12 flex justify-between text-[12px] text-gray-400 tracking-wide">
    <span>Fusion or Confusion? · Becker et al. · CVPRW 2025</span>
    <span>12 / 26</span>
  </div>
</div>
`);
