sed -E 's#^([^[:space:]]+):[[:space:]]+\{#{"location":"\1",#' \
  prometheus_report.txt > prometheus_report.jsonl
