<Slide padding={0}>
    <Box style={{
        width: '100%',
        height: 80,
        flexDirection: 'row',
        alignItems: 'center',
        paddingLeft: 40,
        paddingRight: 40,
        background: '#FFFFFF',
        borderBottom: '2px solid #F0F5FC',
    }}>
        <Box style={{
            width: 40,
            height: 4,
            borderRadius: 2,
            background: '#1E4FA8',
            marginRight: 14,
        }} />
        <Text style={{ color: '#1E4FA8', fontSize: 14, fontWeight: 'bold', letterSpacing: 2 }}>CHAPTER 01 · 研究动机</Text>
        <Box style={{ flex: 1 }} />
        <Text style={{ color: '#8B97A8', fontSize: 13 }}>页 03 / 18</Text>
    </Box>
    <Box style={{
        width: '100%',
        height: 560,
        paddingLeft: 48,
        paddingRight: 48,
        paddingTop: 32,
        paddingBottom: 32,
        flexDirection: 'row',
        gap: 36,
    }}>
        <Box style={{ width: '44%', height: '100%', gap: 18, justifyContent: 'center' }}>
            <Box style={{
                width: 80,
                height: 80,
                borderRadius: 40,
                background: 'linear-gradient(135deg, #1E4FA8 0%, #5B7FCE 100%)',
                justifyContent: 'center',
                alignItems: 'center',
            }}>
                <Text style={{ color: '#FFFFFF', fontSize: 32, fontWeight: 'bold' }}>!</Text>
            </Box>
            <Text style={{
                color: '#1A2230',
                fontSize: 56,
                fontWeight: 'bold',
                lineHeight: 1.15,
            }}>
                IID 强，不等于<br />OOD 也强。
            </Text>
            <Box style={{
                width: 80,
                height: 4,
                borderRadius: 2,
                background: '#FFC247',
                marginTop: 8,
            }} />
            <Text style={{ color: '#4A5568', fontSize: 18, lineHeight: 1.6 }}>
                检测器与多模态大模型在真实部署中遭遇分布偏移时，能力会显著下降；
                但目前缺少系统评测这一痛点的细粒度基准。
            </Text>
        </Box>
        <Box style={{ width: '52%', height: '100%', gap: 18 }}>
            <Box style={{
                width: '100%',
                height: 240,
                borderRadius: 16,
                background: 'linear-gradient(135deg, #F0F5FC 0%, #E8EFF8 100%)',
                border: '1.5px solid #D6DCE5',
                paddingTop: 22,
                paddingBottom: 22,
                paddingLeft: 26,
                paddingRight: 26,
                gap: 18,
                justifyContent: 'center',
            }}>
                <Text style={{ color: '#1E4FA8', fontSize: 14, fontWeight: 'bold', letterSpacing: 2 }}>L1 · 核心数据</Text>
                <Box style={{ flexDirection: 'row', alignItems: 'flex-end', gap: 36 }}>
                    <Box style={{ gap: 4 }}>
                        <Text style={{ color: '#1E4FA8', fontSize: 80, fontWeight: 'bold', lineHeight: 1 }}>70<span style={{ fontSize: 36 }}>%</span></Text>
                        <Text style={{ color: '#4A5568', fontSize: 14 }}>检测器遇到域偏移时<br />的 mAP 跌幅</Text>
                    </Box>
                    <Box style={{ width: 1, height: 90, background: '#D6DCE5' }} />
                    <Box style={{ gap: 4 }}>
                        <Text style={{ color: '#FF8A4C', fontSize: 80, fontWeight: 'bold', lineHeight: 1 }}>−50<span style={{ fontSize: 36 }}>%</span></Text>
                        <Text style={{ color: '#4A5568', fontSize: 14 }}>MLLM 在 ICL 协变量<br />偏移下的相对下降</Text>
                    </Box>
                </Box>
            </Box>
            <Box style={{
                width: '100%',
                height: 220,
                borderRadius: 16,
                paddingTop: 22,
                paddingBottom: 22,
                paddingLeft: 26,
                paddingRight: 26,
                background: '#FFFFFF',
                border: '1.5px solid #FFC247',
                gap: 10,
            }}>
                <Text style={{ color: '#FFC247', fontSize: 14, fontWeight: 'bold', letterSpacing: 2 }}>L2 · 提出问题</Text>
                <Text style={{ color: '#1A2230', fontSize: 24, fontWeight: 'bold', lineHeight: 1.4 }}>
                    我们能否系统评测
                </Text>
                <Text style={{ color: '#1A2230', fontSize: 24, fontWeight: 'bold', lineHeight: 1.4 }}>
                    目标检测 + MLLM grounding
                </Text>
                <Text style={{ color: '#1A2230', fontSize: 24, fontWeight: 'bold', lineHeight: 1.4 }}>
                    在自然分布偏移下的 OOD 泛化？
                </Text>
                <Box style={{ height: 1, background: '#E5E7EB', marginTop: 8, marginBottom: 4 }} />
                <Text style={{ color: '#4A5568', fontSize: 14, lineHeight: 1.5 }}>
                    本文给出肯定答案——COUNTS 数据集 + O(OD)² + OODG 三个工具同时回应这个问题。
                </Text>
            </Box>
        </Box>
    </Box>
    <Box style={{
        position: 'absolute',
        bottom: 0,
        left: 0,
        width: '100%',
        height: 32,
        background: '#F7F9FC',
        flexDirection: 'row',
        alignItems: 'center',
        justifyContent: 'space-between',
        paddingLeft: 40,
        paddingRight: 40,
        borderTop: '1px solid #E5E7EB',
    }}>
        <Text style={{ color: '#8B97A8', fontSize: 12 }}>COUNTS · 跨域目标检测与多模态 grounding</Text>
        <Text style={{ color: '#4A5568', fontSize: 12 }}>03 / 18</Text>
    </Box>
</Slide>
