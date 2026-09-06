"""Bounded OOXML objects translated into the shared presentation model."""
import math
from ooxml_package import NS, find, all_nodes, tag, text_content

def color(ctx, node, default):
    if node is None: return default
    rgb = find(node, 'a:srgbClr')
    if rgb is not None: return rgb.get('val', default)
    scheme = find(node, 'a:schemeClr')
    if scheme is not None: return ctx.brand.get('themeColors', {}).get(scheme.get('val'), default)
    return default

def geometry(ctx, part, node):
    transform = find(node, 'p:spPr/a:xfrm')
    if transform is None: transform = find(node, 'p:xfrm')
    if transform is None:
        ctx.warn(part, 'object has inherited/missing geometry; placed in default box; review source placeholder')
        return {'x': 100, 'y': 220, 'w': 1400, 'h': 300}
    off, extent = find(transform, 'a:off'), find(transform, 'a:ext')
    raw = [float(off.get('x', 0)) * ctx.sx if off is not None else 0,
           float(off.get('y', 0)) * ctx.sy if off is not None else 0,
           float(extent.get('cx', 0)) * ctx.sx if extent is not None else 0,
           float(extent.get('cy', 0)) * ctx.sy if extent is not None else 0]
    if not all(math.isfinite(v) for v in raw): raise ValueError('Nonfinite object geometry')
    x, y = max(0, min(1599, raw[0])), max(0, min(899, raw[1]))
    w, h = max(1, min(1600 - x, raw[2])), max(1, min(900 - y, raw[3]))
    if [x, y, w, h] != raw: ctx.warn(part, 'off-canvas/degenerate object geometry clamped to canvas')
    if any(transform.get(key) not in (None, '0', 'false') for key in ('rot', 'flipH', 'flipV')): ctx.warn(part, 'rotation / flip omitted')
    return dict(zip(('x', 'y', 'w', 'h'), [round(v, 3) for v in (x, y, w, h)]))

def style(ctx, part, node):
    runs = all_nodes(node, './/a:rPr')
    first = runs[0] if runs else find(node, './/a:defRPr')
    attributes = {'fontSize': 32, 'color': ctx.brand['foreground'], 'align': 'left', 'bold': False}
    if first is not None:
        # OOXML points / 100 -> CSS model px, whose export factor is .6.
        attributes['fontSize'] = min(160, max(12, float(first.get('sz', 1920)) / 60))
        attributes['bold'] = first.get('b') == '1'
        attributes['color'] = color(ctx, find(first, 'a:solidFill'), attributes['color'])
    paragraph = find(node, './/a:pPr')
    if paragraph is not None: attributes['align'] = {'l': 'left', 'ctr': 'center', 'r': 'right'}.get(paragraph.get('algn'), 'left')
    if len(runs) > 1 and any(dict(run.attrib) != dict(runs[0].attrib) for run in runs[1:]): ctx.warn(part, 'mixed run formatting normalized to first run; all text retained')
    if all_nodes(node, './/a:buChar') or all_nodes(node, './/a:buAutoNum'): ctx.warn(part, 'bullet/number formatting omitted; paragraph text retained')
    if all_nodes(node, './/a:hlinkClick'): ctx.warn(part, 'hyperlink actions omitted; link text retained')
    return attributes

def table(ctx, part, node, base):
    data = find(node, './/a:tbl')
    rows = [[text_content(find(cell, 'a:txBody')) for cell in all_nodes(row, 'a:tc')] for row in all_nodes(data, 'a:tr')]
    if not rows or len(rows) > 12 or max(map(len, rows), default=0) > 8 or len(set(map(len, rows))) != 1:
        ctx.omit(part, node, 'table omitted: supported size is rectangular 1–12 rows × 1–8 columns'); return None
    if any(any(cell.get(k) not in (None, '0', '1') for k in ('gridSpan', 'rowSpan')) or cell.get('hMerge') == '1' or cell.get('vMerge') == '1' for cell in all_nodes(data, './/a:tc')):
        ctx.warn(part, 'merged table cells flattened; merge geometry not retained')
    ctx.warn(part, 'table uses normalized equal-size cells and brand style; source cell formatting/widths omitted')
    return {**base, 'type': 'table', 'rows': rows, 'fontSize': 28, 'accent': ctx.brand['accent']}

def points(node, paths):
    for path in paths:
        cache = find(node, path)
        if cache is not None:
            entries = all_nodes(cache, 'c:pt')
            if len(entries) > 12: return None
            entries.sort(key=lambda x: int(x.get('idx', 0)))
            indices = [int(x.get('idx', 0)) for x in entries]
            if indices != list(range(len(indices))): return None
            return [(find(p, 'c:v').text or '') if find(p, 'c:v') is not None else '' for p in entries]
    return None

def chart(ctx, part, node, base):
    ref = find(node, './/c:chart')
    relationship = ctx.package.relationships(part).get(ref.get('{' + NS['r'] + '}id')) if ref is not None else None
    if not relationship or relationship['external']:
        ctx.warn(part, 'chart omitted: missing/local chart relationship required'); return None
    chartpart = relationship['target']; data = ctx.package.xml(chartpart)
    plot = find(data, './/c:plotArea')
    kinds = [child for child in plot if tag(child).endswith('Chart')] if plot is not None else []
    mapping = {'barChart': 'bar', 'lineChart': 'line', 'pieChart': 'pie'}
    if len(kinds) != 1 or tag(kinds[0]) not in mapping:
        ctx.warn(part, 'chart omitted: only single bar/line/pie plot supported (' + chartpart + ')'); return None
    kind = mapping[tag(kinds[0])]; series = []; labels = None
    for item in all_nodes(kinds[0], 'c:ser'):
        names = points(item, ['c:tx/c:strRef/c:strCache'])
        direct = find(item, 'c:tx/c:v')
        name = names[0] if names else direct.text if direct is not None else 'Series ' + str(len(series) + 1)
        categories = points(item, ['c:cat/c:strRef/c:strCache', 'c:cat/c:strLit', 'c:cat/c:numRef/c:numCache', 'c:cat/c:numLit'])
        levels = all_nodes(item, 'c:cat/c:multiLvlStrRef/c:multiLvlStrCache/c:lvl')
        if categories is None and len(levels) == 1:
            categories = points(item, ['c:cat/c:multiLvlStrRef/c:multiLvlStrCache/c:lvl'])
        elif len(levels) > 1:
            ctx.warn(part, 'chart omitted: hierarchical multi-level category labels unsupported (' + chartpart + ')'); return None
        values = points(item, ['c:val/c:numRef/c:numCache', 'c:val/c:numLit'])
        if categories is None or values is None or len(categories) != len(values) or not values:
            ctx.warn(part, 'chart omitted: cached categories/data absent, sparse, or over 12 categories (' + chartpart + ')'); return None
        try: numbers = [float(v) for v in values]
        except ValueError:
            ctx.warn(part, 'chart omitted: nonnumeric cached values'); return None
        if any(not math.isfinite(v) or (kind != 'line' and v < 0) for v in numbers):
            ctx.warn(part, 'chart omitted: values outside supported finite range'); return None
        if labels is not None and labels != categories:
            ctx.warn(part, 'chart omitted: series categories differ'); return None
        labels = categories; series.append({'name': name, 'values': numbers})
    if not series or len(series) > (1 if kind == 'pie' else 4):
        ctx.warn(part, 'chart omitted: series count outside support'); return None
    if kind == 'pie' and not any(value > 0 for value in series[0]['values']):
        ctx.warn(part, 'chart omitted: pie chart total must be greater than zero'); return None
    ctx.warn(part, 'chart rebuilt from cached values; source styling, axes, stacking, and workbook formulas not retained (' + chartpart + ')')
    return {**base, 'type': 'chart', 'chartType': kind, 'labels': labels, 'series': series}

def parse_element(ctx, part, node, identifier):
    kind = tag(node)
    if kind in ('nvGrpSpPr', 'grpSpPr'): return None
    if kind == 'grpSp':
        ctx.omit(part, node, 'group omitted (including ' + str(len(list(node))) + ' child records); ungroup in PowerPoint before importing'); return None
    if kind not in ('sp', 'pic', 'graphicFrame', 'cxnSp'):
        ctx.omit(part, node, kind + ' object omitted (unsupported OOXML object)'); return None
    base = {'id': identifier, **geometry(ctx, part, node)}
    if find(node, './/a:effectLst') is not None: ctx.warn(part, identifier + ' effects/shadows omitted')
    if kind == 'pic':
        blip = find(node, './/a:blip')
        if blip is None:
            ctx.warn(part, identifier + ' picture has no supported image reference'); return None
        image = ctx.image(part, blip.get('{' + NS['r'] + '}embed') or blip.get('{' + NS['r'] + '}link'))
        if not image: return None
        if find(node, './/a:srcRect') is not None: ctx.warn(part, identifier + ' source image crop normalized to contain; adjust image crop in editor')
        if find(node, './/a:videoFile') is not None or find(node, './/a:audioFile') is not None: ctx.warn(part, identifier + ' audio/video omitted; poster image retained')
        return {**base, 'type': 'image', 'src': image, 'alt': 'Imported image', 'fit': 'contain', 'positionX': .5, 'positionY': .5}
    if kind == 'graphicFrame':
        if find(node, './/a:tbl') is not None: return table(ctx, part, node, base)
        if find(node, './/c:chart') is not None: return chart(ctx, part, node, base)
        ctx.omit(part, node, identifier + ' graphicFrame omitted (SmartArt/OLE/unknown graphic); preserve or convert manually'); return None
    body = find(node, 'p:txBody'); content = text_content(body)
    props = find(node, 'p:spPr'); preset = find(props, 'a:prstGeom')
    shape = preset.get('prst') if preset is not None else 'line' if kind == 'cxnSp' else None
    mapping = {'rect': 'rect', 'roundRect': 'roundRect', 'ellipse': 'ellipse', 'rightArrow': 'arrow', 'line': 'line'}
    unsupported = find(props, 'a:custGeom') is not None or shape not in (*mapping, None)
    if unsupported: ctx.warn(part, identifier + ' unsupported shape geometry omitted; text retained where present')
    if find(props, 'a:gradFill') is not None or find(props, 'a:pattFill') is not None: ctx.warn(part, identifier + ' gradient/pattern fill replaced by solid brand fill')
    if find(node, './/p:ph') is not None: ctx.warn(part, identifier + ' placeholder styles normalized; inherited style may differ')
    attributes = style(ctx, part, body)
    has_fill = find(props, 'a:solidFill') is not None
    if not unsupported and shape in mapping and (not content or has_fill or kind == 'cxnSp'):
        return {**base, **attributes, 'type': 'shape', 'shape': mapping[shape], 'fill': color(ctx, find(props, 'a:solidFill'), ctx.brand['accent']), 'text': content}
    if content:
        return {**base, **attributes, 'type': 'text', 'text': content}
    ctx.warn(part, identifier + ' empty/unsupported shape omitted')
    return None
