window.slideDataMap.set(14, `
<div class="w-[1440px] h-[810px] shadow-2xl relative overflow-hidden slide-bg">
  <div class="absolute top-0 right-0 w-40 h-40 border-t-4 border-r-4 border-gray-200"></div>

  <div class="w-[1350px] h-[700px] mx-auto my-[40px]">
    <div class="h-full flex flex-col">

      <!-- 标题区 -->
      <div class="mb-7">
        <div class="flex items-center gap-4 mb-2">
          <div class="w-12 h-0.5 bg-primary"></div>
          <span class="text-gray-500 text-[14px] tracking-wider">结论 01 · TABLE 2</span>
        </div>
        <h2 class="text-[38px] font-light text-gray-900">融合通常有帮助，但不是数据越多越好</h2>
      </div>

      <!-- 主内容 -->
      <div class="flex-1 flex gap-10">

        <!-- 左侧结论 -->
        <div class="w-[46%] space-y-5">
          <div>
            <div class="flex items-baseline gap-3 mb-1.5">
              <span class="text-[28px] font-thin text-gray-300">01</span>
              <h3 class="text-[20px] font-semibold text-gray-800">全量池并不总是最优</h3>
            </div>
            <p class="text-gray-600 text-[16px] leading-relaxed pl-11">5 个测试集中有 2 个（FLIR v2、M3FD）由同域 Ground 池取得最好结果，All 池反而下降。</p>
          </div>
          <div>
            <div class="flex items-baseline gap-3 mb-1.5">
              <span class="text-[28px] font-thin text-gray-300">02</span>
              <h3 class="text-[20px] font-semibold text-gray-800">增益只出现在「域内样本更丰富」的测试集</h3>
            </div>
            <p class="text-gray-600 text-[16px] leading-relaxed pl-11">HIT-UAV 上 All 池达到 0.703，比单数据集高 0.034；DroneVehicle 与 TrafficNight 几乎持平（±0.001）。</p>
          </div>
          <div>
            <div class="flex items-baseline gap-3 mb-1.5">
              <span class="text-[28px] font-thin text-gray-300">03</span>
              <h3 class="text-[20px] font-semibold text-gray-800">用更少但更匹配的数据，可以打平全量池</h3>
            </div>
            <p class="text-gray-600 text-[16px] leading-relaxed pl-11">地面测试集上 Ground 池（2 个数据集）就超过了 All 池（5 个数据集）——数据池的<b>组成</b>比<b>规模</b>更关键。</p>
          </div>
        </div>

        <!-- 右侧表格 -->
        <div class="flex-1 flex flex-col justify-center">
          <table class="w-full text-left border-collapse">
            <thead>
              <tr class="border-b-2 border-gray-800">
                <th class="py-3 text-[14px] font-semibold text-gray-900">测试集</th>
                <th class="py-3 text-[14px] font-semibold text-gray-500 text-right">单数据集</th>
                <th class="py-3 text-[14px] font-semibold text-gray-900 text-right">同域池</th>
                <th class="py-3 text-[14px] font-semibold text-gray-900 text-right">All 池</th>
                <th class="py-3 text-[14px] font-semibold text-gray-500 text-right">Δ</th>
              </tr>
            </thead>
            <tbody>
              <tr class="border-b border-gray-100">
                <td class="py-3 text-[15px] text-gray-800">FLIR (v2)</td>
                <td class="py-3 text-[15px] text-gray-500 text-right">0.522</td>
                <td class="py-3 text-[15px] font-semibold text-gray-900 text-right">0.529</td>
                <td class="py-3 text-[15px] text-gray-700 text-right">0.513</td>
                <td class="py-3 text-[15px] text-accent-1 text-right">−0.009</td>
              </tr>
              <tr class="border-b border-gray-100">
                <td class="py-3 text-[15px] text-gray-800">M3FD</td>
                <td class="py-3 text-[15px] text-gray-500 text-right">0.628</td>
                <td class="py-3 text-[15px] font-semibold text-gray-900 text-right">0.632</td>
                <td class="py-3 text-[15px] text-gray-700 text-right">0.612</td>
                <td class="py-3 text-[15px] text-accent-1 text-right">−0.016</td>
              </tr>
              <tr class="border-b border-gray-100">
                <td class="py-3 text-[15px] text-gray-800">DroneVehicle</td>
                <td class="py-3 text-[15px] text-gray-500 text-right">0.601</td>
                <td class="py-3 text-[15px] text-gray-700 text-right">0.602</td>
                <td class="py-3 text-[15px] text-gray-700 text-right">0.601</td>
                <td class="py-3 text-[15px] text-gray-400 text-right">0.000</td>
              </tr>
              <tr class="border-b border-gray-100">
                <td class="py-3 text-[15px] text-gray-800">TrafficNight</td>
                <td class="py-3 text-[15px] text-gray-500 text-right">0.564</td>
                <td class="py-3 text-[15px] font-semibold text-gray-900 text-right">0.566</td>
                <td class="py-3 text-[15px] text-gray-700 text-right">0.563</td>
                <td class="py-3 text-[15px] text-gray-400 text-right">−0.001</td>
              </tr>
              <tr class="border-b border-gray-300">
                <td class="py-3 text-[15px] text-gray-800">HIT-UAV</td>
                <td class="py-3 text-[15px] text-gray-500 text-right">0.669</td>
                <td class="py-3 text-[15px] text-gray-700 text-right">0.696</td>
                <td class="py-3 text-[15px] font-semibold text-gray-900 text-right">0.703</td>
                <td class="py-3 text-[15px] text-accent-2 text-right">+0.034</td>
              </tr>
            </tbody>
          </table>

          <div class="mt-5 flex gap-6 text-[13px] text-gray-400">
            <span class="flex items-center gap-2"><span class="w-3 h-3 bg-gray-900 inline-block"></span>该列最优</span>
            <span class="flex items-center gap-2"><span class="w-3 h-1 bg-accent-1 inline-block"></span>融合后相对单数据集下降</span>
          </div>
        </div>
      </div>

      <!-- 底部信息 -->
      <div class="mt-5 pt-3 border-t border-gray-200 flex justify-between items-center text-[13px] text-gray-400">
        <span>指标：mAP@.5:.95；条件：无预处理、全量微调、不含 DAS 预测（原文 Table 2）</span>
        <span>同域池 = Ground / Aerial 中与测试集同类型者</span>
      </div>
    </div>
  </div>

  <div class="absolute bottom-4 left-12 right-12 flex justify-between text-[12px] text-gray-400 tracking-wide">
    <span>Fusion or Confusion? · Becker et al. · CVPRW 2025</span>
    <span>14 / 26</span>
  </div>
</div>
`);
