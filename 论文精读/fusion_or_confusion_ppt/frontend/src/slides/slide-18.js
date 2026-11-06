window.slideDataMap.set(18, `
<div class="w-[1440px] h-[810px] shadow-2xl relative overflow-hidden slide-bg">
  <div class="w-[1350px] h-[700px] mx-auto my-[40px] flex">
    <div class="w-2 bg-primary"></div>
    <div class="flex-1 px-14 flex flex-col justify-center">

      <div class="mb-7">
        <p class="text-[13px] tracking-widest text-gray-400 mb-2">结论 05 · TABLE 5</p>
        <h2 class="text-[38px] font-light text-gray-900 mb-2">全量微调优于冻结骨干</h2>
        <p class="text-[16px] text-gray-500">在所有测试集、所有数据池上，方向完全一致</p>
      </div>

      <div class="space-y-6">
        <div class="flex items-start gap-6">
          <div class="w-3 h-3 bg-primary mt-2 flex-shrink-0"></div>
          <div>
            <h3 class="text-[21px] font-semibold text-gray-800 mb-1.5">全量微调在全部测试集上更优</h3>
            <p class="text-gray-600 text-[16px] leading-relaxed">All 池、无预处理条件下：FLIR v2 <b class="text-gray-900">0.513 vs 0.461</b>，M3FD <b class="text-gray-900">0.612 vs 0.548</b>，DroneVehicle <b class="text-gray-900">0.601 vs 0.594</b>。</p>
          </div>
        </div>

        <div class="flex items-start gap-6">
          <div class="w-3 h-3 bg-primary mt-2 flex-shrink-0"></div>
          <div>
            <h3 class="text-[21px] font-semibold text-gray-800 mb-1.5">冻结骨干省不下多少，却损失不少</h3>
            <p class="text-gray-600 text-[16px] leading-relaxed">冻结 COCO 预训练骨干看似能防止对单一数据集过拟合，但红外与可见光的底层特征差异过大，不调整就无法适配多数据集分布。</p>
          </div>
        </div>

        <div class="flex items-start gap-6">
          <div class="w-3 h-3 bg-primary mt-2 flex-shrink-0"></div>
          <div>
            <h3 class="text-[21px] font-semibold text-gray-800 mb-1.5">未观察到「逐数据集过拟合」</h3>
            <p class="text-gray-600 text-[16px] leading-relaxed">作者明确说明，实验中<b>没有</b>出现全量微调导致单数据集性能退化的情况——这削弱了「冻结更稳」这一常见假设。</p>
          </div>
        </div>
      </div>

      <div class="mt-7 bg-gray-50 border border-gray-200 px-6 py-3">
        <p class="text-[15px] text-gray-600"><span class="font-semibold text-gray-800">实践含义：</span>跨数据集训练时，「先冻结再解冻」的两段式并非必需；直接全量微调更简单，也更有效。</p>
      </div>
    </div>
  </div>

  <div class="absolute bottom-4 left-12 right-12 flex justify-between text-[12px] text-gray-400 tracking-wide">
    <span>Fusion or Confusion? · Becker et al. · CVPRW 2025</span>
    <span>18 / 26</span>
  </div>
</div>
`);
