<Slide padding={0}>
    <Box style={{
        width: '100%', height: 80,
        flexDirection: 'row', alignItems: 'center',
        paddingLeft: 40, paddingRight: 40,
        background: '#FFFFFF',
        borderBottom: '2px solid #F0F5FC',
    }}>
        <Box style={{ width: 40, height: 4, borderRadius: 2, background: '#FFC247', marginRight: 14 }} />
        <Text style={{ color: '#FFC247', fontSize: 14, fontWeight: 'bold', letterSpacing: 2 }}>CHAPTER 05 · 研究价值与应用</Text>
        <Box style={{ flex: 1 }} />
        <Text style={{ color: '#8B97A8', fontSize: 13 }}>页 17 / 18</Text>
    </Box>
    <Box style={{
        width: '100%', height: 560,
        paddingLeft: 48, paddingRight: 48,
        paddingTop: 22, paddingBottom: 22,
        gap: 14,
    }}>
        <Box style={{ width: '100%', gap: 6 }}>
            <Text style={{ color: '#1E4FA8', fontSize: 13, fontWeight: 'bold', letterSpacing: 3 }}>BROADER IMPACT</Text>
            <Text style={{ color: '#1A2230', fontSize: 30, fontWeight: 'bold' }}>
                从评测到真实部署：COUNTS 启发的下一步
            </Text>
        </Box>
        <Box style={{
            width: '100%', height: 220,
            borderRadius: 14,
            background: 'linear-gradient(135deg, #F0F5FC 0%, #E8EFF8 100%)',
            paddingTop: 18, paddingBottom: 18,
            paddingLeft: 24, paddingRight: 24,
            gap: 14,
        }}>
            <Box style={{ flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between' }}>
                <Text style={{ color: '#1E4FA8', fontSize: 14, fontWeight: 'bold', letterSpacing: 2 }}>DEPLOYMENT SCENARIOS</Text>
                <Box style={{
                    paddingLeft: 10, paddingRight: 10,
                    paddingTop: 4, paddingBottom: 4,
                    borderRadius: 8, background: '#FFC247',
                }}>
                    <Text style={{ color: '#1A2230', fontSize: 11, fontWeight: 'bold', letterSpacing: 1 }}>REAL-WORLD</Text>
                </Box>
            </Box>
            <Box style={{ flexDirection: 'row', gap: 16 }}>
                {[
                    { icon: '🚗', name: '自动驾驶', desc: '雪天/逆光/遮挡下仍需准确定位行人、车辆与障碍物', color: '#1E4FA8' },
                    { icon: '🤖', name: '机器人具身智能', desc: '复杂背景与新场景下的视觉 grounding 对交互至关重要', color: '#2BC5C0' },
                    { icon: '🎥', name: '智能监控', desc: '不同光照与天气下的目标识别与告警', color: '#FF8A4C' },
                    { icon: '🛡️', name: '内容审核', desc: '对图片内容的细粒度 grounding 与违规判定', color: '#FFC247' },
                ].map((s, i) => (
                    <Box key={i} style={{
                        flex: 1, height: 110,
                        borderRadius: 12,
                        background: '#FFFFFF',
                        border: `1.5px solid ${s.color}`,
                        paddingTop: 14, paddingBottom: 14,
                        paddingLeft: 14, paddingRight: 14,
                        gap: 6,
                    }}>
                        <Box style={{ flexDirection: 'row', alignItems: 'center', gap: 8 }}>
                            <Text style={{ fontSize: 24 }}>{s.icon}</Text>
                            <Text style={{ color: '#1A2230', fontSize: 16, fontWeight: 'bold' }}>{s.name}</Text>
                        </Box>
                        <Text style={{ color: '#4A5568', fontSize: 12, lineHeight: 1.5 }}>{s.desc}</Text>
                    </Box>
                ))}
            </Box>
        </Box>
        <Box style={{ width: '100%', flex: 1, gap: 10 }}>
            <Box style={{
                width: '100%', height: 88,
                borderRadius: 12,
                background: 'linear-gradient(90deg, #1E4FA8 0%, #2BC5C0 100%)',
                paddingLeft: 22, paddingRight: 22,
                flexDirection: 'row', alignItems: 'center',
                gap: 16,
            }}>
                <Box style={{
                    width: 48, height: 48, borderRadius: 24,
                    background: '#FFFFFF',
                    justifyContent: 'center', alignItems: 'center',
                }}>
                    <Text style={{ color: '#1E4FA8', fontSize: 22, fontWeight: 'bold' }}>↗</Text>
                </Box>
                <Box style={{ gap: 2, flex: 1 }}>
                    <Text style={{ color: '#FFC247', fontSize: 11, fontWeight: 'bold', letterSpacing: 2 }}>NEXT STEPS</Text>
                    <Text style={{ color: '#FFFFFF', fontSize: 16, lineHeight: 1.4 }}>
                        用 COUNTS 对 MLLM 进行 SFT，<span style={{ fontWeight: 'bold' }}>研究 SFT 阶段分布偏移的影响</span>——
                        本文尚未覆盖，但数据已就绪。
                    </Text>
                </Box>
            </Box>
            <Box style={{
                width: '100%', height: 70,
                borderRadius: 12,
                background: '#FFFFFF',
                border: '1.5px dashed #FFC247',
                paddingLeft: 22, paddingRight: 22,
                flexDirection: 'row', alignItems: 'center',
                gap: 16,
            }}>
                <Box style={{
                    paddingLeft: 10, paddingRight: 10,
                    paddingTop: 4, paddingBottom: 4,
                    borderRadius: 8, background: '#FFC247',
                }}>
                    <Text style={{ color: '#1A2230', fontSize: 11, fontWeight: 'bold', letterSpacing: 1 }}>TAKEAWAY</Text>
                </Box>
                <Text style={{ color: '#1A2230', fontSize: 14, lineHeight: 1.5, flex: 1 }}>
                    鲁棒视觉系统的下一步，不是堆更大模型，而是<span style={{ fontWeight: 'bold', color: '#1E4FA8' }}>对偏移本身给出可信评测与针对性缓解</span>。
                </Text>
            </Box>
        </Box>
    </Box>
    <Box style={{
        position: 'absolute', bottom: 0, left: 0, width: '100%', height: 32,
        background: '#F7F9FC',
        flexDirection: 'row', alignItems: 'center',
        justifyContent: 'space-between',
        paddingLeft: 40, paddingRight: 40,
        borderTop: '1px solid #E5E7EB',
    }}>
        <Text style={{ color: '#8B97A8', fontSize: 12 }}>COUNTS · 跨域目标检测与多模态 grounding</Text>
        <Text style={{ color: '#4A5568', fontSize: 12 }}>17 / 18</Text>
    </Box>
</Slide>
