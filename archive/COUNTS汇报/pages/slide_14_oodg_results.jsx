<Slide padding={0}>
    <Box style={{
        width: '100%', height: 80,
        flexDirection: 'row', alignItems: 'center',
        paddingLeft: 40, paddingRight: 40,
        background: '#FFFFFF',
        borderBottom: '2px solid #F0F5FC',
    }}>
        <Box style={{ width: 40, height: 4, borderRadius: 2, background: '#2BC5C0', marginRight: 14 }} />
        <Text style={{ color: '#2BC5C0', fontSize: 14, fontWeight: 'bold', letterSpacing: 2 }}>CHAPTER 04 · OODG 实验结果</Text>
        <Box style={{ flex: 1 }} />
        <Text style={{ color: '#8B97A8', fontSize: 13 }}>页 14 / 18</Text>
    </Box>
    <Box style={{
        width: '100%', height: 560,
        paddingLeft: 40, paddingRight: 40,
        paddingTop: 22, paddingBottom: 22,
        flexDirection: 'row', gap: 22,
    }}>
        <Box style={{ width: '58%', height: '100%' }}>
            <Box style={{
                width: '100%', height: '100%',
                borderRadius: 14,
                border: '1.5px solid #D6DCE5',
                background: '#FFFFFF',
                paddingTop: 18, paddingBottom: 18,
                paddingLeft: 18, paddingRight: 18,
                gap: 8,
            }}>
                <Box style={{ flexDirection: 'row', justifyContent: 'space-between', alignItems: 'baseline' }}>
                    <Box style={{ gap: 2 }}>
                        <Text style={{ color: '#1E4FA8', fontSize: 12, fontWeight: 'bold', letterSpacing: 2 }}>TABLE 4 · VISUAL GROUNDING</Text>
                        <Text style={{ color: '#1A2230', fontSize: 18, fontWeight: 'bold' }}>不同 ICL 设置下的 grounding 准确率</Text>
                    </Box>
                    <Box style={{ flexDirection: 'row', gap: 14 }}>
                        <Box style={{ flexDirection: 'row', alignItems: 'center', gap: 6 }}>
                            <Box style={{ width: 12, height: 12, borderRadius: 2, background: '#1E4FA8' }} />
                            <Text style={{ color: '#4A5568', fontSize: 12 }}>GPT-4o</Text>
                        </Box>
                        <Box style={{ flexDirection: 'row', alignItems: 'center', gap: 6 }}>
                            <Box style={{ width: 12, height: 12, borderRadius: 2, background: '#FF8A4C' }} />
                            <Text style={{ color: '#4A5568', fontSize: 12 }}>Gemini-1.5</Text>
                        </Box>
                    </Box>
                </Box>
                <Chart
                    style={{ width: '100%', flex: 1, minHeight: 280 }}
                    chartType='lineChart'
                    grouping='standard'
                    background='#FFFFFF'
                    colors={['#1E4FA8', '#FF8A4C']}
                    titleColor='#1A2230'
                    legendColor='#8B97A8'
                    axisColor='#8B97A8'
                    data={[
                        ['ICL Setting', 'GPT-4o', 'Gemini-1.5'],
                        ['Zero-shot', 0.659, 0.591],
                        ['IID ICL', 0.668, 0.670],
                        ['IID ICL+', 0.675, 0.689],
                        ['Covariate', 0.580, 0.358],
                        ['Covariate+', 0.612, 0.346],
                        ['Label', 0.605, 0.317],
                        ['Label+', 0.591, 0.297],
                    ]}
                />
            </Box>
        </Box>
        <Box style={{ width: '40%', height: '100%', gap: 12 }}>
            <Box style={{
                width: '100%',
                borderRadius: 12,
                background: 'linear-gradient(135deg, #1E4FA8 0%, #5B7FCE 100%)',
                paddingTop: 16, paddingBottom: 16,
                paddingLeft: 18, paddingRight: 18,
                gap: 10,
            }}>
                <Text style={{ color: '#FFC247', fontSize: 11, fontWeight: 'bold', letterSpacing: 2 }}>ZERO-SHOT BASELINE</Text>
                <Box style={{ flexDirection: 'row', gap: 22 }}>
                    <Box>
                        <Text style={{ color: '#FFFFFF', fontSize: 32, fontWeight: 'bold', lineHeight: 1 }}>65.9%</Text>
                        <Text style={{ color: '#FFFFFF', fontSize: 12, opacity: 0.85 }}>GPT-4o</Text>
                    </Box>
                    <Box style={{ width: 1, background: 'rgba(255,255,255,0.4)' }} />
                    <Box>
                        <Text style={{ color: '#FFFFFF', fontSize: 32, fontWeight: 'bold', lineHeight: 1 }}>59.1%</Text>
                        <Text style={{ color: '#FFFFFF', fontSize: 12, opacity: 0.85 }}>Gemini-1.5</Text>
                    </Box>
                    <Box style={{ width: 1, background: 'rgba(255,255,255,0.4)' }} />
                    <Box>
                        <Text style={{ color: '#FFFFFF', fontSize: 32, fontWeight: 'bold', lineHeight: 1 }}>62.5%</Text>
                        <Text style={{ color: '#FFFFFF', fontSize: 12, opacity: 0.85 }}>GLaMM</Text>
                    </Box>
                </Box>
            </Box>
            <Box style={{
                width: '100%',
                borderRadius: 12,
                background: 'linear-gradient(135deg, #FF8A4C 0%, #FFC247 100%)',
                paddingTop: 14, paddingBottom: 14,
                paddingLeft: 18, paddingRight: 18,
                gap: 6,
            }}>
                <Text style={{ color: '#FFFFFF', fontSize: 11, fontWeight: 'bold', letterSpacing: 2 }}>GEMINI 协变量偏移</Text>
                <Box style={{ flexDirection: 'row', alignItems: 'baseline', gap: 8 }}>
                    <Text style={{ color: '#FFFFFF', fontSize: 32, fontWeight: 'bold' }}>57.0%</Text>
                    <Text style={{ color: '#FFFFFF', fontSize: 20 }}>→</Text>
                    <Text style={{ color: '#FFFFFF', fontSize: 32, fontWeight: 'bold' }}>28.0%</Text>
                </Box>
                <Text style={{ color: '#FFFFFF', fontSize: 13, lineHeight: 1.5, opacity: 0.95 }}>
                    相对下降 <span style={{ fontWeight: 'bold' }}>50.88%</span>，比 GPT-4o 的 12.1% 严重得多。
                </Text>
            </Box>
            <Box style={{
                width: '100%',
                flex: 1,
                borderRadius: 12,
                background: '#FFFFFF',
                border: '1.5px solid #1E4FA8',
                paddingTop: 14, paddingBottom: 14,
                paddingLeft: 16, paddingRight: 16,
                gap: 8,
            }}>
                <Text style={{ color: '#1E4FA8', fontSize: 11, fontWeight: 'bold', letterSpacing: 2 }}>RECOGNITION & LOCALIZATION · TABLE 5</Text>
                <Text style={{ color: '#1A2230', fontSize: 13, lineHeight: 1.55 }}>
                    整体 mAP 很低：Zero-shot GPT-4o = <span style={{ fontWeight: 'bold', color: '#1E4FA8' }}>0.106</span>，
                    Gemini-1.5 = 0.082；<span style={{ fontWeight: 'bold', color: '#FF8A4C' }}>协变量偏移下 Gemini 整体 mAP 跌至 0.000</span>。
                </Text>
                <Text style={{ color: '#4A5568', fontSize: 12, lineHeight: 1.5 }}>
                    说明当前 MLLM 在精确坐标定位上远未成熟。
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
        <Text style={{ color: '#4A5568', fontSize: 12 }}>14 / 18</Text>
    </Box>
</Slide>
