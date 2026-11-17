# 数据字典

| 字段 | 类型 | 含义 | 清洗规则 |
|---|---|---|---|
| record_id | string | 原始记录编号 | 保留原值 |
| brand | string | 咖啡品牌 | 去空格并统一品牌别名 |
| product | string | 产品名称 | 关键字段，缺失记录删除 |
| price | float | 产品价格，元 | 去除货币符号并转为非负数 |
| rating | float | 消费者评分 | 转数字，仅保留1至5 |
| review | string | 消费者评论 | 关键字段，缺失记录删除 |
| review_date | date | 评论日期 | 统一为YYYY-MM-DD |
| likes | integer | 点赞或互动数 | 转数字，负数记为空 |
| source_url | string | 数据来源 | 保留来源标识 |
| collected_at | date | 采集日期 | 保留采集时间 |
| clean_id | integer | 清洗后编号 | 清洗完成后重新生成 |
