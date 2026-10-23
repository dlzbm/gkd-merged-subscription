import json5, collections, json

d = json5.loads(open("dist/gkd.json5", encoding="utf-8").read())
apps = d["apps"]

err = []
# 1. app 去重
ids = [a["id"] for a in apps]
if len(ids) != len(set(ids)):
    dup = [k for k, v in collections.Counter(ids).items() if v > 1]
    err.append(f"应用包名重复: {dup[:5]}")

# 2. 组内 key 唯一 + preKeys 可解析
bad_prekey = 0
for a in apps:
    gkeys = [g["key"] for g in a["groups"]]
    if len(gkeys) != len(set(gkeys)):
        err.append(f"规则组 key 重复: {a['id']}")
    for g in a["groups"]:
        rkeys = [r.get("key") if isinstance(r, dict) else None for r in g["rules"]]
        rkeys = [k for k in rkeys if k is not None]
        if len(rkeys) != len(set(rkeys)):
            err.append(f"规则 key 重复: {a['id']}/{g['name']}")
        valid = set(rkeys)
        for r in g["rules"]:
            if isinstance(r, dict) and "preKeys" in r:
                pk = r["preKeys"]
                pk = [pk] if isinstance(pk, int) else pk
                miss = [p for p in pk if p not in valid]
                if miss:
                    bad_prekey += 1
                    if bad_prekey <= 3:
                        err.append(f"preKeys 指向不存在: {a['id']}/{g['name']} -> {miss}")

# 3. 每条规则都必须有触发条件
no_match = 0
for a in apps:
    for g in a["groups"]:
        for r in g["rules"]:
            if isinstance(r, str):
                continue
            if not r.get("matches") and not r.get("anyMatches"):
                no_match += 1
if no_match:
    err.append(f"无 matches 的规则: {no_match} 条")

# 4. 规则组名 -> 分类归属覆盖
catnames = [c["name"] for c in d["categories"]]
uncat = collections.Counter()
for a in apps:
    for g in a["groups"]:
        n = g["name"]
        if not any(n.startswith(c) for c in catnames):
            uncat[n.split("-")[0]] += 1
print("未归入任何分类的规则组前缀 TOP15:", uncat.most_common(15))

# 5. 每应用规则数分布
cnt = sorted(((len([r for g in a["groups"] for r in g["rules"]]), a["id"], a["name"]) for a in apps), reverse=True)
print("\n规则数最多的应用 TOP10:")
for c, i, n in cnt[:10]:
    print(f"  {c:5d}  {i}  ({n})")

# 6. 全局组
print("\n全局规则组:")
for g in d["globalGroups"]:
    print(f"  key={g['key']} name={g['name']} rules={len(g['rules'])} enable={g.get('enable', '默认开')}")

# 7. 体积构成
s_all = len(open("dist/gkd.json5", encoding="utf-8").read())
meta = 0
for a in apps:
    for g in a["groups"]:
        for r in g["rules"]:
            if isinstance(r, dict):
                if "snapshotUrls" in r:
                    meta += len(json.dumps(r["snapshotUrls"], ensure_ascii=False))
                if "exampleUrls" in r:
                    meta += len(json.dumps(r["exampleUrls"], ensure_ascii=False))
print(f"\n文件字符数: {s_all}  其中 snapshotUrls+exampleUrls 约占 {meta} ({meta/s_all*100:.1f}%)")

print("\n错误:", err if err else "无")
print("应用数:", len(apps), " 规则组:", sum(len(a['groups']) for a in apps),
      " 规则数:", sum(len(g['rules']) for a in apps for g in a['groups']))
