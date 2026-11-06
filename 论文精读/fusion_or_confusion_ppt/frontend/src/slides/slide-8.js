window.slideDataMap.set(8, `
<div class="w-[1440px] h-[810px] shadow-2xl relative overflow-hidden slide-bg">
  <div class="w-[1350px] h-[700px] mx-auto my-[40px] flex">

    <!-- 左侧标题区 -->
    <div class="w-[330px] flex flex-col justify-center pr-12 border-r border-gray-200 flex-shrink-0">
      <h2 class="text-[38px] font-light text-gray-900 leading-tight mb-5">七个<br/>红外数据集</h2>
      <p class="text-[15px] text-gray-500 leading-relaxed mb-7">数字取自原文 Table 1。前 5 个进入训练池，后 2 个只用于零样本评估。</p>
      <div class="border-l-2 border-accent-1 pl-4">
        <p class="text-[15px] text-gray-600 leading-relaxed">训练池合计<br/><span class="text-[24px] font-semibold text-gray-900">20,477</span> 张图像<br/><span class="text-[24px] font-semibold text-gray-900">239,937</span> 个实例</p>
      </div>
    </div>

    <!-- 右侧表格 -->
    <div class="flex-1 pl-12 flex flex-col justify-center">
      <table class="w-full text-left border-collapse">
        <thead>
          <tr class="border-b-2 border-gray-800">
            <th class="py-3 pr-3 text-[14px] font-semibold text-gray-900">数据集</th>
            <th class="py-3 px-2 text-[14px] font-semibold text-gray-900">类型</th>
            <th class="py-3 px-2 text-[14px] font-semibold text-gray-900">分辨率</th>
            <th class="py-3 px-2 text-[14px] font-semibold text-gray-900 text-right">训练 / 测试图像</th>
            <th class="py-3 px-2 text-[14px] font-semibold text-gray-900 text-right">子类数</th>
            <th class="py-3 pl-2 text-[14px] font-semibold text-gray-900 text-right">训练实例</th>
          </tr>
        </thead>
        <tbody class="text-gray-700">
          <tr class="border-b border-gray-100">
            <td class="py-[11px] pr-3 text-[15px] font-medium text-gray-900">FLIR (v2)</td>
            <td class="py-[11px] px-2 text-[14px] text-gray-500">ground</td>
            <td class="py-[11px] px-2 text-[14px] text-gray-500">640×512</td>
            <td class="py-[11px] px-2 text-[14px] text-right">9,824 / 3,493</td>
            <td class="py-[11px] px-2 text-[14px] text-right">15</td>
            <td class="py-[11px] pl-2 text-[14px] text-right">73,622</td>
          </tr>
          <tr class="border-b border-gray-100">
            <td class="py-[11px] pr-3 text-[15px] font-medium text-gray-900">M3FD</td>
            <td class="py-[11px] px-2 text-[14px] text-gray-500">ground</td>
            <td class="py-[11px] px-2 text-[14px] text-gray-500">1024×768</td>
            <td class="py-[11px] px-2 text-[14px] text-right">2,386 / 613</td>
            <td class="py-[11px] px-2 text-[14px] text-right">6</td>
            <td class="py-[11px] pl-2 text-[14px] text-right">15,407</td>
          </tr>
          <tr class="border-b border-gray-100">
            <td class="py-[11px] pr-3 text-[15px] font-medium text-gray-900">DroneVehicle</td>
            <td class="py-[11px] px-2 text-[14px] text-gray-500">aerial</td>
            <td class="py-[11px] px-2 text-[14px] text-gray-500">640×512</td>
            <td class="py-[11px] px-2 text-[14px] text-right">5,495 / 4,465</td>
            <td class="py-[11px] px-2 text-[14px] text-right">5</td>
            <td class="py-[11px] pl-2 text-[14px] text-right">115,701</td>
          </tr>
          <tr class="border-b border-gray-100">
            <td class="py-[11px] pr-3 text-[15px] font-medium text-gray-900">TrafficNight</td>
            <td class="py-[11px] px-2 text-[14px] text-gray-500">aerial</td>
            <td class="py-[11px] px-2 text-[14px] text-gray-500">1280×1024</td>
            <td class="py-[11px] px-2 text-[14px] text-right">1,759 / 366</td>
            <td class="py-[11px] px-2 text-[14px] text-right">6</td>
            <td class="py-[11px] pl-2 text-[14px] text-right">29,852</td>
          </tr>
          <tr class="border-b border-gray-300">
            <td class="py-[11px] pr-3 text-[15px] font-medium text-gray-900">HIT-UAV</td>
            <td class="py-[11px] px-2 text-[14px] text-gray-500">aerial</td>
            <td class="py-[11px] px-2 text-[14px] text-gray-500">640×512</td>
            <td class="py-[11px] px-2 text-[14px] text-right">1,013 / 272</td>
            <td class="py-[11px] px-2 text-[14px] text-right">5</td>
            <td class="py-[11px] pl-2 text-[14px] text-right">5,355</td>
          </tr>
          <tr class="border-b border-gray-100 bg-gray-50/60">
            <td class="py-[11px] pr-3 text-[15px] font-medium text-gray-500">MCNet <span class="text-accent-1">*</span></td>
            <td class="py-[11px] px-2 text-[14px] text-gray-400">ground</td>
            <td class="py-[11px] px-2 text-[14px] text-gray-400">720×576</td>
            <td class="py-[11px] px-2 text-[14px] text-gray-400 text-right">— / 665</td>
            <td class="py-[11px] px-2 text-[14px] text-gray-400 text-right">10</td>
            <td class="py-[11px] pl-2 text-[14px] text-gray-400 text-right">2,424</td>
          </tr>
          <tr class="border-b border-gray-100 bg-gray-50/60">
            <td class="py-[11px] pr-3 text-[15px] font-medium text-gray-500">WIT-UAS <span class="text-accent-1">*</span></td>
            <td class="py-[11px] px-2 text-[14px] text-gray-400">aerial</td>
            <td class="py-[11px] px-2 text-[14px] text-gray-400">640×512</td>
            <td class="py-[11px] px-2 text-[14px] text-gray-400 text-right">— / 857</td>
            <td class="py-[11px] px-2 text-[14px] text-gray-400 text-right">2</td>
            <td class="py-[11px] pl-2 text-[14px] text-gray-400 text-right">2,396</td>
          </tr>
        </tbody>
      </table>

      <p class="text-[13px] text-gray-400 mt-4 leading-relaxed">
        * 零样本测试集，不参与任何训练。<span class="mx-2">|</span>「子类数」为标签统一前各数据集车辆子类别数量，「训练实例」为统一为 vehicle 后的实例总数。
      </p>
    </div>
  </div>

  <div class="absolute bottom-4 left-12 right-12 flex justify-between text-[12px] text-gray-400 tracking-wide">
    <span>Fusion or Confusion? · Becker et al. · CVPRW 2025</span>
    <span>08 / 26</span>
  </div>
</div>
`);
