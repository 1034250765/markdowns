window.slideDataMap.set(22, `
<div class="w-[1440px] h-[810px] shadow-2xl relative overflow-hidden slide-bg">
  <div class="w-[1350px] h-[700px] mx-auto my-[40px] flex items-center justify-center">
    <div class="max-w-5xl w-full">

      <div class="text-center">
        <div class="inline-block px-3 py-1 border border-gray-300 text-[13px] tracking-widest text-gray-500 mb-7">
          DAS · 5.5 局限
        </div>
        <h2 class="text-[40px] font-light text-gray-900 mb-6">
          DAS 能诊断，但<span class="text-accent-1 font-normal">不能提分</span>
        </h2>
        <p class="text-[17px] text-gray-600 leading-relaxed max-w-3xl mx-auto">
          要求模型同时判断「这是什么目标」和「它来自哪个域」，会分散学习能力。零样本结果里，DAS 让两个测试集都掉点。
        </p>
      </div>

      <div class="flex justify-center gap-16 mt-12">
        <div class="text-center">
          <p class="text-[14px] text-gray-500 mb-3">MCNet</p>
          <div class="flex items-baseline gap-3 justify-center">
            <span class="text-[38px] font-light text-gray-400 line-through decoration-1">0.681</span>
            <span class="text-[15px] text-gray-400">→</span>
            <span class="text-[38px] font-light text-gray-900">0.663</span>
          </div>
          <p class="text-[13px] text-accent-1 mt-2">−0.018</p>
        </div>
        <div class="w-px bg-gray-200"></div>
        <div class="text-center">
          <p class="text-[14px] text-gray-500 mb-3">WIT-UAS</p>
          <div class="flex items-baseline gap-3 justify-center">
            <span class="text-[38px] font-light text-gray-400 line-through decoration-1">0.217</span>
            <span class="text-[15px] text-gray-400">→</span>
            <span class="text-[38px] font-light text-gray-900">0.175</span>
          </div>
          <p class="text-[13px] text-accent-1 mt-2">−0.042</p>
        </div>
      </div>

      <div class="grid grid-cols-3 gap-8 mt-14">
        <div class="border-t border-gray-200 pt-5">
          <h3 class="text-[17px] font-semibold text-gray-900 mb-2">不是因果贡献度</h3>
          <p class="text-[14px] text-gray-600 leading-relaxed">某个框被分给 FLIR，不代表它只由 FLIR 训练而来；模型参数由整个训练池共同优化。</p>
        </div>
        <div class="border-t border-gray-200 pt-5">
          <h3 class="text-[17px] font-semibold text-gray-900 mb-2">不是可直接套用的公式</h3>
          <p class="text-[14px] text-gray-600 leading-relaxed">它能筛候选组合、解释域关系，但不能证明某个组合一定提升 mAP。</p>
        </div>
        <div class="border-t border-gray-200 pt-5">
          <h3 class="text-[17px] font-semibold text-gray-900 mb-2">会牺牲检测精度</h3>
          <p class="text-[14px] text-gray-600 leading-relaxed">本文定位为解释工具而非性能模块——想要精度，就不要在最终模型上加 DAS。</p>
        </div>
      </div>
    </div>
  </div>

  <div class="absolute bottom-4 left-12 right-12 flex justify-between text-[12px] text-gray-400 tracking-wide">
    <span>Fusion or Confusion? · Becker et al. · CVPRW 2025</span>
    <span>22 / 26</span>
  </div>
</div>
`);
