# -*- coding: utf-8 -*-
"""Original, accessible HTML figures and a synthetic map; no map tiles copied."""
from diagram_core import node,arrow,flow,frame
from catalog import SOURCES

def synthetic_map(lang,candidate='A'):
    t=lambda en,zh:zh if lang=='zh' else en
    # A is a fit; B moves the building to the other bank; C removes the junction.
    west=candidate=='B'
    bx=85 if west else 205
    junction=candidate!='C'
    ident='synthetic-'+candidate
    return f'''<svg class="scene-map" viewBox="0 0 360 270" role="img" aria-labelledby="{ident}-title {ident}-desc"><title id="{ident}-title">{t('Synthetic candidate','合成候选')} {candidate}</title><desc id="{ident}-desc">{t('River runs north–south, road crosses east–west.','河流南北向，道路东西向跨河。')} {t('Building west of river' if west else 'Building east of river','建筑在河西' if west else '建筑在河东')} · {t('T-junction east of bridge' if junction else 'No eastern T-junction','桥东有丁字路口' if junction else '东侧无丁字路口')}</desc><rect width="360" height="270" rx="10" fill="#edf0e4"/><path d="M158 0 C130 60 172 130 155 270 L195 270 C212 120 173 65 196 0Z" fill="#98c4d4"/><path d="M0 150H360" stroke="#aeb5ae" stroke-width="24"/><path d="M0 150H360" stroke="#fffaf2" stroke-width="15"/><rect x="146" y="138" width="57" height="24" fill="#737e85"/><path d="M146 150H203" stroke="#fffaf2" stroke-width="15"/>{'<path d="M285 150V265" stroke="#aeb5ae" stroke-width="24"/><path d="M285 150V265" stroke="#fffaf2" stroke-width="15"/>' if junction else ''}<rect x="{bx}" y="48" width="58" height="53" rx="3" fill="#b57255" stroke="#8c563b" stroke-width="2"/><path d="M15 245L130 228" stroke="#495d51" stroke-width="4" stroke-dasharray="9 4"/><circle cx="70" cy="170" r="7" fill="#26384c"/><path d="M78 167L{bx+25} 111" stroke="#26384c" stroke-width="2" stroke-dasharray="5 4"/><text x="18" y="25" fill="#26384c" font-size="13" font-family="sans-serif">{t('CANDIDATE','候选')} {candidate}</text><path d="M325 60V25M319 34L325 25L331 34" stroke="#26384c" stroke-width="2" fill="none"/><text x="320" y="18" fill="#26384c" font-size="12">N</text><text x="{bx-4}" y="42" fill="#684530" font-size="12" font-family="sans-serif">{t('Building','建筑')}</text><text x="120" y="184" fill="#26384c" font-size="12" font-family="sans-serif">{t('Bridge','桥')}</text><text x="18" y="204" fill="#26384c" font-size="12" font-family="sans-serif">{t('Camera region','相机区域')}</text></svg>'''

def diagram(ident,lang):
    t=lambda en,zh:zh if lang=='zh' else en
    datasets={
    'cycle':('Question → evidence → judgment','问题 → 证据 → 判断','berkeley',[
        ('Question','问题','What needs answering?','需要回答什么？'),('Collect','采集','Bounded, traceable inputs','有范围、可溯源输入'),('Verify','核验','Source, scene and alternatives','来源、场景及替代解释'),('Analyze','分析','Claim-specific support','逐项主张依据'),('Report ↺','报告 ↺','Answer, gaps and next checks','答案、缺口及下一项核验')]),
    'lineage':('Three publishers, two observation roots','三个发布者，两个观察根','berkeley',[
        ('Camera X','相机 X','Original image → publisher A → repost B','原图 → 发布者 A → 转发 B'),('Camera Y','相机 Y','Different ground view → publisher C','不同地面视图 → 发布者 C'),('Count roots','统计根来源','A + B = one observation; C may independently support geometry','A + B 为一次观察；C 可独立支持几何')]),
    'media':('Original media and derived artifacts','原始媒体与衍生产物','invid',[
        ('Original file','原件','Source ID, bytes and acquisition time','来源编号、字节及采集时间'),('Frame extraction','提取关键帧','Frame timecodes and parameters','帧时间码及参数'),('Inspection copy','检查副本','Crop / OCR / panorama with provenance','有溯源裁剪 / OCR / 全景'),('Claim check','检验主张','Return to original context','回到原始上下文')]),
    'entities':('Different infrastructure layers','不同基础设施层次','ct',[
        ('Registration','注册信息','Public fields at lookup time','查询时的公开字段'),('DNS','DNS','Observed resolution, not ownership','观察到的解析，不等于所有权'),('Certificate','证书','Logged names, not current service','记录名称，不等于当前服务')]),
    'evidence':('An auditable evidence chain','可审计证据链','webrecorder',[
        ('Acquire','获取','URL + time + original bytes','URL + 时间 + 原始字节'),('Preserve','保存','Hash + context + archive','哈希 + 上下文 + 归档'),('Derive','衍生','New copy + transformation log','新副本 + 转换日志'),('Cite','引用','Claim → evidence ID → original','主张 → 证据编号 → 原件')]),
    'geo':('Narrow, compare, challenge','缩小、比较、质疑','osm-search',[
        ('Observe','观察','Roads, water, text, terrain','道路、水体、文字、地形'),('Bound','限定','Region is a hypothesis','区域是待检验假设'),('Candidates','候选','Rare feature combinations','稀有要素组合'),('Cross-check','交叉核验','Ground + overhead + dates','地面 + 俯视 + 日期'),('Report','报告','Point, segment or unresolved area','点、区间或未解决区域')]),
    'maps':('Three views, three different checks','三种视图，三类检查','streetview',[
        ('Labeled map','标注地图','Name / route / context','名称 / 路线 / 上下文'),('Overhead imagery','俯视影像','Footprints / water / topology','轮廓 / 水体 / 拓扑'),('Ground view','地面视图','Facade / signs / occlusion','立面 / 标牌 / 遮挡')]),
    'imagery':('Sensor scale limits the answer','传感器尺度限制答案','sentinel',[
        ('Broad scene','大范围场景','Smoke / flood / land cover','烟雾 / 洪水 / 地表覆盖'),('Large structures','大型结构','Use a suitable pixel size and clear date','需适用像元大小与清晰日期'),('Small text / identity','小文字 / 身份','Not established by Sentinel-2 pixels','Sentinel-2 像元不能确定')]),
    'terrain':('A camera sees angular order and occlusion','相机看到角度顺序与遮挡','dem',[
        ('Viewpoint','视点','Position + elevation + direction','位置 + 高程 + 朝向'),('Near ridge','近山脊','Can hide a higher distant peak','可能挡住更远高峰'),('Far skyline','远天际线','Compare saddles and peak order','比较鞍部与山峰顺序')]),
    'time':('Four timestamps that should stay separate','应分别记录的四类时间','archive',[
        ('Scene','场景','Capture or event time: may be unknown','拍摄或事件时间：可能未知'),('Publish','发布','A served copy becomes available','某份副本被提供'),('Archive','归档','An archive captures a response','归档采集响应'),('Retrieve','检索','Your research acquisition time','研究者采集时间')]),
    'coordinates':('Same location, different data contracts','同一地点，不同数据约定','geojson',[
        ('Map search','地图搜索','Often lat, lon · check interface','通常纬度、经度 · 核对界面'),('GeoJSON','GeoJSON','lon, lat · degrees','经度、纬度 · 度'),('Projected layer','投影图层','x, y · CRS-specific units','x、y · 取决于 CRS 的单位'),('Provider map','服务地图','Keep GCJ-02 / BD-09 labels explicit','明确 GCJ-02 / BD-09 标签')]),
    'analysis':('One scene, three competing explanations','一个场景，三个竞争解释','guides',[
        ('Candidate A','候选 A','Topology fits; ground check remains','拓扑吻合；仍需地面核验'),('Candidate B','候选 B','Building on the wrong riverbank','建筑在错误河岸'),('Candidate C','候选 C','Required junction is missing','必要路口不存在')]),
    'ai':('A lead needs an external evidence check','线索需要外部证据核验','berkeley',[
        ('Model proposal','模型建议','Candidate / OCR / query variant','候选 / OCR / 查询变体'),('Source inspection','来源检查','Original image and actual page','原始图与实际页面'),('Physical test','物理检验','Geometry, date and alternatives','几何、日期及替代解释'),('Human report','人工报告','Accepted observations + visible uncertainty','接受的观察 + 明确不确定性')])}
    if ident=='clues':
        return frame(lang,'viz-clues',t('Sketch relationships before searching','检索前先画空间关系'),synthetic_map(lang),t('Original synthetic map, not a real location. River runs north–south; the building is east of it, and a T-junction lies east of the bridge. Use these relations together.','原创合成地图，非真实地点。河流南北向，建筑在河东，丁字路口在桥东；应组合使用这些关系。'),SOURCES['osm-search'][2],'Bellingcat OSM Search')
    en,zh,ref,items=datasets[ident]
    mode='compare' if ident in ('lineage','entities','maps','imagery','analysis','coordinates') else 'flow'
    if mode=='compare':body='<div class="viz-three">'+''.join(node(t(a,b),t(c,d),'neutral') for a,b,c,d in items)+'</div>'
    else:
        parts=[]
        for i,(a,b,c,d) in enumerate(items):
            if i:parts.append(arrow())
            parts.append(node(t(a,b),t(c,d),'protected' if i==len(items)-1 else 'neutral'))
        body=flow(parts)
    caption=t('Original teaching diagram. Arrows describe an investigation workflow, not proof of truth; parallel boxes are different evidence types or hypotheses.','原创教学图。箭头表示调查流程，不证明结论真实；并列框表示不同证据类型或假设。')
    if ident=='lineage':caption=t('Independence is claim-specific: an independent view can corroborate geometry without confirming the event or time. Reposts are not additional cameras.','独立性针对具体主张：独立视图可佐证几何，却未必确认事件或时间。转发不等于新增相机。')
    return frame(lang,'viz-'+ident,t(en,zh),body,caption,SOURCES[ref][2],SOURCES[ref][0])
