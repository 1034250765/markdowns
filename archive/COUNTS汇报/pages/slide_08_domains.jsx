<Slide padding={0}>
    <Box style={{
        width: '100%', height: 80,
        flexDirection: 'row', alignItems: 'center',
        paddingLeft: 40, paddingRight: 40,
        background: '#FFFFFF',
        borderBottom: '2px solid #F0F5FC',
    }}>
        <Box style={{ width: 40, height: 4, borderRadius: 2, background: '#2BC5C0', marginRight: 14 }} />
        <Text style={{ color: '#2BC5C0', fontSize: 14, fontWeight: 'bold', letterSpacing: 2 }}>CHAPTER 03 · 14 个自然分布域</Text>
        <Box style={{ flex: 1 }} />
        <Text style={{ color: '#8B97A8', fontSize: 13 }}>页 08 / 18</Text>
    </Box>
    <Box style={{
        width: '100%', height: 560,
        paddingLeft: 36, paddingRight: 36,
        paddingTop: 22, paddingBottom: 22,
        flexDirection: 'row', gap: 24,
    }}>
        <Box style={{ width: '58%', height: '100%' }}>
            <Box style={{
                width: '100%', height: '100%',
                borderRadius: 14,
                background: 'linear-gradient(135deg, #F7F9FC 0%, #FFFFFF 100%)',
                border: '1.5px solid #D6DCE5',
                paddingTop: 18, paddingBottom: 18,
                paddingLeft: 22, paddingRight: 22,
                gap: 12,
            }}>
                <Box style={{
                    width: '100%', flexDirection: 'row',
                    alignItems: 'center', justifyContent: 'space-between',
                }}>
                    <Text style={{ color: '#1E4FA8', fontSize: 14, fontWeight: 'bold', letterSpacing: 2 }}>DOMAIN BUBBLE · 样本量分布</Text>
                    <Box style={{
                        paddingLeft: 10, paddingRight: 10,
                        paddingTop: 4, paddingBottom: 4,
                        borderRadius: 8, background: '#F0F5FC',
                    }}>
                        <Text style={{ color: '#1E4FA8', fontSize: 11, fontWeight: 'bold' }}>14 DOMAINS</Text>
                    </Box>
                </Box>
                <svg width='100%' viewBox='0 0 1000 460' style={{ display: 'block', marginTop: 8 }}>
                    <defs>
                        <linearGradient id='g1' x1='0' y1='0' x2='1' y2='1'>
                            <stop offset='0' stopColor='#1E4FA8' />
                            <stop offset='1' stopColor='#5B7FCE' />
                        </linearGradient>
                        <linearGradient id='g2' x1='0' y1='0' x2='1' y2='1'>
                            <stop offset='0' stopColor='#FFC247' />
                            <stop offset='1' stopColor='#FF8A4C' />
                        </linearGradient>
                        <linearGradient id='g3' x1='0' y1='0' x2='1' y2='1'>
                            <stop offset='0' stopColor='#2BC5C0' />
                            <stop offset='1' stopColor='#3CC9A1' />
                        </linearGradient>
                    </defs>
                    <rect x='0' y='0' width='1000' height='460' fill='#F7F9FC' rx='10' />
                    <circle cx='320' cy='180' r='90' fill='url(#g1)' opacity='0.85' />
                    <text x='320' y='175' textAnchor='middle' fontSize='13' fontWeight='bold' fill='#fff'>indoor</text>
                    <text x='320' y='195' textAnchor='middle' fontSize='11' fill='#fff' opacity='0.95'>82,719</text>
                    <circle cx='540' cy='220' r='70' fill='url(#g1)' opacity='0.85' />
                    <text x='540' y='218' textAnchor='middle' fontSize='12' fontWeight='bold' fill='#fff'>tree</text>
                    <text x='540' y='234' textAnchor='middle' fontSize='10' fill='#fff' opacity='0.95'>45,573</text>
                    <circle cx='150' cy='240' r='58' fill='url(#g1)' opacity='0.85' />
                    <text x='150' y='238' textAnchor='middle' fontSize='11' fontWeight='bold' fill='#fff'>dim</text>
                    <text x='150' y='252' textAnchor='middle' fontSize='10' fill='#fff' opacity='0.95'>26,181</text>
                    <circle cx='710' cy='250' r='52' fill='url(#g1)' opacity='0.85' />
                    <text x='710' y='248' textAnchor='middle' fontSize='11' fontWeight='bold' fill='#fff'>street</text>
                    <text x='710' y='262' textAnchor='middle' fontSize='10' fill='#fff' opacity='0.95'>22,474</text>
                    <circle cx='260' cy='360' r='45' fill='url(#g2)' opacity='0.8' />
                    <text x='260' y='358' textAnchor='middle' fontSize='10' fontWeight='bold' fill='#fff'>sky</text>
                    <text x='260' y='372' textAnchor='middle' fontSize='9' fill='#fff' opacity='0.95'>16,771</text>
                    <circle cx='430' cy='380' r='42' fill='url(#g2)' opacity='0.8' />
                    <text x='430' y='378' textAnchor='middle' fontSize='10' fontWeight='bold' fill='#fff'>grass</text>
                    <text x='430' y='392' textAnchor='middle' fontSize='9' fill='#fff' opacity='0.95'>14,620</text>
                    <circle cx='600' cy='400' r='38' fill='url(#g2)' opacity='0.8' />
                    <text x='600' y='400' textAnchor='middle' fontSize='10' fontWeight='bold' fill='#fff'>road</text>
                    <text x='600' y='412' textAnchor='middle' fontSize='9' fill='#fff' opacity='0.95'>12,637</text>
                    <circle cx='820' cy='100' r='32' fill='url(#g3)' opacity='0.8' />
                    <text x='820' y='100' textAnchor='middle' fontSize='10' fontWeight='bold' fill='#fff'>water</text>
                    <text x='820' y='112' textAnchor='middle' fontSize='9' fill='#fff' opacity='0.95'>8,915</text>
                    <circle cx='90' cy='100' r='24' fill='url(#g3)' opacity='0.8' />
                    <text x='90' y='100' textAnchor='middle' fontSize='9' fontWeight='bold' fill='#fff'>painting</text>
                    <text x='90' y='112' textAnchor='middle' fontSize='8' fill='#fff' opacity='0.95'>4,167</text>
                    <circle cx='870' cy='180' r='22' fill='url(#g3)' opacity='0.8' />
                    <text x='870' y='180' textAnchor='middle' fontSize='9' fontWeight='bold' fill='#fff'>snow</text>
                    <text x='870' y='192' textAnchor='middle' fontSize='8' fill='#fff' opacity='0.95'>3,321</text>
                    <circle cx='130' cy='430' r='18' fill='url(#g3)' opacity='0.8' />
                    <text x='130' y='430' textAnchor='middle' fontSize='9' fontWeight='bold' fill='#fff'>handmade</text>
                    <text x='130' y='442' textAnchor='middle' fontSize='7' fill='#fff' opacity='0.95'>2,150</text>
                    <circle cx='700' cy='430' r='26' fill='url(#g3)' opacity='0.8' />
                    <text x='700' y='428' textAnchor='middle' fontSize='9' fontWeight='bold' fill='#fff'>occlusion</text>
                    <text x='700' y='442' textAnchor='middle' fontSize='8' fill='#fff' opacity='0.95'>4,215</text>
                    <circle cx='470' cy='80' r='18' fill='url(#g3)' opacity='0.8' />
                    <text x='470' y='80' textAnchor='middle' fontSize='9' fontWeight='bold' fill='#fff'>mountain</text>
                    <text x='470' y='92' textAnchor='middle' fontSize='7' fill='#fff' opacity='0.95'>1,452</text>
                    <circle cx='920' cy='320' r='14' fill='url(#g3)' opacity='0.8' />
                    <text x='920' y='320' textAnchor='middle' fontSize='8' fontWeight='bold' fill='#fff'>sand</text>
                    <rect x='40' y='14' width='220' height='70' rx='6' fill='#FFFFFF' stroke='#1E4FA8' />
                    <text x='50' y='34' fontSize='11' fontWeight='bold' fill='#1A2230'>域分布统计</text>
                    <circle cx='58' cy='52' r='5' fill='url(#g1)' />
                    <text x='68' y='55' fontSize='10' fill='#4A5568'>≥ 20k 大域</text>
                    <circle cx='128' cy='52' r='5' fill='url(#g2)' />
                    <text x='138' y='55' fontSize='10' fill='#4A5568'>10-20k 中域</text>
                    <circle cx='208' cy='52' r='5' fill='url(#g3)' />
                    <text x='218' y='55' fontSize='10' fill='#4A5568'>&lt; 10k 小域</text>
                    <text x='50' y='74' fontSize='9' fill='#8B97A8'>气泡面积 ∝ 样本数</text>
                </svg>
            </Box>
        </Box>
        <Box style={{ width: '40%', height: '100%', gap: 14 }}>
            <Text style={{ color: '#8B97A8', fontSize: 12, fontWeight: 'bold', letterSpacing: 3 }}>INTERPRETATION</Text>
            <Text style={{ color: '#1A2230', fontSize: 28, fontWeight: 'bold', lineHeight: 1.25 }}>
                14 个域覆盖日常视觉变化
            </Text>
            <Text style={{ color: '#4A5568', fontSize: 15, lineHeight: 1.65 }}>
                域标签是图像级属性，边界框是目标级标注——目标通常位于前景，
                域体现为背景或整体图像属性。这种"前景-背景"解耦，
                让不同域对同一图像的不同区域产生不同影响。
            </Text>
            <Box style={{
                width: '100%', borderRadius: 12,
                background: '#F0F5FC',
                paddingLeft: 18, paddingRight: 18,
                paddingTop: 14, paddingBottom: 14,
                gap: 10,
            }}>
                <Text style={{ color: '#1E4FA8', fontSize: 13, fontWeight: 'bold', letterSpacing: 1 }}>域类型分组</Text>
                <Box style={{ width: '100%', gap: 6 }}>
                    {[
                        { group: '环境', tag: 'snow/sand/grass/water/road/street/tree', color: '#1E4FA8' },
                        { group: '光照与遮挡', tag: 'dim/occlusion', color: '#FF8A4C' },
                        { group: '风格化', tag: 'painting/handmade', color: '#2BC5C0' },
                        { group: '特殊场景', tag: 'indoor/mountain/sky', color: '#FFC247' },
                    ].map((row, idx) => (
                        <Box key={idx} style={{
                            width: '100%',
                            flexDirection: 'row', alignItems: 'center',
                            gap: 12,
                            paddingTop: 6, paddingBottom: 6,
                        }}>
                            <Box style={{
                                width: 60,
                                paddingLeft: 8, paddingRight: 8,
                                paddingTop: 4, paddingBottom: 4,
                                borderRadius: 6, background: row.color,
                            }}>
                                <Text style={{ color: '#FFFFFF', fontSize: 11, fontWeight: 'bold' }}>{row.group}</Text>
                            </Box>
                            <Text style={{ color: '#1A2230', fontSize: 13 }}>{row.tag}</Text>
                        </Box>
                    ))}
                </Box>
            </Box>
            <Box style={{
                width: '100%', borderRadius: 12,
                paddingLeft: 18, paddingRight: 18,
                paddingTop: 14, paddingBottom: 14,
                gap: 6,
                background: '#FFFFFF',
                border: '1.5px solid #FFC247',
            }}>
                <Text style={{ color: '#FFC247', fontSize: 12, fontWeight: 'bold', letterSpacing: 2 }}>EXCLUSION RULE</Text>
                <Text style={{ color: '#1A2230', fontSize: 14, lineHeight: 1.5 }}>
                    选择原则：常见于日常视觉经验、影响像素分布、域间尽量独立。
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
        <Text style={{ color: '#4A5568', fontSize: 12 }}>08 / 18</Text>
    </Box>
</Slide>
