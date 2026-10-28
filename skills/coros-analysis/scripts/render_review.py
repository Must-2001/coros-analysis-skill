#!/usr/bin/env python3
"""Render explicitly normalized daily observations; never infer missing values."""
import argparse
from collections import Counter
from datetime import date, timedelta
import json
import math
from pathlib import Path
import statistics
from zoneinfo import ZoneInfo


def validate(data):
    ZoneInfo(data['timezone'])
    first, last = (date.fromisoformat(data[k]) for k in ('start_date', 'end_date'))
    if first > last or (last-first).days > 365:
        raise ValueError('Use an ordered interval of at most 366 days')
    if data.get('language', 'en') not in ('en', 'zh'):
        raise ValueError('language must be en or zh')
    seen = set()
    for row in data['days']:
        d = date.fromisoformat(row['date'])
        if d in seen or not first <= d <= last:
            raise ValueError('Duplicate or out-of-range daily date')
        seen.add(d)
        if type(row.get('complete')) is not bool:
            raise ValueError('Each row requires complete: true/false')
        for key in ('main_sleep_minutes', 'nap_minutes', 'steps', 'sleep_hrv_ms'):
            value = row.get(key)
            if value is not None and (type(value) not in (int, float) or not math.isfinite(value) or value < 0):
                raise ValueError(f'{key} must be null or finite and nonnegative')
            if value is not None and not row.get('sources', {}).get(key):
                raise ValueError(f'{key} requires a field-level source')
        for key in ('main_sleep_minutes', 'nap_minutes'):
            if row.get(key) is not None and row[key] > 1440:
                raise ValueError('Sleep minutes exceed one day')
        if row.get('main_sleep_minutes') is not None and row.get('nap_minutes') is not None:
            if row['main_sleep_minutes'] + row['nap_minutes'] > 1440:
                raise ValueError('Main sleep plus naps exceeds one day')
        training = row.get('training')
        if training is not None:
            if not isinstance(training, list) or not row.get('sources', {}).get('training'):
                raise ValueError('training must be null or a sourced list')
            ids = set()
            for item in training:
                if not isinstance(item.get('sport'), str) or not item['sport'].strip():
                    raise ValueError('Each activity needs a sport label')
                v = item.get('minutes')
                if type(v) not in (int, float) or not math.isfinite(v) or v <= 0:
                    raise ValueError('Activity minutes must be finite and positive')
                if item.get('id'):
                    if item['id'] in ids:
                        raise ValueError('Duplicate activity ID within a day')
                    ids.add(item['id'])
    return first, last


def summary(data):
    first, last = validate(data)
    rows = [r for r in data['days'] if r['complete']]
    sleep = [r['main_sleep_minutes'] for r in rows if r.get('main_sleep_minutes') is not None]
    totals = Counter()
    for row in rows:
        for item in row.get('training') or []:
            totals[item['sport']] += item['minutes']
    return {
        'calendar_days': (last-first).days+1,
        'complete_observed_days': len(rows),
        'main_sleep_observed_days': len(sleep),
        'main_sleep_median_minutes': statistics.median(sleep) if sleep else None,
        'training_observed_days': sum(r.get('training') is not None for r in rows),
        'recorded_training_minutes_by_sport': dict(sorted(totals.items())),
        'partial_days_excluded': sum(not r['complete'] for r in data['days']),
    }


def render(data, output):
    first, last = validate(data)
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from matplotlib import font_manager
    zh = data.get('language') == 'zh'
    if zh:
        available = {f.name for f in font_manager.fontManager.ttflist}
        options = ['PingFang SC', 'Noto Sans CJK SC', 'Microsoft YaHei', 'Arial Unicode MS']
        font = next((f for f in options if f in available), None)
        if font is None:
            raise ValueError('Chinese rendering requires a CJK font; install one or use language=en')
        plt.rcParams['font.family'] = font
    plt.rcParams['axes.unicode_minus'] = False
    dates = [first+timedelta(days=i) for i in range((last-first).days+1)]
    rows = {r['date']: r for r in data['days']}
    daily = [rows.get(d.isoformat(), {}) for d in dates]
    complete = lambda r: r.get('complete') is True
    val = lambda r,k: r[k] if complete(r) and r.get(k) is not None else float('nan')
    metrics = summary(data)
    n = len(dates)
    fig, axes = plt.subplots(3, 1, figsize=(max(9, min(18, n*.42)), 8), sharex=True)
    fig.patch.set_facecolor('#f8fafc')
    sports = sorted({a['sport'] for r in daily if complete(r) for a in r.get('training') or []})
    palette = plt.get_cmap('tab10')
    bottoms = [0.]*n
    handles = []
    for i, sport in enumerate(sports):
        values = [sum(a['minutes'] for a in r.get('training') or [] if a['sport']==sport) if complete(r) and r.get('training') is not None else 0 for r in daily]
        bars = axes[0].bar(range(n), values, bottom=bottoms, color=palette(i%10), label=({'Hike':'徒步','Run':'跑步','Strength':'力量','Swim':'游泳','Hiking':'徒步','Swimming':'游泳'}.get(sport,sport) if zh else sport))
        handles.append(bars)
        bottoms = [a+b for a,b in zip(bottoms, values)]
    # Explicit markers distinguish unknown training from known empty lists.
    for i,r in enumerate(daily):
        if not complete(r) or r.get('training') is None:
            axes[0].text(i,.03,'?', transform=axes[0].get_xaxis_transform(), ha='center', color='#64748b')
        elif r['training']==[]:
            axes[0].plot(i,0,'o',color='#94a3b8',markersize=3)
    if handles:
        axes[0].legend(loc='lower left', bbox_to_anchor=(0,1.01), ncol=min(4,len(sports)), frameon=False)
    axes[0].set_ylabel('训练（分钟）' if zh else 'Training (min)')
    main = [val(r,'main_sleep_minutes')/60 for r in daily]
    naps = [val(r,'nap_minutes')/60 for r in daily]
    axes[1].plot(range(n), main, 'o-', color='#2563eb', label='主睡眠（入睡）' if zh else 'Main sleep (asleep)')
    # Naps are separate dots, never silently added to a missing main sleep.
    axes[1].scatter(range(n), naps, marker='s', color='#a855f7', label='午睡（入睡）' if zh else 'Naps (asleep)')
    if metrics['main_sleep_median_minutes'] is not None:
        axes[1].axhline(metrics['main_sleep_median_minutes']/60, linestyle='--', color='#64748b', label='本期观测中位数' if zh else 'Observed-period median')
    axes[1].set_ylabel('睡眠（小时）' if zh else 'Sleep (hours)')
    axes[1].legend(loc='lower left', bbox_to_anchor=(0,1.01), ncol=3, fontsize=8, frameon=False)
    axes[2].bar(range(n), [val(r,'steps')/1000 for r in daily], color='#14b8a6')
    axes[2].set_ylabel('步数（千步）' if zh else 'Steps (thousands)')
    for i, r in enumerate(daily):
        if complete(r) and r.get('steps') is None:
            axes[2].text(i,.03,'?', transform=axes[2].get_xaxis_transform(), ha='center', color='#64748b')
    for ax in axes:
        ax.set_facecolor('white')
        ax.set_ylim(bottom=0)
        ax.grid(axis='y', alpha=.16)
        ax.set_axisbelow(True)
        ax.spines[['top','right']].set_visible(False)
        for i,r in enumerate(daily):
            if not complete(r):
                ax.axvspan(i-.48,i+.48,color='#cbd5e1',alpha=.3)
    stride=max(1,math.ceil(n/14))
    axes[2].set_xticks(list(range(0,n,stride)), [d.strftime('%m-%d') for d in dates[::stride]], rotation=30)
    title='训练、睡眠与日常活动' if zh else 'Training, sleep & everyday activity'
    if data.get('synthetic') is True:
        title += ' · 虚构示例' if zh else ' · FICTIONAL EXAMPLE'
    fig.suptitle(f"{title}\n{first} — {last} · {data['timezone']}", fontsize=15, y=.98)
    note=(f"主睡眠覆盖 {metrics['main_sleep_observed_days']}/{metrics['calendar_days']} 天；? = 该项数据未知；灰色 = 缺失日/未完整日。图示不证明因果。" if zh else f"Main sleep: {metrics['main_sleep_observed_days']}/{metrics['calendar_days']} days. ? = unknown metric; gray = missing/partial day. No causal inference.")
    fig.text(.06,.025,note,fontsize=8,color='#475569')
    fig.tight_layout(rect=(.02,.055,.99,.92), h_pad=2.5)
    output=Path(output)
    if output.suffix.lower() not in ('.png','.svg'):
        raise ValueError('Output must be .png or .svg')
    output.parent.mkdir(parents=True,exist_ok=True)
    fig.savefig(output,dpi=160,facecolor=fig.get_facecolor())
    plt.close(fig)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input',type=Path)
    parser.add_argument('--output',type=Path)
    args=parser.parse_args()
    data=json.loads(args.input.read_text())
    result=summary(data)
    if args.output:
        render(data,args.output)
    print(json.dumps(result,ensure_ascii=False,indent=2))


if __name__=='__main__':
    main()
