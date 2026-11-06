window.slideDataMap.set(25, `
<div class="w-[1440px] h-[810px] shadow-2xl relative overflow-hidden slide-bg">
  <div class="w-[1350px] h-[700px] mx-auto my-[40px] flex flex-col justify-center">

    <div class="mb-9">
      <h2 class="text-[38px] font-light text-gray-900 mb-3">六点贡献：把「该不该合」变成可检验的问题</h2>
      <div class="w-40 h-1 bg-primary mb-3"></div>
      <p class="text-[16px] text-gray-500">没有提出新的检测网络，价值全在实验设计与评估框架上</p>
    </div>

    <div class="grid grid-cols-3 gap-x-12 gap-y-9">

      <div>
        <div class="text-[38px] font-thin text-gray-200 leading-none mb-3">01</div>
        <h3 class="text-[18px] font-semibold text-gray-900 mb-2">三类数据池的系统对照</h3>
        <p class="text-[15px] text-gray-600 leading-relaxed">单数据集 / 同域数据池 / 跨域全量数据池，在同一检测器与训练协议下比较。</p>
      </div>

      <div>
        <div class="text-[38px] font-thin text-gray-200 leading-none mb-3">02</div>
        <h3 class="text-[18px] font-semibold text-gray-900 mb-2">把域差、预处理、零样本放在一起看</h3>
        <p class="text-[15px] text-gray-600 leading-relaxed">7 个红外数据集、5 个训练 + 2 个零样本，覆盖地面与航拍两类平台。</p>
      </div>

      <div>
        <div class="text-[38px] font-thin text-gray-200 leading-none mb-3">03</div>
        <h3 class="text-[18px] font-semibold text-gray-900 mb-2">用两种工具刻画「训练—测试」关系</h3>
        <p class="text-[15px] text-gray-600 leading-relaxed">CLIP + t-SNE 观察图像分布，DAS 观察模型内部的来源判断，信息互补。</p>
      </div>

      <div>
        <div class="text-[38px] font-thin text-gray-200 leading-none mb-3">04</div>
        <h3 class="text-[18px] font-semibold text-gray-900 mb-2">证明「更多数据」≠「更好性能」</h3>
        <p class="text-[15px] text-gray-600 leading-relaxed">WIT-UAS 上单数据集模型 0.219 反超全量池 0.217，是最直接的反例。</p>
      </div>

      <div>
        <div class="text-[38px] font-thin text-gray-200 leading-none mb-3">05</div>
        <h3 class="text-[18px] font-semibold text-gray-900 mb-2">指出稀疏数据池的效率优势</h3>
        <p class="text-[15px] text-gray-600 leading-relaxed">少数但匹配的数据集，可以达到与全量池相当的结果，训练成本却低得多。</p>
      </div>

      <div>
        <div class="text-[38px] font-thin text-gray-200 leading-none mb-3">06</div>
        <h3 class="text-[18px] font-semibold text-gray-900 mb-2">明确相似性分析的边界</h3>
        <p class="text-[15px] text-gray-600 leading-relaxed">t-SNE 与 DAS 都只能辅助筛选候选，最终仍要靠重训与跨数据集 mAP 验证。</p>
      </div>
    </div>
  </div>

  <div class="absolute bottom-4 left-12 right-12 flex justify-between text-[12px] text-gray-400 tracking-wide">
    <span>Fusion or Confusion? · Becker et al. · CVPRW 2025</span>
    <span>25 / 26</span>
  </div>
</div>
`);
