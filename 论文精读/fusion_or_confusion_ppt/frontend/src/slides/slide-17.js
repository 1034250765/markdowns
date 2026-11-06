window.slideDataMap.set(17, `
<div class="w-[1440px] h-[810px] shadow-2xl relative overflow-hidden slide-bg">
  <div class="w-[1350px] h-[700px] mx-auto my-[40px] flex">

    <!-- 左侧标题区 -->
    <div class="w-[330px] flex flex-col justify-center pr-12 border-r border-gray-200 flex-shrink-0">
      <p class="text-[13px] tracking-widest text-gray-400 mb-3">结论 04 · TABLE 4</p>
      <h2 class="text-[38px] font-light text-gray-900 leading-tight mb-5">预处理<br/>没有稳定收益</h2>
      <p class="text-[15px] text-gray-500 leading-relaxed mb-6">在 All 池上分别施加 HE / CLAHE / FieldScale，再对比原始图像。</p>

      <div class="border-l-2 border-accent-1 pl-4 space-y-3">
        <p class="text-[15px] text-gray-600 leading-relaxed">24 组对比中只有 <b class="text-gray-900">1 组</b>微弱提升（WIT-UAS + HE，+0.006）。</p>
        <p class="text-[15px] text-gray-600 leading-relaxed">其余持平或下降，<b class="text-gray-900">最大跌幅 −0.032</b>。</p>
      </div>

      <p class="text-[13px] text-gray-400 leading-relaxed mt-6">
        检测器似乎能在特征学习阶段自行补偿对比度差异。
      </p>
    </div>

    <!-- 右侧表格 -->
    <div class="flex-1 pl-12 flex flex-col justify-center">
      <table class="w-full text-left border-collapse">
        <thead>
          <tr class="border-b-2 border-gray-800">
            <th class="py-3 text-[14px] font-semibold text-gray-900">测试集</th>
            <th class="py-3 text-[14px] font-semibold text-gray-900 text-right">原始图像</th>
            <th class="py-3 text-[14px] font-semibold text-gray-500 text-right">HE</th>
            <th class="py-3 text-[14px] font-semibold text-gray-500 text-right">CLAHE</th>
            <th class="py-3 text-[14px] font-semibold text-gray-500 text-right">FieldScale</th>
            <th class="py-3 text-[14px] font-semibold text-gray-500 text-right">最优方法</th>
          </tr>
        </thead>
        <tbody>
          <tr class="border-b border-gray-100">
            <td class="py-[13px] text-[15px] text-gray-800">FLIR (v2)</td>
            <td class="py-[13px] text-[15px] font-semibold text-gray-900 text-right">0.513</td>
            <td class="py-[13px] text-[15px] text-gray-600 text-right">0.497</td>
            <td class="py-[13px] text-[15px] text-gray-600 text-right">0.496</td>
            <td class="py-[13px] text-[15px] text-gray-600 text-right">0.505</td>
            <td class="py-[13px] text-[14px] text-accent-1 text-right">原始图像</td>
          </tr>
          <tr class="border-b border-gray-100">
            <td class="py-[13px] text-[15px] text-gray-800">M3FD</td>
            <td class="py-[13px] text-[15px] font-semibold text-gray-900 text-right">0.612</td>
            <td class="py-[13px] text-[15px] text-gray-600 text-right">0.607</td>
            <td class="py-[13px] text-[15px] text-gray-600 text-right">0.612</td>
            <td class="py-[13px] text-[15px] text-gray-600 text-right">0.610</td>
            <td class="py-[13px] text-[14px] text-accent-1 text-right">原始/CLAHE</td>
          </tr>
          <tr class="border-b border-gray-100">
            <td class="py-[13px] text-[15px] text-gray-800">DroneVehicle</td>
            <td class="py-[13px] text-[15px] font-semibold text-gray-900 text-right">0.601</td>
            <td class="py-[13px] text-[15px] text-gray-600 text-right">0.601</td>
            <td class="py-[13px] text-[15px] text-gray-600 text-right">0.601</td>
            <td class="py-[13px] text-[15px] text-gray-600 text-right">0.602</td>
            <td class="py-[13px] text-[14px] text-gray-400 text-right">完全持平</td>
          </tr>
          <tr class="border-b border-gray-100">
            <td class="py-[13px] text-[15px] text-gray-800">TrafficNight</td>
            <td class="py-[13px] text-[15px] font-semibold text-gray-900 text-right">0.563</td>
            <td class="py-[13px] text-[15px] text-gray-600 text-right">0.545</td>
            <td class="py-[13px] text-[15px] text-gray-600 text-right">0.556</td>
            <td class="py-[13px] text-[15px] text-gray-600 text-right">0.531</td>
            <td class="py-[13px] text-[14px] text-accent-1 text-right">原始图像</td>
          </tr>
          <tr class="border-b border-gray-100">
            <td class="py-[13px] text-[15px] text-gray-800">HIT-UAV</td>
            <td class="py-[13px] text-[15px] font-semibold text-gray-900 text-right">0.703</td>
            <td class="py-[13px] text-[15px] text-gray-600 text-right">0.699</td>
            <td class="py-[13px] text-[15px] text-gray-600 text-right">0.694</td>
            <td class="py-[13px] text-[15px] text-gray-600 text-right">0.699</td>
            <td class="py-[13px] text-[14px] text-accent-1 text-right">原始图像</td>
          </tr>
          <tr class="border-b border-gray-100">
            <td class="py-[13px] text-[15px] text-gray-800">MCNet <span class="text-gray-400 text-[13px]">零样本</span></td>
            <td class="py-[13px] text-[15px] font-semibold text-gray-900 text-right">0.681</td>
            <td class="py-[13px] text-[15px] text-gray-600 text-right">0.657</td>
            <td class="py-[13px] text-[15px] text-gray-600 text-right">0.666</td>
            <td class="py-[13px] text-[15px] text-gray-600 text-right">0.675</td>
            <td class="py-[13px] text-[14px] text-accent-1 text-right">原始图像</td>
          </tr>
          <tr class="border-b border-gray-300">
            <td class="py-[13px] text-[15px] text-gray-800">WIT-UAS <span class="text-gray-400 text-[13px]">零样本</span></td>
            <td class="py-[13px] text-[15px] font-semibold text-gray-900 text-right">0.217</td>
            <td class="py-[13px] text-[15px] text-accent-2 text-right">0.223</td>
            <td class="py-[13px] text-[15px] text-gray-600 text-right">0.202</td>
            <td class="py-[13px] text-[15px] text-gray-600 text-right">0.212</td>
            <td class="py-[13px] text-[14px] text-accent-2 text-right">HE（+0.006）</td>
          </tr>
        </tbody>
      </table>

      <p class="text-[13px] text-gray-400 mt-4">指标 mAP@.5:.95，训练池固定为 All，骨干全量微调。加粗列为该行基线。</p>
    </div>
  </div>

  <div class="absolute bottom-4 left-12 right-12 flex justify-between text-[12px] text-gray-400 tracking-wide">
    <span>Fusion or Confusion? · Becker et al. · CVPRW 2025</span>
    <span>17 / 26</span>
  </div>
</div>
`);
