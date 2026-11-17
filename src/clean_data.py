
import re
from pathlib import Path
import pandas as pd
ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "data" / "raw" / "raw_data.csv"
OUTPUT = ROOT / "data" / "processed" / "clean_data.csv"
LOG = ROOT / "docs" / "cleaning_log.md"
df = pd.read_csv(INPUT); raw_count=len(df); df.columns=[c.strip().lower() for c in df.columns]
before=len(df); df=df.drop_duplicates(); duplicate_removed=before-len(df)
def clean_price(value):
    if pd.isna(value): return pd.NA
    s=str(value).strip().replace("￥","").replace("元","").replace(",",".")
    s=re.sub(r"[^0-9.\-]","",s)
    try: number=float(s)
    except ValueError: return pd.NA
    return number if number >= 0 else pd.NA
df["price"]=df["price"].apply(clean_price)
df["brand"]=df["brand"].astype("string").str.strip().replace({"STARBUCKS":"星巴克","Starbucks":"星巴克","Luckin Coffee":"瑞幸","MANNER":"Manner"})
df["rating"]=pd.to_numeric(df["rating"],errors="coerce"); df.loc[~df["rating"].between(1,5),"rating"]=pd.NA
df["likes"]=pd.to_numeric(df["likes"],errors="coerce"); df.loc[df["likes"]<0,"likes"]=pd.NA
df["review_date"]=pd.to_datetime(df["review_date"],errors="coerce").dt.strftime("%Y-%m-%d")
missing_key_before=int(df[["brand","product","review"]].isna().any(axis=1).sum()); df=df.dropna(subset=["brand","product","review"]).copy(); df["clean_id"]=range(1,len(df)+1)
df.to_csv(OUTPUT,index=False,encoding="utf-8-sig")
quality=(df.isna().mean()*100).round(2)
LOG.write_text(f"""# 清洗日志

- 原始记录数：{raw_count}
- 删除完全重复记录：{duplicate_removed}
- 删除关键字段缺失记录：{missing_key_before}
- 清洗后记录数：{len(df)}
- 清洗时间：2026-11-17
- 可重复执行：是，运行 python src/clean_data.py 可从原始数据重新生成结果。

## 处理规则

1. 完全重复行只保留一条。
2. 价格去除货币符号、逗号和元，转为非负数；无法解析或小于0的值记为空。
3. 品牌别名统一为标准名称。
4. 评分转为数字，范围必须为1至5，超出范围记为空。
5. 互动数转为数字，负数记为空。
6. 日期统一为 YYYY-MM-DD。
7. brand、product、review 缺失的记录删除。
8. 原始文件不覆盖，清洗结果单独保存。

## 清洗后缺失率

{quality.to_string()}
""",encoding="utf-8")
print(f"cleaned {raw_count} -> {len(df)}; duplicates={duplicate_removed}; key_missing_removed={missing_key_before}")
