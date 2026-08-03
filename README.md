# SIMS-Doctor v0.1.0

ブログ全体を3〜6か月ごとに診断し、Case単位で治療計画を管理するSIMS製品です。

## v0.1.0 vertical slice

1. SBMが`SIMS_DOCTOR_ARTICLE_CATALOG_V1`を手動出力
2. Doctorが契約・SiteID・ArticleID重複を検証
3. Collector Jobを作成（まだSearch Console取得は実行しない）

SBMの日次処理とは別ジョブ・別状態・別トリガーで動作します。
