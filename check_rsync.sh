#rsync -av --checksum --dry-run ~/projets/ssRNA/ /data/backup/projets/ssRNA > /tmp/l2
grep '\w$' /tmp/l2|grep -v '>'|awk -F "/"  '{print $1}'| uniq|tail
