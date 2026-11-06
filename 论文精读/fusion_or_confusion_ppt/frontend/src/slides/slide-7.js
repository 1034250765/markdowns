window.slideDataMap.set(7, `
<div class="w-[1440px] h-[810px] shadow-2xl relative overflow-hidden slide-bg">
  <div class="w-[1350px] h-[700px] mx-auto my-[40px] flex gap-14">

    <div class="flex-1 flex flex-col justify-center">
      <h2 class="text-[36px] font-light text-gray-900 mb-7">第一步：把标签收敛到一个上位类</h2>
      <div class="space-y-6">
        <div class="border-l-4 border-gray-900 pl-6">
          <h3 class="text-[21px] font-semibold text-gray-800 mb-2">问题：各数据集类别体系完全不同</h3>
          <p class="text-gray-600 text-[16px] leading-relaxed">7 个数据集的车辆子类数量从 2 类到 15 类不等，例如 FLIR v2 有 15 类、WIT-UAS 只有 1 类，还混用 car / truck / van / freight car 等不同口径。</p>
        </div>
        <div class="border-l-4 border-gray-300 pl-6">
          <h3 class="text-[21px] font-semibold text-gray-800 mb-2">为什么不用 WordTree 那套层级方案</h3>
          <p class="text-gray-600 text-[16px] leading-relaxed">Redmon 等人用概念层级树整合 ImageNet 与 COCO 标签，但子类粒度与细节差异会让层级难以对齐；作者选择更彻底的做法。</p>
        </div>
        <div class="border-l-4 border-gray-300 pl-6">
          <h3 class="text-[21px] font-semibold text-gray-800 mb-2">做法：全部映射为单一父类 vehicle</h3>
          <p class="text-gray-600 text-[16px] leading-relaxed">把 car / bus / truck / van / freight car 等子类统一为 <span class="font-mono text-[15px] text-accent-1">vehicle</span>，构建单类别检测器。这样「标签冲突」被从实验中剔除，性能差异只剩下来自域的部分。</p>
        </div>
      </div>

      <div class="mt-7 bg-gray-50 border border-gray-200 px-6 py-3">
        <p class="text-[15px] text-gray-600"><span class="font-semibold text-gray-800">代价：</span>放弃了细粒度分类能力，换来的是可比较的实验条件——这正是评估型论文需要的取舍。</p>
      </div>
    </div>

    <div class="w-[330px] flex items-center justify-center border-l border-gray-100">
      <div class="text-center">
        <p class="text-[14px] text-gray-400 mb-4 tracking-wide">SUPER-CATEGORY</p>
        <div class="text-[40px] font-bold text-gray-200 leading-none mb-6">→</div>
        <p class="text-[30px] text-gray-900 font-light tracking-wide mb-3">vehicle</p>
        <div class="w-12 h-px bg-gray-300 mx-auto mb-5"></div>
        <p class="text-[14px] text-gray-500 leading-relaxed">car · bus · truck<br/>van · freight car<br/>…</p>
        <p class="text-[13px] text-gray-400 mt-5 leading-relaxed">7 个数据集<br/>合并为 1 个类别</p>
      </div>
    </div>
  </div>

  <div class="absolute bottom-4 left-12 right-12 flex justify-between text-[12px] text-gray-400 tracking-wide">
    <span>Fusion or Confusion? · Becker et al. · CVPRW 2025</span>
    <span>07 / 26</span>
  </div>
</div>
`);
