window.slideDataMap.set(15, `
<div class="w-[1440px] h-[810px] shadow-2xl relative overflow-hidden slide-bg">
  <div class="w-[1350px] h-[700px] mx-auto my-[40px] flex items-center justify-center">
    <div class="max-w-5xl w-full">

      <div class="text-center mb-2">
        <div class="inline-block px-3 py-1 border border-gray-300 text-[13px] tracking-widest text-gray-500 mb-8">
          结论 02 · ZERO-SHOT
        </div>
        <h2 class="text-[42px] font-light text-gray-900 leading-tight mb-6">
          零样本测试：<br/>单数据集模型可以<span class="text-accent-1 font-normal">打赢全量池</span>
        </h2>
        <p class="text-[18px] text-gray-600 leading-relaxed max-w-3xl mx-auto">
          MCNet（地面）与 WIT-UAS（航拍）从未参与训练。如果「池化能提升对未知域的泛化」成立，
          它们应该被 All 池大幅超越——但事实并非如此。
        </p>
      </div>

      <div class="flex justify-center gap-12 mt-12">
        <div class="text-center">
          <div class="text-[52px] font-light text-accent-1 leading-none mb-3">0.219</div>
          <p class="text-[14px] text-gray-500 leading-relaxed">WIT-UAS<br/>TrafficNight 单模型</p>
        </div>
        <div class="w-px bg-gray-200"></div>
        <div class="text-center">
          <div class="text-[52px] font-light text-gray-900 leading-none mb-3">0.217</div>
          <p class="text-[14px] text-gray-500 leading-relaxed">WIT-UAS<br/>All 池（5 个数据集）</p>
        </div>
        <div class="w-px bg-gray-200"></div>
        <div class="text-center">
          <div class="text-[52px] font-light text-gray-400 leading-none mb-3">0.001</div>
          <p class="text-[14px] text-gray-500 leading-relaxed">WIT-UAS<br/>Ground 池（0 覆盖）</p>
        </div>
      </div>

      <div class="mt-12 mx-auto max-w-4xl border-t border-gray-200 pt-6 space-y-3">
        <p class="text-[16px] text-gray-600 leading-relaxed">
          <span class="font-semibold text-gray-900">MCNet 上：</span>All 池 0.681、单 FLIR 模型 0.656、Ground 池 0.672——用 2/5 的数据拿到 98% 的收益。
        </p>
        <p class="text-[16px] text-gray-600 leading-relaxed">
          <span class="font-semibold text-gray-900">WIT-UAS 上：</span>Ground 池几乎完全失效（0.001），说明该测试域在训练池里<b>没有对应覆盖</b>；加数据之前，先得有「对的数据」。
        </p>
      </div>
    </div>
  </div>

  <div class="absolute bottom-4 left-12 right-12 flex justify-between text-[12px] text-gray-400 tracking-wide">
    <span>Fusion or Confusion? · Becker et al. · CVPRW 2025</span>
    <span>15 / 26</span>
  </div>
</div>
`);
