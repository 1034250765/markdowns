<Slide padding={0}>
    <Box style={{
        width: '100%', height: '100%',
        background: 'linear-gradient(135deg, #1E4FA8 0%, #5B7FCE 60%, #2BC5C0 100%)',
        justifyContent: 'center',
        alignItems: 'center',
        paddingTop: 60, paddingBottom: 60,
        paddingLeft: 60, paddingRight: 60,
    }}>
        <Box style={{
            width: '100%', maxWidth: 880,
            gap: 24,
            alignItems: 'center',
        }}>
            <Box style={{
                width: 88, height: 88, borderRadius: 44,
                background: 'rgba(255,255,255,0.2)',
                border: '2px solid rgba(255,255,255,0.5)',
                justifyContent: 'center', alignItems: 'center',
            }}>
                <Text style={{ color: '#FFFFFF', fontSize: 36, fontWeight: 'bold' }}>?</Text>
            </Box>
            <Text style={{ color: '#FFFFFF', fontSize: 22, opacity: 0.85, letterSpacing: 4 }}>Q & A</Text>
            <Text style={{
                color: '#FFFFFF', fontSize: 88,
                fontWeight: 'bold', textAlign: 'center',
                lineHeight: 1.1,
            }}>
                感谢聆听
            </Text>
            <Text style={{
                color: '#FFFFFF', fontSize: 18,
                textAlign: 'center',
                opacity: 0.9, lineHeight: 1.6, maxWidth: 600,
            }}>
                欢迎讨论：在你自己的下游任务里，COUNTS 是否能帮你评估 OOD 风险？
            </Text>
            <Box style={{ width: 100, height: 4, borderRadius: 2, background: '#FFC247' }} />
            <Box style={{
                width: '100%',
                paddingTop: 22, paddingBottom: 22,
                paddingLeft: 30, paddingRight: 30,
                borderRadius: 16,
                background: 'rgba(255,255,255,0.12)',
                border: '1.5px solid rgba(255,255,255,0.32)',
                gap: 12,
            }}>
                <Text style={{ color: '#FFC247', fontSize: 12, fontWeight: 'bold', letterSpacing: 3, textAlign: 'center' }}>RESOURCES</Text>
                <Box style={{ flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between', gap: 20 }}>
                    <Box style={{ gap: 4 }}>
                        <Text style={{ color: '#FFFFFF', fontSize: 11, opacity: 0.7, letterSpacing: 2 }}>PAPER</Text>
                        <Text style={{ color: '#FFFFFF', fontSize: 16, fontWeight: 'bold' }}>arXiv:2504.10158</Text>
                    </Box>
                    <Box style={{ width: 1, height: 36, background: 'rgba(255,255,255,0.3)' }} />
                    <Box style={{ gap: 4 }}>
                        <Text style={{ color: '#FFFFFF', fontSize: 11, opacity: 0.7, letterSpacing: 2 }}>CODE</Text>
                        <Text style={{ color: '#FFFFFF', fontSize: 14, fontWeight: 600 }}>github.com/jiansheng-li/<br />COUNTS_benchmark</Text>
                    </Box>
                    <Box style={{ width: 1, height: 36, background: 'rgba(255,255,255,0.3)' }} />
                    <Box style={{ gap: 4 }}>
                        <Text style={{ color: '#FFFFFF', fontSize: 11, opacity: 0.7, letterSpacing: 2 }}>DATASET</Text>
                        <Text style={{ color: '#FFFFFF', fontSize: 14, fontWeight: 600 }}>huggingface.co/<br />jianshengli/COUNTS</Text>
                    </Box>
                </Box>
            </Box>
            <Text style={{ color: '#FFFFFF', fontSize: 14, textAlign: 'center', opacity: 0.7, marginTop: 16 }}>
                论文作者：Jiansheng Li, Xingxuan Zhang, Hao Zou 等 · 清华大学计算机科学系
            </Text>
        </Box>
    </Box>
    <Box style={{
        position: 'absolute', bottom: 0, left: 0, width: '100%', height: 36,
        background: 'rgba(0,0,0,0.2)',
        flexDirection: 'row', alignItems: 'center',
        justifyContent: 'space-between',
        paddingLeft: 40, paddingRight: 40,
    }}>
        <Text style={{ color: '#FFFFFF', fontSize: 12, letterSpacing: 1, opacity: 0.7 }}>COUNTS · 论文汇报 · 结束</Text>
        <Text style={{ color: '#FFFFFF', fontSize: 12, opacity: 0.7 }}>18 / 18</Text>
    </Box>
</Slide>
