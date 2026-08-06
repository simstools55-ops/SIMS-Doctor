# SIMS Doctor v1.0.2 Release Notes

## 概要
SBMからWriter・Creator・Mergeへ迷わず引き渡すためのワークフロー完成版。診断ロジックは変更せず、利用者向け指示、治療区分、優先順位、依頼文JSONを強化した。

## 変更
- 「SBMへ渡す依頼」を「利用者が確認すること」へ変更
- 番号付き優先順位チェックリストを追加
- 治療区分を追加
- `workflow_handoff` をJSONへ追加
- Writer・Creator・Merge依頼文全文をJSONで返却
- 既存契約との後方互換を維持
