<Slide padding={0}>
    <Box style={{
        width: '100%', height: '100%',
        background: 'linear-gradient(135deg, #1E4FA8 0%, #5B7FCE 50%, #2BC5C0 100%)',
        flexDirection: 'row',
        paddingLeft: 56, paddingRight: 56,
        paddingTop: 56, paddingBottom: 56,
        gap: 40,
    }}>
        <Box style={{ width: '38%', height: '100%', gap: 18, justifyContent: 'center' }}>
            <Text style={{ color: '#FFC247', fontSize: 14, fontWeight: 'bold', letterSpacing: 4 }}>CHAPTER 03 · 数据集</Text>
            <Text style={{ color: '#FFFFFF', fontSize: 26, fontWeight: 'bold', lineHeight: 1.2, opacity: 0.85 }}>
                COUNTS
            </Text>
            <Text style={{
                color: '#FFFFFF', fontSize: 88,
                fontWeight: 'bold', lineHeight: 1,
            }}>
                三档核心<br />数据
            </Text>
            <Box style={{ width: 80, height: 4, borderRadius: 2, background: '#FFC247' }} />
            <Text style={{ color: '#FFFFFF', fontSize: 16, lineHeight: 1.5, opacity: 0.85 }}>
                Common Objects UNder disTribution Shifts<br />
                首个同时支持目标检测与 grounding 的<br />
                真实世界 OOD 细粒度数据集
            </Text>
        </Box>
        <Box style={{ width: '60%', height: '100%', gap: 22, justifyContent: 'center' }}>
            {[
                { num: '222,234', unit: '张', label: '真实世界图像', color: '#FFC247', icon: 'IMG' },
                { num: '1,196,114', unit: '个', label: '带标注边界框', color: '#FFFFFF', icon: 'BOX' },
                { num: '14', unit: '个', label: '分布域 · 真实场景', color: '#FF8A4C', icon: 'DOM' },
            ].map((kpi, idx) => (
                <Box key={idx} style={{
                    width: '100%',
                    height: 170,
                    borderRadius: 18,
                    background: 'rgba(255,255,255,0.12)',
                    border: '1.5px solid rgba(255,255,255,0.32)',
                    paddingLeft: 26, paddingRight: 26,
                    paddingTop: 22, paddingBottom: 22,
                    flexDirection: 'row',
                    alignItems: 'center',
                    gap: 24,
                }}>
                    <Box style={{
                        width: 100, height: 100,
                        borderRadius: 18,
                        background: kpi.color,
                        justifyContent: 'center', alignItems: 'center',
                    }}>
                        <Text style={{ color: '#1E4FA8', fontSize: 20, fontWeight: 'bold', letterSpacing: 2 }}>{kpi.icon}</Text>
                    </Box>
                    <Box style={{ flex: 1, gap: 4 }}>
                        <Box style={{ flexDirection: 'row', alignItems: 'baseline', gap: 6 }}>
                            <Text style={{ color: '#FFFFFF', fontSize: 64, fontWeight: 'bold', lineHeight: 1 }}>{kpi.num}</Text>
                            <Text style={{ color: '#FFFFFF', fontSize: 22, opacity: 0.7 }}>{kpi.unit}</Text>
                        </Box>
                        <Box style={{ width: 40, height: 2, borderRadius: 1, background: kpi.color, marginTop: 4, marginBottom: 4 }} />
                        <Text style={{ color: '#FFFFFF', fontSize: 16, opacity: 0.85, fontWeight: 500 }}>{kpi.label}</Text>
                    </Box>
                </Box>
            ))}
        </Box>
    </Box>
    <Box style={{
        position: 'absolute', bottom: 0, left: 0, width: '100%', height: 36,
        background: 'rgba(0,0,0,0.18)',
        flexDirection: 'row', alignItems: 'center',
        justifyContent: 'space-between',
        paddingLeft: 40, paddingRight: 40,
    }}>
        <Text style={{ color: '#FFFFFF', fontSize: 12, letterSpacing: 1, opacity: 0.7 }}>COUNTS · 数据集概览</Text>
        <Text style={{ color: '#FFFFFF', fontSize: 12, opacity: 0.7 }}>06 / 18</Text>
    </Box>
</Slide>
