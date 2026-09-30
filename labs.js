(() => {
  'use strict';
  const zh = document.documentElement.lang.startsWith('zh');
  const t = (en, cn) => zh ? cn : en;
  const el = id => document.getElementById(id);
  const show = (id, status, pass, output) => {
    el(id + '-state').textContent = status;
    el(id + '-state').dataset.pass = pass;
    el(id + '-output').textContent = output;
  };
  const actions = {
    candidate() {
      const c = el('candidate-choice').value;
      const independent = el('candidate-check').value === 'verified';
      const lines = [
        t('North–south river: MATCH', '南北河流：匹配'),
        t('East–west bridge: MATCH', '东西桥梁：匹配'),
        c === 'B' ? t('East-bank building: CONTRADICTION (building is west)', '河东建筑：矛盾（建筑在河西）') : t('East-bank building: MATCH', '河东建筑：匹配'),
        c === 'C' ? t('Eastern T-junction: CONTRADICTION (absent)', '东侧丁字路口：矛盾（缺失）') : t('Eastern T-junction: MATCH', '东侧丁字路口：匹配'),
        independent ? t('Independent ground view: selected as VERIFIED', '独立地面图：设为已核验') : t('Independent ground view: UNVERIFIED', '独立地面图：未核验')
      ];
      if (c !== 'A') {
        show('candidate', t('Reject under the stated geometry assumptions', '在所述几何假设下排除'), 'false', lines.join('\n') + '\n\n' + t('A claimed additional match does not cancel a hard contradiction. Recheck the observation or the new evidence before accepting this candidate.', '新增声称匹配不能抵消强矛盾。接受候选前，应重新检查观察或新证据。'));
      } else {
        show('candidate', independent ? t('Strongly supported for scene geometry', '场景几何得到充分支持') : t('Plausible candidate; independent check missing', '合理候选；缺少独立核验'), independent ? 'true' : 'info', lines.join('\n') + '\n\n' + t('The exact camera point, date and event identity remain outside this exercise.', '精确拍摄点、日期及事件身份不在本练习结论范围内。'));
      }
    },
    lineage() {
      const kind = el('lineage-choice').value;
      const claim = el('lineage-claim').value;
      const roots = kind === 'camera' || (kind === 'map' && claim === 'geometry') ? 2 : 1;
      const details = {
        reposts: t('X → repost A\nX → repost B\nAll three publications inherit one observation root.', 'X → 转发 A\nX → 转发 B\n三份发布继承同一个观察根。'),
        camera: t('X: first camera\nY: stipulated independent simultaneous camera\nBoth record the scene and event in the fixture.', 'X：第一台相机\nY：设定为独立同时拍摄的相机\n两者在示例中都记录场景及事件。'),
        map: t('X: photo\nM: stipulated independent dated site map\nM can corroborate geometry, but does not observe the depicted event.', 'X：照片\nM：设定为独立有日期地点地图\nM 可佐证几何，但未观察图中事件。'),
        model: t('X → model guess A\nX → model guess B\nDerived guesses add no new observation of the world.', 'X → 模型猜测 A\nX → 模型猜测 B\n衍生猜测没有增加对现实世界的新观察。')
      };
      show('lineage', t(`${roots} supporting observation root(s) for this claim`, `该主张有 ${roots} 个支持观察根`), roots === 2 ? 'true' : 'info', details[kind] + '\n\n' + t('Root count is not a truth probability. The stipulated sources still need authentication in a real investigation.', '根数量不是真实概率。真实调查中仍需认证这些设定来源。'));
    },
    coordinate() {
      const aText = el('coordinate-first').value.trim();
      const bText = el('coordinate-second').value.trim();
      const a = Number(aText), b = Number(bText);
      if (!aText || !bText || !Number.isFinite(a) || !Number.isFinite(b)) {
        show('coordinate', t('Enter two finite decimal values', '请输入两个有限十进制数值'), 'false', ''); return;
      }
      const latFirst = el('coordinate-order').value === 'latlon';
      const lat = latFirst ? a : b, lon = latFirst ? b : a;
      if (Math.abs(lat) > 90 || Math.abs(lon) > 180) {
        show('coordinate', t('Invalid range for the selected order', '所选顺序下数值越界'), 'false', `latitude = ${lat}\nlongitude = ${lon}\n` + t('Latitude must be in [−90, 90], longitude in [−180, 180]. Check axis order before changing the values.', '纬度须在 [−90, 90]，经度须在 [−180, 180]。修改数值前先核对轴顺序。')); return;
      }
      if (el('coordinate-system').value !== 'wgs') {
        show('coordinate', t('Range valid; reference unresolved — no conversion performed', '范围有效；参考体系未确定 — 未进行转换'), 'info', t('Do not label unknown or provider coordinates as WGS 84 or output them as RFC 7946 GeoJSON. Establish the source system first.', '不要把未知或服务特有坐标标为 WGS 84，也不要作为 RFC 7946 GeoJSON 输出。应先确定源体系。')); return;
      }
      const rad = x => x * Math.PI / 180;
      const h = Math.sin(rad(lat - 30) / 2) ** 2 + Math.cos(rad(30)) * Math.cos(rad(lat)) * Math.sin(rad(lon - 120) / 2) ** 2;
      const km = 6371 * 2 * Math.asin(Math.sqrt(Math.max(0, Math.min(1, h))));
      const pos = {type: 'Point', coordinates: [lon, lat]};
      show('coordinate', t('Contract valid under the selected WGS 84 assumption', '在所选 WGS 84 假设下约定有效'), 'true', `latitude = ${lat}°\nlongitude = ${lon}°\nGeoJSON = ${JSON.stringify(pos)}\n` + t(`Approximate distance to synthetic reference: ${km.toFixed(2)} km`, `距合成参考点近似距离：${km.toFixed(2)} 公里`) + '\n\n' + t('Valid ranges and a declared CRS do not verify the real-world location. Both orders can pass when both values are within ±90°.', '有效范围与声明的 CRS 不证明现实地点。当两个值均位于 ±90° 时，两种顺序都可能通过检查。'));
    }
  };
  document.addEventListener('click', event => {
    const button = event.target.closest('[data-action]');
    if (button && Object.hasOwn(actions, button.dataset.action)) actions[button.dataset.action]();
  });
})();
