<Slide padding={0}>
    <Box style={{
        width: '100%', height: 80,
        flexDirection: 'row', alignItems: 'center',
        paddingLeft: 40, paddingRight: 40,
        background: '#FFFFFF',
        borderBottom: '2px solid #F0F5FC',
    }}>
        <Box style={{ width: 40, height: 4, borderRadius: 2, background: '#FFC247', marginRight: 14 }} />
        <Text style={{ color: '#FFC247', fontSize: 14, fontWeight: 'bold', letterSpacing: 2 }}>CHAPTER 04 · O(OD)² 基准设计</Text>
        <Box style={{ flex: 1 }} />
        <Text style={{ color: '#8B97A8', fontSize: 13 }}>页 11 / 18</Text>
    </Box>
    <Box style={{
        width: '100%', height: 560,
        paddingLeft: 48, paddingRight: 48,
        paddingTop: 24, paddingBottom: 24,
        flexDirection: 'row', gap: 32,
    }}>
        <Box style={{ width: '32%', height: '100%', gap: 14, justifyContent: 'flex-start' }}>
            <Text style={{ color: '#FFC247', fontSize: 13, fontWeight: 'bold', letterSpacing: 3 }}>TARGET DOMAINS</Text>
            <Text style={{ color: '#1A2230', fontSize: 38, fontWeight: 'bold', lineHeight: 1.2 }}>
                6 个目标域<br />测出真本事
            </Text>
            <Box style={{ width: 60, height: 4, borderRadius: 2, background: '#FFC247' }} />
            <Text style={{ color: '#4A5568', fontSize: 14, lineHeight: 1.65 }}>
                训练时使用其他 8 个域，目标域完全不出现；这样才能测出模型对"未知域"的真实泛化能力。
            </Text>
            <Box style={{ gap: 8, marginTop: 8 }}>
                {[
                    { d: 'sky', n: 'sky' },
                    { d: 'occlusion', n: 'occlusion' },
                    { d: 'grass', n: 'grass' },
                    { d: 'water', n: 'water' },
                    { d: 'dim', n: 'dim' },
                    { d: 'handmake', n: 'handmake' },
                ].map((d, i) => (
                    <Box key={i} style={{
                        paddingLeft: 14, paddingRight: 14,
                        paddingTop: 8, paddingBottom: 8,
                        borderRadius: 10,
                        background: '#F0F5FC',
                        border: '1px solid #1E4FA8',
                    }}>
                        <Text style={{ color: '#1E4FA8', fontSize: 14, fontWeight: 600 }}>目标域 · {d.d}</Text>
                    </Box>
                ))}
            </Box>
        </Box>
        <Box style={{ width: '64%', height: '100%', gap: 14 }}>
            <Text style={{ color: '#1A2230', fontSize: 18, fontWeight: 'bold' }}>每个目标域对应一类独特偏移类型</Text>
            <Box style={{
                width: '100%', height: '100%',
                flexDirection: 'row', flexWrap: 'wrap',
                gap: 14,
            }}>
                {[
                    {
                        d: 'sky', type: '拍摄角度偏移',
                        desc: '天空背景下目标离相机较远或从低角度拍摄，带来光照与尺度变化。',
                        color: '#1E4FA8',
                    },
                    {
                        d: 'occlusion', type: '遮挡偏移',
                        desc: '目标部分或完全被遮挡（如人群中被他人遮挡），考验检测器推断能力。',
                        color: '#FF8A4C',
                    },
                    {
                        d: 'grass / water', type: '复杂背景纹理',
                        desc: '草地/水面引入复杂背景纹理与反射，容易让检测 head 误激活。',
                        color: '#2BC5C0',
                    },
                    {
                        d: 'dim', type: '低光照偏移',
                        desc: '黄昏/黎明/逆光下目标融合背景，纹理模糊，考验细节特征提取。',
                        color: '#5B7FCE',
                    },
                ].map((m, idx) => (
                    <Box key={idx} style={{
                        flexBasis: 'calc(50% - 7px)',
                        flexGrow: 1,
                        height: 'calc(50% - 8px)',
                        minWidth: 280,
                        borderRadius: 12,
                        background: '#FFFFFF',
                        border: `1.5px solid ${m.color}`,
                        paddingTop: 16, paddingBottom: 16,
                        paddingLeft: 20, paddingRight: 20,
                        gap: 8,
                    }}>
                        <Box style={{ flexDirection: 'row', alignItems: 'center', gap: 10 }}>
                            <Box style={{
                                paddingLeft: 10, paddingRight: 10,
                                paddingTop: 4, paddingBottom: 4,
                                borderRadius: 8, background: m.color,
                            }}>
                                <Text style={{ color: '#FFFFFF', fontSize: 11, fontWeight: 'bold', letterSpacing: 1 }}>{m.d.toUpperCase()}</Text>
                            </Box>
                            <Text style={{ color: '#1A2230', fontSize: 18, fontWeight: 'bold' }}>{m.type}</Text>
                        </Box>
                        <Text style={{ color: '#4A5568', fontSize: 13, lineHeight: 1.55 }}>{m.desc}</Text>
                    </Box>
                ))}
            </Box>
            <Box style={{
                width: '100%', borderRadius: 12,
                background: 'linear-gradient(135deg, #F0F5FC 0%, #E8EFF8 100%)',
                paddingLeft: 18, paddingRight: 18,
                paddingTop: 14, paddingBottom: 14,
                gap: 6,
            }}>
                <Text style={{ color: '#1E4FA8', fontSize: 12, fontWeight: 'bold', letterSpacing: 2 }}>DESIGN NOTE</Text>
                <Text style={{ color: '#1A2230', fontSize: 14, lineHeight: 1.55 }}>
                    在多目标域评估 + 完整训练集设置下，模型若仅在单域上看起来"不错"——不能代表真实部署能力。
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
        <Text style={{ color: '#4A5568', fontSize: 12 }}>11 / 18</Text>
    </Box>
</Slide>
