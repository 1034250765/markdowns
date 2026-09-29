<Slide padding={0}>
    <Box style={{
        width: '100%', height: '100%',
        background: 'linear-gradient(135deg, #1A2230 0%, #1E4FA8 60%, #5B7FCE 100%)',
        paddingLeft: 56, paddingRight: 56,
        paddingTop: 56, paddingBottom: 56,
        flexDirection: 'row',
        gap: 32,
    }}>
        <Box style={{ width: '40%', height: '100%', justifyContent: 'center', gap: 16 }}>
            <Text style={{ color: '#FFC247', fontSize: 14, fontWeight: 'bold', letterSpacing: 4 }}>CHAPTER 04 · 基准与实验</Text>
            <Text style={{
                color: '#FFFFFF', fontSize: 28,
                fontWeight: 'bold', lineHeight: 1.2, opacity: 0.85,
            }}>
                一个数据集，
            </Text>
            <Text style={{
                color: '#FFFFFF', fontSize: 80,
                fontWeight: 'bold', lineHeight: 1.05,
            }}>
                两个基准
            </Text>
            <Box style={{ width: 80, height: 4, borderRadius: 2, background: '#FFC247' }} />
            <Text style={{ color: '#FFFFFF', fontSize: 16, lineHeight: 1.6, opacity: 0.85 }}>
                同时考察目标检测器和多模态大模型在 OOD 下的真实能力
            </Text>
        </Box>
        <Box style={{ width: '58%', height: '100%', flexDirection: 'row', gap: 24 }}>
            <Box style={{
                flex: 1, height: '100%',
                borderRadius: 20,
                background: 'rgba(255,255,255,0.1)',
                border: '2px solid rgba(255,255,255,0.32)',
                paddingTop: 28, paddingBottom: 28,
                paddingLeft: 24, paddingRight: 24,
                gap: 18, justifyContent: 'space-between',
            }}>
                <Box style={{ gap: 12 }}>
                    <Box style={{
                        paddingLeft: 12, paddingRight: 12,
                        paddingTop: 6, paddingBottom: 6,
                        borderRadius: 14,
                        background: '#FFC247',
                        alignSelf: 'flex-start',
                    }}>
                        <Text style={{ color: '#1A2230', fontSize: 13, fontWeight: 'bold', letterSpacing: 1 }}>DETECTOR BENCHMARK</Text>
                    </Box>
                    <Text style={{
                        color: '#FFFFFF', fontSize: 64,
                        fontWeight: 'bold', lineHeight: 1,
                    }}>O(OD)²</Text>
                    <Text style={{ color: '#FFFFFF', fontSize: 18, lineHeight: 1.5, opacity: 0.85 }}>
                        OOD in Object Detection<br />评估检测器在自然分布偏移下的目标检测能力
                    </Text>
                </Box>
                <Box style={{ gap: 8 }}>
                    {['6 个目标域', '覆盖多种偏移类型', '衡量 backbone / neck / head'].map((t, i) => (
                        <Box key={i} style={{ flexDirection: 'row', alignItems: 'center', gap: 10 }}>
                            <Box style={{ width: 8, height: 8, borderRadius: 4, background: '#FFC247' }} />
                            <Text style={{ color: '#FFFFFF', fontSize: 14, opacity: 0.85 }}>{t}</Text>
                        </Box>
                    ))}
                </Box>
            </Box>
            <Box style={{
                flex: 1, height: '100%',
                borderRadius: 20,
                background: 'rgba(255,255,255,0.1)',
                border: '2px solid rgba(255,255,255,0.32)',
                paddingTop: 28, paddingBottom: 28,
                paddingLeft: 24, paddingRight: 24,
                gap: 18, justifyContent: 'space-between',
            }}>
                <Box style={{ gap: 12 }}>
                    <Box style={{
                        paddingLeft: 12, paddingRight: 12,
                        paddingTop: 6, paddingBottom: 6,
                        borderRadius: 14,
                        background: '#2BC5C0',
                        alignSelf: 'flex-start',
                    }}>
                        <Text style={{ color: '#1A2230', fontSize: 13, fontWeight: 'bold', letterSpacing: 1 }}>MLLM BENCHMARK</Text>
                    </Box>
                    <Text style={{
                        color: '#FFFFFF', fontSize: 64,
                        fontWeight: 'bold', lineHeight: 1,
                    }}>OODG</Text>
                    <Text style={{ color: '#FFFFFF', fontSize: 18, lineHeight: 1.5, opacity: 0.85 }}>
                        OOD Grounding<br />评估 MLLM 在 ICL 偏移下的视觉 grounding 能力
                    </Text>
                </Box>
                <Box style={{ gap: 8 }}>
                    {['3 类任务', '5 种评测设置', '聚焦 ICL 分布偏移'].map((t, i) => (
                        <Box key={i} style={{ flexDirection: 'row', alignItems: 'center', gap: 10 }}>
                            <Box style={{ width: 8, height: 8, borderRadius: 4, background: '#2BC5C0' }} />
                            <Text style={{ color: '#FFFFFF', fontSize: 14, opacity: 0.85 }}>{t}</Text>
                        </Box>
                    ))}
                </Box>
            </Box>
        </Box>
    </Box>
    <Box style={{
        position: 'absolute', bottom: 0, left: 0, width: '100%', height: 36,
        background: 'rgba(0,0,0,0.25)',
        flexDirection: 'row', alignItems: 'center',
        justifyContent: 'space-between',
        paddingLeft: 40, paddingRight: 40,
    }}>
        <Text style={{ color: '#FFFFFF', fontSize: 12, letterSpacing: 1, opacity: 0.7 }}>COUNTS · 基准导览</Text>
        <Text style={{ color: '#FFFFFF', fontSize: 12, opacity: 0.7 }}>10 / 18</Text>
    </Box>
</Slide>
