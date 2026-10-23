"""
GKD 订阅整合器
- 读取 10 份第三方订阅 dist json5
- 以应用包名聚合，按「规则组名」归并，组内按规则语义去重
- 重映射 rule.key / preKeys，避免跨源引用失效
- 输出 dist/gkd.json5 + dist/gkd.version.json5
"""
import json5, json, os, hashlib, collections

SRC = [
    ("linarm",   "gkd/linarm.json5",   "id667"),
    ("volcano",  "gkd/volcano.json5",  "火山虾"),
    ("ganlin",   "gkd/ganlin.json5",   "甘霖"),
    ("mrlc",     "gkd/mrlc.json5",     "Mrlc"),
    ("mengnian", "gkd/mengnian.json5", "梦念逍遥"),
    ("aisouler", "gkd/aisouler.json5", "AIsouler"),
    ("aoguai",   "gkd/aoguai.json5",   "奥怪"),
    ("muqi",     "gkd/muqi.json5",     "言木七"),
    ("lemon",    "gkd/lemon.json5",    "Lemon-D"),
    ("linrules", "gkd/linrules.json5", "少年阿鲲"),
]

CATEGORY_NAMES = [
    "开屏广告", "青少年模式", "更新提示", "评价提示", "通知提示", "权限提示",
    "局部广告", "全屏广告", "分段广告", "功能类", "其他",
    "定位提示", "全屏弹窗", "权限控制", "青少年弹窗", "其它",
]
CATEGORIES = [{"key": i, "name": n, "enable": (n == "开屏广告")} for i, n in enumerate(CATEGORY_NAMES)]

DROP_GROUP_FIELDS = {"scopeKeys"}   # 依赖源分类 key，跨源失效
BASE_GLOBAL_SRC = "linarm"


def norm_list(v):
    if v is None:
        return None
    if isinstance(v, str):
        return v.strip()
    if isinstance(v, list):
        return [x.strip() if isinstance(x, str) else x for x in v]
    return v


def rule_signature(r):
    """规则语义签名：只取决定「何时触发、点哪里」的字段，元数据不计入"""
    if isinstance(r, str):
        return json.dumps(["s", r.strip()], ensure_ascii=False)
    return json.dumps([
        "d",
        norm_list(r.get("matches")),
        norm_list(r.get("anyMatches")),
        norm_list(r.get("excludeMatches")),
        norm_list(r.get("activityIds")),
        norm_list(r.get("excludeActivityIds")),
        r.get("action"),
        r.get("position"),
        r.get("matchRoot"),
    ], sort_keys=True, ensure_ascii=False)


def norm_rule(r):
    return {"matches": r.strip()} if isinstance(r, str) else dict(r)


def is_empty_rule(r):
    """空选择器规则（源数据坏数据），无法触发且可能误匹配，丢弃"""
    if isinstance(r, str):
        return not r.strip()
    m, am = r.get("matches"), r.get("anyMatches")
    m_ok = bool(m) if not isinstance(m, list) else any(x for x in m)
    am_ok = bool(am) if not isinstance(am, list) else any(x for x in am)
    return not (m_ok or am_ok)


def merge_rules(buckets, stats, tag, used=None):
    """buckets: [(srcname, [rule...])] 按优先级。返回合并后规则列表。
    used 传入时为「应用级」已占用 key 集合，保证同一应用内规则 key 全局唯一。"""
    seen = {}                                  # sig -> final key
    out = []
    app_used = set() if used is None else used  # 应用级已占用 key（新 key 从这里分配）
    used = set()                                # 本组内已占用 key（保号优先看这个）
    keymaps = collections.defaultdict(dict)    # src -> {oldkey: newkey}
    pending = []                               # (src, raw_rule, target_key)

    for src, rules in buckets:
        km = keymaps[src]
        for idx, raw in enumerate(rules):
            if is_empty_rule(raw):
                stats[tag + "_empty"] += 1
                continue
            sig = rule_signature(raw)
            oldkey = raw.get("key", idx) if isinstance(raw, dict) else idx
            if sig in seen:
                stats[tag + "_dup"] += 1
                km[oldkey] = seen[sig]
                if isinstance(raw, dict) and raw.get("preKeys"):
                    pending.append((src, raw, seen[sig]))
                continue
            # 组内优先保号（preKeys 依赖原 key），否则从应用级池分配
            newkey = oldkey if (isinstance(oldkey, int) and oldkey not in used) else None
            if newkey is None:
                n = 0
                while n in app_used:
                    n += 1
                newkey = n
            used.add(newkey)
            app_used.add(newkey)
            r = norm_rule(raw)
            r["key"] = newkey
            out.append(r)
            seen[sig] = newkey
            km[oldkey] = newkey
            stats[tag + "_keep"] += 1
            if isinstance(raw, dict) and raw.get("preKeys"):
                pending.append((src, raw, newkey))

    # 重映射 preKeys：优先采用高优先级源的定义
    bykey = {x["key"]: x for x in out}
    touched = set()
    for src, raw, target in pending:
        if target in touched:
            continue
        tgt = bykey.get(target)
        if tgt is None:
            continue
        km = keymaps[src]
        pk = raw["preKeys"]
        pk = [pk] if isinstance(pk, int) else list(pk)
        tgt["preKeys"] = sorted({km.get(p, p) for p in pk})
        touched.add(target)
    return out


def merge_group_config(srcs):
    cfg = {}
    for src, g in srcs:
        for k, v in g.items():
            if k in ("rules", "key", "name", "enable", "desc"):
                continue
            if k in DROP_GROUP_FIELDS:
                continue
            if k not in cfg:
                cfg[k] = v
    return cfg


def main():
    data = {n: json5.loads(open(p, encoding="utf-8").read()) for n, p, _ in SRC}
    stats = collections.Counter()
    apps_index = collections.defaultdict(lambda: collections.defaultdict(list))
    app_names = {}

    for name, _, _ in SRC:
        for a in data[name].get("apps", []):
            pkg = a.get("id")
            if not pkg:
                continue
            app_names.setdefault(pkg, a.get("name") or pkg)
            for g in a.get("groups", []) or []:
                apps_index[pkg][g.get("name") or "未命名"].append((name, g))

    merged_apps = []
    for pkg, gbuckets in apps_index.items():
        final_groups = []
        seen_fp = set()
        app_used_keys = set()          # 应用级唯一 key，避免跨组 key 冲突
        for gname, srcs in gbuckets.items():
            rules_out = merge_rules([(s, g.get("rules", []) or []) for s, g in srcs],
                                    stats, "rule", used=app_used_keys)
            if not rules_out:
                continue
            cfg = merge_group_config(srcs)
            fp = hashlib.md5(
                (json.dumps([rule_signature(x) for x in rules_out], ensure_ascii=False)
                 + json.dumps(cfg, sort_keys=True, ensure_ascii=False)).encode()
            ).hexdigest()
            if fp in seen_fp:
                stats["group_dup"] += 1
                continue
            seen_fp.add(fp)
            grp = {"name": gname}
            grp.update(cfg)
            for _, g in srcs:
                if g.get("desc"):
                    grp["desc"] = g["desc"]
                    break
            grp["rules"] = rules_out
            final_groups.append(grp)
        if not final_groups:
            continue
        for i, g in enumerate(final_groups):
            g["key"] = i
        merged_apps.append({"id": pkg, "name": app_names.get(pkg, pkg), "groups": final_groups})
        stats["group_keep"] += len(final_groups)

    # ---------- 全局规则组 ----------
    def global_category(gname):
        for c in CATEGORY_NAMES:
            if (gname or "").startswith(c):
                return c
        return "其他"

    gbuckets = collections.defaultdict(list)
    for name, _, _ in SRC:
        for g in data[name].get("globalGroups", []) or []:
            merged_name = global_category(g.get("name") or "") + "-全局"
            is_base = (name == BASE_GLOBAL_SRC)
            gbuckets[(merged_name, is_base)].append((name, g))

    merged_globals = []
    for is_base in (True, False):
        seen_fp = set()
        for (gname, base_flag), srcs in gbuckets.items():
            if base_flag != is_base:
                continue
            rules_out = merge_rules([(s, g.get("rules", []) or []) for s, g in srcs], stats, "grule")
            if not rules_out:
                continue
            fp = hashlib.md5(
                json.dumps([rule_signature(x) for x in rules_out], ensure_ascii=False).encode()
            ).hexdigest()
            if fp in seen_fp:
                stats["global_dup"] += 1
                continue
            seen_fp.add(fp)
            cfg = merge_group_config(srcs)
            appmap = {}
            for _, g in srcs:
                for e in g.get("apps", []) or []:
                    aid = e.get("id")
                    if aid is None:
                        continue
                    appmap[aid] = (appmap[aid] and e.get("enable", False)) if aid in appmap else e.get("enable", False)
            if appmap:
                cfg["apps"] = [{"id": k, "enable": v} for k, v in appmap.items()]
            grp = {"name": gname}
            grp.update(cfg)
            grp["rules"] = rules_out
            if not is_base:
                grp["enable"] = False          # 非基线全局规则默认关闭，避免误触
            merged_globals.append(grp)
    for i, g in enumerate(merged_globals):
        g["key"] = i

    # ---------- 输出 ----------
    SUB_ID, VERSION = 20261023, 1
    out = {
        "id": SUB_ID,
        "name": "GKD整合订阅",
        "version": VERSION,
        "author": "merged",
        "checkUpdateUrl": "https://cdn.jsdelivr.net/gh/dlzbm/gkd-merged-subscription@main/dist/gkd.version.json5",
        "supportUri": "https://github.com/dlzbm/gkd-merged-subscription/issues",
        "categories": CATEGORIES,
        "globalGroups": merged_globals,
        "apps": merged_apps,
    }
    os.makedirs("dist", exist_ok=True)
    body = json.dumps(out, ensure_ascii=False, separators=(",", ":"))
    open("dist/gkd.json5", "w", encoding="utf-8").write(body)
    open("dist/gkd.version.json5", "w", encoding="utf-8").write('{"id":%d,"version":%d}\n' % (SUB_ID, VERSION))

    n_rule = sum(len(g["rules"]) for a in merged_apps for g in a["groups"])
    n_grule = sum(len(g["rules"]) for g in merged_globals)
    print("=== 合并结果 ===")
    print("应用数: %d" % len(merged_apps))
    print("应用规则组: %d" % stats["group_keep"])
    print("应用规则数: %d" % n_rule)
    print("全局规则组: %d  全局规则数: %d" % (len(merged_globals), n_grule))
    print("去重丢弃: 应用规则 %d 条 / 全局规则 %d 条 / 重复规则组 %d 个 / 空选择器 %d 条"
          % (stats["rule_dup"], stats["grule_dup"], stats["group_dup"], stats["rule_empty"]))
    print("文件大小: %.2f MB" % (len(body.encode("utf-8")) / 1024 / 1024))


if __name__ == "__main__":
    main()
