Simple backup for Kibana saved objects: config, index patterns, dashboards, saved searches, etc.

Uses python3 and [python-requests](https://requests.readthedocs.io/) library, which you have to install on your every host anyway, because it's awesome.

### Usage
Available actions:

* `backup` - write backup file in newline-delimitered json format to stdout
* `restore` - restore backup from stdin
* `convert` - convert `json` or `ndjson` format to `yaml`

Available arguments:

* `--kibana-url` - base URL to access Kibana API, default: `http://127.0.0.1:5601`
* `--space-id` - kibana space id. If not set then the default space is used.
* `--user` - kibana user
* `--password` - kibana password
* `--file` - file that will be converted or restored
* `--backup-dir` - backup location
* `--extension` - backup extension. Available `yml` or `yaml` or `json`. Defaults to `json`
* `--resolve-conflicts` - removes references if it get an exception on restoring the backup object. Defaults to `true`.
* `--insecure` - do not verify SSL CA authority

*Note:* To use the default space you should not set `--space-id` parameter. Setting it to the default space id: `default` does not work.

Example:

Below examples has been done on Kibana Opendistro for Elasticsearch.

```
# Backup as json
kibana-backup.py --kibana-url https://$(hostname):5601 --backup-dir $(pwd) --user admin --password mypassword  backup

# Backup as a yaml
kibana-backup.py --kibana-url https://$(hostname):5601 --extension yml --backup-dir $(pwd) --user admin --password mypassword  backup

# Restore backup
kibana-backup.py --kibana-url https://$(hostname):5601 --file dashboard.yml --user admin --password mypassword restore

# Convert json/ndjson to yaml
kibana-backup.py --file dashboard.ndjson --extension yaml convert
```

### Documentation

* https://www.elastic.co/guide/en/kibana/current/saved-objects-api-export.html
* https://www.elastic.co/guide/en/kibana/current/saved-objects-api-import.html

### License

[WTFPL](LICENSE)

**P.S.** If this code is useful for you - don't forget to put a star on it's [github repo](https://github.com/selivan/kibana-backup-simple).
