<Slide padding={0}>
    <Box style={{
        width: '100%', height: 80,
        flexDirection: 'row', alignItems: 'center',
        paddingLeft: 40, paddingRight: 40,
        background: '#FFFFFF',
        borderBottom: '2px solid #F0F5FC',
    }}>
        <Box style={{ width: 40, height: 4, borderRadius: 2, background: '#FF8A4C', marginRight: 14 }} />
        <Text style={{ color: '#FF8A4C', fontSize: 14, fontWeight: 'bold', letterSpacing: 2 }}>CHAPTER 04 · ICL 双刃剑</Text>
        <Box style={{ flex: 1 }} />
        <Text style={{ color: '#8B97A8', fontSize: 13 }}>页 15 / 18</Text>
    </Box>
    <Box style={{
        width: '100%', height: 560,
        paddingLeft: 48, paddingRight: 48,
        paddingTop: 24, paddingBottom: 24,
        gap: 18,
    }}>
        <Box style={{ width: '100%', gap: 6 }}>
            <Text style={{ color: '#FF8A4C', fontSize: 13, fontWeight: 'bold', letterSpacing: 3 }}>COUNTERINTUITIVE FINDING</Text>
            <Text style={{ color: '#1A2230', fontSize: 28, fontWeight: 'bold', lineHeight: 1.3 }}>
                越会利用示例的模型，在分布偏移时跌得越狠。
            </Text>
            <Text style={{ color: '#4A5568', fontSize: 14, lineHeight: 1.6 }}>
                同分布下 Gemini 显著受益于 ICL，但协变量偏移中却因被带偏而严重降级——展示了 MLLM 知识提取的双面性。
            </Text>
        </Box>
        <Box style={{ width: '100%', flex: 1, flexDirection: 'row', gap: 18 }}>
            <Box style={{
                flex: 1, height: '100%',
                borderRadius: 16,
                background: 'linear-gradient(135deg, #1E4FA8 0%, #5B7FCE 100%)',
                paddingTop: 22, paddingBottom: 22,
                paddingLeft: 22, paddingRight: 22,
                gap: 14,
            }}>
                <Box style={{
                    paddingLeft: 12, paddingRight: 12,
                    paddingTop: 5, paddingBottom: 5,
                    borderRadius: 12, background: 'rgba(255,255,255,0.18)',
                    alignSelf: 'flex-start',
                }}>
                    <Text style={{ color: '#FFFFFF', fontSize: 11, fontWeight: 'bold', letterSpacing: 1 }}>GPT-4o · 稳健派</Text>
                </Box>
                <Text style={{ color: '#FFFFFF', fontSize: 36, fontWeight: 'bold', lineHeight: 1.2 }}>
                    表现稳定
                </Text>
                <Box style={{ gap: 10 }}>
                    <Box style={{ gap: 6 }}>
                        <Text style={{ color: '#FFC247', fontSize: 12, fontWeight: 'bold' }}>· IID 下提升小</Text>
                        <Text style={{ color: '#FFFFFF', fontSize: 13, lineHeight: 1.5, opacity: 0.95 }}>
                            从 IID ICL 看，GPT-4o 没有出现 Gemini 那种明显的"借力"提升。
                        </Text>
                    </Box>
                    <Box style={{ gap: 6 }}>
                        <Text style={{ color: '#FFC247', fontSize: 12, fontWeight: 'bold' }}>· 偏移下下降轻</Text>
                        <Text style={{ color: '#FFFFFF', fontSize: 13, lineHeight: 1.5, opacity: 0.95 }}>
                            协变量偏移下最大相对降幅仅 <span style={{ fontWeight: 'bold' }}>12.1%</span>。
                        </Text>
                    </Box>
                    <Box style={{ gap: 6 }}>
                        <Text style={{ color: '#FFC247', fontSize: 12, fontWeight: 'bold' }}>· 解读</Text>
                        <Text style={{ color: '#FFFFFF', fontSize: 13, lineHeight: 1.5, opacity: 0.95 }}>
                            GPT-4o 对 ICE 的依赖有限，更接近"看图说话"，不容易被示例带偏。
                        </Text>
                    </Box>
                </Box>
            </Box>
            <Box style={{
                flex: 1, height: '100%',
                borderRadius: 16,
                background: 'linear-gradient(135deg, #FF8A4C 0%, #FFC247 100%)',
                paddingTop: 22, paddingBottom: 22,
                paddingLeft: 22, paddingRight: 22,
                gap: 14,
            }}>
                <Box style={{
                    paddingLeft: 12, paddingRight: 12,
                    paddingTop: 5, paddingBottom: 5,
                    borderRadius: 12, background: 'rgba(255,255,255,0.25)',
                    alignSelf: 'flex-start',
                }}>
                    <Text style={{ color: '#FFFFFF', fontSize: 11, fontWeight: 'bold', letterSpacing: 1 }}>Gemini-1.5 · 易感派</Text>
                </Box>
                <Text style={{ color: '#FFFFFF', fontSize: 36, fontWeight: 'bold', lineHeight: 1.2 }}>
                    高敏感型
                </Text>
                <Box style={{ gap: 10 }}>
                    <Box style={{ gap: 6 }}>
                        <Text style={{ color: '#1A2230', fontSize: 12, fontWeight: 'bold' }}>· IID 下大幅提升</Text>
                        <Text style={{ color: '#FFFFFF', fontSize: 13, lineHeight: 1.5, opacity: 0.95 }}>
                            Zero-shot 59.1% → IID ICL+ 提升至 <span style={{ fontWeight: 'bold' }}>68.9%</span>。
                        </Text>
                    </Box>
                    <Box style={{ gap: 6 }}>
                        <Text style={{ color: '#1A2230', fontSize: 12, fontWeight: 'bold' }}>· 偏移下严重跌</Text>
                        <Text style={{ color: '#FFFFFF', fontSize: 13, lineHeight: 1.5, opacity: 0.95 }}>
                            协变量偏移下平均准确率从最高 57.0% 跌到 28.0%，相对下降 <span style={{ fontWeight: 'bold' }}>50.88%</span>。
                        </Text>
                    </Box>
                    <Box style={{ gap: 6 }}>
                        <Text style={{ color: '#1A2230', fontSize: 12, fontWeight: 'bold' }}>· 解读</Text>
                        <Text style={{ color: '#FFFFFF', fontSize: 13, lineHeight: 1.5, opacity: 0.95 }}>
                            Gemini 倾向于"重"用 ICE，一旦示例有偏，可能学到伪相关而产生严重误判。
                        </Text>
                    </Box>
                </Box>
            </Box>
        </Box>
        <Box style={{
            width: '100%', height: 60,
            borderRadius: 12,
            background: 'linear-gradient(90deg, #1A2230 0%, #2BC5C0 100%)',
            paddingLeft: 22, paddingRight: 22,
            flexDirection: 'row', alignItems: 'center',
            gap: 18,
        }}>
            <Box style={{
                width: 40, height: 40, borderRadius: 20,
                background: '#FFC247',
                justifyContent: 'center', alignItems: 'center',
            }}>
                <Text style={{ color: '#1A2230', fontSize: 18, fontWeight: 'bold' }}>!</Text>
            </Box>
            <Text style={{ color: '#FFFFFF', fontSize: 15, lineHeight: 1.5, flex: 1 }}>
                <span style={{ fontWeight: 'bold' }}>研究问题被打开：</span>
                MLLM 应当如何区分"事实信息"与 ICE 引入的"统计偏差"？何时该学 ICE，何时该无视 ICE？
            </Text>
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
        <Text style={{ color: '#4A5568', fontSize: 12 }}>15 / 18</Text>
    </Box>
</Slide>
